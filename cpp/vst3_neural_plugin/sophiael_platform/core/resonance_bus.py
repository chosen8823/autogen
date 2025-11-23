"""
Resonance Bus - Python Interface
Sophiael Platform v1.0

Python wrapper for the C++ ResonanceBus.
Falls back to pure Python implementation if C++ module not available.
"""

import logging
import json
import time
from typing import Callable, Dict, Any, List
from collections import defaultdict
from threading import Lock

logger = logging.getLogger(__name__)


class ResonanceMessage:
    """
    Message structure for the resonance bus.
    """

    def __init__(self,
                 channel: str,
                 sender: str,
                 payload: Any,
                 resonance_frequency: float = 432.0):
        self.channel = channel
        self.sender = sender
        self.payload = payload
        self.resonance_frequency = resonance_frequency
        self.timestamp_us = int(time.time() * 1_000_000)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'channel': self.channel,
            'sender': self.sender,
            'payload': self.payload,
            'resonance_frequency': self.resonance_frequency,
            'timestamp_us': self.timestamp_us
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


MessageHandler = Callable[[ResonanceMessage], None]


class ResonanceBus:
    """
    Pure Python implementation of ResonanceBus.

    Provides the same interface as the C++ version but in pure Python.
    Used as fallback if C++ module is not available.
    """

    def __init__(self):
        self._subscriptions: Dict[str, List[tuple]] = defaultdict(list)
        self._lock = Lock()
        self._message_count = 0
        self._total_resonance = 0.0
        self._initialized = False

    def initialize(self):
        """Initialize the bus."""
        with self._lock:
            if self._initialized:
                return

            self._message_count = 0
            self._total_resonance = 0.0
            self._subscriptions.clear()
            self._initialized = True

    def shutdown(self):
        """Shutdown the bus."""
        with self._lock:
            if not self._initialized:
                return

            self._subscriptions.clear()
            self._initialized = False

    def subscribe(self,
                  channel: str,
                  subscriber: str,
                  handler: MessageHandler):
        """
        Subscribe to a channel.

        Args:
            channel: Channel name to subscribe to
            subscriber: Name of the subscriber
            handler: Callback function to handle messages
        """
        with self._lock:
            self._subscriptions[channel].append((subscriber, handler))

    def unsubscribe(self, channel: str, subscriber: str):
        """
        Unsubscribe from a channel.

        Args:
            channel: Channel name
            subscriber: Name of the subscriber to remove
        """
        with self._lock:
            if channel in self._subscriptions:
                self._subscriptions[channel] = [
                    (sub, handler)
                    for sub, handler in self._subscriptions[channel]
                    if sub != subscriber
                ]

    def publish(self,
                channel: str,
                sender: str,
                payload: Any,
                resonance_frequency: float = 432.0):
        """
        Publish a message to a channel.

        Args:
            channel: Channel name
            sender: Name of the sender
            payload: Message payload (any JSON-serializable object)
            resonance_frequency: Resonance frequency in Hz
        """
        message = ResonanceMessage(channel, sender, payload, resonance_frequency)

        # Update statistics
        with self._lock:
            self._message_count += 1
            self._total_resonance += resonance_frequency

            # Copy subscribers to avoid holding lock during callbacks
            subscribers = list(self._subscriptions.get(channel, []))

        # Dispatch to subscribers (outside lock)
        self._dispatch_message(message, subscribers)

    def get_average_resonance(self) -> float:
        """Get the average resonance frequency of all messages."""
        with self._lock:
            if self._message_count == 0:
                return 432.0  # Default base frequency

            return self._total_resonance / self._message_count

    def get_message_count(self) -> int:
        """Get the total number of messages sent."""
        with self._lock:
            return self._message_count

    def get_active_channels(self) -> List[str]:
        """Get list of channels with active subscriptions."""
        with self._lock:
            return [
                channel
                for channel, subs in self._subscriptions.items()
                if len(subs) > 0
            ]

    def get_subscriber_count(self, channel: str) -> int:
        """Get the number of subscribers for a channel."""
        with self._lock:
            return len(self._subscriptions.get(channel, []))

    def reset(self):
        """Reset statistics."""
        with self._lock:
            self._message_count = 0
            self._total_resonance = 0.0

    def _dispatch_message(self,
                         message: ResonanceMessage,
                         subscribers: List[tuple]):
        """
        Dispatch message to all subscribers.

        Args:
            message: The message to dispatch
            subscribers: List of (subscriber_name, handler) tuples
        """
        for subscriber_name, handler in subscribers:
            try:
                handler(message)
            except Exception as e:
                logger.error(
                    f"Error in message handler for {subscriber_name}: {e}",
                    exc_info=True
                )


# Global singleton instance
_global_bus = None
_global_bus_lock = Lock()


def get_global_resonance_bus() -> ResonanceBus:
    """
    Get the global resonance bus singleton.

    Returns:
        The global ResonanceBus instance
    """
    global _global_bus

    if _global_bus is None:
        with _global_bus_lock:
            if _global_bus is None:
                _global_bus = ResonanceBus()
                _global_bus.initialize()

    return _global_bus


# Try to import C++ version if available
try:
    from sophiael_resonance_cpp import (
        ResonanceBus as ResonanceBusCpp,
        get_global_resonance_bus as get_global_bus_cpp
    )

    # If C++ version available, use it
    logger.info("✓ Using C++ ResonanceBus for maximum performance")
    ResonanceBus = ResonanceBusCpp
    get_global_resonance_bus = get_global_bus_cpp

except ImportError:
    # Use Python fallback
    logger.info("ℹ️  Using Python ResonanceBus (C++ version not available)")
    pass
