find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_DMR gnuradio-dmr)

FIND_PATH(
    GR_DMR_INCLUDE_DIRS
    NAMES gnuradio/dmr/api.h
    HINTS $ENV{DMR_DIR}/include
        ${PC_DMR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_DMR_LIBRARIES
    NAMES gnuradio-dmr
    HINTS $ENV{DMR_DIR}/lib
        ${PC_DMR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-dmrTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_DMR DEFAULT_MSG GR_DMR_LIBRARIES GR_DMR_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_DMR_LIBRARIES GR_DMR_INCLUDE_DIRS)
