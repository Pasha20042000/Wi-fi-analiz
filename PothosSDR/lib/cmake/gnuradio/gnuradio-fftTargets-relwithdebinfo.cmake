#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-fft" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-fft APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-fft PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-fft.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-fft.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-fft )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-fft "${_IMPORT_PREFIX}/lib/gnuradio-fft.lib" "${_IMPORT_PREFIX}/bin/gnuradio-fft.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
