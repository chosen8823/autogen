# Neural VST Plugin Architecture

## Overview

This document describes the architecture of the Neural VST Plugin with AutoGen integration. The system combines real-time audio processing, neural network inference, and multi-agent decision-making.

## System Components

### 1. VST3 Plugin Layer (C++)

The VST3 plugin implements the standard Steinberg VST3 interface and manages real-time audio processing.

#### NeuralVSTPlugin Class
- **Responsibilities**:
  - Audio I/O management
  - Parameter handling
  - Plugin lifecycle (initialize, activate, process, deactivate, terminate)
  - State management (save/restore)
  - Bus arrangement configuration

- **Key Methods**:
  - `process()`: Main audio processing callback
  - `initialize()`: Setup plugin resources
  - `setState()/getState()`: Persistence
  - `setupProcessing()`: Configure sample rate and buffer size

#### Audio Flow
```
DAW Audio Thread
    ↓
process() callback
    ↓
Update Parameters
    ↓
NeuralProcessor::processAudio()
    ↓
Output to DAW
```

### 2. Neural Processor (C++)

Handles neural network inference for audio processing.

#### NeuralProcessor Class
- **Responsibilities**:
  - Load and manage neural models (TorchScript/ONNX)
  - Real-time inference
  - Audio buffer conversion (audio ↔ tensor)
  - Mix/gain processing

- **Inference Backends**:
  1. **LibTorch** (PyTorch C++)
     - Load `.pt` TorchScript models
     - CPU and CUDA support
     - Dynamic shape handling

  2. **ONNX Runtime**
     - Load `.onnx` models
     - Optimized inference
     - Cross-platform acceleration

  3. **Fallback**
     - Simple waveshaping when no backend available
     - Always functional

#### Processing Pipeline
```
Input Audio Buffer (float**)
    ↓
prepareBuffers()
    ↓
convertToTensor()
    ↓
model.forward() / Run()
    ↓
convertFromTensor()
    ↓
Apply Mix & Gain
    ↓
Output Audio Buffer (float**)
```

### 3. AutoGen Bridge (C++/Python)

Connects the C++ plugin to Python-based AutoGen agents.

#### AutoGenBridge Class (C++)
- **Responsibilities**:
  - Python interpreter management
  - C++ ↔ Python communication
  - Feature extraction
  - Agent interaction

- **Key Methods**:
  - `sendAudioFeatures()`: Send audio features to agents
  - `requestModelSelection()`: Get model recommendation
  - `optimizeParameters()`: Get optimized mix/gain

#### Communication Flow
```
C++ Plugin
    ↓
extractAudioFeatures()
    ↓
Python C API
    ↓
NeuralAgentController (Python)
    ↓
AutoGen Agents
    ↓
Return Decision
    ↓
C++ Plugin
```

### 4. AutoGen Multi-Agent System (Python)

Intelligent decision-making using AutoGen's agent framework.

#### NeuralAgentController Class
- **Responsibilities**:
  - Manage AutoGen agents
  - Coordinate agent communication
  - Process agent decisions
  - Feature analysis

#### Agents

1. **Audio Analyzer Agent**
   ```python
   Role: Expert audio analyzer
   Tasks:
   - Analyze audio features
   - Identify content type
   - Detect quality issues
   - Provide recommendations
   ```

2. **Model Selector Agent**
   ```python
   Role: Neural model expert
   Tasks:
   - Select appropriate model
   - Consider performance constraints
   - Balance quality vs. latency
   Available Models:
   - speech_enhancer
   - music_mastering
   - creative_fx
   - general_processor
   ```

3. **Parameter Optimizer Agent**
   ```python
   Role: Parameter optimization expert
   Tasks:
   - Optimize mix parameter
   - Optimize gain parameter
   - Ensure valid ranges [0.0, 1.0]
   - Consider audio characteristics
   ```

## Data Flow

