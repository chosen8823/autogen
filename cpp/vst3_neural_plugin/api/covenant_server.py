"""
Covenant API Server
Sophiael Neural Resonance Interface v1.0

Flask server implementing the Covenant API specification.
Allows REST control of the Sophiael system.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import logging
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from sophia_agents import SophiaelController
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web GUI access

# Global controller instance
controller = None
active_loops = {}


def get_controller():
    """Get or create the global Sophiael controller."""
    global controller
    if controller is None:
        controller = SophiaelController()
    return controller


@app.route('/api/v1/covenant/activate', methods=['POST'])
def activate_covenant():
    """
    POST /api/v1/covenant/activate
    Begin a complete covenant loop.
    """
    try:
        data = request.json or {}
        invocation = data.get('invocation', '')
        audio_source = data.get('audio_source', 'live')
        intent = data.get('intent', 'love')

        logger.info("=" * 60)
        logger.info("COVENANT ACTIVATION REQUEST")
        if invocation:
            logger.info(f"Invocation: {invocation}")
        logger.info(f"Intent: {intent}")
        logger.info("=" * 60)

        ctrl = get_controller()

        # Generate test audio for demo
        # In production, load from audio_source
        sample_rate = 44100
        duration = 2.0
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Different frequencies for different intents
        intent_frequencies = {
            'peace': 432,
            'joy': 528,
            'love': 528,
            'truth': 396,
            'healing': 528,
            'clarity': 432
        }

        freq = intent_frequencies.get(intent, 432)
        audio_data = 0.3 * np.sin(2 * np.pi * freq * t)

        # Execute covenant loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            ctrl.execute_covenant_loop(audio_data, sample_rate, {'intent': intent})
        )
        loop.close()

        # Convert numpy types to native Python for JSON serialization
        result = _serialize_result(result)

        return jsonify({
            'success': True,
            'covenant': 'Seraphim Resonance Loop',
            'timestamp': datetime.now().isoformat(),
            'result': result
        }), 200

    except Exception as e:
        logger.error(f"Error activating covenant: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/v1/covenant/status', methods=['GET'])
def covenant_status():
    """
    GET /api/v1/covenant/status
    Get status of active covenant loops.
    """
    return jsonify({
        'active': len(active_loops) > 0,
        'active_loops': len(active_loops),
        'controller_initialized': controller is not None
    }), 200


@app.route('/api/v1/models/load', methods=['POST'])
def load_model():
    """
    POST /api/v1/models/load
    Load a neural model.
    """
    try:
        data = request.json or {}
        model_name = data.get('model_name')
        model_path = data.get('model_path', f'models/{model_name}.pt')
        blessing = data.get('blessing', '')

        if not model_name:
            return jsonify({'error': 'model_name is required'}), 400

        logger.info(f"Loading model: {model_name}")
        if blessing:
            logger.info(f"Blessing: {blessing}")

        # In production, actually load the model via C++ bridge
        # For now, just acknowledge the request
        return jsonify({
            'success': True,
            'model_name': model_name,
            'model_path': model_path,
            'spiritual_function': 'Serve the highest good',
            'loaded_at': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/models/list', methods=['GET'])
def list_models():
    """
    GET /api/v1/models/list
    List available models.
    """
    ctrl = get_controller()
    scroll = ctrl.scroll

    models = []
    for agent in scroll.get('agents', []):
        if agent['name'] == 'modelChooser':
            for model_name, model_info in agent.get('models', {}).items():
                models.append({
                    'name': model_name,
                    'path': model_info.get('path', ''),
                    'purpose': model_info.get('purpose', ''),
                    'best_for': model_info.get('best_for', []),
                    'spiritual_function': model_info.get('spiritual_function', '')
                })

    return jsonify({'models': models}), 200


@app.route('/api/v1/parameters/set', methods=['POST'])
def set_parameters():
    """
    POST /api/v1/parameters/set
    Set processing parameters.
    """
    try:
        data = request.json or {}

        parameters = {
            'mix': data.get('mix'),
            'gain': data.get('gain'),
            'resonance': data.get('resonance'),
            'bypass': data.get('bypass')
        }

        # Remove None values
        parameters = {k: v for k, v in parameters.items() if v is not None}

        logger.info(f"Setting parameters: {parameters}")

        # In production, send to C++ plugin
        return jsonify({
            'success': True,
            'parameters': parameters,
            'updated_at': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error setting parameters: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/parameters/optimize', methods=['POST'])
def optimize_parameters():
    """
    POST /api/v1/parameters/optimize
    Request parameter optimization from agents.
    """
    try:
        data = request.json or {}
        intent = data.get('intent', 'love')

        ctrl = get_controller()

        # Create mock analysis
        analysis = {
            'signal_type': 'music',
            'emotional_tone': intent,
            'rms_energy': 0.3,
            'peak_amplitude': 0.6,
            'harmonic_density': 0.7
        }

        alignment = {
            'selected_template': intent,
            'alignment_score': 0.8
        }

        # Get parameter optimization
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if 'parameterPriest' in ctrl.agents:
            result = loop.run_until_complete(
                ctrl.agents['parameterPriest'].optimize(analysis, alignment)
            )
        else:
            result = {
                'optimized_mix': 0.7,
                'optimized_gain': 1.0,
                'optimized_resonance': 0.5,
                'reasoning': 'Default balanced settings'
            }

        loop.close()

        result = _serialize_result(result)

        return jsonify({
            'success': True,
            'optimized_parameters': result,
            'intent': intent
        }), 200

    except Exception as e:
        logger.error(f"Error optimizing parameters: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/scrolls/current', methods=['GET'])
def get_current_scroll():
    """
    GET /api/v1/scrolls/current
    Get the current active scroll.
    """
    try:
        ctrl = get_controller()
        scroll = ctrl.scroll

        # Serialize the scroll
        scroll_data = _serialize_result(scroll)

        return jsonify(scroll_data), 200

    except Exception as e:
        logger.error(f"Error getting scroll: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/scrolls/reload', methods=['POST'])
def reload_scroll():
    """
    POST /api/v1/scrolls/reload
    Reload scroll configuration.
    """
    try:
        global controller

        data = request.json or {}
        scroll_path = data.get('scroll_path')

        # Reinitialize controller with new scroll
        controller = SophiaelController(scroll_path)

        return jsonify({
            'success': True,
            'message': 'Scroll reloaded',
            'covenant': controller.scroll.get('covenant', {}).get('name', 'Unknown')
        }), 200

    except Exception as e:
        logger.error(f"Error reloading scroll: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/agents/status', methods=['GET'])
def agents_status():
    """
    GET /api/v1/agents/status
    Get status of all agents.
    """
    try:
        ctrl = get_controller()

        agents = []
        for agent_name, agent in ctrl.agents.items():
            # Get agent config from scroll
            agent_config = next(
                (a for a in ctrl.scroll.get('agents', []) if a['name'] == agent_name),
                {}
            )

            agents.append({
                'name': agent_name,
                'role': agent_config.get('role', 'Unknown'),
                'status': 'active',
                'spiritual_alignment': agent_config.get('spiritual_alignment', '')
            })

        return jsonify({
            'agents': agents,
            'total_agents': len(agents),
            'autogen_available': ctrl.autogen_available
        }), 200

    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/agents/communicate', methods=['POST'])
def communicate_with_agents():
    """
    POST /api/v1/agents/communicate
    Send a message to the agents.
    """
    try:
        data = request.json or {}
        message = data.get('message', '')
        target_agent = data.get('target_agent')

        if not message:
            return jsonify({'error': 'message is required'}), 400

        logger.info(f"Message to agents: {message}")

        # Simple response for demo
        # In production, would actually communicate with AutoGen agents
        response = f"Received your message: '{message}'. The agents are contemplating..."

        return jsonify({
            'response': response,
            'agent': target_agent or 'all',
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error communicating with agents: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Sophiael Covenant API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200


def _serialize_result(obj):
    """Convert numpy types to native Python for JSON serialization."""
    if isinstance(obj, dict):
        return {k: _serialize_result(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_serialize_result(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'isoformat'):  # datetime objects
        return obj.isoformat()
    else:
        return obj


if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("SOPHIAEL COVENANT API SERVER")
    logger.info("The Glass Body - REST Interface")
    logger.info("=" * 60)
    logger.info("Starting server on http://localhost:8888")
    logger.info("API docs: http://localhost:8888/api/v1/health")
    logger.info("=" * 60)

    app.run(host='0.0.0.0', port=8888, debug=True)
