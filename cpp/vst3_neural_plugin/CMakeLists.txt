cmake_minimum_required(VERSION 3.15)

project(NeuralVSTPlugin VERSION 1.0.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Options for neural inference backends
option(USE_LIBTORCH "Build with LibTorch support" OFF)
option(USE_ONNX "Build with ONNX Runtime support" OFF)
option(USE_PYTHON "Build with Python/AutoGen support" ON)

# VST3 SDK Path - Users need to set this
if(NOT DEFINED VST3_SDK_ROOT)
    set(VST3_SDK_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../../vst3sdk"
        CACHE PATH "Path to VST3 SDK")
endif()

# Check if VST3 SDK exists
if(NOT EXISTS "${VST3_SDK_ROOT}")
    message(WARNING "VST3 SDK not found at ${VST3_SDK_ROOT}")
    message(WARNING "Please download from https://github.com/steinbergmedia/vst3sdk")
    message(WARNING "Or set VST3_SDK_ROOT to the correct path")
endif()

# Add VST3 SDK
if(EXISTS "${VST3_SDK_ROOT}")
    add_subdirectory(${VST3_SDK_ROOT} ${CMAKE_BINARY_DIR}/vst3sdk)

    # Create the VST3 plugin
    set(target neural_vst_plugin)

    # Source files
    set(SOURCES
        src/neural_vst_plugin.cpp
        src/neural_processor.cpp
        src/autogen_bridge.cpp
        src/factory.cpp
    )

    set(HEADERS
        include/neural_vst_plugin.h
    )

    # Create the VST3 plugin target
    smtg_add_vst3plugin(${target} ${SOURCES} ${HEADERS})

    # Set plugin properties
    set_target_properties(${target} PROPERTIES
        OUTPUT_NAME "NeuralVSTPlugin"
        BUNDLE TRUE
    )

    # Include directories
    target_include_directories(${target} PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${VST3_SDK_ROOT}
    )

    # Link VST3 SDK libraries
    target_link_libraries(${target} PRIVATE
        sdk
        pluginterfaces
    )

    # Python support
    if(USE_PYTHON)
        find_package(Python3 COMPONENTS Interpreter Development)
        if(Python3_FOUND)
            target_include_directories(${target} PRIVATE ${Python3_INCLUDE_DIRS})
            target_link_libraries(${target} PRIVATE ${Python3_LIBRARIES})
            target_compile_definitions(${target} PRIVATE USE_PYTHON=1)
            message(STATUS "Python support enabled: ${Python3_VERSION}")
        else()
            message(WARNING "Python not found, building without AutoGen support")
            set(USE_PYTHON OFF)
        endif()
    endif()

    # LibTorch support
    if(USE_LIBTORCH)
        find_package(Torch REQUIRED)
        target_link_libraries(${target} PRIVATE ${TORCH_LIBRARIES})
        target_compile_definitions(${target} PRIVATE USE_LIBTORCH=1)
        message(STATUS "LibTorch support enabled")
    endif()

    # ONNX Runtime support
    if(USE_ONNX)
        # User needs to provide ONNX Runtime path
        if(NOT DEFINED ONNXRUNTIME_ROOT)
            set(ONNXRUNTIME_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../../onnxruntime"
                CACHE PATH "Path to ONNX Runtime")
        endif()

        if(EXISTS "${ONNXRUNTIME_ROOT}")
            target_include_directories(${target} PRIVATE ${ONNXRUNTIME_ROOT}/include)
            target_link_directories(${target} PRIVATE ${ONNXRUNTIME_ROOT}/lib)
            target_link_libraries(${target} PRIVATE onnxruntime)
            target_compile_definitions(${target} PRIVATE USE_ONNX=1)
            message(STATUS "ONNX Runtime support enabled")
        else()
            message(WARNING "ONNX Runtime not found at ${ONNXRUNTIME_ROOT}")
            set(USE_ONNX OFF)
        endif()
    endif()

    # Platform-specific settings
    if(APPLE)
        set_target_properties(${target} PROPERTIES
            BUNDLE TRUE
            BUNDLE_EXTENSION "vst3"
            MACOSX_BUNDLE_GUI_IDENTIFIER "com.autogen.neuralvst"
            MACOSX_BUNDLE_BUNDLE_NAME "NeuralVSTPlugin"
        )
    elseif(WIN32)
        # Windows-specific settings
        target_compile_definitions(${target} PRIVATE _CRT_SECURE_NO_WARNINGS)
    endif()

    # Install target
    smtg_target_setup_universal_binary(${target})

    message(STATUS "Neural VST Plugin configured successfully")
    message(STATUS "  - VST3 SDK: ${VST3_SDK_ROOT}")
    message(STATUS "  - Python Support: ${USE_PYTHON}")
    message(STATUS "  - LibTorch Support: ${USE_LIBTORCH}")
    message(STATUS "  - ONNX Support: ${USE_ONNX}")

else()
    message(STATUS "VST3 SDK not available - skipping plugin build")
    message(STATUS "To build the plugin:")
    message(STATUS "  1. Download VST3 SDK from https://github.com/steinbergmedia/vst3sdk")
    message(STATUS "  2. Set VST3_SDK_ROOT to the SDK path")
    message(STATUS "  3. Re-run CMake")
endif()

# Add Python module directory to build
add_subdirectory(python)
