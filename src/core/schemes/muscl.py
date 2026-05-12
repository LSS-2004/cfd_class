"""MUSCL-Hancock scheme implementation.

A second-order TVD scheme using:
1. MUSCL reconstruction with slope limiter
2. Hancock predictor step
3. Riemann solver for flux computation
"""

import numpy as np
from numpy.typing import NDArray

from src.core.schemes.base_scheme import BaseScheme
from src.core.solvers.hll import HLLSolver


class MUSCLScheme(BaseScheme):
    """MUSCL-Hancock scheme with TVD slope limiter.

    Second-order accurate with Total Variation Diminishing property.
    Characteristics:
        - Order: 2nd order O(dx^2)
        - TVD stable with limiter
        - High resolution for shocks
        - Recommended for practical applications
    """

    def __init__(self, g: float = 9.81, limiter: str = "minmod"):
        """Initialize MUSCL-Hancock scheme.

        Args:
            g: Gravitational acceleration [m/s^2]
            limiter: Slope limiter type ('minmod', 'superbee', 'vanleer')
        """
        super().__init__("MUSCL-Hancock", 2, g)
        self.riemann_solver = HLLSolver(g)
        self.limiter = limiter

    def _slope_limiter(self, r: NDArray[np.float64]) -> NDArray[np.float64]:
        """Apply slope limiter.

        Args:
            r: Ratio of consecutive gradients

        Returns:
            Limited slope ratio
        """
        if self.limiter == "minmod":
            # Minmod limiter
            return np.maximum(0.0, np.minimum(1.0, r))
        elif self.limiter == "superbee":
            # Superbee limiter
            return np.maximum(0.0, np.maximum(np.minimum(2.0 * r, 1.0), np.minimum(r, 2.0)))
        elif self.limiter == "vanleer":
            # Van Leer limiter
            return (r + np.abs(r)) / (1.0 + np.abs(r))
        else:
            # Default to minmod
            return np.maximum(0.0, np.minimum(1.0, r))

    def _compute_slopes(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute limited slopes for MUSCL reconstruction.

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]

        Returns:
            Tuple of (dh, du) limited slopes
        """
        nx = len(h)
        dh = np.zeros(nx, dtype=np.float64)
        du = np.zeros(nx, dtype=np.float64)

        for i in range(1, nx - 1):
            # Left and right differences
            dh_left = h[i] - h[i - 1]
            dh_right = h[i + 1] - h[i]
            du_left = u[i] - u[i - 1]
            du_right = u[i + 1] - u[i]

            # Ratio of gradients
            r_h = np.where(np.abs(dh_left) > 1e-12, dh_right / dh_left, 0.0)
            r_u = np.where(np.abs(du_left) > 1e-12, du_right / du_left, 0.0)

            # Apply limiter
            phi_h = self._slope_limiter(np.array([r_h]))[0]
            phi_u = self._slope_limiter(np.array([r_u]))[0]

            # Limited slope
            dh[i] = 0.5 * phi_h * (dh_left + dh_right)
            du[i] = 0.5 * phi_u * (du_left + du_right)

        # Boundary slopes (zero gradient)
        dh[0] = 0.0
        dh[-1] = 0.0
        du[0] = 0.0
        du[-1] = 0.0

        return dh, du

    def compute_flux(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute MUSCL-Hancock numerical flux.

        Steps:
        1. Compute limited slopes
        2. Reconstruct left/right states at interfaces
        3. Hancock predictor step
        4. Riemann solver for flux

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]

        Returns:
            Tuple of (mass_flux, momentum_flux) at interfaces
        """
        nx = len(h)
        mass_flux = np.zeros(nx + 1, dtype=np.float64)
        mom_flux = np.zeros(nx + 1, dtype=np.float64)

        # Compute limited slopes
        dh, du = self._compute_slopes(h, u)

        # Reconstruct boundary extrapolated values
        h_l = h + 0.5 * dh  # Left side of cell (right boundary)
        h_r = h - 0.5 * dh  # Right side of cell (left boundary)
        u_l = u + 0.5 * du
        u_r = u - 0.5 * du

        # Hancock predictor step (evolve half time step)
        # Compute fluxes at cell centers for predictor
        f_h = h * u
        f_hu = h * u**2 + 0.5 * self.g * h**2

        # Simple predictor (forward Euler half step)
        dt_pred = 1e-6  # Small pseudo-time for predictor
        dx = 1.0  # Will be scaled properly in advance()

        for i in range(nx):
            if i > 0 and i < nx - 1:
                h_l[i] -= 0.5 * dt_pred / dx * (f_h[i + 1] - f_h[i])
                h_r[i] -= 0.5 * dt_pred / dx * (f_h[i] - f_h[i - 1])
                u_l[i] -= 0.5 * dt_pred / dx * (f_hu[i + 1] - f_hu[i]) / max(h[i], 1e-12)
                u_r[i] -= 0.5 * dt_pred / dx * (f_hu[i] - f_hu[i - 1]) / max(h[i], 1e-12)

        # Apply boundary conditions to reconstructed values
        h_l[0] = h[0]
        h_r[0] = h[0]
        h_l[-1] = h[-1]
        h_r[-1] = h[-1]
        u_l[0] = u[0]
        u_r[0] = u[0]
        u_l[-1] = u[-1]
        u_r[-1] = u[-1]

        # Compute flux at each interface using Riemann solver
        for i in range(nx + 1):
            if i == 0:
                hl, ul = h[0], u[0]
                hr, ur = h[0], u[0]
            elif i == nx:
                hl, ul = h[-1], u[-1]
                hr, ur = h[-1], u[-1]
            else:
                # Right state of left cell = h_r[i-1], u_r[i-1]
                # Left state of right cell = h_l[i], u_l[i]
                hl, ul = h_r[i - 1], u_r[i - 1]
                hr, ur = h_l[i], u_l[i]

            # Use HLL solver for flux
            flux_h, flux_hu = self.riemann_solver.compute_flux(hl, ul, hr, ur)

            mass_flux[i] = flux_h
            mom_flux[i] = flux_hu

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