### Real-Time Audio Processing

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DAW sends audio buffer to plugin                         │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Plugin updates parameters from parameter changes         │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. NeuralProcessor processes audio through neural network   │
│    - Convert audio to tensor                                │
│    - Run inference (GPU/CPU)                                │
│    - Convert tensor back to audio                           │
│    - Apply mix and gain                                     │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Return processed audio to DAW                            │
└─────────────────────────────────────────────────────────────┘
```

### Agent Decision-Making (Async)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Extract audio features (background thread)               │
│    - RMS energy                                             │
│    - Peak amplitude                                         │
│    - Zero crossing rate                                     │
│    - Spectral centroid                                      │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Send features to AutoGen bridge                          │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. NeuralAgentController receives features                  │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Agents collaborate to make decisions:                    │
│    - Audio Analyzer: Classify audio type                    │
│    - Model Selector: Choose best model                      │
│    - Parameter Optimizer: Optimize mix/gain                 │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Return decisions to C++ plugin                           │
└───────────────────────┬─────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Plugin updates model and parameters                      │
└─────────────────────────────────────────────────────────────┘
```

## Threading Model

### Audio Thread (Real-Time)
- **Priority**: Highest
- **Tasks**:
  - Audio I/O
  - Parameter updates
  - Neural inference (if fast enough)
- **Constraints**:
  - No memory allocation
  - No blocking operations
  - No Python calls
  - Lock-free where possible

### Background Thread (Non-Real-Time)
- **Priority**: Normal
- **Tasks**:
  - Feature extraction
  - AutoGen communication
  - Model loading
  - Heavy computations
- **Constraints**:
  - Can allocate memory
  - Can block
  - Can call Python

### Synchronization
- `std::mutex` for shared data
- Lock-free queues for audio thread communication
- Parameter updates via atomic operations where possible

## Memory Management

### Audio Buffers
- Pre-allocated at initialization
- Fixed size based on max buffer size
- No allocation in audio thread

### Neural Models
- Loaded once at plugin initialization
- Cached in memory for fast access
- Unloaded at plugin termination

### Python Objects
- Managed by Python C API
- Reference counting for lifetime
- Cleanup at plugin shutdown

## Performance Optimization

### Neural Inference
1. **GPU Acceleration**
   - Use CUDA for LibTorch
   - Use GPU providers for ONNX Runtime
   - Fall back to CPU if GPU unavailable

2. **Model Optimization**
   - Use TorchScript traced models
   - Apply quantization
   - Optimize for target buffer size

3. **Batching**
   - Process entire buffer at once
   - Avoid per-sample processing

### Threading
1. **Offload Heavy Work**
   - Move AutoGen to background thread
   - Use lock-free queues
   - Update parameters asynchronously

2. **Cache Decisions**
   - Cache agent decisions
   - Update periodically, not per-buffer
   - Use time-based or threshold-based updates

## Error Handling

### Audio Thread
- Never throw exceptions
- Fail gracefully to bypass mode
- Log errors for later inspection

### Background Thread
- Catch and log exceptions
- Attempt recovery
- Disable failing components

### Python Integration
- Check Python errors after each API call
- Print Python tracebacks
- Continue without AutoGen if initialization fails

## Extension Points

### Adding New Neural Backends
1. Define compile flag (e.g., `USE_CUSTOM_BACKEND`)
2. Add conditional includes in `neural_processor.cpp`
3. Implement `loadModel()` and `processAudio()` for backend
4. Update CMakeLists.txt

### Adding New Agents
1. Add agent in `NeuralAgentController.__init__()`
2. Define agent role and system message
3. Implement decision method
4. Expose to C++ via bridge

### Custom Audio Features
1. Extend `extractAudioFeatures()` in `autogen_bridge.cpp`
2. Update feature vector size
3. Update agents to use new features

## Future Enhancements

### Planned Features
1. **Adaptive Buffer Processing**
   - Dynamically adjust based on CPU load
   - Latency-aware processing

2. **Model Hot-Swapping**
   - Load models without interrupting audio
   - Smooth transitions between models

3. **Agent Learning**
   - Learn from user preferences
   - Adapt decisions over time

4. **GUI Integration**
   - Visual feedback from agents
   - Interactive parameter control
   - Model visualization

5. **Distributed Processing**
   - Offload inference to remote servers
   - AutoGen distributed runtime

## References

- [VST3 API Documentation](https://steinbergmedia.github.io/vst3_doc/)
- [PyTorch C++ API](https://pytorch.org/cppdocs/)
- [Python C API](https://docs.python.org/3/c-api/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
