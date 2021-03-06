#!C:\Python39\python.exe
#
# Copyright 2008,2009,2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from gnuradio import gr
from osmosdr import osmocom_siggen_base as osmocom_siggen
import sys

def main():
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Note: failed to enable realtime scheduling, continuing")

    # Grab command line options and create top block
    try:
        (options, args) = osmocom_siggen.get_options()
        tb = osmocom_siggen.top_block(options, args)

    except RuntimeError as e:
        print(e)
        sys.exit(1)

    tb.start()
    input('Press Enter to quit: ')
    tb.stop()
    tb.wait()

# Make sure to create the top block (tb) within a function:
# That code in main will allow tb to go out of scope on return,
# which will call the decontructor on usrp and stop transmit.
# Whats odd is that grc works fine with tb in the __main__,
# perhaps its because the try/except clauses around tb.
if __name__ == "__main__":
    main()
