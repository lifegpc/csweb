find_package(PkgConfig)
if (PkgConfig_FOUND)
    pkg_check_modules(PC_CMARKGFM QUIET IMPORTED_TARGET GLOBAL libcmark-gfm)
endif()

if (PC_CMARKGFM_FOUND)
    set(CMARKGFM_FOUND TRUE)
    set(CMARKGFM_VERSION ${PC_CMARKGFM_VERSION})
    set(CMARKGFM_VERSION_STRING ${PC_CMARKGFM_STRING})
    set(CMARKGFM_LIBRARYS ${PC_CMARKGFM_LIBRARIES})
    if (USE_STATIC_LIBS)
        set(CMARKGFM_INCLUDE_DIRS ${PC_CMARKGFM_STATIC_INCLUDE_DIRS})
    else()
        set(CMARKGFM_INCLUDE_DIRS ${PC_CMARKGFM_INCLUDE_DIRS})
    endif()
    if (NOT TARGET CMARKGFM::CMARKGFM)
        add_library(CMARKGFM::CMARKGFM ALIAS PkgConfig::PC_CMARKGFM)
    endif()
else()
    message(FATAL_ERROR "failed.")
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(CMARKGFM
    FOUND_VAR CMARKGFM_FOUND
    REQUIRED_VARS
        CMARKGFM_LIBRARYS
    VERSION_VAR CMARKGFM_VERSION
)
