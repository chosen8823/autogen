# Neural VST3 Plugin with AutoGen Integration

A VST3 audio plugin that combines neural network processing with AutoGen's multi-agent framework for intelligent, adaptive audio processing in DAWs like Cakewalk, Ableton, FL Studio, and more.

## Overview

This project demonstrates how to integrate:
- **VST3 SDK** - Industry-standard audio plugin framework
- **Neural Network Inference** - Real-time audio processing using LibTorch or ONNX Runtime
- **AutoGen Multi-Agent System** - Intelligent decision-making for model selection and parameter optimization

## Features

- ✅ **Real-time Neural Audio Processing** - Process audio through neural networks in real-time
- ✅ **AutoGen Integration** - Multi-agent system for intelligent processing decisions
- ✅ **Flexible Model Loading** - Support for TorchScript (.pt) and ONNX models
- ✅ **Parameter Optimization** - AI-driven parameter tuning based on audio characteristics
- ✅ **Cross-Platform** - Windows, macOS, and Linux support
- ✅ **DAW Compatible** - Works with any VST3-compatible DAW

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DAW (Cakewalk, etc.)                  │
└───────────────────────┬─────────────────────────────────┘
                        │ Audio Stream
                        ▼
┌─────────────────────────────────────────────────────────┐
│              Neural VST3 Plugin (C++)                    │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │ Audio I/O    │───▶│   Neural     │───▶│  Output   │ │
│  │  Buffers     │    │  Processor   │    │  Buffers  │ │
│  └──────────────┘    └──────┬───────┘    └───────────┘ │
│                              │                           │
│                              ▼                           │
│                     ┌──────────────┐                    │
│                     │  AutoGen     │                    │
│                     │   Bridge     │                    │
│                     └──────┬───────┘                    │
└────────────────────────────┼────────────────────────────┘
                             │ Python C API
                             ▼
┌─────────────────────────────────────────────────────────┐
│           AutoGen Multi-Agent System (Python)            │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │    Audio     │  │    Model     │  │  Parameter    │ │
│  │   Analyzer   │  │   Selector   │  │  Optimizer    │ │
│  └──────────────┘  └──────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Prerequisites

