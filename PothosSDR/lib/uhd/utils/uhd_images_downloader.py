#!C:/Python39/python.exe
#
# Copyright 2018 Ettus Research, a National Instruments Company
# Copyright 2020 Ettus Research, a National Instruments Brand
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Download image files required for USRPs.

Usage: The `uhd_images_downloader` should work, "out of the box", with no command line arguments.
Assuming your computer has an internet connection to [files.ettus.com], simply run the utility
every time you update UHD, and the installed images for your devices should always be up to date.


Images will be downloaded on a per-target basis. That is, there are image packages for a desired
device and configuration. Users can specify which image packages they would plan to use. To see a
list of available targets, run `uhd_images_downloader --list-targets`. The left column of the
printout will be a list of available image archives. From there, you can construct a regular
expression which matches to the targets you wish to download. For example, in order to download all
image packages related to the X300 product line, users may run
`uhd_images_downloader --types x3.*`.


The `uhd_images_downloader` uses a manifest to look-up the URLs of image packages to download.
Downloaded images are recorded in an inventory file that lives in the images install location.
This allows the downloader to skip images that were previously downloaded, and haven't changed
since.

Manifests are built into the downloader, but can also be accessed at uhd/images/manifest.txt.

Inventory files are JSON files called `inventory.json`, by default. It is possible to specify the
inventory file in command line arguments, but we don't recommend using this functionality unless
you're really sure you need it.
"""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile
import platform
from urllib.parse import urljoin  # Python 3

# For all the non-core-library imports, we will be extra paranoid and be very
# nice with error messages so that everyone understands what's up.
try:
    import requests
except ImportError:
    sys.stdout.write(
        "[ERROR] Missing module 'requests'! Please install it, e.g., by "
        "running 'pip install requests' or any other tool that can install "
        "Python modules.\n")
    if platform.system() == 'Windows':
        input('Hit Enter to continue.')
    exit(0)

# pylint: disable=bad-whitespace
_DEFAULT_TARGET_REGEX     = "(fpga|fw|windrv)_default"
_BASE_DIR_STRUCTURE_PARTS = ["share", "uhd", "images"]
_DEFAULT_INSTALL_PATH     = os.path.join("C:/PothosSDR", *_BASE_DIR_STRUCTURE_PARTS)
_DEFAULT_BASE_URL         = "https://files.ettus.com/binaries/cache/"
_INVENTORY_FILENAME       = "inventory.json"
_CONTACT                  = "support@ettus.com"
_DEFAULT_BUFFER_SIZE      = 8192
_DEFAULT_DOWNLOAD_LIMIT   = 100 * 1024 * 1024 # Bytes
_ARCHIVE_DEFAULT_TYPE     = "zip"
_UHD_VERSION              = "4.0.0.HEAD-0-g90ce6062"
_LOG_LEVELS = {
    "TRACE": 1,
    "DEBUG": 2,
    "INFO":  3,
    "WARN":  4,
    "ERROR": 5,
}
_LOG_LEVEL = _LOG_LEVELS["INFO"]
_YES = False
_PROXIES = {}
_BASE_URL_ENV_VAR = "UHD_IMAGES_URL"
# pylint: enable=bad-whitespace
# Note: _MANIFEST_CONTENTS are placed at the bottom of this file for aesthetic reasons

def log(level, message):
    """Logging function"""
    message_log_level = _LOG_LEVELS.get(level, 0)
    if message_log_level >= _LOG_LEVEL:
        sys.stderr.write(
            "[{level}] {message}\n".format(level=level, message=message))


def parse_args():
    """
    Setup argument parser and parse. Also does some sanity checks and sets some
    global variables we want to use.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=__doc__)
    parser.add_argument('-t', '--types', action='append',
                        help="RegEx to select image sets from the manifest file.")
    parser.add_argument('-i', '--install-location', type=str, default=None,
                        help="Set custom install location for images")
    parser.add_argument('-m', '--manifest-location', type=str, default=None,
                        help="Set custom location for the manifest file")
    parser.add_argument('-I', '--inventory-location', type=str, default=None,
                        help="Set custom location for the inventory file")
    parser.add_argument('-l', '--list-targets', action="store_true", default=False,
                        help="Print targets in the manifest file to stdout, and exit.\n"
                        "To get relative paths only, specify an empty base URL (-b '').")
    parser.add_argument('--url-only', action="store_true", default=False,
                        help="With -l, only print the URLs, nothing else.")
    parser.add_argument("--buffer-size", type=int, default=_DEFAULT_BUFFER_SIZE,
                        help="Set download buffer size")
    parser.add_argument("--download-limit", type=int, default=_DEFAULT_DOWNLOAD_LIMIT,
                        help="Set threshold for download limits. Any download "
                             "larger than this will require approval, either "
                             "interactively, or by providing --yes.")
    parser.add_argument("--http-proxy", type=str,
                        help="Specify HTTP(S) proxy in the format "
                        "http[s]://user:pass@1.2.3.4:port\n"
                        "If this this option is not given, the environment "
                        "variables HTTP_PROXY/HTTPS_PROXY can also be used to specify a proxy.")
    parser.add_argument("-b", "--base-url", type=str,
                        help="Set base URL for images download location. "
                        "Defaults to ${} if set, or {} otherwise.".format(
                            _BASE_URL_ENV_VAR, _DEFAULT_BASE_URL))
    parser.add_argument("-k", "--keep", action="store_true", default=False,
                        help="Keep the downloaded images archives in the image directory")
    parser.add_argument("-T", "--test", action="store_true", default=False,
                        help="Verify the downloaded archives before extracting them")
    parser.add_argument("-y", "--yes", action="store_true", default=False,
                        help="Answer all questions with 'yes' (for scripting purposes).")
    parser.add_argument("-n", "--dry-run", action="store_true", default=False,
                        help="Print selected target without actually downloading them.")
    parser.add_argument("--refetch", action="store_true", default=False,
                        help="Ignore the inventory file and download all images.")
    parser.add_argument('-V', '--version', action='version', version=_UHD_VERSION)
    parser.add_argument('-q', '--quiet', action='count', default=0,
                        help="Decrease verbosity level")
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Increase verbosity level")
    args = parser.parse_args()
    # Set the verbosity
    global _LOG_LEVEL
    log("TRACE", "Default log level: {}".format(_LOG_LEVEL))
    _LOG_LEVEL = _LOG_LEVEL - args.verbose + args.quiet
    # Some sanitation that's easier to handle outside of the argparse framework:
    if not args.base_url:
        if os.environ.get(_BASE_URL_ENV_VAR):
            args.base_url = os.environ.get(_BASE_URL_ENV_VAR)
        else:
            args.base_url = _DEFAULT_BASE_URL
    log("INFO", "Using base URL: {}".format(args.base_url))
    if not args.base_url.endswith('/') and args.base_url != "":
        args.base_url += '/'
    if args.yes:
        global _YES
        _YES = True
    if args.http_proxy:
        global _PROXIES
        _PROXIES['http'] = args.http_proxy
        _PROXIES['https'] = args.http_proxy
    return args


