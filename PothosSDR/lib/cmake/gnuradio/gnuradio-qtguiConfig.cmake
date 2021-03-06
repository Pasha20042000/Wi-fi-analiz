# Copyright 2018 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

include(CMakeFindDependencyMacro)

set(target_deps "Qwt;Qt5Widgets;FFTW3f")
foreach(dep IN LISTS target_deps)
    find_package(${dep})
endforeach()
include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-qtguiTargets.cmake")
