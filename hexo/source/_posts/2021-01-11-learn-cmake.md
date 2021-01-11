---
title: 学习CMake
date: 2021-01-11 20:56:32
tags: cpp
---

https://hsf-training.github.io/hsf-training-cmake-webpage/

## 1. 构建

### 构建 

```shell
git clone --recursive https://github.com/CLIUtils/CLI11.git
cd CLI11
cmake -S . -B build
cmake --build build
cmake --build build --target test
```

### 另一种构建

```shell
mkdir build
cd build
cmake ..
make
make test
```

**永远不要**在源码目录直接 `cmake .` 这样会污染源码目录。

### 选择编译器

```shell
CC=clang CXX=clang++ cmake -S . -B build
```

### 设置选项 `-D` 列出选项 `-L`

- [`CMAKE_BUILD_TYPE`](https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html):  `Release`, `RelWithDebInfo`, `Debug`, 或其他编译选项。
- [`CMAKE_INSTALL_PREFIX`](https://cmake.org/cmake/help/latest/variable/CMAKE_INSTALL_PREFIX.html): 安装位置，Unix上默认是 `/usr/local` , 用户安装目录常是 `~/.local` 
- [`BUILD_SHARED_LIBS`](https://cmake.org/cmake/help/latest/variable/BUILD_SHARED_LIBS.html):  `ON` or `OFF` 
- [`BUILD_TESTING`](https://cmake.org/cmake/help/latest/module/CTest.html): 

### 调试Cmake files 在source目录执行下面的命令：

```shell
cmake build --trace-source="CMakeLists.txt"
```

## 2. 编写 CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.14)
# 项目名称，未设置LANGUAGES的话，则是 C, CXX 的混合项目
project(MyProject)
# 至少一个 add_executeable 或 add_library 来作为target。
add_executable(myexample simple.cpp)
```

可以设置更多信息

```cmake
# 最小。。最大版本
cmake_minimum_required(VERSION 3.14...3.18)
# 更详细的项目信息
project(MyProject
  VERSION
    1.0
  DESCRIPTION
    "Very nice project"
  LANGUAGES
    CXX
)

# 可添加 STATIC, SHARED, or MODULE; 默认通过 BUILD_SHARED_LIBS 选择.
add_library(mylibrary simplelib.cpp)

```

### Target可用的设置

- [`target_link_libraries`](https://cmake.org/cmake/help/latest/command/target_link_libraries.html): Other targets; can also pass library names directly
- [`target_include_directories`](https://cmake.org/cmake/help/latest/command/target_include_directories.html): Include directories
- [`target_compile_features`](https://cmake.org/cmake/help/latest/command/target_compile_features.html): The compiler features you need activated, like `cxx_std_11`
- [`target_compile_definitions`](https://cmake.org/cmake/help/latest/command/target_compile_definitions.html): Definitions
- [`target_compile_options`](https://cmake.org/cmake/help/latest/command/target_compile_options.html): More general compile flags
- [`target_link_directories`](https://cmake.org/cmake/help/latest/command/target_link_directories.html): Don’t use, give full paths instead (CMake 3.13+)
- [`target_link_options`](https://cmake.org/cmake/help/latest/command/target_link_options.html): General link flags (CMake 3.13+)
- [`target_sources`](https://cmake.org/cmake/help/latest/command/target_sources.html): Add source files

```cmake
# 不需要添加任何source，导出一个 header-only library。
add_library(some_header_only_lib INTERFACE)
```

#### 什么是 INTERFACE IMPORETED？？

### Script

```cmake
# cache.cmake
# 设置变量
set(MY_VARIABLE "I am a variable")
message(STATUS "${MY_VARIABLE}")

set(MY_CACHE_VAR "I am a cached variable" CACHE STRING "Description")
message(STATUS "${MY_CACHE_VAR}")
```

```shell
cmake -DMY_CACHE_VAR="command line" -P cache.cmake
```

Try setting a cached variable using `-DMY_VARIABLE=something` *before* the `-P`. Which variable is shown?

```cmake
option(MY_OPTION "On or off" OFF)
# $ENV{name}
# if(DEFINED ENV{name})  
file(GLOB OUTPUT_VAR *.cxx)
file(GLOB_RECURSE  OUTPU_VAR *.cxx)
```



## 3. 项目结构

```
code/03-structure/
├── CMakeLists.txt
├── README.md
├── apps
│   ├── CMakeLists.txt
│   └── app.cpp
├── cmake
│   └── FindSomeLib.cmake
├── docs
│   ├── CMakeLists.txt
│   └── mainpage.md
├── include
│   └── modern
│       └── lib.hpp
├── src
│   ├── CMakeLists.txt
│   └── lib.cpp
└── tests
    ├── CMakeLists.txt
    └── testlib.cpp
```



### /CMakeLists.txt

```cmake
# Works with 3.14 and tested through 3.18
cmake_minimum_required(VERSION 3.14...3.18)

# Project name and a few useful settings. Other commands can pick up the results
project(
  ModernCMakeExample
  VERSION 0.1
  DESCRIPTION "An example project with CMake"
  LANGUAGES CXX)

# 仅在主项目中运行，若是子项目中 add_subdirectory 则忽略
if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)

  # Optionally set things like CMAKE_CXX_STANDARD,
  # CMAKE_POSITION_INDEPENDENT_CODE here

  # Let's ensure -std=c++xx instead of -std=g++xx
  set(CMAKE_CXX_EXTENSIONS OFF)

  # Let's nicely support folders in IDE's
  set_property(GLOBAL PROPERTY USE_FOLDERS ON)

  # Testing only available if this is the main app. Note this needs to be done
  # in the main CMakeLists since it calls enable_testing, which must be in the
  # main CMakeLists.
  include(CTest)

  # Docs only available if this is the main app
  find_package(Doxygen)
  if(Doxygen_FOUND)
    add_subdirectory(docs)
  else()
    message(STATUS "Doxygen not found, not building docs")
  endif()
endif()

# FetchContent added in CMake 3.11, downloads during the configure step
# FetchContent_MakeAvailable was not added until CMake 3.14
include(FetchContent)

# Accumulator library This is header only, so could be replaced with git
# submodules or FetchContent
find_package(Boost REQUIRED)
# Adds Boost::boost / Boost::headers (newer FindBoost / BoostConfig 3.15 name)

# Formatting library, adds fmt::fmt
FetchContent_Declare(
  fmtlib
  GIT_REPOSITORY https://github.com/fmtlib/fmt.git
  GIT_TAG 7.0.2)
FetchContent_MakeAvailable(fmtlib)

# The compiled library code is here
add_subdirectory(src)

# The executable code is here
add_subdirectory(apps)

# Testing only available if this is the main app
if(BUILD_TESTING)
  add_subdirectory(tests)
endif()
```

### /src/CMakeLists.txt

```cmake
# Note that headers are optional, and do not affect add_library, but they will
# not show up in IDEs unless they are listed in add_library.

# Optionally glob, but only for CMake 3.12 or later: file(GLOB HEADER_LIST
# CONFIGURE_DEPENDS "${ModernCMakeExample_SOURCE_DIR}/include/modern/*.hpp")
set(HEADER_LIST "${ModernCMakeExample_SOURCE_DIR}/include/modern/lib.hpp")

# Make an automatic library - will be static or dynamic based on user setting
add_library(modern_library lib.cpp ${HEADER_LIST})

# We need this directory, and users of our library will need it too
target_include_directories(modern_library PUBLIC ../include)

# This depends on (header only) boost
target_link_libraries(modern_library PRIVATE Boost::boost)

# All users of this library will need at least C++11
target_compile_features(modern_library PUBLIC cxx_std_11)

# IDEs should put the headers in a nice place
source_group(
  TREE "${PROJECT_SOURCE_DIR}/include"
  PREFIX "Header Files"
  FILES ${HEADER_LIST})
```

### /apps/CMakeLists.txt

```cmake
add_executable(app app.cpp)
target_compile_features(app PRIVATE cxx_std_17)

target_link_libraries(app PRIVATE modern_library fmt::fmt)
```

### /docs/CMakeLists.txt

```cmake

set(DOXYGEN_EXTRACT_ALL YES)
set(DOXYGEN_BUILTIN_STL_SUPPORT YES)

doxygen_add_docs(docs modern/lib.hpp "${CMAKE_CURRENT_SOURCE_DIR}/mainpage.md"
                 WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/include")
```

### /tests/CMakeLists.txt

```cmake
# Testing library
FetchContent_Declare(
  catch2
  GIT_REPOSITORY https://github.com/catchorg/Catch2.git
  GIT_TAG v2.9.1)
FetchContent_MakeAvailable(catch2)
# Adds Catch2::Catch2

# Tests need to be added as executables first
add_executable(testlib testlib.cpp)

# I'm using C++17 in the test
target_compile_features(testlib PRIVATE cxx_std_17)

# Should be linked to the main library, as well as the Catch2 testing library
target_link_libraries(testlib PRIVATE modern_library Catch2::Catch2)

# If you register a test, then ctest and make test will run it. You can also run
# examples and check the output, as well.
add_test(NAME testlibtest COMMAND testlib) # Command can be a target
```



[更多内容](https://hsf-training.github.io/hsf-training-cmake-webpage/)