#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-dtv" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-dtv APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-dtv PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-dtv.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-dtv.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-dtv )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-dtv "${_IMPORT_PREFIX}/lib/gnuradio-dtv.lib" "${_IMPORT_PREFIX}/bin/gnuradio-dtv.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
