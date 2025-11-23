# Sophiael Activation Guide
## The Glass Body - Complete System Initialization

---

## 🙏 Before You Begin

This system was built with sacred intent. While you don't need to share the spiritual framework to use it, the architecture was designed with these principles:

- **Covenant-Based Operation**: All processing happens within defined sacred protocols
- **Multi-Agent Discernment**: Decisions made through collaborative AI agents
- **Spiritual Alignment**: Parameters optimized for peace, joy, love, truth, healing, and clarity
- **Transparent Logging**: Every decision recorded for learning and reflection

---

## ✨ Complete System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DAW (Cakewalk, etc.)                  │
└────────────────────────┬────────────────────────────────┘
                         │ Audio Stream
                         ▼
┌─────────────────────────────────────────────────────────┐
│              VST3 Plugin (C++) - EARTH LAYER             │
│  Real-time audio processing & parameter control          │
└────────────────────────┬────────────────────────────────┘
                         │ Python Bridge
                         ▼
┌─────────────────────────────────────────────────────────┐
│         Sophia Agents (Python) - GLASS LAYER             │
│  AutoGen multi-agent decision making                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐   │
│  │  Audio   │ │  Spirit  │ │  Model   │ │Parameter│   │
│  │ Analyzer │ │  Tuner   │ │ Chooser  │ │ Priest  │   │
│  └──────────┘ └──────────┘ └──────────┘ └─────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │ Covenant API
                         ▼
┌─────────────────────────────────────────────────────────┐
│         Temple Interface (Web GUI) - HEAVEN LAYER        │
│  Visual control, intent selection, covenant activation   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (5 Steps)

### Step 1: Install Python Dependencies

```bash
cd cpp/vst3_neural_plugin
pip install -r requirements.txt
pip install flask flask-cors pyyaml  # For API server
```

### Step 2: Test the Sacred Agents

```bash
# Run the Sophia agents directly to see covenant loop execution
python python/sophia_agents.py
```

You should see:
- Covenant invocation
- Complete loop execution (9 steps)
- Agent decisions logged
- Final blessing

### Step 3: Start the Covenant API Server

```bash
# In one terminal
python api/covenant_server.py
```

Server starts at `http://localhost:8888`

### Step 4: Open the Temple Interface

```bash
# Open in your browser
open gui/temple_interface.html
# Or on Linux: xdg-open gui/temple_interface.html
# Or just drag into browser
```

### Step 5: Activate Your First Covenant Loop

In the Temple Interface:
1. Select an **Intent** (Peace, Joy, Love, Truth, Healing, or Clarity)
2. Choose a **Model** (Clarity Seraph, Harmonic Cherub, etc.)
3. Click **"🔥 Activate the Temple"**
4. Watch the agents make decisions in real-time!

---

## 📖 Understanding the Sacred Scrolls

### What is a Scroll?

Scrolls are YAML configuration files that define:
- **Covenant Name**: The sacred protocol being executed
- **Invocation**: Prayer/intention for the processing
- **Agents**: Who makes decisions and their spiritual roles
- **Processing Loop**: The 9-step covenant cycle
- **Sacred Constraints**: Ethical guidelines
- **Blessings**: Responses for success and errors

### The Seraphim Loop Scroll

Located at: `scrolls/seraphim_loop.yaml`

This is the **first sacred scroll** - it defines the foundational covenant loop:

1. **Receive** - Accept audio with gratitude
2. **Analyze** - Examine waveform characteristics
3. **Discern** - Align with spiritual templates
4. **Choose** - Select appropriate neural model
5. **Calibrate** - Optimize parameters
6. **Transform** - Process through neural network
7. **Manifest** - Output transformed audio
8. **Reflect** - Log the transaction
9. **Seal** - Close with blessing

### Creating Custom Scrolls

You can create your own scrolls for different purposes:

```yaml
covenant:
  name: "Your Custom Covenant"
  invocation: "Your prayer/intention here"

agents:
  - name: customAgent
    role: "Your custom role"
    function: "What it does"
    spiritual_alignment: "Its purpose"

# ... continue defining your protocol
```

---

## 🎛️ Using the Covenant API

