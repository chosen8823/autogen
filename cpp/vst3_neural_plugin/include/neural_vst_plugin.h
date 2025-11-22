#pragma once

#include "public.sdk/source/vst/vstaudioeffect.h"
#include "pluginterfaces/vst/ivstevents.h"
#include "pluginterfaces/vst/ivstparameterchanges.h"
#include <memory>
#include <vector>
#include <mutex>
#include <queue>

namespace NeuralVST {

// Forward declarations
class NeuralProcessor;
class AutoGenBridge;

//------------------------------------------------------------------------
// NeuralVSTPlugin - Main VST3 Plugin Class
//------------------------------------------------------------------------
class NeuralVSTPlugin : public Steinberg::Vst::AudioEffect
{
public:
    NeuralVSTPlugin();
    ~NeuralVSTPlugin() override;

    // AudioEffect overrides
    Steinberg::tresult PLUGIN_API initialize(Steinberg::FUnknown* context) override;
    Steinberg::tresult PLUGIN_API terminate() override;
    Steinberg::tresult PLUGIN_API setActive(Steinberg::TBool state) override;
    Steinberg::tresult PLUGIN_API process(Steinberg::Vst::ProcessData& data) override;
    Steinberg::tresult PLUGIN_API setState(Steinberg::IBStream* state) override;
    Steinberg::tresult PLUGIN_API getState(Steinberg::IBStream* state) override;
    Steinberg::tresult PLUGIN_API setupProcessing(Steinberg::Vst::ProcessSetup& setup) override;
    Steinberg::tresult PLUGIN_API setBusArrangements(
        Steinberg::Vst::SpeakerArrangement* inputs,
        Steinberg::int32 numIns,
        Steinberg::Vst::SpeakerArrangement* outputs,
        Steinberg::int32 numOuts) override;

    // Factory method
    static Steinberg::FUnknown* createInstance(void* context);

    // Plugin UID
    static const Steinberg::FUID kClassUID;

private:
    // Neural processing components
    std::unique_ptr<NeuralProcessor> neuralProcessor;
    std::unique_ptr<AutoGenBridge> autoGenBridge;

    // Audio buffer management
    std::vector<std::vector<float>> processingBuffer;
    std::mutex processingMutex;

    // Plugin state
    bool isProcessingActive;
    double sampleRate;
    int32_t maxSamplesPerBlock;

    // Parameter IDs
    enum ParameterIds {
        kParamMixId = 0,
        kParamGainId = 1,
        kParamModelSelectId = 2,
        kParamBypassId = 3,
        kNumParameters
    };

    // Parameter values
    float mixValue;
    float gainValue;
    int32_t modelSelect;
    bool bypass;

    // Helper methods
    void processAudioBlock(float** inputs, float** outputs, int32_t numChannels, int32_t numSamples);
    void updateParameters(Steinberg::Vst::IParameterChanges* paramChanges);
};

//------------------------------------------------------------------------
// NeuralProcessor - Handles neural network inference
//------------------------------------------------------------------------
class NeuralProcessor
{
public:
    NeuralProcessor();
    ~NeuralProcessor();

    // Initialize with sample rate and block size
    bool initialize(double sampleRate, int32_t maxBlockSize);
    void cleanup();

    // Process audio through neural network
    void processAudio(const float** inputs, float** outputs, int32_t numChannels, int32_t numSamples);

    // Model management
    bool loadModel(const std::string& modelPath);
    void unloadModel();
    bool isModelLoaded() const { return modelLoaded; }

    // Configuration
    void setMixAmount(float mix) { mixAmount = mix; }
    void setGain(float gain) { gainAmount = gain; }

private:
    // Model state
    bool modelLoaded;
    std::string currentModelPath;

    // Processing parameters
    double sampleRate;
    int32_t maxBlockSize;
    float mixAmount;
    float gainAmount;

    // Internal buffers
    std::vector<std::vector<float>> inputBuffer;
    std::vector<std::vector<float>> outputBuffer;

    // Platform-specific neural inference handle (can be LibTorch, ONNX, etc.)
    void* modelHandle;

    // Helper methods
    void prepareBuffers(int32_t numChannels, int32_t numSamples);
    void convertToTensor(const float** audio, int32_t numChannels, int32_t numSamples);
    void convertFromTensor(float** audio, int32_t numChannels, int32_t numSamples);
};

//------------------------------------------------------------------------
// AutoGenBridge - Bridge to Python AutoGen framework
//------------------------------------------------------------------------
class AutoGenBridge
{
public:
    AutoGenBridge();
    ~AutoGenBridge();

    // Initialize Python interpreter and AutoGen
    bool initialize();
    void cleanup();

    // Communication with AutoGen agents
    bool sendAudioFeatures(const std::vector<float>& features);
    bool getProcessingDecision(std::string& decision);

    // Model selection via AutoGen agents
    bool requestModelSelection(const std::string& audioCharacteristics, std::string& modelPath);

    // Parameter optimization via AutoGen
    bool optimizeParameters(const std::vector<float>& audioData, float& mix, float& gain);

private:
    bool pythonInitialized;
    void* pythonModule;
    void* agentInstance;

    // Helper methods
    bool initializePython();
    void cleanupPython();
    std::vector<float> extractAudioFeatures(const std::vector<float>& audio);
};

} // namespace NeuralVST
