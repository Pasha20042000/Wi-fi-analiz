#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-runtime" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-runtime APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-runtime PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-runtime.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-runtime.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-runtime )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-runtime "${_IMPORT_PREFIX}/lib/gnuradio-runtime.lib" "${_IMPORT_PREFIX}/bin/gnuradio-runtime.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
