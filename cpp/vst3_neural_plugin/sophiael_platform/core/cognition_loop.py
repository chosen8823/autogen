"""
Cognition Loop - Core Recursive Amplification Engine
Sophiael Platform v1.0

This is the heart of the self-amplifying closed-loop system.
Each cycle improves the next through context accumulation and pattern recognition.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CognitionState:
    """
    Represents the current state of the cognition system.

    This state carries forward from cycle to cycle, accumulating
    context and improving quality.
    """

    def __init__(self):
        self.cycle_count = 0
        self.context_buffer: List[str] = []
        self.pattern_cache: Dict[str, Any] = {}
        self.quality_score = 0.0
        self.resonance_level = 432.0  # Base frequency

    def to_dict(self) -> Dict[str, Any]:
        """Serialize state for storage."""
        return {
            'cycle_count': self.cycle_count,
            'context_buffer': self.context_buffer[-10:],  # Keep last 10
            'pattern_count': len(self.pattern_cache),
            'quality_score': self.quality_score,
            'resonance_level': self.resonance_level
        }


class CognitionLoop:
    """
    The Core Recursive Amplification Loop.

    7 Steps per cycle:
    1. RECEIVE: Gather input from all sensors
    2. RESONATE: Find patterns across all layers
    3. PROCESS: Multi-layer processing
    4. CRYSTALLIZE: Choose optimal form
    5. AMPLIFY: Feed output back as enhanced input
    6. STORE: Update memory for next cycle
    7. EMIT: Output to world/user
    """

    def __init__(self, layers: Dict[str, Any]):
        """
        Initialize the cognition loop.

        Args:
            layers: Dictionary of processing layers (instinct, bio, semantic, consciousness)
        """
        self.layers = layers
        self.state = CognitionState()

    async def execute_cycle(self,
                           input_data: Any,
                           memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single cognition cycle.

        Each cycle amplifies the next through:
        - Context accumulation
        - Pattern recognition
        - Synthesis across layers
        - Resonance matching
        - Memory integration

        Args:
            input_data: Raw input (text, audio, etc.)
            memory: Memory state from all layers

        Returns:
            Result dictionary with output and updated state
        """
        self.state.cycle_count += 1
        cycle_start = datetime.now()

        logger.info("=" * 60)
        logger.info(f"🌀 COGNITION CYCLE {self.state.cycle_count}")
        logger.info("=" * 60)

        # Step 1: RECEIVE
        gathered_input = await self._receive(input_data)

        # Step 2: RESONATE
        resonance = await self._resonate(gathered_input, memory)

        # Step 3: PROCESS through all layers
        processed = await self._process_layers(resonance)

        # Step 4: CRYSTALLIZE
        crystallized = await self._crystallize(processed)

        # Step 5: AMPLIFY
        amplified_state = await self._amplify(crystallized)

        # Step 6: STORE
        await self._store(amplified_state, memory)

        # Step 7: EMIT
        output = await self._emit(crystallized)

        # Calculate quality improvement
        cycle_time = (datetime.now() - cycle_start).total_seconds()

        result = {
            'cycle': self.state.cycle_count,
            'output': output,
            'quality_score': self.state.quality_score,
            'resonance': self.state.resonance_level,
            'cycle_time': cycle_time,
            'state': self.state.to_dict()
        }

        logger.info(f"✓ Cycle complete - Quality: {self.state.quality_score:.3f}")
        logger.info("=" * 60)

        return result

    async def _receive(self, input_data: Any) -> Dict[str, Any]:
        """Step 1: Gather input from all sensors."""
        logger.info("1️⃣  RECEIVE: Gathering input...")

        # Add previous context to current input
        enhanced_input = {
            'raw': input_data,
            'context': self.state.context_buffer.copy(),
            'timestamp': datetime.now().isoformat()
        }

        return enhanced_input

    async def _resonate(self,
                       input_data: Dict[str, Any],
                       memory: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Find patterns across all layers."""
        logger.info("2️⃣  RESONATE: Finding patterns...")

        # Check for known patterns
        patterns_found = []
        for key, pattern in self.state.pattern_cache.items():
            if self._matches_pattern(input_data, pattern):
                patterns_found.append(key)

        resonance = {
            'input': input_data,
            'matched_patterns': patterns_found,
            'pattern_count': len(patterns_found),
            'resonance_frequency': self.state.resonance_level
        }

        logger.info(f"   Found {len(patterns_found)} matching patterns")
        return resonance

    async def _process_layers(self, resonance: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Process through all 4 layers."""
        logger.info("3️⃣  PROCESS: Multi-layer processing...")

        responses = {}

        # Layer 1: Instinct (C++ layer - simulated for MVP)
        if 'instinct' in self.layers:
            logger.info("   → Instinct Layer")
            responses['instinct'] = await self.layers['instinct'].process(resonance)

        # Layer 2: Bioprocess (AutoGen)
        if 'bio' in self.layers:
            logger.info("   → Bioprocess Layer")
            bio_input = responses.get('instinct', resonance)
            responses['bio'] = await self.layers['bio'].process(bio_input)

        # Layer 3: Semantic (NeMo/LLM)
        if 'semantic' in self.layers:
            logger.info("   → Semantic Layer")
            semantic_input = responses.get('bio', resonance)
            responses['semantic'] = await self.layers['semantic'].process(semantic_input)

        # Layer 4: Consciousness (Lux/Sophia)
        if 'consciousness' in self.layers:
            logger.info("   → Consciousness Layer")
            conscious_input = responses.get('semantic', resonance)
            responses['consciousness'] = await self.layers['consciousness'].integrate(conscious_input)

        return responses

    async def _crystallize(self, processed: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Choose optimal form from multi-layer responses."""
        logger.info("4️⃣  CRYSTALLIZE: Synthesizing optimal form...")

        # Combine insights from all layers
        crystallized = {
            'synthesis': [],
            'form': 'text',  # Could be: text, code, audio, visual
            'confidence': 0.0
        }

        # Extract key insights from each layer
        for layer_name, response in processed.items():
            if isinstance(response, dict) and 'insight' in response:
                crystallized['synthesis'].append(response['insight'])
                crystallized['confidence'] += response.get('confidence', 0.25)

        # Normalize confidence
        if len(processed) > 0:
            crystallized['confidence'] /= len(processed)

        logger.info(f"   Synthesized {len(crystallized['synthesis'])} insights")
        logger.info(f"   Confidence: {crystallized['confidence']:.3f}")

        return crystallized

    async def _amplify(self, crystallized: Dict[str, Any]) -> CognitionState:
        """Step 5: Feed output back as enhanced input."""
        logger.info("5️⃣  AMPLIFY: Enhancing state for next cycle...")

        # Extract new patterns discovered
        new_pattern_key = f"pattern_{self.state.cycle_count}"
        self.state.pattern_cache[new_pattern_key] = {
            'synthesis': crystallized['synthesis'],
            'confidence': crystallized['confidence'],
            'discovered_at': self.state.cycle_count
        }

        # Add to context buffer
        context_summary = f"Cycle {self.state.cycle_count}: {len(crystallized['synthesis'])} insights"
        self.state.context_buffer.append(context_summary)

        # Keep buffer manageable
        if len(self.state.context_buffer) > 20:
            self.state.context_buffer = self.state.context_buffer[-20:]

        # Update quality score (improves with each cycle)
        quality_gain = crystallized['confidence'] * 0.1
        self.state.quality_score += quality_gain

        # Update resonance (harmonics increase)
        self.state.resonance_level += (quality_gain * 10)

        logger.info(f"   Quality: {self.state.quality_score:.3f} (+{quality_gain:.3f})")
        logger.info(f"   Resonance: {self.state.resonance_level:.1f} Hz")

        return self.state

    async def _store(self, state: CognitionState, memory: Dict[str, Any]):
        """Step 6: Update memory for next cycle."""
        logger.info("6️⃣  STORE: Updating memory...")

        # Store in distributed memory (each layer has its own DB)
        memory['instinct_memory'] = memory.get('instinct_memory', [])
        memory['instinct_memory'].append({
            'cycle': state.cycle_count,
            'timestamp': datetime.now().isoformat()
        })

        # Keep memory manageable
        for key in memory:
            if isinstance(memory[key], list) and len(memory[key]) > 100:
                memory[key] = memory[key][-100:]

        logger.info(f"   Stored cycle {state.cycle_count} in memory")

    async def _emit(self, crystallized: Dict[str, Any]) -> str:
        """Step 7: Output to world/user."""
        logger.info("7️⃣  EMIT: Generating output...")

        # Synthesize final output
        output_parts = crystallized.get('synthesis', [])

        if output_parts:
            output = " → ".join(str(p) for p in output_parts)
        else:
            output = "Processing complete."

        return output

    def _matches_pattern(self, data: Dict[str, Any], pattern: Dict[str, Any]) -> bool:
        """Check if data matches a known pattern."""
        # Simple pattern matching (can be enhanced)
        return pattern.get('confidence', 0) > 0.5