### Required
- **CMake** 3.15 or later
- **C++ Compiler** with C++17 support (MSVC, GCC, or Clang)
- **Python** 3.10 or later
- **VST3 SDK** - Download from [Steinberg Developer Portal](https://www.steinberg.net/developers/)

### Optional (for neural inference)
- **LibTorch** (PyTorch C++) - For TorchScript model support
- **ONNX Runtime** - For ONNX model support
- **CUDA Toolkit** - For GPU acceleration (highly recommended for real-time)

### Python Dependencies
```bash
pip install autogen-agentchat autogen-ext torch numpy
```

## Building the Plugin

### 1. Download VST3 SDK

```bash
cd cpp
git clone --recursive https://github.com/steinbergmedia/vst3sdk.git
```

### 2. Configure CMake

```bash
cd vst3_neural_plugin
mkdir build && cd build

# Basic build
cmake .. -DVST3_SDK_ROOT=../../vst3sdk

# With LibTorch support
cmake .. -DVST3_SDK_ROOT=../../vst3sdk \
         -DUSE_LIBTORCH=ON \
         -DCMAKE_PREFIX_PATH=/path/to/libtorch

# With ONNX Runtime support
cmake .. -DVST3_SDK_ROOT=../../vst3sdk \
         -DUSE_ONNX=ON \
         -DONNXRUNTIME_ROOT=/path/to/onnxruntime
```

### 3. Build

```bash
# Build the plugin
cmake --build . --config Release

# On Windows with Visual Studio
cmake --build . --config Release --target ALL_BUILD
```

### 4. Install

The plugin will be built in:
- **Windows**: `build/VST3/Release/NeuralVSTPlugin.vst3`
- **macOS**: `build/VST3/Release/NeuralVSTPlugin.vst3`
- **Linux**: `build/VST3/Release/NeuralVSTPlugin.vst3`

Copy the `.vst3` file to your DAW's VST3 plugin folder:
- **Windows**: `C:\Program Files\Common Files\VST3\`
- **macOS**: `~/Library/Audio/Plug-Ins/VST3/`
- **Linux**: `~/.vst3/`

## Creating Neural Models

### Using PyTorch (TorchScript)

```python
# See examples/simple_neural_model.py
python examples/simple_neural_model.py --output my_model.pt

# Test the model
python examples/simple_neural_model.py --output my_model.pt --test
```

The model should:
- Accept input shape: `[batch, channels, samples]`
- Return output shape: `[batch, channels, samples]`
- Output values in range `[-1, 1]`

### Using ONNX

Export your model to ONNX format with the same input/output specifications.

## AutoGen Integration

The plugin uses AutoGen's multi-agent system for intelligent audio processing:

### Audio Analyzer Agent
- Analyzes audio characteristics
- Identifies content type (speech, music, effects)
- Detects quality issues

### Model Selector Agent
- Selects appropriate neural model based on audio content
- Balances quality and performance
- Considers real-time constraints

### Parameter Optimizer Agent
- Optimizes mix and gain parameters
- Adapts to audio characteristics
- Ensures parameters stay in valid ranges

### Running the Demo

```bash
cd examples
python autogen_demo.py
```

This demonstrates how AutoGen agents make processing decisions for different audio types.

## Usage in DAW

1. **Load the Plugin**
   - Open your DAW (Cakewalk, Ableton, etc.)
   - Insert the Neural VST Plugin on an audio track

2. **Configure Parameters**
   - **Mix**: Blend between dry (0%) and processed (100%) signal
   - **Gain**: Output level adjustment
   - **Model**: Select neural processing model
   - **Bypass**: Enable/disable processing

3. **Load a Model** (if using custom models)
   - Place your `.pt` or `.onnx` model file in the plugin directory
   - The plugin will automatically detect and load it

## Parameters

| Parameter | Range | Description |
|-----------|-------|-------------|
| Mix | 0.0 - 1.0 | Dry/wet blend (0 = dry, 1 = fully processed) |
| Gain | 0.0 - 1.0 | Output gain adjustment |
| Model | 0 - 10 | Neural model selection |
| Bypass | On/Off | Enable/disable processing |

## Performance Considerations

### Real-Time Processing
Neural networks are computationally intensive. For real-time audio:

1. **Use GPU Acceleration**
   - Build with CUDA support
   - Use GPU-enabled LibTorch or ONNX Runtime

2. **Optimize Model Size**
   - Keep models lightweight (< 50M parameters)
   - Use quantization if possible
   - Consider model pruning

3. **Buffer Management**
   - Larger buffer sizes reduce CPU load but increase latency
   - Typical real-time buffer: 512-2048 samples
   - Test at your DAW's buffer size

4. **Threading**
   - The plugin uses background processing for heavy operations
   - AutoGen runs in a separate thread to avoid blocking audio

## Project Structure

```
vst3_neural_plugin/
├── CMakeLists.txt           # Build configuration
├── README.md                # This file
├── include/
│   └── neural_vst_plugin.h  # Plugin headers
├── src/
│   ├── neural_vst_plugin.cpp    # Main plugin implementation
│   ├── neural_processor.cpp     # Neural network processing
│   ├── autogen_bridge.cpp       # AutoGen integration
│   └── factory.cpp              # VST3 plugin factory
├── python/
│   ├── __init__.py
│   ├── autogen_vst_bridge.py    # AutoGen agent controller
│   └── CMakeLists.txt
├── examples/
│   ├── simple_neural_model.py   # Create & export models
│   └── autogen_demo.py          # AutoGen demo
└── docs/
    ├── ARCHITECTURE.md          # Detailed architecture
    └── API.md                   # API documentation
```

## Troubleshooting

### Plugin Not Loading in DAW
- Ensure VST3 SDK version compatibility
- Check plugin is in correct VST3 folder
- Verify all dependencies are available
- Check DAW plugin scan/rescan

### Python/AutoGen Not Working
- Ensure Python is in system PATH
- Install required packages: `pip install autogen-agentchat autogen-ext`
- Check Python version (3.10+)
- Verify Python C API linking

### Model Loading Fails
- Check model file format (TorchScript or ONNX)
- Verify model input/output shapes
- Ensure LibTorch/ONNX Runtime is available
- Check model file path accessibility

### High CPU Usage
- Enable GPU acceleration
- Reduce model complexity
- Increase DAW buffer size
- Disable AutoGen if not needed

## Development

### Adding New Models
1. Train your model with compatible I/O shapes
2. Export to TorchScript or ONNX
3. Test with `examples/simple_neural_model.py --test`
4. Place in plugin directory

### Extending AutoGen Agents
1. Modify `python/autogen_vst_bridge.py`
2. Add new agent types
3. Implement new decision logic
4. Test with `examples/autogen_demo.py`

### Custom Audio Features
1. Extend `extractAudioFeatures()` in `autogen_bridge.cpp`
2. Add spectral, temporal, or perceptual features
3. Update Python side to handle new features

## Contributing

Contributions are welcome! Please see the main AutoGen [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE-CODE](../../LICENSE-CODE) for details.

## References

- [VST3 SDK Documentation](https://steinbergmedia.github.io/vst3_doc/)
- [PyTorch C++ API](https://pytorch.org/cppdocs/)
- [ONNX Runtime](https://onnxruntime.ai/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [JUCE Framework](https://juce.com/) - Alternative plugin framework

## Acknowledgments

- **Steinberg** for the VST3 SDK
- **Microsoft AutoGen Team** for the multi-agent framework
- **PyTorch** and **ONNX** teams for neural inference libraries

## Support

For issues and questions:
- Check [FAQ.md](../../FAQ.md)
- Open an issue on [GitHub](https://github.com/microsoft/autogen/issues)
- Join [AutoGen Discord](https://aka.ms/autogen-discord)

---

**Built with ❤️ using AutoGen**