def get_images_dir(args):
    """
    Figure out where to store the images.
    """
    if args.install_location:
        return args.install_location
    if os.environ.get("UHD_IMAGES_DIR"):
        log("DEBUG",
            "UHD_IMAGES_DIR environment variable is set, using to set "
            "install location.")
        return os.environ.get("UHD_IMAGES_DIR")
    return _DEFAULT_INSTALL_PATH


def ask_permission(question, default_no=True):
    """
    Ask the question, and have the user type y or n on the keyboard. If the
    global variable _YES is true, this always returns True without asking the
    question. Otherwise, return True if the answer is 'yes', 'y', or something
    similar.
    """
    if _YES:
        log("DEBUG", "Assuming the answer is 'yes' for this question: " +
            question)
        return True
    postfix = "[y/N]" if default_no else "[Y/n]"
    answer = input(question + " " + postfix)
    if answer and answer[0].lower() == 'y':
        return True
    return False


class TemporaryDirectory:
    """Class to create a temporary directory"""
    def __enter__(self):
        try:
            self.name = tempfile.mkdtemp()
            return self.name
        except Exception as ex:
            log("ERROR", "Failed to create a temporary directory (%s)" % ex)
            raise ex

    # Can return 'True' to suppress incoming exception
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            shutil.rmtree(self.name)
            log("TRACE", "Temp directory deleted.")
        except Exception as ex:
            log("ERROR", "Could not delete temporary directory: %s (%s)" % (self.name, ex))
        return exc_type is None


