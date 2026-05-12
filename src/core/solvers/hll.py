"""HLL approximate Riemann solver for shallow water equations.

Implements the Harten-Lax-van Leer (HLL) approximate Riemann solver,
which provides a robust and efficient alternative to the exact solver.
"""

from typing import Tuple

import numpy as np
from numpy.typing import NDArray


class HLLSolver:
    """HLL approximate Riemann solver.

    Computes numerical flux at cell interfaces using the HLL approximation:
    F_HLL = (S_R * F_L - S_L * F_R + S_L * S_R * (U_R - U_L)) / (S_R - S_L)

    Attributes:
        g: Gravitational acceleration [m/s^2]
    """

    def __init__(self, g: float = 9.81):
        """Initialize HLL solver.

        Args:
            g: Gravitational acceleration [m/s^2]
        """
        self.g = g

    def _compute_wave_speeds(
        self,
        h_l: float,
        u_l: float,
        h_r: float,
        u_r: float,
    ) -> Tuple[float, float]:
        """Compute left and right wave speeds.

        Args:
            h_l: Left water depth [m]
            u_l: Left velocity [m/s]
            h_r: Right water depth [m]
            u_r: Right velocity [m/s]

        Returns:
            Tuple of (S_L, S_R) wave speeds
        """
        c_l = np.sqrt(self.g * h_l) if h_l > 0 else 0.0
        c_r = np.sqrt(self.g * h_r) if h_r > 0 else 0.0

        # Roe average
        sqrt_h_l = np.sqrt(h_l)
        sqrt_h_r = np.sqrt(h_r)

        if sqrt_h_l + sqrt_h_r < 1e-14:
            return 0.0, 0.0

        u_roe = (sqrt_h_l * u_l + sqrt_h_r * u_r) / (sqrt_h_l + sqrt_h_r)
        c_roe = np.sqrt(
            self.g * (sqrt_h_l * h_l + sqrt_h_r * h_r) / (sqrt_h_l + sqrt_h_r)
        )

        s_l = min(u_l - c_l, u_roe - c_roe)
        s_r = max(u_r + c_r, u_roe + c_roe)

        return s_l, s_r

    def compute_flux(
        self,
        h_l: float,
        u_l: float,
        h_r: float,
        u_r: float,
    ) -> NDArray[np.float64]:
        """Compute HLL numerical flux.

        Args:
            h_l: Left water depth [m]
            u_l: Left velocity [m/s]
            h_r: Right water depth [m]
            u_r: Right velocity [m/s]

        Returns:
            Flux vector [mass_flux, momentum_flux]
        """
        # Conservative variables
        u_l_vec = np.array([h_l, h_l * u_l], dtype=np.float64)
        u_r_vec = np.array([h_r, h_r * u_r], dtype=np.float64)

        # Physical fluxes
        f_l = np.array(
            [h_l * u_l, h_l * u_l**2 + 0.5 * self.g * h_l**2],
            dtype=np.float64,
        )
        f_r = np.array(
            [h_r * u_r, h_r * u_r**2 + 0.5 * self.g * h_r**2],
            dtype=np.float64,
        )

        # Wave speeds
        s_l, s_r = self._compute_wave_speeds(h_l, u_l, h_r, u_r)

        # Handle stationary case
        if abs(s_r - s_l) < 1e-14:
            return 0.5 * (f_l + f_r)

        # HLL flux formula
        if s_l >= 0:
            return f_l
        elif s_r <= 0:
            return f_r
        else:
            return (
                s_r * f_l - s_l * f_r + s_l * s_r * (u_r_vec - u_l_vec)
            ) / (s_r - s_l)

    def compute_flux_vectorized(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute HLL flux for all cell interfaces.

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]

        Returns:
            Tuple of (mass_flux, momentum_flux) arrays at interfaces
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

            flux = self.compute_flux(h_l, u_l, h_r, u_r)
            mass_flux[i] = flux[0]
            mom_flux[i] = flux[1]

        return mass_flux, mom_flux
