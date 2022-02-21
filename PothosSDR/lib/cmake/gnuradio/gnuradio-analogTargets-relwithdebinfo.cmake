#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-analog" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-analog APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-analog PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-analog.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-analog.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-analog )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-analog "${_IMPORT_PREFIX}/lib/gnuradio-analog.lib" "${_IMPORT_PREFIX}/bin/gnuradio-analog.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
