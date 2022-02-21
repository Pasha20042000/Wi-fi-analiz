#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-vocoder" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-vocoder APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-vocoder PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-vocoder.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-vocoder.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-vocoder )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-vocoder "${_IMPORT_PREFIX}/lib/gnuradio-vocoder.lib" "${_IMPORT_PREFIX}/bin/gnuradio-vocoder.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
