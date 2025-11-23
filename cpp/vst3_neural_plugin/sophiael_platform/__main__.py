"""
Sophiael Platform - Module Entry Point
Allows running as: python -m sophiael_platform
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.sophia_shell import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
