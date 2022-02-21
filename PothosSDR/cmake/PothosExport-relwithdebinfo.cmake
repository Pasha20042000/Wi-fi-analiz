#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Pothos" for configuration "RelWithDebInfo"
set_property(TARGET Pothos APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Pothos PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/Pothos.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/Pothos.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS Pothos )
list(APPEND _IMPORT_CHECK_FILES_FOR_Pothos "${_IMPORT_PREFIX}/lib/Pothos.lib" "${_IMPORT_PREFIX}/bin/Pothos.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