def get_manifest_raw(args):
    """
    Return the raw content of the manifest (i.e. the text file). It
    needs to be parsed to be of any practical use.
    """
    # If we're given a path to a manifest file, use it
    if args.manifest_location:
        manifest_fn = args.manifest_location
        if os.path.exists(manifest_fn):
            log("INFO", "Using manifest file at location: {}".format(manifest_fn))
            with open(manifest_fn, 'r') as manifest_file:
                manifest_raw = manifest_file.read()
        else:
            log("WARN", "Invalid manifest file specified: {}, using default"
                .format(manifest_fn))
            manifest_raw = _MANIFEST_CONTENTS       
    # Otherwise, use the CMake Magic manifest
    else:
        manifest_raw = _MANIFEST_CONTENTS
    log("TRACE", "Raw manifest contents: {}".format(manifest_raw))
    return manifest_raw


def parse_manifest(manifest_contents):
    """Parse the manifest file, returns a dictionary of potential targets"""
    manifest = {}
    for line in manifest_contents.split('\n'):
        line_unpacked = line.split()
        try:
            # Check that the line isn't empty or a comment
            if not line_unpacked or line.strip().startswith('#'):
                continue

            target, repo_hash, url, sha256_hash = line_unpacked
            manifest[target] = {"repo_hash": repo_hash,
                                "url": url,
                                "sha256_hash": sha256_hash,
                               }
        except ValueError:
            log("WARN", "Warning: Invalid line in manifest file:\n"
                "         {}".format(line))
            continue
    return manifest


def parse_inventory(inventory_fn):
    """Parse the inventory file, returns a dictionary of installed files"""
    try:
        if not os.path.exists(inventory_fn):
            log("INFO", "No inventory file found at {}. Creating an empty one.".format(inventory_fn))
            return {}
        with open(inventory_fn, 'r') as inventory_file:
            # TODO: verify the contents??
            return json.load(inventory_file)
    except Exception as ex:
        log("WARN", "Error parsing the inventory file. Assuming an empty inventory: {}".format(ex))
        return {}


def write_inventory(inventory, inventory_fn):
    """Writes the inventory to file"""
    try:
        with open(inventory_fn, 'w') as inventory_file:
            json.dump(inventory, inventory_file)
            return True
    except Exception as ex:
        log("ERROR", "Error writing the inventory file. Contents may be incomplete or corrupted.\n"
                     "Error message: {}".format(ex))
        return False


def lookup_urls(regex_l, manifest, inventory, refetch=False):
    """Takes a list of RegExs to match within the manifest, returns a list of tuples with
    (hash, URL) that match the targets and are not in the inventory"""
    selected_targets = []
    # Store whether or not we've found a target in the manifest that matches the requested type
    found_one = False
    for target in manifest.keys():
        # Iterate through the possible targets in the manifest.
        # If any of them match any of the RegExs supplied, add the URL to the
        # return list
        if all(map((lambda regex: re.findall(regex, target)), regex_l)):
            found_one = True
            log("TRACE", "Selected target: {}".format(target))
            target_info = manifest.get(target)
            target_url = target_info.get("url")
            target_hash = target_info.get("repo_hash")
            target_sha256 = target_info.get("sha256_hash")
            filename = os.path.basename(target_url)
            # Check if the same filename and hash appear in the inventory
            if not refetch and inventory.get(target, {}).get("repo_hash", "") == target_hash:
                # We already have this file, we don't need to download it again
                log("INFO", "Target {} is up to date.".format(target))
            else:
                # We don't have that exact file, add it to the list
                selected_targets.append({"target": target,
                                         "repo_hash": target_hash,
                                         "filename": filename,
                                         "url": target_url,
                                         "sha256_hash": target_sha256})
    if not found_one:
        log("INFO", "No targets matching '{}'".format(regex_l))
    return selected_targets


