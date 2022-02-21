# Copyright 2013 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

set(MAJOR_VERSION 3)
set(API_COMPAT 9)
set(MINOR_VERSION 2)
set(MAINT_VERSION git)

set(PACKAGE_VERSION
  ${MAJOR_VERSION}.${API_COMPAT}.${MINOR_VERSION}.${MAINT_VERSION})

if("${PACKAGE_VERSION}" VERSION_LESS "${PACKAGE_FIND_VERSION}")
  set(PACKAGE_VERSION_COMPATIBLE FALSE)
else()
  set(PACKAGE_VERSION_COMPATIBLE TRUE)
  if ("${PACKAGE_VERSION}" VERSION_EQUAL "${PACKAGE_FIND_VERSION}")
    set(PACKAGE_VERSION_EXACT TRUE)
  endif()
endif()
