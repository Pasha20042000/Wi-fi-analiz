#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-blocks" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-blocks APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-blocks PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-blocks.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-blocks.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-blocks )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-blocks "${_IMPORT_PREFIX}/lib/gnuradio-blocks.lib" "${_IMPORT_PREFIX}/bin/gnuradio-blocks.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
