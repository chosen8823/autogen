#include "../include/neural_vst_plugin.h"
#include <algorithm>
#include <cmath>
#include <cstring>

// Conditional includes for neural inference libraries
#ifdef USE_LIBTORCH
#include <torch/script.h>
#endif

#ifdef USE_ONNX
#include <onnxruntime_cxx_api.h>
#endif

namespace NeuralVST {

//------------------------------------------------------------------------
// NeuralProcessor Implementation
//------------------------------------------------------------------------
NeuralProcessor::NeuralProcessor()
    : modelLoaded(false)
    , sampleRate(44100.0)
    , maxBlockSize(4096)
    , mixAmount(1.0f)
    , gainAmount(1.0f)
    , modelHandle(nullptr)
{
}

//------------------------------------------------------------------------
NeuralProcessor::~NeuralProcessor()
{
    cleanup();
}

//------------------------------------------------------------------------
bool NeuralProcessor::initialize(double sampleRate_, int32_t maxBlockSize_)
{
    sampleRate = sampleRate_;
    maxBlockSize = maxBlockSize_;

    // Pre-allocate buffers
    inputBuffer.resize(2);
    outputBuffer.resize(2);
    for (size_t i = 0; i < 2; ++i) {
        inputBuffer[i].resize(maxBlockSize, 0.0f);
        outputBuffer[i].resize(maxBlockSize, 0.0f);
    }

    return true;
}

//------------------------------------------------------------------------
void NeuralProcessor::cleanup()
{
    unloadModel();
    inputBuffer.clear();
    outputBuffer.clear();
}

//------------------------------------------------------------------------
bool NeuralProcessor::loadModel(const std::string& modelPath)
{
    // Unload any existing model
    unloadModel();

    currentModelPath = modelPath;

#ifdef USE_LIBTORCH
    try {
        // Load TorchScript model
        torch::jit::script::Module* module = new torch::jit::script::Module();
        *module = torch::jit::load(modelPath);
        module->eval(); // Set to evaluation mode
        modelHandle = static_cast<void*>(module);
        modelLoaded = true;
        return true;
    } catch (const c10::Error& e) {
        // Log error in production
        modelLoaded = false;
        return false;
    }
#endif

#ifdef USE_ONNX
    try {
        // Load ONNX model
        Ort::Env* env = new Ort::Env(ORT_LOGGING_LEVEL_WARNING, "NeuralVST");
        Ort::SessionOptions sessionOptions;
        sessionOptions.SetIntraOpNumThreads(1);
        sessionOptions.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

        Ort::Session* session = new Ort::Session(*env, modelPath.c_str(), sessionOptions);
        modelHandle = static_cast<void*>(session);
        modelLoaded = true;
        return true;
    } catch (const Ort::Exception& e) {
        // Log error in production
        modelLoaded = false;
        return false;
    }
#endif

    // If no inference library is available, just mark as loaded
    // but processing will be bypass/simple processing
    modelLoaded = true;
    return true;
}

//------------------------------------------------------------------------
void NeuralProcessor::unloadModel()
{
    if (!modelLoaded)
        return;

#ifdef USE_LIBTORCH
    if (modelHandle) {
        torch::jit::script::Module* module = static_cast<torch::jit::script::Module*>(modelHandle);
        delete module;
        modelHandle = nullptr;
    }
#endif

#ifdef USE_ONNX
    if (modelHandle) {
        Ort::Session* session = static_cast<Ort::Session*>(modelHandle);
        delete session;
        modelHandle = nullptr;
    }
#endif

    modelLoaded = false;
    currentModelPath.clear();
}

//------------------------------------------------------------------------
void NeuralProcessor::processAudio(const float** inputs, float** outputs,
                                   int32_t numChannels, int32_t numSamples)
{
    if (!modelLoaded || numChannels <= 0 || numSamples <= 0) {
        // Bypass - copy input to output
        for (int32_t ch = 0; ch < numChannels; ++ch) {
            memcpy(outputs[ch], inputs[ch], numSamples * sizeof(float));
        }
        return;
    }

    // Prepare buffers
    prepareBuffers(numChannels, numSamples);

#ifdef USE_LIBTORCH
    if (modelHandle) {
        try {
            torch::jit::script::Module* module = static_cast<torch::jit::script::Module*>(modelHandle);

            // Convert audio to tensor [batch, channels, samples]
            std::vector<float> audioData;
            audioData.reserve(numChannels * numSamples);
            for (int32_t ch = 0; ch < numChannels; ++ch) {
                audioData.insert(audioData.end(), inputs[ch], inputs[ch] + numSamples);
            }

            auto options = torch::TensorOptions().dtype(torch::kFloat32);
            torch::Tensor inputTensor = torch::from_blob(
                audioData.data(),
                {1, numChannels, numSamples},
                options).clone();

            // Run inference
            std::vector<torch::jit::IValue> inputsVec;
            inputsVec.push_back(inputTensor);
            torch::Tensor outputTensor = module->forward(inputsVec).toTensor();

            // Convert tensor back to audio
            auto outputData = outputTensor.accessor<float, 3>();
            for (int32_t ch = 0; ch < numChannels; ++ch) {
                for (int32_t s = 0; s < numSamples; ++s) {
                    float processed = outputData[0][ch][s];
                    // Apply mix and gain
                    outputs[ch][s] = inputs[ch][s] * (1.0f - mixAmount) +
                                    processed * mixAmount * gainAmount;
                }
            }
            return;
        } catch (const c10::Error& e) {
            // Fall through to simple processing on error
        }
    }
#endif

#ifdef USE_ONNX
    if (modelHandle) {
        try {
            Ort::Session* session = static_cast<Ort::Session*>(modelHandle);

            // Prepare input tensor
            std::vector<int64_t> inputShape = {1, numChannels, numSamples};
            std::vector<float> audioData;
            audioData.reserve(numChannels * numSamples);
            for (int32_t ch = 0; ch < numChannels; ++ch) {
                audioData.insert(audioData.end(), inputs[ch], inputs[ch] + numSamples);
            }

            // Create input tensor
            Ort::MemoryInfo memInfo = Ort::MemoryInfo::CreateCpu(
                OrtArenaAllocator, OrtMemTypeDefault);
            Ort::Value inputTensor = Ort::Value::CreateTensor<float>(
                memInfo, audioData.data(), audioData.size(),
                inputShape.data(), inputShape.size());

            // Run inference
            const char* inputNames[] = {"input"};
            const char* outputNames[] = {"output"};
            auto outputTensors = session->Run(
                Ort::RunOptions{nullptr},
                inputNames, &inputTensor, 1,
                outputNames, 1);

            // Get output data
            float* outputData = outputTensors[0].GetTensorMutableData<float>();
            for (int32_t ch = 0; ch < numChannels; ++ch) {
                for (int32_t s = 0; s < numSamples; ++s) {
                    float processed = outputData[ch * numSamples + s];
                    outputs[ch][s] = inputs[ch][s] * (1.0f - mixAmount) +
                                    processed * mixAmount * gainAmount;
                }
            }
            return;
        } catch (const Ort::Exception& e) {
            // Fall through to simple processing on error
        }
    }
#endif

    // Simple processing (when no neural library is available)
    // Apply a simple gain and saturation as demonstration
    for (int32_t ch = 0; ch < numChannels; ++ch) {
        for (int32_t s = 0; s < numSamples; ++s) {
            float sample = inputs[ch][s];

            // Simple waveshaping/saturation
            float processed = std::tanh(sample * gainAmount * 2.0f);

            // Mix dry and wet
            outputs[ch][s] = sample * (1.0f - mixAmount) + processed * mixAmount;
        }
    }
}

//------------------------------------------------------------------------
void NeuralProcessor::prepareBuffers(int32_t numChannels, int32_t numSamples)
{
    if (static_cast<int32_t>(inputBuffer.size()) < numChannels) {
        inputBuffer.resize(numChannels);
        outputBuffer.resize(numChannels);
    }

    for (int32_t ch = 0; ch < numChannels; ++ch) {
        if (static_cast<int32_t>(inputBuffer[ch].size()) < numSamples) {
            inputBuffer[ch].resize(numSamples);
            outputBuffer[ch].resize(numSamples);
        }
    }
}

} // namespace NeuralVST
