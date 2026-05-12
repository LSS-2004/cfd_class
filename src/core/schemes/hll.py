"""HLL scheme implementation.

Harten-Lax-van Leer approximate Riemann solver scheme.
First-order accurate, robust and computationally efficient.
"""

import numpy as np
from numpy.typing import NDArray

from src.core.schemes.base_scheme import BaseScheme
from src.core.solvers.hll import HLLSolver


class HLLScheme(BaseScheme):
    """HLL scheme using approximate Riemann solver.

    Uses the HLL approximate Riemann solver to compute numerical flux.
    Characteristics:
        - Order: 1st order O(dx)
        - TVD stable (approximate)
        - More efficient than exact solver
        - Good for practical engineering applications
    """

    def __init__(self, g: float = 9.81):
        """Initialize HLL scheme.

        Args:
            g: Gravitational acceleration [m/s^2]
        """
        super().__init__("HLL", 1, g)
        self.riemann_solver = HLLSolver(g)

    def compute_flux(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute HLL numerical flux.

        Uses HLL approximate Riemann solver at each interface.

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

            # Use HLL solver for flux
            flux = self.riemann_solver.compute_flux(h_l, u_l, h_r, u_r)
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
