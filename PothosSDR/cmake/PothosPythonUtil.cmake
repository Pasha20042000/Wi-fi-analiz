if(DEFINED INCLUDED_POTHOS_PYTHON_UTIL_CMAKE)
    return()
endif()
set(INCLUDED_POTHOS_PYTHON_UTIL_CMAKE TRUE)

# the directory which contains this CMake module
set(POTHOS_PYTHON_UTIL_CMAKE_DIR "${CMAKE_CURRENT_LIST_DIR}")

########################################################################
# Find python interp
########################################################################
find_package(PythonInterp)
if (NOT PYTHONINTERP_FOUND)
    message(WARNING "Python bindings require python exe, skipping...")
endif ()
message(STATUS "PYTHON_EXECUTABLE: ${PYTHON_EXECUTABLE}")

########################################################################
# Determine install directory
########################################################################
execute_process(
    COMMAND ${PYTHON_EXECUTABLE} -c
    "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True, prefix=''))"
    OUTPUT_STRIP_TRAILING_WHITESPACE
    OUTPUT_VARIABLE POTHOS_PYTHON_DIR_SYSCONF
)
set(POTHOS_PYTHON_DIR "${POTHOS_PYTHON_DIR_SYSCONF}" CACHE STRING "python install prefix")

file(TO_CMAKE_PATH "${POTHOS_PYTHON_DIR}" POTHOS_PYTHON_DIR)
message(STATUS "POTHOS_PYTHON_DIR: \${prefix}/${POTHOS_PYTHON_DIR}")

if(NOT POTHOS_PYTHON_DIR)
    message(WARNING "Python: get_python_lib() extraction failed, skipping...")
endif(NOT POTHOS_PYTHON_DIR)

########################################################################
## POTHOS_PYTHON_UTIL - build and install python modules for Pothos
##
## TARGET - the name of the module to build
## This module will contain the block factory registrations
## and block description markup parsed out of the sources.
##
## SOURCES - the list of python sources to install
##
## FACTORIES - a list of block paths to python module paths
## Each entry in the factories list is a colon separated tuple of
## /block/registry/path:MyPythonModule.ClassName
##
## DESTINATION - relative destination path
## This is the destination for the python sources and the module.
##
## DOC_SOURCES - an alternative list of sources to scan for docs
##
## ENABLE_DOCS - enable scanning of SOURCES for documentation markup.
##
## Most arguments are passed directly to the POTHOS_MODULE_UTIL()
## See documentation for POTHOS_MODULE_UTIL() in PothosUtil.cmake
########################################################################
function(POTHOS_PYTHON_UTIL)

    include(CMakeParseArguments)
    CMAKE_PARSE_ARGUMENTS(POTHOS_PYTHON_UTIL "ENABLE_DOCS" "TARGET;DESTINATION" "SOURCES;DOC_SOURCES;FACTORIES" ${ARGN})

    #generate block registries
    unset(factory_sources)
    foreach(factory ${POTHOS_PYTHON_UTIL_FACTORIES})

        #parse the factory markup string
        string(REGEX MATCH "^(.+):(.+)$" factory_matched "${factory}")
        if (NOT factory_matched)
            message(FATAL_ERROR "malformed factory string: '${factory}'")
        endif()

        #extract registration variables
        set(block_path ${CMAKE_MATCH_1})
        set(class_name ${CMAKE_MATCH_2})
        string(REPLACE "/" "." package_name "${POTHOS_PYTHON_UTIL_DESTINATION}")

        #generate a registration
        set(factory_source ${CMAKE_CURRENT_BINARY_DIR}/${class_name}Factory.cpp)
        configure_file(
            ${POTHOS_PYTHON_UTIL_CMAKE_DIR}/PothosPythonBlockFactory.in.cpp
            ${factory_source}
        @ONLY)
        list(APPEND factory_sources ${factory_source})
    endforeach(factory)

    #install python sources
    if (POTHOS_PYTHON_UTIL_SOURCES)
        install(
            FILES ${POTHOS_PYTHON_UTIL_SOURCES}
            DESTINATION ${POTHOS_PYTHON_DIR}/${POTHOS_PYTHON_UTIL_DESTINATION}
        )
    endif()

    #build the module
    list(APPEND POTHOS_PYTHON_UTIL_SOURCES ${factory_sources})
    if (POTHOS_PYTHON_UTIL_ENABLE_DOCS)
        set(POTHOS_PYTHON_UTIL_ENABLE_DOCS "ENABLE_DOCS")
    else()
        unset(POTHOS_PYTHON_UTIL_ENABLE_DOCS)
    endif()
    POTHOS_MODULE_UTIL(
        TARGET ${POTHOS_PYTHON_UTIL_TARGET}
        DESTINATION ${POTHOS_PYTHON_UTIL_DESTINATION}
        SOURCES ${POTHOS_PYTHON_UTIL_SOURCES}
        DOC_SOURCES ${POTHOS_PYTHON_UTIL_DOC_SOURCES}
        ${POTHOS_PYTHON_UTIL_ENABLE_DOCS}
    )

endfunction(POTHOS_PYTHON_UTIL)
