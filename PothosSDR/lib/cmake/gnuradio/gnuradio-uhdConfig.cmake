# Copyright 2018 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

include(CMakeFindDependencyMacro)

set(target_deps "UHD")
foreach(dep IN LISTS target_deps)
    find_package(${dep})
endforeach()
include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-uhdTargets.cmake")
