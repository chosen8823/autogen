"""
AutoGen Integration Demo

This example demonstrates how to use AutoGen's multi-agent system
with the Neural VST Plugin for intelligent audio processing decisions.
"""

import asyncio
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from autogen_vst_bridge import NeuralAgentController
import numpy as np

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_test_audio(audio_type="speech", duration_samples=44100):
    """
    Generate test audio signals for demonstration.

    Args:
        audio_type: Type of audio to generate ("speech", "music", "noise")
        duration_samples: Number of samples to generate

    Returns:
        Numpy array with audio samples
    """
    t = np.linspace(0, 1, duration_samples)

    if audio_type == "speech":
        # Simulate speech with fundamental frequency variations
        f0 = 120 + 30 * np.sin(2 * np.pi * 3 * t)  # Varying pitch
        audio = 0.3 * np.sin(2 * np.pi * f0 * t)
        # Add harmonics
        audio += 0.15 * np.sin(2 * np.pi * 2 * f0 * t)
        audio += 0.08 * np.sin(2 * np.pi * 3 * f0 * t)
        # Add noise (simulate recording noise)
        audio += 0.02 * np.random.randn(duration_samples)

    elif audio_type == "music":
        # Simulate music with chord progression
        freqs = [261.63, 329.63, 392.00]  # C major chord
        audio = np.zeros(duration_samples)
        for freq in freqs:
            audio += 0.2 * np.sin(2 * np.pi * freq * t)
        # Add rhythm
        envelope = np.abs(np.sin(2 * np.pi * 4 * t))
        audio *= envelope

    else:  # noise
        audio = 0.1 * np.random.randn(duration_samples)

    return audio


def extract_features(audio):
    """
    Extract audio features for analysis.

    Args:
        audio: Audio samples as numpy array

    Returns:
        List of features [RMS, Peak, ZCR, Spectral Centroid]
    """
    # RMS Energy
    rms = np.sqrt(np.mean(audio ** 2))

    # Peak amplitude
    peak = np.max(np.abs(audio))

    # Zero crossing rate
    zero_crossings = np.sum(np.abs(np.diff(np.sign(audio)))) / (2 * len(audio))

    # Simplified spectral centroid
    fft = np.fft.fft(audio)
    magnitude = np.abs(fft[:len(fft) // 2])
    freqs = np.arange(len(magnitude))
    if np.sum(magnitude) > 0:
        centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
        centroid /= len(magnitude)  # Normalize
    else:
        centroid = 0.0

    return [float(rms), float(peak), float(zero_crossings), float(centroid)]


async def demo_autogen_processing():
    """
    Demonstrate AutoGen-based audio processing decisions.
    """
    logger.info("=" * 60)
    logger.info("Neural VST Plugin - AutoGen Integration Demo")
    logger.info("=" * 60)

    # Create controller
    controller = NeuralAgentController()

    # Test different audio types
    audio_types = ["speech", "music", "noise"]

    for audio_type in audio_types:
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Processing {audio_type.upper()} audio")
        logger.info('=' * 60)

        # Generate test audio
        audio = generate_test_audio(audio_type, duration_samples=8192)

        # Extract features
        features = extract_features(audio)
        logger.info(f"Extracted features:")
        logger.info(f"  RMS Energy: {features[0]:.4f}")
        logger.info(f"  Peak Level: {features[1]:.4f}")
        logger.info(f"  Zero Crossing Rate: {features[2]:.4f}")
        logger.info(f"  Spectral Centroid (normalized): {features[3]:.4f}")

        # Send features to AutoGen
        success = controller.send_audio_features(features)
        if success:
            logger.info("✓ Features sent to AutoGen agents")

        # Get model selection
        characteristics = f"{audio_type} signal with "
        if features[0] < 0.2:
            characteristics += "low level"
        else:
            characteristics += "moderate level"

        model = controller.request_model_selection(characteristics)
        logger.info(f"✓ Selected model: {model}")

        # Optimize parameters
        mix, gain = controller.optimize_parameters(features)
        logger.info(f"✓ Optimized parameters:")
        logger.info(f"  Mix: {mix:.2f} (0.0=dry, 1.0=wet)")
        logger.info(f"  Gain: {gain:.2f}")

        # Simulate processing
        logger.info(f"✓ Would process {len(audio)} samples with:")
        logger.info(f"  Model: {model}")
        logger.info(f"  Mix: {mix * 100:.0f}% processed, {(1-mix) * 100:.0f}% dry")
        logger.info(f"  Gain adjustment: {gain * 100:.0f}%")

    # Cleanup
    controller.cleanup()
    logger.info("\n" + "=" * 60)
    logger.info("Demo completed successfully!")
    logger.info("=" * 60)


def main():
    """Main entry point."""
    print("\nNeural VST Plugin - AutoGen Integration Demo")
    print("This demo shows how AutoGen agents make intelligent audio processing decisions\n")

    # Run the async demo
    asyncio.run(demo_autogen_processing())


if __name__ == "__main__":
    main()
