"""Lax-Friedrichs scheme implementation.

A first-order centered scheme with numerical diffusion.
More isotropic diffusion compared to upwind scheme.
"""

import numpy as np
from numpy.typing import NDArray

from src.core.schemes.base_scheme import BaseScheme


class LaxFriedrichsScheme(BaseScheme):
    """Lax-Friedrichs scheme.

    Uses centered averaging with global maximum wave speed for diffusion.
    Characteristics:
        - Order: 1st order O(dx)
        - Centered diffusion (more isotropic than upwind)
        - CFL <= 1.0
    """

    def __init__(self, g: float = 9.81):
        """Initialize Lax-Friedrichs scheme.

        Args:
            g: Gravitational acceleration [m/s^2]
        """
        super().__init__("Lax-Friedrichs", 1, g)

    def compute_flux(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute Lax-Friedrichs numerical flux.

        Uses global maximum wave speed for diffusion (not local like Rusanov).

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]

        Returns:
            Tuple of (mass_flux, momentum_flux) at interfaces
        """
        nx = len(h)
        mass_flux = np.zeros(nx + 1, dtype=np.float64)
        mom_flux = np.zeros(nx + 1, dtype=np.float64)

        # Global maximum wave speed (Lax-Friedrichs uses global, not local)
        c = np.sqrt(self.g * np.maximum(h, 1e-12))
        s_max = np.max(np.abs(u) + c)

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

            # Lax-Friedrichs flux with global wave speed
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
