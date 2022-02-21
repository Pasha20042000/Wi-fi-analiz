#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-soapy" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-soapy APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-soapy PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-soapy.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-soapy.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-soapy )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-soapy "${_IMPORT_PREFIX}/lib/gnuradio-soapy.lib" "${_IMPORT_PREFIX}/bin/gnuradio-soapy.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
