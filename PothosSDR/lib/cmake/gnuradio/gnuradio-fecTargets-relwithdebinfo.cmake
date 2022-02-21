#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-fec" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-fec APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-fec PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-fec.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-fec.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-fec )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-fec "${_IMPORT_PREFIX}/lib/gnuradio-fec.lib" "${_IMPORT_PREFIX}/bin/gnuradio-fec.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
