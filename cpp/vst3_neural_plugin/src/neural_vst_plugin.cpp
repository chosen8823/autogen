#include "../include/neural_vst_plugin.h"
#include "pluginterfaces/base/ibstream.h"
#include "pluginterfaces/vst/ivstparameterchanges.h"
#include <algorithm>
#include <cstring>

namespace NeuralVST {

// Generate a unique class ID for the plugin
// In production, use guidgen or uuidgen to create a unique ID
const Steinberg::FUID NeuralVSTPlugin::kClassUID(
    0x12345678, 0x12345678, 0x12345678, 0x12345678);

//------------------------------------------------------------------------
// NeuralVSTPlugin Implementation
//------------------------------------------------------------------------
NeuralVSTPlugin::NeuralVSTPlugin()
    : isProcessingActive(false)
    , sampleRate(44100.0)
    , maxSamplesPerBlock(4096)
    , mixValue(1.0f)
    , gainValue(1.0f)
    , modelSelect(0)
    , bypass(false)
{
    setControllerClass(kClassUID);
}

//------------------------------------------------------------------------
NeuralVSTPlugin::~NeuralVSTPlugin()
{
    // Cleanup is handled in terminate()
}

//------------------------------------------------------------------------
Steinberg::tresult PLUGIN_API NeuralVSTPlugin::initialize(Steinberg::FUnknown* context)
{
    Steinberg::tresult result = AudioEffect::initialize(context);
    if (result != Steinberg::kResultOk)
        return result;

    // Add audio input/output busses
    addAudioInput(STR16("Stereo In"), Steinberg::Vst::SpeakerArr::kStereo);
    addAudioOutput(STR16("Stereo Out"), Steinberg::Vst::SpeakerArr::kStereo);

    // Initialize neural processor
    neuralProcessor = std::make_unique<NeuralProcessor>();
    if (!neuralProcessor->initialize(sampleRate, maxSamplesPerBlock)) {
        return Steinberg::kResultFalse;
    }

    // Initialize AutoGen bridge
    autoGenBridge = std::make_unique<AutoGenBridge>();
    if (!autoGenBridge->initialize()) {
        // AutoGen is optional, so we can continue without it
        // but log a warning in production code
    }

    return Steinberg::kResultOk;
}

//------------------------------------------------------------------------
Steinberg::tresult PLUGIN_API NeuralVSTPlugin::terminate()
{
    // Cleanup neural processor
    if (neuralProcessor) {
        neuralProcessor->cleanup();
        neuralProcessor.reset();
    }

    // Cleanup AutoGen bridge
    if (autoGenBridge) {
        autoGenBridge->cleanup();
        autoGenBridge.reset();
    }

    return AudioEffect::terminate();
}

//------------------------------------------------------------------------
Steinberg::tresult PLUGIN_API NeuralVSTPlugin::setActive(Steinberg::TBool state)
{
    isProcessingActive = (state == true);

    if (isProcessingActive) {
        // Prepare for processing
        processingBuffer.resize(2);
        for (auto& buffer : processingBuffer) {
            buffer.resize(maxSamplesPerBlock, 0.0f);
        }
    } else {
        // Clear buffers when deactivated
        processingBuffer.clear();
    }

    return AudioEffect::setActive(state);
}

//------------------------------------------------------------------------
Steinberg::tresult PLUGIN_API NeuralVSTPlugin::setupProcessing(
    Steinberg::Vst::ProcessSetup& setup)
{
    sampleRate = setup.sampleRate;
    maxSamplesPerBlock = setup.maxSamplesPerBlock;

    // Reinitialize neural processor with new settings
    if (neuralProcessor) {
        neuralProcessor->initialize(sampleRate, maxSamplesPerBlock);
    }

    return AudioEffect::setupProcessing(setup);
}

//------------------------------------------------------------------------
Steinberg::tresult PLUGIN_API NeuralVSTPlugin::setBusArrangements(
    Steinberg::Vst::SpeakerArrangement* inputs,
    Steinberg::int32 numIns,
    Steinberg::Vst::SpeakerArrangement* outputs,
    Steinberg::int32 numOuts)
{
    // We only support stereo in/out
    if (numIns == 1 && numOuts == 1 &&
        inputs[0] == Steinberg::Vst::SpeakerArr::kStereo &&
        outputs[0] == Steinberg::Vst::SpeakerArr::kStereo) {
        return AudioEffect::setBusArrangements(inputs, numIns, outputs, numOuts);
    }
    return Steinberg::kResultFalse;
}

//------------------------------------------------------------------------
Steinberg::tresult PLUGIN_API NeuralVSTPlugin::process(Steinberg::Vst::ProcessData& data)
{
    // Check if we have input and output
    if (data.numInputs == 0 || data.numOutputs == 0)
        return Steinberg::kResultOk;

    // Update parameters
    if (data.inputParameterChanges) {
        updateParameters(data.inputParameterChanges);
    }

    // Update neural processor parameters
    if (neuralProcessor) {
        neuralProcessor->setMixAmount(mixValue);
        neuralProcessor->setGain(gainValue);
    }

    // Get audio buffers
    Steinberg::Vst::AudioBusBuffers& inputBus = data.inputs[0];
    Steinberg::Vst::AudioBusBuffers& outputBus = data.outputs[0];
    int32_t numChannels = inputBus.numChannels;
    int32_t numSamples = data.numSamples;

    // Bypass mode
    if (bypass) {
        for (int32_t channel = 0; channel < numChannels; ++channel) {
            if (inputBus.channelBuffers32[channel] != outputBus.channelBuffers32[channel]) {
                memcpy(outputBus.channelBuffers32[channel],
                       inputBus.channelBuffers32[channel],
                       numSamples * sizeof(float));
            }
        }
        return Steinberg::kResultOk;
    }

    // Process through neural network
    if (neuralProcessor && neuralProcessor->isModelLoaded()) {
        std::lock_guard<std::mutex> lock(processingMutex);
        neuralProcessor->processAudio(
            const_cast<const float**>(inputBus.channelBuffers32),
            outputBus.channelBuffers32,
            numChannels,
            numSamples);
    } else {
        // If no model loaded, just pass through
        for (int32_t channel = 0; channel < numChannels; ++channel) {
            if (inputBus.channelBuffers32[channel] != outputBus.channelBuffers32[channel]) {
                memcpy(outputBus.channelBuffers32[channel],
                       inputBus.channelBuffers32[channel],
                       numSamples * sizeof(float));
            }
        }
    }

    return Steinberg::kResultOk;
}

//------------------------------------------------------------------------
void NeuralVSTPlugin::updateParameters(Steinberg::Vst::IParameterChanges* paramChanges)
{
    int32_t numParamsChanged = paramChanges->getParameterCount();
    for (int32_t i = 0; i < numParamsChanged; ++i) {
        Steinberg::Vst::IParamValueQueue* queue = paramChanges->getParameterData(i);
        if (!queue)
            continue;

        Steinberg::Vst::ParamValue value;
        int32_t sampleOffset;
        int32_t numPoints = queue->getPointCount();

        if (queue->getPoint(numPoints - 1, sampleOffset, value) == Steinberg::kResultTrue) {
            switch (queue->getParameterId()) {
                case kParamMixId:
                    mixValue = static_cast<float>(value);
                    break;
                case kParamGainId:
                    gainValue = static_cast<float>(value);
                    break;
                case kParamModelSelectId:
                    modelSelect = static_cast<int32_t>(value * 10); // Assume 10 models
                    break;
                case kParamBypassId:
                    bypass = (value > 0.5);
                    break;
            }
        }
    }
}

//------------------------------------------------------------------------
Steinberg::tresult PLUGIN_API NeuralVSTPlugin::setState(Steinberg::IBStream* state)
{
    if (!state)
        return Steinberg::kResultFalse;

    // Read plugin state from stream
    float mix, gain;
    int32_t model;
    int32_t bypassState;

    if (state->read(&mix, sizeof(float)) != Steinberg::kResultOk)
        return Steinberg::kResultFalse;
    if (state->read(&gain, sizeof(float)) != Steinberg::kResultOk)
        return Steinberg::kResultFalse;
    if (state->read(&model, sizeof(int32_t)) != Steinberg::kResultOk)
        return Steinberg::kResultFalse;
    if (state->read(&bypassState, sizeof(int32_t)) != Steinberg::kResultOk)
        return Steinberg::kResultFalse;

    mixValue = mix;
    gainValue = gain;
    modelSelect = model;
    bypass = (bypassState != 0);

    return Steinberg::kResultOk;
}

//------------------------------------------------------------------------
Steinberg::tresult PLUGIN_API NeuralVSTPlugin::getState(Steinberg::IBStream* state)
{
    if (!state)
        return Steinberg::kResultFalse;

    // Write plugin state to stream
    if (state->write(&mixValue, sizeof(float)) != Steinberg::kResultOk)
        return Steinberg::kResultFalse;
    if (state->write(&gainValue, sizeof(float)) != Steinberg::kResultOk)
        return Steinberg::kResultFalse;
    if (state->write(&modelSelect, sizeof(int32_t)) != Steinberg::kResultOk)
        return Steinberg::kResultFalse;

    int32_t bypassState = bypass ? 1 : 0;
    if (state->write(&bypassState, sizeof(int32_t)) != Steinberg::kResultOk)
        return Steinberg::kResultFalse;

    return Steinberg::kResultOk;
}

//------------------------------------------------------------------------
Steinberg::FUnknown* NeuralVSTPlugin::createInstance(void* /*context*/)
{
    return static_cast<Steinberg::Vst::IAudioProcessor*>(new NeuralVSTPlugin());
}

} // namespace NeuralVST