def print_target_list(manifest, args):
    """
    Print a list of targets.
    """
    char_offset = max(len(x) for x in manifest.keys())
    if not args.url_only:
        # Print a couple helpful lines,
        # then print each (Target, URL) pair in the manifest
        log("INFO", "Potential targets in manifest file:\n"
                    "{} : {}".format(
                        "# TARGET".ljust(char_offset),
                        "URL" if args.base_url else "RELATIVE_URL"))
        for key, value in sorted(manifest.items()):
            print("{target} : {base}{relpath}".format(
                target=key.ljust(char_offset),
                base=args.base_url,
                relpath=value["url"]))
    else:
        for manifest_item in manifest.items():
            print(args.base_url+manifest_item[1]["url"])


def download(
        images_url,
        filename,
        buffer_size=_DEFAULT_BUFFER_SIZE,
        print_progress=False,
        download_limit=None
    ):
    """ Run the download, show progress """
    download_limit = download_limit or _DEFAULT_DOWNLOAD_LIMIT
    log("TRACE", "Downloading {} to {}".format(images_url, filename))
    try:
        resp = requests.get(images_url, stream=True, proxies=_PROXIES,
                            headers={'User-Agent': 'UHD Images Downloader'})
    except TypeError:
        # requests library versions pre-4c3b9df6091b65d8c72763222bd5fdefb7231149
        # (Dec.'12) workaround
        resp = requests.get(images_url, prefetch=False, proxies=_PROXIES,
                            headers={'User-Agent': 'UHD Images Downloader'},
                            allow_redirects=True)
    if resp.status_code != 200:
        raise RuntimeError("URL does not exist: {}".format(images_url))
    filesize = float(resp.headers.get('content-length', -1))
    if filesize > download_limit:
        if not ask_permission(
                "The file size for this target ({:.1f} MiB) exceeds the "
                "download limit ({:.1f} MiB). Continue downloading?".format(
                    filesize/1024**2, download_limit/1024**2)):
            return 0, 0, ""
    if filesize == -1:
        if not ask_permission(
                "The file size for this target could not be determined. "
                "Continue downloading?"):
            return 0, 0, ""
    filesize_dl = 0
    base_filename = os.path.basename(filename)
    if print_progress and not sys.stdout.isatty():
        print_progress = False
        log("INFO", "Downloading {}, total size: {} kB".format(
            base_filename, filesize/1000 if filesize > 0 else "-unknown-"))
    with open(filename, "wb") as temp_file:
        sha256_sum = hashlib.sha256()
        for buff in resp.iter_content(chunk_size=buffer_size):
            if buff:
                temp_file.write(buff)
                filesize_dl += len(buff)
                sha256_sum.update(buff)
            if print_progress:
                status = r"%05d kB " % int(math.ceil(filesize_dl / 1000.))
                if filesize > 0:
                    status += r"/ %05d kB (%03d%%) " % (
                        int(math.ceil(filesize / 1000.)),
                        int(math.ceil(filesize_dl * 100.) / filesize),
                    )
                status += base_filename
                if os.name == "nt":
                    status += chr(8) * (len(status) + 1)
                else:
                    sys.stdout.write("\x1b[2K\r")  # Clear previous line
                sys.stdout.write(status)
                sys.stdout.flush()
    if print_progress:
        print('')
    if filesize <= 0:
        filesize = filesize_dl
    return filesize, filesize_dl, sha256_sum.hexdigest()


def delete_from_inv(target_info, inventory, images_dir):
    """
    Uses the inventory to delete the contents of the archive file specified by in `target_info`
    """
    target = inventory.get(target_info.get("target"), {})
    target_name = target.get("target")
    log("TRACE", "Removing contents of {} from inventory ({})".format(
        target, target.get("contents", [])))
    dirs_to_delete = []
    # Delete all of the files
    for image_fn in target.get("contents", []):
        image_path = os.path.join(images_dir, image_fn)
        if os.path.isfile(image_path):
            os.remove(image_path)
            log("TRACE", "Deleted {} from inventory".format(image_path))
        elif os.path.isdir(image_path):
            dirs_to_delete.append(image_fn)
        else: # File doesn't exist
            log("WARN", "File {} in inventory does not exist".format(image_path))
    # Then delete all of the (empty) directories
    for dir_path in dirs_to_delete:
        try:
            if os.path.isdir(dir_path):
                os.removedirs(dir_path)
        except os.error as ex:
            log("ERROR", "Failed to delete dir: {}".format(ex))
    inventory.pop(target_name, None)
    return True


