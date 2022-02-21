#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-wavelet" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-wavelet APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-wavelet PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-wavelet.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-wavelet.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-wavelet )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-wavelet "${_IMPORT_PREFIX}/lib/gnuradio-wavelet.lib" "${_IMPORT_PREFIX}/bin/gnuradio-wavelet.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
