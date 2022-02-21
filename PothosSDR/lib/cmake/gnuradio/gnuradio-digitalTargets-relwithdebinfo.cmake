#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-digital" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-digital APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-digital PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-digital.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-digital.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-digital )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-digital "${_IMPORT_PREFIX}/lib/gnuradio-digital.lib" "${_IMPORT_PREFIX}/bin/gnuradio-digital.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