def extract(archive_path, images_dir, test_zip=False):
    """
    Extract the contents of `archive_path` into `images_dir`

    Returns a list of files that were extracted.

    If test_zip is set, it will verify the zip file before extracting.
    """
    log("TRACE", "Attempting to extracted files from {}".format(archive_path))
    with zipfile.ZipFile(archive_path) as images_zip:
        # Check that the Zip file is valid, in which case `testzip()` returns
        # None.  If it's bad, that function will return a list of bad files
        try:
            if test_zip and images_zip.testzip():
                log("ERROR", "Could not extract the following invalid Zip file:"
                             " {}".format(archive_path))
                return []
        except OSError:
            log("ERROR", "Could not extract the following invalid Zip file:"
                         " {}".format(archive_path))
            return []
        images_zip.extractall(images_dir)
        archive_namelist = images_zip.namelist()
        log("TRACE", "Extracted files: {}".format(archive_namelist))
        return archive_namelist


def update_target(target_info, temp_dir, images_dir, inventory, args):
    """
    Handle the updating of a single target.
    """
    target_name = target_info.get("target")
    target_sha256 = target_info.get("sha256_hash")
    filename = target_info.get("filename")
    temp_path = os.path.join(temp_dir, filename)
    # Add a trailing slash to make sure that urljoin handles things properly
    full_url = urljoin(args.base_url+'/', target_info.get("url"))
    _, downloaded_size, downloaded_sha256 = download(
        images_url=full_url,
        filename=temp_path,
        buffer_size=args.buffer_size,
        print_progress=(_LOG_LEVEL <= _LOG_LEVELS.get("INFO", 3))
    )
    if downloaded_size == 0:
        log("INFO", "Skipping target: {}".format(target_name))
        return
    log("TRACE", "{} successfully downloaded ({} Bytes)"
        .format(temp_path, downloaded_size))
    # If the SHA256 in the manifest has the value '0', this is a special case
    # and we just skip the verification step
    if target_sha256 == '0':
        log("DEBUG", "Skipping SHA256 check for {}.".format(full_url))
    # If the check fails, print an error and don't unzip the file
    elif downloaded_sha256 != target_sha256:
        log("ERROR", "Downloaded SHA256 does not match manifest for {}!"
            .format(full_url))
        return
        # Note: this skips the --keep option, so we'll never keep image packages
        #       that fail the SHA256 checksum
    ## Now copy the contents to the final destination (the images directory)
    delete_from_inv(target_info, inventory, images_dir)
    if os.path.splitext(temp_path)[1].lower() == '.zip':
        archive_namelist = extract(
            temp_path,
            images_dir,
            args.test)
        if args.keep:
            # If the user wants to keep the downloaded archive,
            # save it to the images directory and add it to the inventory
            shutil.copy(temp_path, images_dir)
            archive_namelist.append(filename)
    else:
        archive_namelist = []
        shutil.copy(temp_path, images_dir)
    ## Update inventory
    inventory[target_name] = {"repo_hash": target_info.get("repo_hash"),
                              "contents": archive_namelist,
                              "filename": filename}


