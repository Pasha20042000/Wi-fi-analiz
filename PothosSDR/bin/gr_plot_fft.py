#!C:\Python39\python.exe
#
# Copyright 2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#

from gnuradio.plot_fft_base import plot_fft_base

# This is a wrapper program for plot_fft_base. It handles any data
# type and defaults to complex64.

def main():
    parser = plot_fft_base.setup_options()
    args = parser.parse_args()

    plot_fft_base(None, args.file, args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
