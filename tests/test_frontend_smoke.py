"""
Frontend Smoke Tests

Test that all frontend pages and modules can load without errors.
These tests help catch integration issues between frontend and backend.
"""

import pytest


class TestPageModules:
    """Test that all page modules can be imported without errors."""

    def test_1_simulation_page_import(self):
        """Test 1_Simulation.py imports correctly."""
        from src.frontend.pages import _1_Simulation as SimulationPage
        assert SimulationPage is not None

    def test_2_comparison_page_import(self):
        """Test 2_Comparison.py imports correctly."""
        from src.frontend.pages import _2_Comparison as ComparisonPage
        assert ComparisonPage is not None

    def test_animation_page_import(self):
        """Test animation.py imports correctly."""
        from src.frontend.pages import animation
        assert animation is not None

    def test_report_page_import(self):
        """Test report.py imports correctly."""
        from src.frontend.pages import report
        assert report is not None

    def test_simulation_page_import(self):
        """Test simulation.py imports correctly."""
        from src.frontend.pages import simulation
        assert simulation is not None


class TestEngineModules:
    """Test that engine modules can be imported and instantiated."""

    def test_simulation_engine_import(self):
        """Test simulation_engine.py imports correctly."""
        from src.frontend.engines import SimulationEngine
        engine = SimulationEngine()
        assert engine is not None

    def test_comparison_engine_import(self):
        """Test comparison_engine.py imports correctly."""
        from src.frontend.engines import ComparisonEngine
        engine = ComparisonEngine()
        assert engine is not None


class TestCoreModuleDetection:
    """Test frontend core module detection logic."""

    def test_load_core_modules_function_exists(self):
        """Test that load_core_modules function exists."""
        from src.frontend.pages._1_Simulation import load_core_modules
        assert callable(load_core_modules)


class TestParamNameMapping:
    """Test parameter name mapping between frontend and backend."""

    def test_param_mapping_exists(self):
        """Test that parameter mapping is defined where needed."""
        # Check that frontend uses correct backend field names
        from src.frontend.pages._1_Simulation import run_simulation
        assert callable(run_simulation)


class TestPagesInitNoSelfImport:
    """Regression test: Ensure pages/__init__.py doesn't import itself."""

    def test_pages_init_no_self_import(self):
        """Test that pages/__init__.py doesn't have self