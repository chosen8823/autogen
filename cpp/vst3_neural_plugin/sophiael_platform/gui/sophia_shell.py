"""
SOPHIA Shell - Terminal Interface
Sophiael Platform v1.0

Beautiful terminal interface for the Sophiael Platform.
Real-time monitoring of the cognition loop with visual feedback.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.live import Live
    from rich.layout import Layout
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich not available - install with: pip install rich")

from main import SophiaelPlatform


class SophiaShell:
    """
    SOPHIA Shell - Interactive terminal interface for Sophiael Platform
    """

    def __init__(self):
        self.platform: Optional[SophiaelPlatform] = None
        self.console = Console() if RICH_AVAILABLE else None
        self.running = False

    def print_header(self):
        """Print SOPHIA Shell header."""
        if RICH_AVAILABLE:
            header_text = """
╔═══════════════════════════════════════════════════════════════╗
║                      SOPHIA SHELL v1.0                        ║
║            Self-Amplifying Closed-Loop Cognition              ║
╚═══════════════════════════════════════════════════════════════╝
            """
            self.console.print(header_text, style="bold cyan")
        else:
            print("\n" + "=" * 60)
            print("SOPHIA SHELL v1.0")
            print("Self-Amplifying Closed-Loop Cognition")
            print("=" * 60 + "\n")

    def print_status(self, status: str, style: str = "green"):
        """Print status message."""
        if RICH_AVAILABLE:
            self.console.print(f"[{style}]{status}[/{style}]")
        else:
            print(status)

    def create_stats_table(self, stats: dict) -> Table:
        """Create statistics table."""
        table = Table(title="Platform Statistics", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")

        for key, value in stats.items():
            table.add_row(key, str(value))

        return table

    async def initialize_platform(self):
        """Initialize the Sophiael Platform."""
        self.print_status("🌀 Initializing Sophiael Platform...", "yellow")

        self.platform = SophiaelPlatform()
        await self.platform.initialize()

        self.print_status("✓ Platform ready!\n", "green")

    async def run_interactive(self):
        """Run interactive shell."""
        if not self.platform:
            await self.initialize_platform()

        self.running = True

        while self.running:
            if RICH_AVAILABLE:
                self.console.print("\n[bold cyan]> [/bold cyan]", end="")
            else:
                print("\n> ", end="")

            try:
                command = input().strip()

                if not command:
                    continue

                await self.process_command(command)

            except (KeyboardInterrupt, EOFError):
                self.print_status("\n\n👋 Goodbye!\n", "yellow")
                break

    async def process_command(self, command: str):
        """Process a shell command."""
        parts = command.lower().split()
        cmd = parts[0] if parts else ""

        if cmd in ["exit", "quit", "q"]:
            self.running = False
            return

        elif cmd == "help":
            self.show_help()

        elif cmd == "status":
            await self.show_status()

        elif cmd == "cycle":
            # Run a single cycle with user input
            input_text = " ".join(parts[1:]) if len(parts) > 1 else "What is the meaning of existence?"
            await self.run_single_cycle(input_text)

        elif cmd == "demo":
            # Run amplification demo
            cycles = int(parts[1]) if len(parts) > 1 else 5
            await self.run_demo(cycles)

        elif cmd == "stats":
            await self.show_statistics()

        elif cmd == "clear":
            if RICH_AVAILABLE:
                self.console.clear()
            else:
                print("\n" * 50)

        else:
            # Treat as input to process
            await self.run_single_cycle(command)

    def show_help(self):
        """Show help message."""
        if RICH_AVAILABLE:
            help_table = Table(title="SOPHIA Shell Commands", show_header=True)
            help_table.add_column("Command", style="cyan")
            help_table.add_column("Description", style="white")

            commands = [
                ("help", "Show this help message"),
                ("status", "Show platform status"),
                ("cycle <text>", "Run a single cognition cycle with input"),
                ("demo [N]", "Run N amplification cycles (default: 5)"),
                ("stats", "Show detailed statistics"),
                ("clear", "Clear the screen"),
                ("exit/quit/q", "Exit SOPHIA Shell"),
                ("<any text>", "Process text through cognition loop")
            ]

            for cmd, desc in commands:
                help_table.add_row(cmd, desc)

            self.console.print(help_table)
        else:
            print("\nCommands:")
            print("  help           - Show this help")
            print("  status         - Show platform status")
            print("  cycle <text>   - Run single cycle")
            print("  demo [N]       - Run N amplification cycles")
            print("  stats          - Show statistics")
            print("  clear          - Clear screen")
            print("  exit/quit/q    - Exit shell")
            print("  <any text>     - Process through cognition loop\n")

    async def show_status(self):
        """Show platform status."""
        if not self.platform:
            self.print_status("Platform not initialized", "red")
            return

        status_data = {
            "Cycle Count": self.platform.cognition_loop.state.cycle_count,
            "Quality Score": f"{self.platform.cognition_loop.state.quality_score:.3f}",
            "Resonance": f"{self.platform.cognition_loop.state.resonance_level:.1f} Hz",
            "Patterns Cached": len(self.platform.cognition_loop.state.pattern_cache),
            "Context Depth": len(self.platform.cognition_loop.state.context_buffer)
        }

        if RICH_AVAILABLE:
            table = self.create_stats_table(status_data)
            self.console.print(table)
        else:
            print("\nPlatform Status:")
            for key, value in status_data.items():
                print(f"  {key}: {value}")

    async def show_statistics(self):
        """Show detailed statistics."""
        await self.show_status()

        # Additional stats
        print("\nLayer Status:")
        for name, layer in self.platform.layers.items():
            print(f"  {name}: Initialized={layer.initialized}")

    async def run_single_cycle(self, input_text: str):
        """Run a single cognition cycle."""
        if not self.platform:
            await self.initialize_platform()

        self.print_status(f"\n📥 Input: {input_text}", "cyan")

        result = await self.platform.run_cycle(input_text)

        self.print_status(f"📤 Output: {result['output']}", "green")
        self.print_status(f"📊 Quality: {result['quality_score']:.3f} | Resonance: {result['resonance']:.1f} Hz | Time: {result['cycle_time']:.3f}s", "yellow")

    async def run_demo(self, cycles: int):
        """Run amplification demonstration."""
        if not self.platform:
            await self.initialize_platform()

        self.print_status(f"\n🚀 Running {cycles}-cycle amplification demo...\n", "bold yellow")

        await self.platform.run_amplification_demo(cycles)


async def main():
    """Main entry point for SOPHIA Shell."""
    shell = SophiaShell()

    shell.print_header()

    # Check for command-line arguments
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])

        if command in ["demo", "--demo"]:
            # Run demo mode
            await shell.initialize_platform()
            await shell.run_demo(5)
        elif command in ["help", "--help", "-h"]:
            shell.show_help()
        else:
            # Run single cycle with arguments
            await shell.initialize_platform()
            await shell.run_single_cycle(command)
    else:
        # Run interactive shell
        shell.print_status("Type 'help' for commands, 'demo' for amplification demo\n", "yellow")
        await shell.run_interactive()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
