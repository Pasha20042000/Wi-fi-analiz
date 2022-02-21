#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-trellis" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-trellis APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-trellis PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-trellis.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-trellis.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-trellis )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-trellis "${_IMPORT_PREFIX}/lib/gnuradio-trellis.lib" "${_IMPORT_PREFIX}/bin/gnuradio-trellis.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