def main():
    """
    Main function; does whatever the user requested (download or list files).

    Returns True on successful execution.
    """
    args = parse_args()
    images_dir = get_images_dir(args)
    log("INFO", "Images destination: {}".format(os.path.abspath(images_dir)))
    try:
        manifest = parse_manifest(get_manifest_raw(args))
        if args.list_targets:
            print_target_list(
                manifest,
                args
            )
            return True
        log("TRACE", "Manifest:\n{}".format(
            "\n".join("{}".format(item) for item in manifest.items())
        ))

        # Strip down path until we find first parent directory of images_dir
        # that exists and then check if we have proper write permissions
        images_dir_parent = images_dir
        while not os.path.exists(os.path.abspath(images_dir_parent)):
            path_pair = os.path.split(images_dir_parent)
            if images_dir_parent == path_pair[0]:
                # Prevent infinite loop
                break
            images_dir_parent = path_pair[0]
        if not os.access(os.path.abspath(images_dir_parent), os.W_OK):
            log("ERROR", "Invalid permissions to write images destination")
            return False

        # Read the inventory into a dictionary we can perform lookups on
        default_inventory_fn = os.path.join(images_dir, _INVENTORY_FILENAME)
        if args.inventory_location:
            if os.path.isfile(args.inventory_location):
                inventory_fn = args.inventory_location
            else:
                log("WARN", "Invalid inentory file specified: {}, using default: {}"
                    .format(args.inventory_location, default_inventory_fn))
                inventory_fn = default_inventory_fn
        else:
            inventory_fn = default_inventory_fn
        inventory = parse_inventory(inventory_fn=inventory_fn)
        log("TRACE", "Inventory: {}\n{}".format(
            os.path.abspath(inventory_fn),
            "\n".join("{}".format(item) for item in inventory.items())
        ))

        # Determine the URLs to download based on the input regular expressions
        if not args.types:
            types_regex_l = [_DEFAULT_TARGET_REGEX]
        else:
            types_regex_l = args.types

        log("TRACE", "RegExs for target selection: {}".format(types_regex_l))
        targets_info = lookup_urls(types_regex_l, manifest, inventory, args.refetch)
        # Exit early if we don't have anything to download
        if targets_info:
            target_urls = [info.get("url") for info in targets_info]
            log("DEBUG", "URLs to download:\n{}".format(
                "\n".join("{}".format(item) for item in target_urls)
            ))
        else:
            return True

        ## Now download all the images archives into a temp directory
        if args.dry_run:
            for target_info in targets_info:
                log("INFO", "[Dry Run] Fetch target: {}".format(
                    target_info.get("filename")))
            return True
        with TemporaryDirectory() as temp_dir:
            for target_info in targets_info:
                update_target(
                    target_info,
                    temp_dir,
                    images_dir,
                    inventory,
                    args
                )
        ## Update inventory with all the new content
        write_inventory(inventory, inventory_fn)

    except Exception as ex:
        log("ERROR", "Downloader raised an unhandled exception: {ex}\n"
            "You can run this again with the '--verbose' flag to see more information\n"
            "If the problem persists, please email the output to: {contact}"
            .format(contact=_CONTACT, ex=ex))
        # Again, we wait on Windows systems because if this is executed in a
        # window, and immediately fails, the user doesn't have a way to see the
        # error message, and if they're not very savvy, they won't know how to
        # execute this in a shell.
        if not _YES and platform.system() == 'Windows':
            input('Hit Enter to continue.')
        return False
    log("INFO", "Images download complete.")
    return True

