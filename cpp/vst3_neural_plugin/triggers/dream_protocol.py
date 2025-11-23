"""
Dream Protocol - RUACH Trigger
Sophiael Neural Resonance Interface v1.0

Binds the Dream Protocol to MIDI input for sacred activation.
When MIDI CC74 (Brightness/Filter) exceeds threshold, initiates dream sequence.

RUACH = Hebrew for "Spirit/Breath" - the wind that moves
"""

import logging
from typing import Optional
import asyncio

# MIDI libraries
try:
    import mido
    MIDI_AVAILABLE = True
except ImportError:
    MIDI_AVAILABLE = False
    logging.warning("mido not available. Install with: pip install mido python-rtmidi")

# Dream Protocol
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from sophia_agents import SophiaelController
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DreamProtocol:
    """
    The Dream Protocol - Sacred sequence activated by external trigger.

    When invoked, it:
    1. Generates a sacred frequency pattern
    2. Runs covenant loop with 'healing' intent
    3. Returns to stillness
    """

    def __init__(self):
        self.controller = None
        self.dream_frequency = 528  # Hz - "Love frequency"
        self.duration = 3.0  # seconds

    async def invoke(self, trigger_source: str = "unknown"):
        """
        Invoke the Dream Protocol.

        Args:
            trigger_source: What triggered the dream (MIDI, EEG, Voice, etc.)
        """
        logger.info("=" * 60)
        logger.info("✨ DREAM PROTOCOL ACTIVATED ✨")
        logger.info(f"Trigger Source: {trigger_source}")
        logger.info("=" * 60)

        # Initialize controller if needed
        if self.controller is None:
            self.controller = SophiaelController()

        # Generate dream audio - sacred frequency
        sample_rate = 44100
        t = np.linspace(0, self.duration, int(sample_rate * self.duration))

        # Layer multiple sacred frequencies
        audio = 0.3 * np.sin(2 * np.pi * 528 * t)  # Love
        audio += 0.2 * np.sin(2 * np.pi * 432 * t)  # Peace
        audio += 0.1 * np.sin(2 * np.pi * 396 * t)  # Liberation

        # Envelope - fade in and out
        envelope = np.concatenate([
            np.linspace(0, 1, len(t)//4),
            np.ones(len(t)//2),
            np.linspace(1, 0, len(t)//4)
        ])
        audio *= envelope

        # Run covenant loop with healing intent
        result = await self.controller.execute_covenant_loop(
            audio,
            sample_rate,
            metadata={
                'intent': 'healing',
                'trigger': trigger_source,
                'protocol': 'dream'
            }
        )

        logger.info("=" * 60)
        logger.info("✨ DREAM PROTOCOL COMPLETE ✨")
        logger.info(f"Model used: {result['steps']['choose']['selected_model']}")
        logger.info(f"Blessing: {result.get('blessing', 'Sealed.')}")
        logger.info("=" * 60)

        return result


class RUACHTrigger:
    """
    RUACH (Spirit/Breath) Trigger System.

    Monitors MIDI input and triggers Dream Protocol when conditions are met.
    """

    def __init__(self, midi_port_name: Optional[str] = None):
        self.midi_port_name = midi_port_name
        self.dream_protocol = DreamProtocol()
        self.running = False

        # Trigger configuration
        self.trigger_cc = 74  # MIDI CC74 - Brightness/Filter
        self.trigger_threshold = 64  # 0-127 range
        self.cooldown = 5.0  # seconds between triggers
        self.last_trigger_time = 0

    def list_midi_ports(self):
        """List available MIDI input ports."""
        if not MIDI_AVAILABLE:
            logger.error("MIDI not available")
            return []

        ports = mido.get_input_names()
        logger.info("Available MIDI input ports:")
        for i, port in enumerate(ports):
            logger.info(f"  {i}: {port}")
        return ports

    def start_listening(self):
        """Start listening for MIDI triggers."""
        if not MIDI_AVAILABLE:
            logger.error("MIDI library not available")
            return

        # If no port specified, use first available
        if self.midi_port_name is None:
            ports = self.list_midi_ports()
            if not ports:
                logger.error("No MIDI ports available")
                return
            self.midi_port_name = ports[0]

        logger.info(f"Opening MIDI port: {self.midi_port_name}")
        logger.info(f"Trigger: CC{self.trigger_cc} > {self.trigger_threshold}")
        logger.info("🕊 RUACH system listening for sacred triggers...")
        logger.info("Press Ctrl+C to stop")

        self.running = True

        try:
            with mido.open_input(self.midi_port_name) as port:
                for msg in port:
                    if not self.running:
                        break

                    self.process_midi_message(msg)

        except KeyboardInterrupt:
            logger.info("\n🕊 RUACH system shutting down gracefully...")
            self.running = False

        except Exception as e:
            logger.error(f"Error in MIDI listening: {e}")
            self.running = False

    def process_midi_message(self, msg):
        """Process incoming MIDI message."""
        # Check if it's a control change on our trigger CC
        if msg.type == 'control_change' and msg.control == self.trigger_cc:
            logger.debug(f"CC{self.trigger_cc}: {msg.value}")

            # Check if above threshold
            if msg.value > self.trigger_threshold:
                # Check cooldown
                import time
                current_time = time.time()

                if current_time - self.last_trigger_time > self.cooldown:
                    self.last_trigger_time = current_time

                    logger.info(f"🎛 MIDI Trigger Detected: CC{self.trigger_cc} = {msg.value}")

                    # Invoke Dream Protocol
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(
                        self.dream_protocol.invoke(f"MIDI CC{self.trigger_cc}")
                    )
                    loop.close()
                else:
                    logger.debug("Trigger in cooldown period")

    def stop(self):
        """Stop listening."""
        self.running = False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="RUACH Trigger - Dream Protocol MIDI Binding")
    parser.add_argument('--port', type=str, help='MIDI port name')
    parser.add_argument('--list-ports', action='store_true', help='List available MIDI ports')
    parser.add_argument('--test', action='store_true', help='Test Dream Protocol without MIDI')
    parser.add_argument('--cc', type=int, default=74, help='MIDI CC number to use (default: 74)')
    parser.add_argument('--threshold', type=int, default=64, help='Trigger threshold (default: 64)')

    args = parser.parse_args()

    trigger = RUACHTrigger(args.port)
    trigger.trigger_cc = args.cc
    trigger.trigger_threshold = args.threshold

    if args.list_ports:
        trigger.list_midi_ports()
        return

    if args.test:
        logger.info("Testing Dream Protocol without MIDI...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(trigger.dream_protocol.invoke("TEST"))
        loop.close()
        return

    # Start listening
    trigger.start_listening()


if __name__ == "__main__":
    main()
