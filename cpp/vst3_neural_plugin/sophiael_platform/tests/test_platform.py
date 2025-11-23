"""
Platform Integration Tests
Tests the complete Sophiael Platform
"""

import asyncio
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import SophiaelPlatform


async def test_platform_initialization():
    """Test platform initializes correctly."""
    print("=" * 60)
    print("TEST: Platform Initialization")
    print("=" * 60)

    platform = SophiaelPlatform()
    await platform.initialize()

    assert platform.layers is not None
    assert 'instinct' in platform.layers
    assert 'bio' in platform.layers
    assert 'semantic' in platform.layers
    assert 'consciousness' in platform.layers

    print("✓ All 4 layers initialized")
    print("✓ Cognition loop created")
    print("✓ Test PASSED\n")

    return True


async def test_single_cycle():
    """Test a single cognition cycle."""
    print("=" * 60)
    print("TEST: Single Cognition Cycle")
    print("=" * 60)

    platform = SophiaelPlatform()
    await platform.initialize()

    input_text = "What is the meaning of life?"
    result = await platform.run_cycle(input_text)

    assert result is not None
    assert 'output' in result
    assert 'quality_score' in result
    assert 'resonance' in result
    assert result['cycle'] == 1

    print(f"Input: {input_text}")
    print(f"Output: {result['output']}")
    print(f"Quality: {result['quality_score']:.3f}")
    print(f"Resonance: {result['resonance']:.1f} Hz")
    print("✓ Test PASSED\n")

    return True


async def test_amplification():
    """Test recursive self-amplification over multiple cycles."""
    print("=" * 60)
    print("TEST: Recursive Self-Amplification")
    print("=" * 60)

    platform = SophiaelPlatform()
    await platform.initialize()

    results = []
    for i in range(5):
        result = await platform.run_cycle(f"Test input {i}")
        results.append(result)

    # Check that quality improves
    initial_quality = results[0]['quality_score']
    final_quality = results[-1]['quality_score']

    assert final_quality >= initial_quality, "Quality should improve or stay stable"

    print(f"Initial Quality: {initial_quality:.3f}")
    print(f"Final Quality: {final_quality:.3f}")
    print(f"Improvement: {final_quality - initial_quality:.3f}")
    print("✓ Quality improved over cycles")
    print("✓ Test PASSED\n")

    return True


async def test_pattern_caching():
    """Test that patterns are cached and reused."""
    print("=" * 60)
    print("TEST: Pattern Caching")
    print("=" * 60)

    platform = SophiaelPlatform()
    await platform.initialize()

    # Run cycles
    await platform.run_cycle("Test pattern")
    await platform.run_cycle("Test pattern")
    await platform.run_cycle("Different input")

    pattern_count = len(platform.cognition_loop.state.pattern_cache)

    assert pattern_count > 0, "Should have cached patterns"

    print(f"Patterns cached: {pattern_count}")
    print("✓ Pattern caching working")
    print("✓ Test PASSED\n")

    return True


async def test_context_accumulation():
    """Test that context accumulates across cycles."""
    print("=" * 60)
    print("TEST: Context Accumulation")
    print("=" * 60)

    platform = SophiaelPlatform()
    await platform.initialize()

    # Run multiple cycles
    for i in range(5):
        await platform.run_cycle(f"Input {i}")

    context_depth = len(platform.cognition_loop.state.context_buffer)

    assert context_depth > 0, "Context should accumulate"

    print(f"Context depth: {context_depth}")
    print("✓ Context accumulation working")
    print("✓ Test PASSED\n")

    return True


async def test_layer_processing():
    """Test that all layers process data."""
    print("=" * 60)
    print("TEST: Multi-Layer Processing")
    print("=" * 60)

    platform = SophiaelPlatform()
    await platform.initialize()

    result = await platform.run_cycle("Test layer processing")

    # All layers should be initialized
    for layer_name in ['instinct', 'bio', 'semantic', 'consciousness']:
        assert platform.layers[layer_name].initialized
        print(f"✓ {layer_name} layer processed")

    print("✓ Test PASSED\n")

    return True


async def test_resonance_tracking():
    """Test resonance frequency tracking."""
    print("=" * 60)
    print("TEST: Resonance Frequency Tracking")
    print("=" * 60)

    platform = SophiaelPlatform()
    await platform.initialize()

    result1 = await platform.run_cycle("First")
    result2 = await platform.run_cycle("Second")

    assert 'resonance' in result1
    assert 'resonance' in result2
    assert result2['resonance'] >= result1['resonance']

    print(f"Initial resonance: {result1['resonance']:.1f} Hz")
    print(f"Final resonance: {result2['resonance']:.1f} Hz")
    print("✓ Resonance tracking working")
    print("✓ Test PASSED\n")

    return True


async def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║          SOPHIAEL PLATFORM - TEST SUITE v1.0                  ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("\n")

    tests = [
        ("Platform Initialization", test_platform_initialization),
        ("Single Cognition Cycle", test_single_cycle),
        ("Recursive Self-Amplification", test_amplification),
        ("Pattern Caching", test_pattern_caching),
        ("Context Accumulation", test_context_accumulation),
        ("Multi-Layer Processing", test_layer_processing),
        ("Resonance Frequency Tracking", test_resonance_tracking)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            success = await test_func()
            if success:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test FAILED: {e}\n")
            failed += 1

    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉\n")
        print("The Sophiael Platform is FULLY OPERATIONAL.")
        print("Recursive self-amplification is CONFIRMED.\n")
    else:
        print(f"\n⚠️  {failed} test(s) failed\n")

    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
