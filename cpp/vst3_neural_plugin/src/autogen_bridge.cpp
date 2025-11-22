#include "../include/neural_vst_plugin.h"
#include <Python.h>
#include <iostream>
#include <sstream>

namespace NeuralVST {

//------------------------------------------------------------------------
// AutoGenBridge Implementation
//------------------------------------------------------------------------
AutoGenBridge::AutoGenBridge()
    : pythonInitialized(false)
    , pythonModule(nullptr)
    , agentInstance(nullptr)
{
}

//------------------------------------------------------------------------
AutoGenBridge::~AutoGenBridge()
{
    cleanup();
}

//------------------------------------------------------------------------
bool AutoGenBridge::initialize()
{
    if (pythonInitialized)
        return true;

    if (!initializePython())
        return false;

    // Import the AutoGen VST bridge module
    PyObject* moduleName = PyUnicode_DecodeFSDefault("autogen_vst_bridge");
    pythonModule = PyImport_Import(moduleName);
    Py_DECREF(moduleName);

    if (!pythonModule) {
        PyErr_Print();
        std::cerr << "Failed to load autogen_vst_bridge module" << std::endl;
        cleanupPython();
        return false;
    }

    // Get the NeuralAgentController class
    PyObject* agentClass = PyObject_GetAttrString(
        static_cast<PyObject*>(pythonModule), "NeuralAgentController");

    if (!agentClass || !PyCallable_Check(agentClass)) {
        std::cerr << "Cannot find NeuralAgentController class" << std::endl;
        Py_XDECREF(agentClass);
        cleanupPython();
        return false;
    }

    // Create an instance of the agent controller
    agentInstance = PyObject_CallObject(agentClass, nullptr);
    Py_DECREF(agentClass);

    if (!agentInstance) {
        PyErr_Print();
        std::cerr << "Failed to create NeuralAgentController instance" << std::endl;
        cleanupPython();
        return false;
    }

    pythonInitialized = true;
    return true;
}

//------------------------------------------------------------------------
void AutoGenBridge::cleanup()
{
    if (agentInstance) {
        Py_DECREF(static_cast<PyObject*>(agentInstance));
        agentInstance = nullptr;
    }

    if (pythonModule) {
        Py_DECREF(static_cast<PyObject*>(pythonModule));
        pythonModule = nullptr;
    }

    cleanupPython();
}

//------------------------------------------------------------------------
bool AutoGenBridge::initializePython()
{
    if (pythonInitialized)
        return true;

    // Initialize Python interpreter
    Py_Initialize();

    if (!Py_IsInitialized()) {
        std::cerr << "Failed to initialize Python interpreter" << std::endl;
        return false;
    }

    // Add the python directory to the Python path
    PyRun_SimpleString(
        "import sys\n"
        "sys.path.append('.')\n"
        "sys.path.append('./python')\n"
    );

    return true;
}

//------------------------------------------------------------------------
void AutoGenBridge::cleanupPython()
{
    if (Py_IsInitialized()) {
        Py_Finalize();
    }
    pythonInitialized = false;
}

//------------------------------------------------------------------------
bool AutoGenBridge::sendAudioFeatures(const std::vector<float>& features)
{
    if (!pythonInitialized || !agentInstance)
        return false;

    // Create a Python list from the features
    PyObject* pyFeatures = PyList_New(features.size());
    for (size_t i = 0; i < features.size(); ++i) {
        PyList_SetItem(pyFeatures, i, PyFloat_FromDouble(features[i]));
    }

    // Call the send_audio_features method
    PyObject* result = PyObject_CallMethod(
        static_cast<PyObject*>(agentInstance),
        "send_audio_features",
        "O",
        pyFeatures);

    Py_DECREF(pyFeatures);

    if (!result) {
        PyErr_Print();
        return false;
    }

    bool success = PyObject_IsTrue(result);
    Py_DECREF(result);
    return success;
}

//------------------------------------------------------------------------
bool AutoGenBridge::getProcessingDecision(std::string& decision)
{
    if (!pythonInitialized || !agentInstance)
        return false;

    // Call the get_processing_decision method
    PyObject* result = PyObject_CallMethod(
        static_cast<PyObject*>(agentInstance),
        "get_processing_decision",
        nullptr);

    if (!result) {
        PyErr_Print();
        return false;
    }

    if (PyUnicode_Check(result)) {
        const char* str = PyUnicode_AsUTF8(result);
        if (str) {
            decision = str;
            Py_DECREF(result);
            return true;
        }
    }

    Py_DECREF(result);
    return false;
}

//------------------------------------------------------------------------
bool AutoGenBridge::requestModelSelection(const std::string& audioCharacteristics,
                                          std::string& modelPath)
{
    if (!pythonInitialized || !agentInstance)
        return false;

    // Call the request_model_selection method
    PyObject* result = PyObject_CallMethod(
        static_cast<PyObject*>(agentInstance),
        "request_model_selection",
        "s",
        audioCharacteristics.c_str());

    if (!result) {
        PyErr_Print();
        return false;
    }

    if (PyUnicode_Check(result)) {
        const char* str = PyUnicode_AsUTF8(result);
        if (str) {
            modelPath = str;
            Py_DECREF(result);
            return true;
        }
    }

    Py_DECREF(result);
    return false;
}

//------------------------------------------------------------------------
bool AutoGenBridge::optimizeParameters(const std::vector<float>& audioData,
                                       float& mix, float& gain)
{
    if (!pythonInitialized || !agentInstance)
        return false;

    // Extract features from audio data
    std::vector<float> features = extractAudioFeatures(audioData);

    // Create Python list for features
    PyObject* pyFeatures = PyList_New(features.size());
    for (size_t i = 0; i < features.size(); ++i) {
        PyList_SetItem(pyFeatures, i, PyFloat_FromDouble(features[i]));
    }

    // Call the optimize_parameters method
    PyObject* result = PyObject_CallMethod(
        static_cast<PyObject*>(agentInstance),
        "optimize_parameters",
        "O",
        pyFeatures);

    Py_DECREF(pyFeatures);

    if (!result) {
        PyErr_Print();
        return false;
    }

    // Parse the result tuple (mix, gain)
    if (PyTuple_Check(result) && PyTuple_Size(result) == 2) {
        PyObject* pyMix = PyTuple_GetItem(result, 0);
        PyObject* pyGain = PyTuple_GetItem(result, 1);

        if (PyFloat_Check(pyMix) && PyFloat_Check(pyGain)) {
            mix = static_cast<float>(PyFloat_AsDouble(pyMix));
            gain = static_cast<float>(PyFloat_AsDouble(pyGain));
            Py_DECREF(result);
            return true;
        }
    }

    Py_DECREF(result);
    return false;
}

//------------------------------------------------------------------------
std::vector<float> AutoGenBridge::extractAudioFeatures(const std::vector<float>& audio)
{
    std::vector<float> features;

    if (audio.empty())
        return features;

    // Calculate basic audio features
    // In production, use more sophisticated feature extraction (spectral, temporal, etc.)

    // RMS Energy
    float rms = 0.0f;
    for (float sample : audio) {
        rms += sample * sample;
    }
    rms = std::sqrt(rms / audio.size());
    features.push_back(rms);

    // Peak amplitude
    float peak = 0.0f;
    for (float sample : audio) {
        peak = std::max(peak, std::abs(sample));
    }
    features.push_back(peak);

    // Zero crossing rate
    int zeroCrossings = 0;
    for (size_t i = 1; i < audio.size(); ++i) {
        if ((audio[i - 1] >= 0 && audio[i] < 0) ||
            (audio[i - 1] < 0 && audio[i] >= 0)) {
            zeroCrossings++;
        }
    }
    float zcr = static_cast<float>(zeroCrossings) / audio.size();
    features.push_back(zcr);

    // Spectral centroid (simplified)
    float centroid = 0.0f;
    float sumMagnitude = 0.0f;
    for (size_t i = 0; i < audio.size(); ++i) {
        float magnitude = std::abs(audio[i]);
        centroid += i * magnitude;
        sumMagnitude += magnitude;
    }
    if (sumMagnitude > 0) {
        centroid /= sumMagnitude;
    }
    features.push_back(centroid / audio.size());

    return features;
}

} // namespace NeuralVST