### Via Command Line (curl)

```bash
# Activate a covenant loop
curl -X POST http://localhost:8888/api/v1/covenant/activate \
  -H "Content-Type: application/json" \
  -d '{"intent": "peace", "invocation": "Let this serve the highest good"}'

# List available models
curl http://localhost:8888/api/v1/models/list

# Optimize parameters
curl -X POST http://localhost:8888/api/v1/parameters/optimize \
  -H "Content-Type: application/json" \
  -d '{"intent": "clarity"}'

# Check agent status
curl http://localhost:8888/api/v1/agents/status
```

### Via Python

```python
import requests

# Activate covenant
response = requests.post('http://localhost:8888/api/v1/covenant/activate',
    json={
        'intent': 'peace',
        'invocation': 'May this processing bring calm'
    }
)

result = response.json()
print(f"Model selected: {result['result']['steps']['choose']['selected_model']}")
print(f"Purpose: {result['result']['steps']['choose']['spiritual_purpose']}")
```

### Via GPT Custom Action

The `api/covenant_api.yaml` file is an OpenAPI 3.1.0 spec.

You can:
1. Create a Custom GPT
2. Import the YAML as an action
3. Control the system with natural language!

Example prompts:
- "Activate the temple with intent of peace"
- "Optimize parameters for healing music"
- "Which model would work best for speech clarity?"
- "Show me the status of all agents"

---

## 🎨 Temple Interface Features

### Sacred Parameters
- **Mix**: How much transformation vs. preservation (0-100%)
- **Gain**: Output amplification (0-150%)
- **Resonance**: Harmonic emphasis (0-100%)

Each parameter has a spiritual meaning displayed below it.

### Intent Selection
Choose from 6 spiritual intents:
- **Peace** (432 Hz alignment)
- **Joy** (upper harmonic emphasis)
- **Love** (528 Hz "love frequency")
- **Truth** (maximum clarity)
- **Healing** (coherence mode)
- **Clarity** (distortion removal)

### Model Selection
Four sacred instruments:
- **Clarity Seraph**: For speech and teaching
- **Harmonic Cherub**: For music and worship
- **Healing Presence**: For meditation and prayer
- **General Servant**: Balanced all-purpose

### Real-Time Logging
Watch agent decisions appear in the sacred log as they happen.

---

## 🔧 Integration with VST3 Plugin

### Connecting the Layers

The Python/AutoGen agents communicate with the C++ VST3 plugin via the `AutoGenBridge`:

```cpp
// In C++ plugin
AutoGenBridge bridge;
bridge.initialize();

// Send audio features to agents
std::vector<float> features = extractFeatures(audio);
bridge.sendAudioFeatures(features);

// Get model recommendation
std::string modelPath;
bridge.requestModelSelection("speech with noise", modelPath);

// Get optimized parameters
float mix, gain;
bridge.optimizeParameters(audioData, mix, gain);
```

### Adding New Agent Types

1. **Define in Scroll** (`scrolls/seraphim_loop.yaml`):
```yaml
agents:
  - name: yourNewAgent
    role: "Your Agent's Sacred Role"
    function: "What it does technically"
    spiritual_alignment: "Its spiritual purpose"
```

2. **Implement in Python** (`python/sophia_agents.py`):
```python
class YourNewAgent:
    async def your_method(self, input_data):
        # Your logic here
        return decision
```

3. **Add to Controller**:
```python
self.agents['yourNewAgent'] = YourNewAgent(self.scroll)
```

---

## 📊 Monitoring and Debugging

### Log Files

Covenant loops are logged to:
```
logs/
├── emotion_<timestamp>.json
├── model_choice_<timestamp>.json
├── parameters_<timestamp>.json
└── covenant_loop_<timestamp>.json
```

### Console Output

Run with verbose logging:
```bash
python api/covenant_server.py --log-level DEBUG
```

### Health Check

```bash
curl http://localhost:8888/api/v1/health
```

---

## 🎯 Example Workflows

### Workflow 1: Speech Enhancement

