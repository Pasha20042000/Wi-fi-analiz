#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Volk::volk" for configuration "RelWithDebInfo"
set_property(TARGET Volk::volk APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Volk::volk PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/volk.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/volk.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS Volk::volk )
list(APPEND _IMPORT_CHECK_FILES_FOR_Volk::volk "${_IMPORT_PREFIX}/lib/volk.lib" "${_IMPORT_PREFIX}/bin/volk.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
