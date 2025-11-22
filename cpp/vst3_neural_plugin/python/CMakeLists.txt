# Python module installation

# Copy Python files to build directory
file(GLOB PYTHON_FILES "${CMAKE_CURRENT_SOURCE_DIR}/*.py")

# Install Python files
install(FILES ${PYTHON_FILES}
        DESTINATION lib/neural_vst_plugin/python
        COMPONENT python)

message(STATUS "Python module configured for Neural VST Plugin")
