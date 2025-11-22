"""
Simple Neural Audio Processing Model Example

This example demonstrates how to create and export a simple neural network
model for audio processing that can be used with the Neural VST Plugin.

The model performs basic audio enhancement using a simple neural network.
"""

import torch
import torch.nn as nn
import numpy as np


class SimpleAudioProcessor(nn.Module):
    """
    A simple neural network for audio processing.

    This model uses 1D convolutions to process audio signals.
    It's designed to be lightweight enough for real-time processing.
    """

    def __init__(self, channels=2, kernel_size=7):
        super(SimpleAudioProcessor, self).__init__()

        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv1d(channels, 16, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Conv1d(16, 32, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Conv1d(32, 64, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
        )

        # Decoder
        self.decoder = nn.Sequential(
            nn.Conv1d(64, 32, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Conv1d(32, 16, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Conv1d(16, channels, kernel_size=kernel_size, padding=kernel_size // 2),
            nn.Tanh(),  # Output in [-1, 1] range
        )

    def forward(self, x):
        """
        Forward pass.

        Args:
            x: Input tensor of shape (batch, channels, samples)

        Returns:
            Processed audio tensor of same shape
        """
        # Encode
        encoded = self.encoder(x)

        # Decode
        output = self.decoder(encoded)

        return output


def create_and_export_model(output_path="neural_model.pt", sample_rate=44100):
    """
    Create and export a TorchScript model for the VST plugin.

    Args:
        output_path: Path to save the exported model
        sample_rate: Audio sample rate (for reference)
    """
    print("Creating neural audio processing model...")

    # Create model
    model = SimpleAudioProcessor(channels=2, kernel_size=7)
    model.eval()

    # Create example input (batch=1, channels=2, samples=4096)
    example_input = torch.randn(1, 2, 4096)

    print("Testing model with example input...")
    with torch.no_grad():
        output = model(example_input)
        print(f"  Input shape: {example_input.shape}")
        print(f"  Output shape: {output.shape}")

    # Export to TorchScript
    print(f"Exporting model to {output_path}...")
    traced_model = torch.jit.trace(model, example_input)
    traced_model.save(output_path)

    print("Model exported successfully!")
    print(f"Model file: {output_path}")
    print(f"Sample rate: {sample_rate} Hz")
    print("\nTo use this model in the VST plugin:")
    print(f"  1. Copy {output_path} to your DAW's plugin folder")
    print("  2. Load the Neural VST Plugin in your DAW")
    print("  3. The plugin will automatically load the model")

    return traced_model


def test_model(model_path="neural_model.pt"):
    """
    Test a TorchScript model with random audio data.

    Args:
        model_path: Path to the TorchScript model
    """
    print(f"Loading model from {model_path}...")
    model = torch.jit.load(model_path)
    model.eval()

    # Test with various buffer sizes
    test_sizes = [512, 1024, 2048, 4096]

    print("\nTesting model with different buffer sizes:")
    for size in test_sizes:
        test_input = torch.randn(1, 2, size)
        with torch.no_grad():
            output = model(test_input)
            print(f"  Buffer size {size}: ✓ (output shape: {output.shape})")

    print("\nModel testing complete!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create and export neural audio model")
    parser.add_argument("--output", default="neural_model.pt", help="Output model path")
    parser.add_argument("--test", action="store_true", help="Test the exported model")
    parser.add_argument("--sample-rate", type=int, default=44100, help="Sample rate")

    args = parser.parse_args()

    if args.test:
        test_model(args.output)
    else:
        model = create_and_export_model(args.output, args.sample_rate)
        print("\nRun with --test flag to test the exported model")
