#!/usr/bin/env python3
# Copyright (C) 2008 Ian Chapman
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from pytzx.tzx import *
from pytzx.zxfile import *

################################################################################
# EXAMPLE 1 - Pure python script that generates a TZX file to load a screen.   #
#                                                                              #
# A normal spectrum tape file basically consists of two blocks. The first      #
# being the header which essentially holds meta information about the file and #
# the second is the actual "data" itself. As we are going to create a spectrum #
# loading screen we need to create two spectrum files which in turn means *4*  #
# blocks. The first file is nothing more than a small spectrum basic program   #
# which bootstraps the second file, the actual loading screen.                 #
#                                                                              #
################################################################################

# Main code starts around line 453

# A packed string representation of spectrum screen data
screenbytes = \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x55\x55\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x01\x55\x55\x55\x55\x55\x55\x55\x55\x55\x54" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x15\x50\x00\x01\x55\x55\x55\x55\x55\x55\x55\x50\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x15\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x55\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x01\x11\x11\x11\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55\x55\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x50\x01\x11\x11\x11\x15\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xAA\xAA\xBB\xBA\xAA" \
    b"\xAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xBB\xBB\xBB\xBB\xBB\xBB\xBB" \
    b"\xBB\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x2A\xA8\x00\x02\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xA8" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x3B\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xB8\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\xBB\xBB\xBB\xBB\xBB\xB8\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xAA\xAB\xBB\xBB\xBB" \
    b"\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xB8\x02\xAA\xAA\xAA\xA0\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x02\xAA\xBB\xBB\xBB\xBB\xBB\xBB\xBB" \
    b"\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xB8\x0A\xAA\xAA\xAA\xAA\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x55" \
    b"\x55\x55\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x40\x15\x55\x55\x55\x55\x55" \
    b"\x55\x55\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x15\x50\x00\x01\x55\x55\x55\x55\x55\x55\x55" \
    b"\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x15\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55\x55\x55\x50\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x04\x45\x55\x55\x40" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x55\x55\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x05\x55\x55\x55\x55\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xAE\xEE\xEE\xEE" \
    b"\xEE\xEE\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0E\xEE\x00\x0E\xEE\xEE\xEE\xEE" \
    b"\xEE\xEE\xEE\xC0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x2E\xE8\x00\x02\xEE\xEE\xEE\xEE\xEE\xEE" \
    b"\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x2E\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xE8" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEE\xEE\xEE\xEE\xEE\xE8\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0E\xEE\xEE\xEE" \
    b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xE8\x0A\xAA\xAA\xAA" \
    b"\xA8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xEE\xEE\xEE\xEE\xEE\xEE" \
    b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xE8\x0A\xAA\xAA\xAA\xAA\x80" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x54\x00\x05\x55\x55\x55" \
    b"\x55\x55\x55\x55\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x15\x50\x00\x01\x55\x55\x55\x55\x55" \
    b"\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55" \
    b"\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x55\x55\x55\x55\x55\x50\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x01\x11\x11" \
    b"\x11\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x01\x11\x11\x15\x55" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2A\xAA\xAB" \
    b"\xBB\xBB\xBB\xBB\xBB\xBA\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xA8\x00\x03\xBB\xBB" \
    b"\xBB\xBB\xBB\xBB\xBB\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2B\xBA\x00\x0B\xBB\xBB\xBB\xBB" \
    b"\xBB\xBB\xBB\xB8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x3B\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB" \
    b"\xBB\xB8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xBB\xBB\xBB\xBB\xBB\xB8" \
    b"\x02\xAA\xAA\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2A\xAA" \
    b"\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xB8\x0A\xAA" \
    b"\xAA\xAA\xAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xBB\xBB\xBB\xBB" \
    b"\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xA8\x0A\xAA\xAA\xAA" \
    b"\xAA\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x50\x00\x01\x55" \
    b"\x55\x55\x55\x55\x55\x55\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x00\x15\x55\x55\x55" \
    b"\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55\x55\x55\x55\x55" \
    b"\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x01\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55" \
    b"\x50\x04\x44\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x04" \
    b"\x45\x55\x55\x54\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x05\x55\x55" \
    b"\x55\x55\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xEE" \
    b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0E\xE8\x00\x02" \
    b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2E\xEE\xAA\xAE\xEE\xEE" \
    b"\xEE\xEE\xEE\xEE\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2E\xEE\xEE\xEE\xEE\xEE\xEE\xEE" \
    b"\xEE\xEE\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x2E\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE" \
    b"\xEE\xE8\x0A\xAA\xAA\xAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xE8" \
    b"\x0A\xAA\xAA\xAA\xAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0E\xEE\xEE" \
    b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xE0\x0A\xAA" \
    b"\xAA\xAA\xAA\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x11\x11\x15\x55" \
    b"\x55\x40\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x00\x01\x11\x15\x55\x55\x55\x50" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55\x55\x55\x55\x55\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x11\x11\x15\x55\x55\x55\x55\x50\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55\x54\x00\x00\x00\x01\x11" \
    b"\x11\x11\x11\x11\x11\x11\x55\x55\x55\x55\x55\x55\x50\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x05\x55\x55\x55\x55\x40\x00\x00\x11\x11\x11\x11\x11" \
    b"\x11\x11\x55\x55\x55\x55\x55\x55\x55\x55\x40\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x55\x55\x55\x55\x40\x01\x11\x11\x11\x11\x11\x11\x11\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x54\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x05\x55\x55\x40\x11\x11\x11\x11\x11\x11\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x11\x11\x11\x11\x11\x55\x55\x55\x55\x55\x55\x50\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0B\xBB\xBB\xBB" \
    b"\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xA0\x0A\xAA\xAA" \
    b"\xAA\xAA\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x3B\xBB\xBB\xBB\xBB\xBB" \
    b"\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\x00\x02\xAA\xAA\xAA\xAA\xAA" \
    b"\xA8\x00\x00\x00\x00\x00\x00\x00\x00\x3B\xBB\xBB\xBB\xBB\xBB\xBA\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x02\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xA8\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x3B\xBB\xBB\xBB\xBB\xBA\x02\xAA\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xA8\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x03\xBB\xBB\xBB\xBB\xA0\x0A\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAB\xBB\x80\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x3B\xBB\xBB\xBB\xA0\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xBB\xBB\xB8\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x2B\xBB\xA0\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\xAA\xAB\xBB\xBA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xB8" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x40\x15\x55" \
    b"\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x00\x05\x55\x55\x55\x55" \
    b"\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55\x55\x55\x55\x54" \
    b"\x00\x04\x44\x44\x44\x44\x44\x55\x55\x55\x55\x55\x55\x55\x55\x55\x54" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55\x50\x00\x44\x44" \
    b"\x44\x44\x44\x45\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x55\x40\x04\x44\x44\x44\x44" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x40\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x15\x55\x55\x55\x40\x04\x44\x44\x44\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x04\x44\x45\x55\x55\x54\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x04\x45\x55\x55\x55\x55\x55\x55\x55\x55\x55" \
    b"\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2E\xEE" \
    b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xC0\x2A" \
    b"\xAA\xAA\xAA\xAA\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x6E\xEE\xEE\xEE" \
    b"\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xE8\x00\x2A\xAA\xAA\xAA" \
    b"\xAA\xAE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x2E\xEE\xEE\xEE\xEE\xEE" \
    b"\xE0\x00\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAE\xEE" \
    b"\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x2E\xEE\xEE\xEE\xEE\xE8\x02\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAE\xEE\xEE\xEE\xE8\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x02\xEE\xEE\xEE\xEE\xE0\x0A\xAA\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xEE\xEE\xEE\xEE\xEE\x80\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x0E\xEE\xEE\xEE\xE0\x0A\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xAE\xEE\xEE\xEE\xEE\xEE\xE8\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA\xAA\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xEE\xEE" \
    b"\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x00" \
    b"\x11\x11\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55" \
    b"\x55\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x11\x15\x55" \
    b"\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55" \
    b"\x55\x40\x00\x00\x00\x01\x11\x11\x11\x11\x11\x11\x15\x55\x55\x55\x55" \
    b"\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x55\x50\x00" \
    b"\x00\x00\x11\x11\x11\x11\x11\x11\x11\x55\x55\x55\x55\x55\x55\x55\x50" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x01\x55\x55\x55\x55\x40\x00\x01\x11" \
    b"\x11\x11\x11\x11\x11\x15\x55\x55\x55\x55\x55\x55\x55\x55\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x40\x11\x11\x11\x11\x11" \
    b"\x11\x11\x55\x55\x55\x55\x55\x55\x55\x55\x55\x40\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x11\x11\x11\x11\x14\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x11\x11\x11\x11\x55\x55\x55\x55\x55" \
    b"\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x3B\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBB\xBA" \
    b"\x00\x2A\xAA\xAA\xAA\xAA\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x3B\xBB" \
    b"\xBB\xBB\xBB\xBB\xBB\xBA\x80\x00\x00\x00\x00\x00\x00\x00\x00\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xA8\x00\x00\x00\x00\x00\x00\x00\x00\x3B\xBB\xBB\xBB" \
    b"\xBB\xBB\x80\x02\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\xAA\xA8\x00\x00\x00\x00\x00\x00\x00\x00\x0B\xBB\xBB\xBB\xBB\xA0" \
    b"\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAB" \
    b"\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x02\xBB\xBB\xBB\xBB\xA0\x0A\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xBB\xBB\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x03\xBB\xBB\xBB\xA0\x0A\xAA\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAB\xBB\xBB\x80\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA\xAA" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\xAA\xAB\xB8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x15\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55" \
    b"\x54\x00\x55\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x55" \
    b"\x55\x55\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55" \
    b"\x55\x55\x55\x55\x55\x54\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55" \
    b"\x55\x55\x55\x00\x04\x44\x44\x44\x44\x44\x45\x55\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x54\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x55" \
    b"\x40\x04\x44\x44\x44\x44\x44\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55" \
    b"\x55\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55\x55\x40\x04" \
    b"\x44\x44\x44\x45\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x54\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\x55\x55\x40\x04\x44\x44" \
    b"\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x45\x55\x55\x55" \
    b"\x54\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55\x55\x55" \
    b"\x55\x55\x55\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x2E\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE\xEE" \
    b"\xEE\xE8\x00\xAA\xAA\xAA\xAA\xAA\xE8\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x6E\xEE\xEE\xEE\xEE\xEE\xEE\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x0A" \
    b"\xAA\xAA\xAA\xAA\xAE\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x2E\xEE" \
    b"\xEE\xEE\xEE\xEE\x00\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\xEE\xEE\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x0E\xEE\xEE\xEE" \
    b"\xEE\xE0\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAE\xEE\xEE" \
    b"\xEE\xEE\xE0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEE\xEE\xEE\xEE\xE0" \
    b"\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xEE\xEE\xEE\xEE\xEE\xEE" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2E\xEE\xEE\xE0\x0A\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAE\xEE\xEE\xEE\xEE\xEE\xE8\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xA8\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\xAE\xE8\x02\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x11\x11\x15\x55\x55\x55\x55" \
    b"\x40\x00\x55\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x01\x11\x55\x55\x55\x55\x55\x55\x00\x00" \
    b"\x15\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x01\x55\x55\x55\x55\x55\x55\x55\x55\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA\xAA\xAA" \
    b"\xAA\x80\x00\xBB\xB8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA\xAA\xAA\xAA\x80" \
    b"\x00\x3B\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\xAA\xAA\xAA\xAA\xAA\xAB\xBB\xBA\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55\x55" \
    b"\x55\x55\x00\x00\x15\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x55\x55\x55\x55" \
    b"\x40\x00\x55\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x55\x55\x55\x55\x55\x55\x54" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA\xAA\xAA" \
    b"\xAA\xAE\xEE\x00\x00\x2E\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xAA\xAA\xAA\xAA\xEE\xEE" \
    b"\xEE\xE8\x02\xEE\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAE\xEE\xEE\xEE\xEE\xEE" \
    b"\xA0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x11\x11\x55" \
    b"\x55\x55\x55\x55\x00\x00\x15\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55" \
    b"\x55\x55\x55\x15\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55\x55\x55" \
    b"\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA\xAA" \
    b"\xAA\xAA\xAA\xAA\xAA\x00\x00\x2B\xA8\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xAA\xAA\xAA\xAA" \
    b"\xAA\xAA\xAA\xBB\xBB\xBA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xAA\xAA\xAB" \
    b"\xBA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55" \
    b"\x55\x55\x55\x55\x55\x55\x00\x00\x15\x50\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x55\x55" \
    b"\x55\x55\x55\x55\x55\x55\x54\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04" \
    b"\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A" \
    b"\xAA\xAA\xAA\xAA\xAA\xEE\xEE\x00\x00\x2E\xE0\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0A\xAA" \
    b"\xAA\xEE\xEE\xEE\xEE\xEE\xEE\xE8\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x08\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\x00\x00\x00\x00\x00\x00\x00\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x3D\x3D" \
    b"\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x3D\x3D\x3D\x3D" \
    b"\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x3D\x3D\x3D\x3D\x3D\x3D" \
    b"\x3D\x3D\x3D\x3D\x3D\x3D\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D" \
    b"\x3D\x3D\x3D\x3D\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D" \
    b"\x3D\x3D\x3E\x3E\x3E\x3E\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D" \
    b"\x3E\x3E\x3E\x3E\x3E\x38\x38\x38\x38\x38\x38\x38\x38\x38\x3D\x3D\x3D" \
    b"\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3E\x3E" \
    b"\x3E\x3E\x3E\x3E\x38\x38\x38\x38\x38\x38\x38\x38\x3D\x3D\x3D\x3D\x3D" \
    b"\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3E\x3E\x3E\x3E" \
    b"\x3E\x3E\x38\x38\x38\x38\x38\x38\x38\x38\x3D\x3D\x3D\x3D\x3D\x3D\x3D" \
    b"\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x3D\x3D\x3D\x3D\x3D\x3D\x3D\x3E\x3E" \
    b"\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x3D\x3D\x3D\x3D\x3D\x3D\x3E\x3E\x3E\x3E\x3E" \
    b"\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x3D\x3D\x3D\x3D\x3D\x3D\x3E\x3E\x3E\x3E\x3E\x3E\x3E" \
    b"\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x3D\x3D\x3D\x3D\x3D\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E" \
    b"\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x3D\x3D\x3D\x3D\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E" \
    b"\x3E\x3E\x3E\x3E\x3E\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x38\x3E\x3E\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x3E" \
    b"\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x3E\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38" \
    b"\x38\x38\x38\x38\x38\x38\x38\x38\x38\x38"