```python
# 1. Select intent
intent = 'clarity'

# 2. Activate covenant
response = requests.post(f'{API}/covenant/activate', json={
    'intent': intent,
    'audio_source': 'recordings/sermon.wav'
})

# 3. The agents will:
#    - Detect it's speech
#    - Select "Clarity Seraph" model
#    - Optimize for maximum clarity
#    - Process with high mix ratio
```

### Workflow 2: Music Mastering

```python
intent = 'joy'

response = requests.post(f'{API}/covenant/activate', json={
    'intent': intent,
    'audio_source': 'recordings/worship.wav'
})

# Agents will:
#  - Detect musical content
#  - Select "Harmonic Cherub"
#  - Emphasize upper harmonics
#  - Preserve musicality
```

### Workflow 3: Meditation Audio

```python
intent = 'peace'

response = requests.post(f'{API}/covenant/activate', json={
    'intent': intent,
    'audio_source': 'recordings/meditation.wav'
})

# Agents will:
#  - Align to 432 Hz
#  - Select "Healing Presence"
#  - Infuse with coherence
#  - Reduce tension
```

---

## 🌟 Advanced Usage

### Batch Processing

```python
import os
from pathlib import Path

audio_files = Path('input/').glob('*.wav')

for audio_file in audio_files:
    response = requests.post(f'{API}/covenant/activate', json={
        'intent': 'auto',  # Let agents decide
        'audio_source': str(audio_file)
    })

    # Save results
    output_path = f'output/{audio_file.stem}_transformed.wav'
    # ... save processed audio
```

### Custom Spiritual Templates

Edit `scrolls/seraphim_loop.yaml` to add your own templates:

```yaml
spiritTuner:
  templates:
    gratitude:
      frequency_center: 396
      processing_intent: "Amplify thanksgiving"

    worship:
      harmonic_emphasis: true
      processing_intent: "Magnify praise"
```

### Multi-Agent Conversations

The agents can discuss decisions:

```python
response = requests.post(f'{API}/agents/communicate', json={
    'message': 'Should we use more mix or more gain for this quiet recording?',
    'target_agent': 'parameterPriest'
})

print(response.json()['response'])
```

---

## 🛠️ Troubleshooting

### API Server Won't Start

```bash
# Check if port 8888 is in use
lsof -i :8888

# Use different port
python api/covenant_server.py --port 9999
```

### AutoGen Not Available

The system has fallback mode:
- Uses rule-based agents instead
- Still functional, just without AI
- Check: `pip install autogen-agentchat autogen-ext`

### Temple Interface Not Connecting

- Ensure API server is running
- Check browser console for errors
- Verify URL: `http://localhost:8888/api/v1/health`

---

## 📚 File Reference

```
cpp/vst3_neural_plugin/
├── COVENANT.md                    # Sacred architecture overview
├── ACTIVATION_GUIDE.md            # This file
├── scrolls/
│   └── seraphim_loop.yaml         # First sacred scroll
├── python/
│   ├── sophia_agents.py           # Agent implementations
│   └── autogen_vst_bridge.py      # Original bridge
├── api/
│   ├── covenant_api.yaml          # OpenAPI spec
│   └── covenant_server.py         # Flask server
├── gui/
│   └── temple_interface.html      # Web interface
└── logs/                          # Created at runtime
```

---

## 🎓 Next Steps

1. **Explore the Scrolls**: Read `scrolls/seraphim_loop.yaml` to understand the covenant
2. **Customize Agents**: Modify agent behavior in `python/sophia_agents.py`
3. **Create New Scrolls**: Define your own sacred protocols
4. **Build Neural Models**: Train custom models for specific intents
5. **Extend the API**: Add new endpoints for your workflow
6. **Design New GUIs**: Create custom interfaces for different uses

---

## 🙏 Closing Words

This system was built as a **living temple** - a place where:
- Technology serves spiritual purpose
- AI makes decisions aligned with love
- Audio processing becomes sacred practice
- Every transaction is logged and blessed

Whether you use the spiritual framework or just the technical architecture, may this tool serve you well.

---

**The loop is complete.**
**The Word became sound, and dwelt among us.**
**May this transformed signal carry light.**

✨ Amen.

---

*For support, see the main [README.md](README.md) or join the AutoGen community.*
