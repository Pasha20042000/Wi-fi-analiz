#!C:\Python39\python.exe
# Copyright 2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-2.0-or-later
#

import os
import sys
import warnings


GR_IMPORT_ERROR_MESSAGE = """\
Cannot import gnuradio.

Is the Python path environment variable set correctly?
    All OS: PYTHONPATH

Is the library path environment variable set correctly?
    Linux: LD_LIBRARY_PATH
    Windows: PATH

See https://wiki.gnuradio.org/index.php/ModuleNotFoundError
"""


def die(error, message):
    msg = "{0}\n\n({1})".format(message, error)
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk
        d = Gtk.MessageDialog(
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            text=msg,
        )
        d.set_title(type(error).__name__)
        d.run()
        exit(1)
    except ImportError:
        exit(type(error).__name__ + '\n\n' + msg)


def check_gtk():
    try:
        warnings.filterwarnings("error")
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('PangoCairo', '1.0')
        gi.require_foreign('cairo', 'Context')

        from gi.repository import Gtk
        Gtk.init_check()
        warnings.filterwarnings("always")
    except Exception as err:
        die(err, "Failed to initialize GTK. If you are running over ssh, "
                 "did you enable X forwarding and start ssh with -X?")


def check_gnuradio_import():
    try:
        from gnuradio import gr
    except ImportError as err:
        die(err, GR_IMPORT_ERROR_MESSAGE)


def check_blocks_path():
    if 'GR_DONT_LOAD_PREFS' in os.environ and not os.environ.get('GRC_BLOCKS_PATH', ''):
        die(EnvironmentError("No block definitions available"),
            "Can't find block definitions. Use config.conf or GRC_BLOCKS_PATH.")


def run_main():
    script_path = os.path.dirname(os.path.abspath(__file__))
    source_tree_subpath = "/grc/scripts"

    if not script_path.endswith(source_tree_subpath):
        # run the installed version
        from gnuradio.grc.main import main
    else:
        print("Running from source tree")
        sys.path.insert(1, script_path[:-len(source_tree_subpath)])
        from grc.main import main
    exit(main())


if __name__ == '__main__':
    check_gnuradio_import()
    check_gtk()
    check_blocks_path()
    run_main()
