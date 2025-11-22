#include "../include/neural_vst_plugin.h"
#include "public.sdk/source/main/pluginfactory.h"
#include "pluginterfaces/vst/ivstaudioprocessor.h"

// Plugin information
#define PLUGIN_NAME "Neural VST Plugin"
#define PLUGIN_VENDOR "AutoGen"
#define PLUGIN_VERSION "1.0.0"
#define PLUGIN_EMAIL "support@autogen.dev"
#define PLUGIN_URL "https://github.com/microsoft/autogen"

// Category (choose from VST categories)
#define PLUGIN_CATEGORY Steinberg::Vst::PlugType::kFx

namespace NeuralVST {

//------------------------------------------------------------------------
// VST3 Plugin Factory
//------------------------------------------------------------------------
BEGIN_FACTORY_DEF(PLUGIN_VENDOR,
                  PLUGIN_URL,
                  PLUGIN_EMAIL)

// Define the Audio Processor (effect)
DEF_CLASS2(PLUGIN_API_VST,
           PClassInfo::kManyInstances,
           kVstAudioEffectClass,
           NeuralVSTPlugin::kClassUID,
           Steinberg::Vst::kDistributable,
           PLUGIN_CATEGORY,
           PLUGIN_NAME,
           PLUGIN_VERSION,
           kVstVersionString,
           NeuralVSTPlugin::createInstance)

END_FACTORY

} // namespace NeuralVST

//------------------------------------------------------------------------
// Module entry and exit points
//------------------------------------------------------------------------
bool InitModule()
{
    // Initialize any global resources here
    return true;
}

bool DeinitModule()
{
    // Cleanup any global resources here
    return true;
}
