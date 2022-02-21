#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-filter" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-filter APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-filter PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-filter.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-filter.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-filter )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-filter "${_IMPORT_PREFIX}/lib/gnuradio-filter.lib" "${_IMPORT_PREFIX}/bin/gnuradio-filter.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
