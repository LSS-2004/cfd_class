"""Configuration management for dam break simulations.

This module provides the DamBreakConfig dataclass for managing simulation
parameters with validation and serialization capabilities.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Literal
import json

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class DamBreakConfig:
    """Configuration for one-dimensional dam break simulations.

    Attributes:
        h_l: Left initial water depth [m], must be > 0
        h_r: Right initial water depth [m], must be >= 0
        u_l: Left initial velocity [m/s]
        u_r: Right initial velocity [m/s]
        g: Gravitational acceleration [m/s^2], default 9.81
        cfl: CFL stability number, must be in (0, 1]
        nx: Number of grid cells, must be >= 2
        t_end: Simulation end time [s], must be > 0
        x_dam: Dam position [m], default 500.0
        domain_length: Domain length [m], default 1000.0
        boundary_type: Boundary condition type, default "transmissive"
    """

    # Physical parameters
    h_l: float = 10.0
    h_r: float = 1.0
    u_l: float = 0.0
    u_r: float = 0.0
    g: float = 9.81

    # Numerical parameters
    cfl: float = 0.9
    nx: int = 100
    t_end: float = 50.0

    # Domain parameters
    x_dam: float = 500.0
    domain_length: float = 1000.0
    boundary_type: Literal["transmissive", "reflective", "periodic"] = "transmissive"

    # Internal constants
    _eps_h: float = field(default=1e-12, repr=False)

    def __post_init__(self) -> None:
        """Validate configuration parameters after initialization."""
        self.validate()

    def validate(self) -> None:
        """Validate all configuration parameters.

        Raises:
            ValueError: If any parameter is out of valid range.
        """
        errors = []

        if self.h_l <= 0:
            errors.append(f"h_l must be positive, got {self.h_l}")
        if self.h_r < 0:
            errors.append(f"h_r must be non-negative, got {self.h_r}")
        if self.g <= 0:
            errors.append(f"g must be positive, got {self.g}")
        if not 0 < self.cfl <= 1.0:
            errors.append(f"cfl must be in (0, 1], got {self.cfl}")
        if self.nx < 2:
            errors.append(f"nx must be >= 2, got {self.nx}")
        if self.t_end <= 0:
            errors.append(f"t_end must be positive, got {self.t_end}")
        if self.domain_length <= 0:
            errors.append(
                f"domain_length must be positive, got {self.domain_length}"
            )
        if not 0 <= self.x_dam <= self.domain_length:
            errors.append(
                f"x_dam must be within [0, domain_length], got {self.x_dam}"
            )
        if self.boundary_type not in ("transmissive", "reflective", "periodic"):
            errors.append(
                f"boundary_type must be 'transmissive', 'reflective', or 'periodic', "
                f"got {self.boundary_type}"
            )

        if errors:
            raise ValueError("; ".join(errors))

    @property
    def dx(self) -> float:
        """Grid spacing [m]."""
        return self.domain_length / self.nx

    @property
    def x(self) -> NDArray[np.float64]:
        """Cell center coordinates [m]."""
        return np.linspace(
            self.dx / 2,
            self.domain_length - self.dx / 2,
            self.nx,
        )

    @property
    def eps_h(self) -> float:
        """Minimum water depth tolerance [m]."""
        return self._eps_h

    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return asdict(self)

    def to_json(self, indent: Optional[int] = 2) -> str:
        """Serialize configuration to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict) -> "DamBreakConfig":
        """Create configuration from dictionary."""
        # Filter out internal fields
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

    @classmethod
    def from_json(cls, json_str: str) -> "DamBreakConfig":
        """Create configuration from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def initial_condition(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Generate initial condition arrays.

        Returns:
            Tuple of (h, u) arrays at t=0.
        """
        h = np.where(self.x < self.x_dam, self.h_l, self.h_r)
        u = np.where(self.x < self.x_dam, self.u_l, self.u_r)
        return h.astype(np.float64), u.astype(np.float64)
