#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-pmt" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-pmt APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-pmt PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-pmt.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-pmt.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-pmt )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-pmt "${_IMPORT_PREFIX}/lib/gnuradio-pmt.lib" "${_IMPORT_PREFIX}/bin/gnuradio-pmt.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