# A packed string representation of a tokenised Spectrum Basic Program
# 10 LOAD "" CODE
basicprog = b"\x00\x0A\x05\x00\xEF\x22\x22\xAF\x0D"

# Before dealing with the TZX file itself, we can use some spectrum specific
# classes and methods to create the data that needs to encapsulated into a
# TZX block and added to a TZX.

# First file: The spectrum basic "loader"
# CREATE THE HEADER
# For an explanation of the parameters, see zxfile.py
loaderheader = ZX_FileHdr(SPEC_FILE_PROG, 'ScrLoader', 0, 10, 9)

# CREATE THE DATA and incorporate our basic program
loaderdata = ZX_FileData(basicprog)

# Tell the header, the size of the data.
loaderheader.setdatalen(loaderdata.datalen())

# Second File: The screen data (this is code ie "Bytes:")
# CREATE THE HEADER
# For an explanation of the parameters, see zxfile.py
screenheader = ZX_FileHdr(SPEC_FILE_CODE, 'PyLogo', 0, 16384, 32768)

# CREATE THE DATA and incorporate out spectrum screen
screendata = ZX_FileData(screenbytes)

# Tell the header, the size of the data.
screenheader.setdatalen(screendata.datalen())

# Now that we have prepared our spectrum files, they need to be incorporated
# into TZX blocks. We will be using the "Standard Speed Data Block".
# Essentially this block means "normal" spectrum loading.

# Incorporate the loader header into a TZX block.
loaderblock1 = Blk_SSDB(data=loaderheader.get())

# Incorporate the loader data into a TZX block.
loaderblock2 = Blk_SSDB(data=loaderdata.get())

# Incorporate the screen's header into a TZX block.
screenblock1 = Blk_SSDB(data=screenheader.get())

# Incorporate the screen's data into a TZX block.
screenblock2 = Blk_SSDB(data=screendata.get())

# Now we create a new TZX layout and add the TZX blocks to it in the order that
# you want them to appear on the tape.
logotape = TZX()
logotape.add_block(loaderblock1)
logotape.add_block(loaderblock2)
logotape.add_block(screenblock1)
logotape.add_block(screenblock2)

# Almost complete, the final stage is to write the TZX to a file.
tzxfile = open('pylogo.tzx', 'wb')
logotape.write(tzxfile)
tzxfile.close()

# The resulting tzx file should load and run in an emulator!