"""Unified automated test runner for the TalentScout chatbot.

This lightweight wrapper simply executes the intelligent, context-aware
test suite implemented in `smart_test.py`.
"""

import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH so `smart_test` imports work
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

import smart_test  # noqa: E402


def main() -> None:
    """Run all automated tests."""
    smart_test.run_intelligent_test()


if __name__ == "__main__":
    main()
