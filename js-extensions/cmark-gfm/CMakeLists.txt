cmake_minimum_required(VERSION 3.6)

project(cmark-gfm-wasm)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../cmake")

find_package(CMARKGFM 0.29.0 REQUIRED)

include(GNUInstallDirs)

add_link_options("SHELL:-s WASM=1")
add_link_options("SHELL:-s EXPORTED_RUNTIME_METHODS='[\"cwrap\"]'")
add_link_options("SHELL:-s EXPORTED_FUNCTIONS='[\"_malloc\", \"_free\", \"_strlen\"]'")
add_link_options("SHELL:--post-js \"${CMAKE_CURRENT_SOURCE_DIR}/post.js\"")
add_link_options("SHELL:--pre-js \"${CMAKE_CURRENT_SOURCE_DIR}/pre.js\"")
add_link_options("SHELL:-s ENVIRONMENT=web")

add_executable(_cmark_gfm cmark_wasm.c)
target_link_libraries(_cmark_gfm CMARKGFM::CMARKGFM)
install(TARGETS _cmark_gfm)
install(FILES ${CMAKE_BINARY_DIR}/_cmark_gfm.wasm DESTINATION ${CMAKE_INSTALL_BINDIR})
