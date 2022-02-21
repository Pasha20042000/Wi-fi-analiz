#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-zeromq" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-zeromq APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-zeromq PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-zeromq.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-zeromq.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-zeromq )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-zeromq "${_IMPORT_PREFIX}/lib/gnuradio-zeromq.lib" "${_IMPORT_PREFIX}/bin/gnuradio-zeromq.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
