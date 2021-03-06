#!C:\Python39\python.exe
#
# Copyright 2008,2009,2011,2012,2015 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Command-line siggen app
"""

try:
    import uhd_siggen_base as uhd_siggen
except ImportError:
    from gnuradio.uhd import uhd_siggen_base as uhd_siggen

if __name__ == "__main__":
    uhd_siggen.main()
