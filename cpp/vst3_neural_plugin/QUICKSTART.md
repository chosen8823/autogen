# Neural VST Plugin - Quick Start Guide

Get up and running with the Neural VST Plugin in under 10 minutes!

## Prerequisites

Make sure you have:
- Python 3.10+ installed
- CMake 3.15+ installed
- C++ compiler (MSVC on Windows, GCC/Clang on Linux/macOS)

## Step 1: Install Python Dependencies (2 minutes)

```bash
cd cpp/vst3_neural_plugin
pip install -r requirements.txt
```

## Step 2: Try the AutoGen Demo (1 minute)

Before building the full plugin, let's see AutoGen in action:

```bash
cd examples
python autogen_demo.py
```

You should see AutoGen agents analyzing different audio types and making intelligent processing decisions!

## Step 3: Create a Test Neural Model (2 minutes)

```bash
# Still in examples/ directory
python simple_neural_model.py --output test_model.pt
```

This creates a lightweight neural network for audio processing.

## Step 4: Download VST3 SDK (1 minute)

```bash
cd ../..  # Back to cpp/ directory
git clone --recursive https://github.com/steinbergmedia/vst3sdk.git
```

## Step 5: Build the Plugin (3 minutes)

### Windows (Visual Studio)
```bash
cd vst3_neural_plugin
mkdir build && cd build
cmake .. -DVST3_SDK_ROOT=../../vst3sdk
cmake --build . --config Release
```

### macOS/Linux
```bash
cd vst3_neural_plugin
mkdir build && cd build
cmake .. -DVST3_SDK_ROOT=../../vst3sdk
make -j4
```

## Step 6: Install the Plugin (1 minute)

### Windows
```bash
# Copy the plugin to VST3 folder
copy VST3\Release\NeuralVSTPlugin.vst3 "C:\Program Files\Common Files\VST3\"
```

### macOS
```bash
cp -r VST3/Release/NeuralVSTPlugin.vst3 ~/Library/Audio/Plug-Ins/VST3/
```

### Linux
```bash
cp -r VST3/Release/NeuralVSTPlugin.vst3 ~/.vst3/
```

## Step 7: Use in Your DAW

1. Open your DAW (Cakewalk, Ableton, FL Studio, etc.)
2. Rescan for plugins if necessary
3. Insert "Neural VST Plugin" on an audio track
4. Adjust the Mix and Gain parameters
5. Process your audio with neural networks!

## What's Happening Under the Hood?

When you load the plugin:

1. **VST3 Layer** handles audio I/O from your DAW
2. **Neural Processor** runs your model on the audio in real-time
3. **AutoGen Bridge** connects to Python for intelligent decisions
4. **Multi-Agent System** optimizes parameters and selects models

## Next Steps

### Add GPU Acceleration (Optional)

For better real-time performance:

```bash
# Install PyTorch with CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Rebuild with LibTorch support
cd build
cmake .. -DVST3_SDK_ROOT=../../vst3sdk \
         -DUSE_LIBTORCH=ON \
         -DCMAKE_PREFIX_PATH=/path/to/libtorch
cmake --build . --config Release
```

### Create Custom Models

1. Train your audio processing model in PyTorch
2. Export to TorchScript:
   ```python
   import torch
   model = YourModel()
   traced = torch.jit.trace(model, example_input)
   traced.save("my_model.pt")
   ```
3. Copy to plugin directory
4. Select in plugin UI

### Customize AutoGen Agents

Edit `python/autogen_vst_bridge.py` to:
- Add new agent types
- Change agent behavior
- Implement custom decision logic
- Add new audio features

## Troubleshooting

### Plugin doesn't load in DAW
- Check that you copied to the correct VST3 folder
- Rescan plugins in your DAW
- Check DAW supports VST3 format

### Build errors
- Ensure VST3 SDK path is correct
- Check C++ compiler is in PATH
- Try a clean build: `rm -rf build && mkdir build`

### Python errors
- Verify Python 3.10+: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check Python is in system PATH

### No audio processing happening
- Check that "Bypass" is OFF
- Increase Mix parameter (controls dry/wet blend)
- Verify model is loaded (check plugin logs)

## Quick Reference

### Parameters
- **Mix**: 0% = dry signal, 100% = fully processed
- **Gain**: Output level adjustment
- **Bypass**: Turn processing on/off

### File Locations
- **Plugin**: VST3 folder (see Step 6)
- **Models**: Place `.pt` files in plugin directory
- **Python**: `cpp/vst3_neural_plugin/python/`

### Useful Commands

```bash
# Test AutoGen demo
python examples/autogen_demo.py

# Create new model
python examples/simple_neural_model.py --output mymodel.pt

# Test a model
python examples/simple_neural_model.py --output mymodel.pt --test

# Rebuild plugin
cd build
cmake --build . --config Release
```

## Getting Help

- 📖 Read the full [README.md](README.md)
- 🏗️ Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) for details
- 💬 Join [AutoGen Discord](https://aka.ms/autogen-discord)
- 🐛 Report issues on [GitHub](https://github.com/microsoft/autogen/issues)

## What's Next?

Now that you have the plugin running:

1. **Experiment** with different neural models
2. **Customize** the AutoGen agents for your workflow
3. **Optimize** for your DAW's buffer size
4. **Share** your models with the community!

---

**🎉 Congratulations!** You're now processing audio with neural networks and AutoGen!
