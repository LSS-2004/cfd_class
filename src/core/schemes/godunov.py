"""Godunov scheme implementation.

Uses the exact Riemann solver to compute numerical flux.
First-order accurate but captures shocks exactly.
"""

import numpy as np
from numpy.typing import NDArray

from src.core.schemes.base_scheme import BaseScheme
from src.core.solvers.exact import ExactRiemannSolver


class GodunovScheme(BaseScheme):
    """Godunov scheme using exact Riemann solver.

    Solves the exact Riemann problem at each interface to compute flux.
    Characteristics:
        - Order: 1st order O(dx)
        - Exact shock capturing
        - Most accurate for discontinuities
        - Computationally expensive (Newton iteration)
    """

    def __init__(self, g: float = 9.81):
        """Initialize Godunov scheme.

        Args:
            g: Gravitational acceleration [m/s^2]
        """
        super().__init__("Godunov", 1, g)
        self.riemann_solver = ExactRiemannSolver(g)

    def compute_flux(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute Godunov numerical flux using exact Riemann solver.

        Solves the Riemann problem at each interface with left state
        (h[i-1], u[i-1]) and right state (h[i], u[i]).

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

            # Solve exact Riemann problem
            state = self.riemann_solver.solve(h_l, u_l, h_r, u_r)

            # Compute flux from middle state
            h_star = state.h
            u_star = state.u

            # Physical flux at interface
            mass_flux[i] = h_star * u_star
            mom_flux[i] = h_star * u_star**2 + 0.5 * self.g * h_star**2

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
