#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-audio" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-audio APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-audio PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-audio.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-audio.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-audio )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-audio "${_IMPORT_PREFIX}/lib/gnuradio-audio.lib" "${_IMPORT_PREFIX}/bin/gnuradio-audio.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
