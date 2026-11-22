"""
Shared fixtures and test configuration for the IR test suite.
"""
import os
import sys
import pytest

# Ensure project root is available to tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
