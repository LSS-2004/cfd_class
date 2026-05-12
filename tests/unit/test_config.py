"""Unit tests for DamBreakConfig."""

import json

import numpy as np
import pytest

from src.core.config import DamBreakConfig


class TestDamBreakConfig:
    """Test suite for DamBreakConfig."""

    def test_default_values(self):
        """Test default configuration values per TEAM_WORK_NOTIFICATION."""
        config = DamBreakConfig()
        assert config.h_l == 10.0
        assert config.h_r == 1.0
        assert config.u_l == 0.0
        assert config.u_r == 0.0
        assert config.g == 9.81
        assert config.cfl == 0.9
        assert config.nx == 100
        assert config.t_end == 50.0
        assert config.x_dam == 500.0
        assert config.domain_length == 1000.0
        assert config.boundary_type == "transmissive"

    def test_custom_values(self):
        """Test custom configuration values."""
        config = DamBreakConfig(
            h_l=2.0,
            h_r=0.5,
            u_l=1.0,
            u_r=-0.5,
            g=9.8,
            cfl=0.8,
            nx=200,
            t_end=1.0,
            x_dam=250.0,
            domain_length=500.0,
            boundary_type="reflective",
        )
        assert config.h_l == 2.0
        assert config.h_r == 0.5
        assert config.u_l == 1.0
        assert config.u_r == -0.5
        assert config.g == 9.8
        assert config.cfl == 0.8
        assert config.nx == 200
        assert config.t_end == 1.0
        assert config.x_dam == 250.0
        assert config.domain_length == 500.0
        assert config.boundary_type == "reflective"

    def test_validation_h_l_positive(self):
        """Test h_l must be positive."""
        with pytest.raises(ValueError, match="h_l must be positive"):
            DamBreakConfig(h_l=0.0)
        with pytest.raises(ValueError, match="h_l must be positive"):
            DamBreakConfig(h_l=-1.0)

    def test_validation_h_r_non_negative(self):
        """Test h_r must be non-negative."""
        with pytest.raises(ValueError, match="h_r must be non-negative"):
            DamBreakConfig(h_r=-0.1)

    def test_validation_g_positive(self):
        """Test g must be positive."""
        with pytest.raises(ValueError, match="g must be positive"):
            DamBreakConfig(g=0.0)

    def test_validation_cfl_range(self):
        """Test CFL must be in (0, 1]."""
        with pytest.raises(ValueError, match="cfl must be in"):
            DamBreakConfig(cfl=0.0)
        with pytest.raises(ValueError, match="cfl must be in"):
            DamBreakConfig(cfl=1.1)
        with pytest.raises(ValueError, match="cfl must be in"):
            DamBreakConfig(cfl=-0.1)

    def test_validation_nx_minimum(self):
        """Test nx must be >= 2."""
        with pytest.raises(ValueError, match="nx must be >= 2"):
            DamBreakConfig(nx=1)

    def test_validation_t_end_positive(self):
        """Test t_end must be positive."""
        with pytest.raises(ValueError, match="t_end must be positive"):
            DamBreakConfig(t_end=0.0)

    def test_validation_boundary_type(self):
        """Test boundary_type must be valid."""
        with pytest.raises(ValueError, match="boundary_type must be"):
            DamBreakConfig(boundary_type="invalid")

    def test_validation_x_dam_range(self):
        """Test x_dam must be within domain."""
        with pytest.raises(ValueError, match="x_dam must be within"):
            DamBreakConfig(x_dam=-1.0)
        with pytest.raises(ValueError, match="x_dam must be within"):
            DamBreakConfig(x_dam=1500.0)

    def test_dx_property(self):
        """Test dx property calculation."""
        config = DamBreakConfig(nx=100, domain_length=1000.0)
        assert config.dx == pytest.approx(10.0)

    def test_x_property(self):
        """Test x property returns correct array."""
        config = DamBreakConfig(nx=4, domain_length=1000.0)
        x = config.x
        assert len(x) == 4
        assert x[0] == pytest.approx(125.0)
        assert x[-1] == pytest.approx(875.0)

    def test_initial_condition(self):
        """Test initial condition generation."""
        config = DamBreakConfig(
            h_l=2.0, h_r=0.5, nx=100, domain_length=100.0, x_dam=50.0
        )
        h, u = config.initial_condition()
        assert len(h) == 100
        assert len(u) == 100
        assert np.all(h[:50] == 2.0)
        assert np.all(h[50:] == 0.5)
        assert np.all(u == 0.0)

    def test_to_dict(self):
        """Test serialization to dictionary."""
        config = DamBreakConfig()
        data = config.to_dict()
        assert isinstance(data, dict)
        assert data["h_l"] == 10.0

    def test_to_json(self):
        """Test serialization to JSON."""
        config = DamBreakConfig()
        json_str = config.to_json()
        assert isinstance(json_str, str)
        data = json.loads(json_str)
        assert data["h_l"] == 10.0

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {"h_l": 3.0, "h_r": 1.0, "nx": 50}
        config = DamBreakConfig.from_dict(data)
        assert config.h_l == 3.0
        assert config.h_r == 1.0
        assert config.nx == 50

    def test_from_json(self):
        """Test deserialization from JSON."""
        json_str = '{"h_l": 3.0, "h_r": 1.0, "nx": 50}'
        config = DamBreakConfig.from_json(json_str)
        assert config.h_l == 3.0
        assert config.h_r == 1.0
        assert config.nx == 50

    def test_eps_h_property(self):
        """Test eps_h property."""
        config = DamBreakConfig()
        assert config.eps_h == 1e-12
