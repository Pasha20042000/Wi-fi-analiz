#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "gnuradio::gnuradio-network" for configuration "RelWithDebInfo"
set_property(TARGET gnuradio::gnuradio-network APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(gnuradio::gnuradio-network PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/gnuradio-network.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/gnuradio-network.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS gnuradio::gnuradio-network )
list(APPEND _IMPORT_CHECK_FILES_FOR_gnuradio::gnuradio-network "${_IMPORT_PREFIX}/lib/gnuradio-network.lib" "${_IMPORT_PREFIX}/bin/gnuradio-network.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