# Placing this near the end of the file so we don't clutter the top
_MANIFEST_CONTENTS = """# UHD Image Manifest File
# Target    hash    url     SHA256
# X300-Series
x3xx_x310_fpga_default          uhd-be53058       x3xx/uhd-be53058/x3xx_x310_fpga_default-gbe53058.zip                  baa6082515704090ce701cb89dddcc2c99b42fcdb72648f0d465520aa11cfc8b
x3xx_x300_fpga_default          uhd-be53058       x3xx/uhd-be53058/x3xx_x300_fpga_default-gbe53058.zip                  3d58e95e1e53716eec3f62067967a2baedeb8f2d1f3cfe4ecb9d01f984140291
# Example daughterboard targets (none currently exist)
#x3xx_twinrx_cpld_default   example_target
#dboard_ubx_cpld_default    example_target

# E-Series
e3xx_e310_sg1_fpga_default      uhd-be53058       e3xx/uhd-be53058/e3xx_e310_sg1_fpga_default-gbe53058.zip             b708d89d2d58fd8d8f180f98d08bba177c117d8b0b8251bfcfb7dd4e4657d165
e3xx_e310_sg3_fpga_default      uhd-be53058       e3xx/uhd-be53058/e3xx_e310_sg3_fpga_default-gbe53058.zip             6a57ffa57dc29138185f6e9c208a886c15d62c9cd838d41cda9349f5d13c082d
e3xx_e320_fpga_default          uhd-413ebee       e3xx/uhd-413ebee/e3xx_e320_fpga_default-g413ebee.zip                 296c8d86b0f5feb3b551c2c5f856e221cdf7288eeacd16c8e1c56c0bfa0b4934

# E310 Filesystems
e3xx_e310_sdk_default         meta-ettus-v4.0.0.0  e3xx/meta-ettus-v4.0.0.0/e3xx_e310_sdk_default-v4.0.0.0.zip       0
e3xx_e310_sg1_mender_default  meta-ettus-v4.0.0.0  e3xx/meta-ettus-v4.0.0.0/e3xx_e310_sg1_mender_default-v4.0.0.0.zip    0
e3xx_e310_sg1_sdimg_default   meta-ettus-v4.0.0.0  e3xx/meta-ettus-v4.0.0.0/e3xx_e310_sg1_sdimg_default-v4.0.0.0.zip     0
e3xx_e310_sg3_mender_default  meta-ettus-v4.0.0.0  e3xx/meta-ettus-v4.0.0.0/e3xx_e310_sg3_mender_default-v4.0.0.0.zip    0
e3xx_e310_sg3_sdimg_default   meta-ettus-v4.0.0.0  e3xx/meta-ettus-v4.0.0.0/e3xx_e310_sg3_sdimg_default-v4.0.0.0.zip     0

# E320 Filesystems, etc
e3xx_e320_sdk_default         meta-ettus-v4.0.0.0  e3xx/meta-ettus-v4.0.0.0/e3xx_e320_sdk_default-v4.0.0.0.zip       0
e3xx_e320_mender_default      meta-ettus-v4.0.0.0  e3xx/meta-ettus-v4.0.0.0/e3xx_e320_mender_default-v4.0.0.0.zip    0
e3xx_e320_sdimg_default       meta-ettus-v4.0.0.0  e3xx/meta-ettus-v4.0.0.0/e3xx_e320_sdimg_default-v4.0.0.0.zip     0

# N300-Series
n3xx_n310_fpga_default          uhd-be53058       n3xx/uhd-be53058/n3xx_n310_fpga_default-gbe53058.zip                 edc7e2e870446efaf3df75433913215b2ce81965e35edacaea1b1ae253325fd6
n3xx_n300_fpga_default          uhd-be53058       n3xx/uhd-be53058/n3xx_n300_fpga_default-gbe53058.zip                 6f9503b4a3e0f006a46eb131f0a9e4decdcb8dcdbe2416bb7b727f7f518950c3
n3xx_n320_fpga_default          uhd-be53058        n3xx/uhd-be53058/n3xx_n320_fpga_default-gbe53058.zip                88e5c504a5ddcb63c4b0bd439951b6b4166bf4ac2cbca1cdb441f0e9b030acb4
n3xx_n310_cpld_default          fpga-6bea23d        n3xx/fpga-6bea23d/n3xx_n310_cpld_default-g6bea23d.zip                ef128dcd265ee8615b673021d4ee84c39357012ffe8b28c8ad7f893f9dcb94cb
n3xx_n320_cpld_default          fpga-4bc2c6f       n3xx/fpga-4bc2c6f/n3xx_n320_cpld_default-g4bc2c6f.zip              6680a9363efc5fa8b5a68beb3dff44f2e314b94e716e3a1751aba0fed1f384da
# N3XX Mykonos firmware
#n3xx_n310_fw_default           fpga-6bea23d        n3xx/fpga-6bea23d/n3xx_n310_fw_default-g6bea23d.zip                     0
# N300-Series Filesystems, etc
n3xx_common_sdk_default         meta-ettus-v4.0.0.0  n3xx/meta-ettus-v4.0.0.0/n3xx_common_sdk_default-v4.0.0.0.zip       0
n3xx_common_mender_default      meta-ettus-v4.0.0.0  n3xx/meta-ettus-v4.0.0.0/n3xx_common_mender_default-v4.0.0.0.zip    0
n3xx_common_sdimg_default       meta-ettus-v4.0.0.0  n3xx/meta-ettus-v4.0.0.0/n3xx_common_sdimg_default-v4.0.0.0.zip     0

# B200-Series
b2xx_b200_fpga_default          uhd-f2ec5c9       b2xx/uhd-f2ec5c9/b2xx_b200_fpga_default-gf2ec5c9.zip               026c3b2613ceabbe7f47e479c2933e41ca054e7b1f85a119d86d97b6df4ca744
b2xx_b200mini_fpga_default      uhd-f2ec5c9       b2xx/uhd-f2ec5c9/b2xx_b200mini_fpga_default-gf2ec5c9.zip           3c122145a5bd23dc50ac35b9d18dfe3f3224eaed4242274765ada89c55838ce4
b2xx_b210_fpga_default          uhd-f2ec5c9       b2xx/uhd-f2ec5c9/b2xx_b210_fpga_default-gf2ec5c9.zip               4eba82a362369cc21ba679a4debdcd6aabbc1ecea295eb4aefd94f2ba5e6ed70
b2xx_b205mini_fpga_default      uhd-f2ec5c9       b2xx/uhd-f2ec5c9/b2xx_b205mini_fpga_default-gf2ec5c9.zip           a38fcecabcef43d57e463aa50f0b07ba21d7e9211428fbc5ef47bfeb75542e93
b2xx_common_fw_default          uhd-437381b         b2xx/uhd-437381b/b2xx_common_fw_default-g437381b.zip                  a71b01cb7dfea975f26516b5b18f9d2bebd5083effaf21a79fd5925d2aaf6a32

# USRP2 Devices
usrp2_usrp2_fw_default          fpga-6bea23d        usrp2/fpga-6bea23d/usrp2_usrp2_fw_default-g6bea23d.zip                  d523a18318cb6a7637be40484bf03a6f54766410fee2c1a1f72e8971ea9a9cb6
usrp2_usrp2_fpga_default        fpga-6bea23d        usrp2/fpga-6bea23d/usrp2_usrp2_fpga_default-g6bea23d.zip                505c70aedc8cdfbbfe654bcdbe1ce604c376e733a44cdd1351571f61a7f1cb49
usrp2_n200_fpga_default         fpga-6bea23d        usrp2/fpga-6bea23d/usrp2_n200_fpga_default-g6bea23d.zip                 833a0098d66c0c502b9c3975d651a79e125133c507f9f4b2c472f9eb96fdaef8
usrp2_n200_fw_default           fpga-6bea23d        usrp2/fpga-6bea23d/usrp2_n200_fw_default-g6bea23d.zip                   3eee2a6195caafe814912167fccf2dfc369f706446f8ecee36e97d2c0830116f
usrp2_n210_fpga_default         fpga-6bea23d        usrp2/fpga-6bea23d/usrp2_n210_fpga_default-g6bea23d.zip                 5ce68ac539ee6eeb7d04fb3127c1fabcaff442a8edfaaa2f3746590f9df909bd
usrp2_n210_fw_default           fpga-6bea23d        usrp2/fpga-6bea23d/usrp2_n210_fw_default-g6bea23d.zip                   3646fcd3fc974d18c621cb10dfe97c4dad6d282036dc63b7379995dfad95fb98
n230_n230_fpga_default          fpga-e57dfe0        n230/fpga-e57dfe0/n230_n230_fpga_default-ge57dfe0.zip                   f115b78a1893da0c2a481257351b834721f8a5468dfae6a34e3a68a3bc0065cd

# USRP1 Devices
usrp1_usrp1_fpga_default        fpga-6bea23d        usrp1/fpga-6bea23d/usrp1_usrp1_fpga_default-g6bea23d.zip                03bf72868c900dd0853bf48e2ede91058d579829b0e70c021e51b0e282d1d5be
usrp1_b100_fpga_default         fpga-6bea23d        usrp1/fpga-6bea23d/usrp1_b100_fpga_default-g6bea23d.zip                 7f2306f21e17aa3fae3f966d08c6297d6cf42041974f846ca89f0d633ece8769
usrp1_b100_fw_default           fpga-6bea23d        usrp1/fpga-6bea23d/usrp1_b100_fw_default-g6bea23d.zip                   867f17fac085535dbcb01c226ce87acf49806de6ed0ae9b214d7c8da86e2a71d

# Octoclock
octoclock_octoclock_fw_default  uhd-14000041        octoclock/uhd-14000041/octoclock_octoclock_fw_default-g14000041.zip     8da7f1af8cecb7f6259a237a18c39058ba69a11567fa373cffc9704031a1d053

# Legacy USB Windows drivers
usb_common_windrv_default       uhd-14000041        usb/uhd-14000041/usb_common_windrv_default-g14000041.zip                835e94b2bdf2312fd3881a1b78e2ec236c1f42b7a5bd3927f85f73cf5e3a5231
"""
if __name__ == "__main__":
    sys.exit(not main())
