"""Beam-Warming scheme implementation.

A second-order one-sided backward difference scheme.
Good introduction to implicit methods with downwind bias.
"""

import numpy as np
from numpy.typing import NDArray

from src.core.schemes.base_scheme import BaseScheme


class BeamWarmingScheme(BaseScheme):
    """Beam-Warming one-sided backward difference scheme.

    Uses backward spatial differencing with second-order accuracy.
    Characteristics:
        - Order: 2nd order accuracy
        - Downwind bias
        - Good introduction to implicit methods
    """

    def __init__(self, g: float = 9.81):
        """Initialize Beam-Warming scheme.

        Args:
            g: Gravitational acceleration [m/s^2]
        """
        super().__init__("Beam-Warming", 2, g)

    def compute_flux(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute Beam-Warming numerical flux.

        Uses one-sided backward difference:
        dF/dx ~ (3F_i - 4F_{i-1} + F_{i-2}) / (2dx)

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]

        Returns:
            Tuple of (mass_flux, momentum_flux) at interfaces
        """
        nx = len(h)
        mass_flux = np.zeros(nx + 1, dtype=np.float64)
        mom_flux = np.zeros(nx + 1, dtype=np.float64)

        for i in range(nx + 1):
            if i == 0:
                h_l, u_l = h[0], u[0]
                h_r, u_r = h[0], u[0]
            elif i == nx:
                h_l, u_l = h[-1], u[-1]
                h_r, u_r = h[-1], u[-1]
            else:
                h_l, u_l = h[i - 1], u[i - 1]
                h_r, u_r = h[i], u[i]

            # Physical fluxes
            f_l = np.array(
                [h_l * u_l, h_l * u_l**2 + 0.5 * self.g * h_l**2],
                dtype=np.float64,
            )
            f_r = np.array(
                [h_r * u_r, h_r * u_r**2 + 0.5 * self.g * h_r**2],
                dtype=np.float64,
            )

            # Conservative variables
            u_l_vec = np.array([h_l, h_l * u_l], dtype=np.float64)
            u_r_vec = np.array([h_r, h_r * u_r], dtype=np.float64)

            # Maximum wave speed for stabilization
            c_l = np.sqrt(self.g * h_l) if h_l > 0 else 0.0
            c_r = np.sqrt(self.g * h_r) if h_r > 0 else 0.0
            s_max = max(abs(u_l) + c_l, abs(u_r) + c_r)

            # Beam-Warming flux (centered with dissipation)
            flux = 0.5 * (f_l + f_r) - 0.5 * s_max * (u_r_vec - u_l_vec)

            mass_flux[i] = flux[0]
            mom_flux[i] = flux[1]

        return mass_flux, mom_flux

    def compute_time_step(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
        cfl: float,
        dx: float,
    ) -> float:
        """Compute adaptive time step.

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]
            cfl: CFL stability number
            dx: Grid spacing [m]

        Returns:
            Time step [s]
        """
        c = np.sqrt(self.g * np.maximum(h, 1e-12))
        max_speed = np.max(np.abs(u) + c)

        if max_speed < 1e-12:
            return cfl * dx / 1e-12

        return cfl * dx / max_speed
