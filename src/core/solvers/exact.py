"""Exact Riemann solver for shallow water equations.

Implements the exact solution of the Riemann problem for the 1D shallow
water equations following Toro (2009).

Supports both wet-bed and dry-bed cases.
"""

from dataclasses import dataclass
from typing import Tuple

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class RiemannState:
    """Solution state at a point in the Riemann problem.

    Attributes:
        h: Water depth [m]
        u: Velocity [m/s]
        wave_speeds: Tuple of wave speeds (S_l, S_r, S_star)
    """

    h: float
    u: float
    wave_speeds: Tuple[float, float, float]


class ExactRiemannSolver:
    """Exact Riemann solver for shallow water equations.

    Solves the Riemann problem with left state (h_l, u_l) and right
    state (h_r, u_r) using Newton iteration for the exact solution.
    """

    def __init__(self, g: float = 9.81, tol: float = 1e-6, max_iter: int = 100):
        """Initialize solver.

        Args:
            g: Gravitational acceleration [m/s^2]
            tol: Convergence tolerance for Newton iteration
            max_iter: Maximum Newton iterations
        """
        self.g = g
        self.tol = tol
        self.max_iter = max_iter

    def _f(
        self, h: float, h_k: float, u_k: float
    ) -> Tuple[float, float]:
        """Compute f(h) and f'(h) for Newton iteration.

        Args:
            h: Guess for middle state depth
            h_k: Left or right depth
            u_k: Left or right velocity

        Returns:
            Tuple of (f, df/dh)
        """
        if h > h_k:
            # Shock wave
            sqrt_term = np.sqrt(0.5 * self.g * (h + h_k) / (h * h_k))
            f = (h - h_k) * sqrt_term
            df = sqrt_term - 0.25 * self.g * (h - h_k) / (
                h * h_k * sqrt_term
            )
        else:
            # Rarefaction wave
            c_k = np.sqrt(self.g * h_k)
            c = np.sqrt(self.g * h)
            f = 2.0 * (c - c_k)
            df = self.g / c

        return f, df

    def solve(
        self, h_l: float, u_l: float, h_r: float, u_r: float
    ) -> RiemannState:
        """Solve Riemann problem.

        Args:
            h_l: Left water depth [m]
            u_l: Left velocity [m/s]
            h_r: Right water depth [m]
            u_r: Right velocity [m/s]

        Returns:
            RiemannState with middle state solution
        """
        # Handle dry bed cases
        if h_l <= 0 and h_r <= 0:
            return RiemannState(0.0, 0.0, (0.0, 0.0, 0.0))

        if h_l <= 0:
            # Left dry bed
            c_r = np.sqrt(self.g * h_r)
            s = u_r + 2.0 * c_r
            return RiemannState(0.0, s, (0.0, s, s))

        if h_r <= 0:
            # Right dry bed
            c_l = np.sqrt(self.g * h_l)
            s = u_l - 2.0 * c_l
            return RiemannState(0.0, s, (s, 0.0, s))

        # Wet bed case - Newton iteration for h_star
        c_l = np.sqrt(self.g * h_l)
        c_r = np.sqrt(self.g * h_r)

        # Initial guess
        h_star = 0.5 * (h_l + h_r)

        for _ in range(self.max_iter):
            f_l, df_l = self._f(h_star, h_l, u_l)
            f_r, df_r = self._f(h_star, h_r, u_r)

            f_total = f_l + f_r + u_r - u_l
            df_total = df_l + df_r

            if abs(df_total) < 1e-14:
                break

            h_new = h_star - f_total / df_total

            if abs(h_new - h_star) < self.tol:
                h_star = h_new
                break

            h_star = max(h_new, self.tol)

        # Compute u_star
        f_l_final, _ = self._f(h_star, h_l, u_l)
        f_r_final, _ = self._f(h_star, h_r, u_r)
        u_star = 0.5 * (u_l + u_r) + 0.5 * (f_r_final - f_l_final)

        # Compute wave speeds
        if h_star > h_l:
            s_l = u_l - c_l * np.sqrt(
                0.5 * (h_star / h_l) * (1.0 + h_star / h_l)
            )
        else:
            s_l = u_l - c_l

        if h_star > h_r:
            s_r = u_r + c_r * np.sqrt(
                0.5 * (h_star / h_r) * (1.0 + h_star / h_r)
            )
        else:
            s_r = u_r + c_r

        s_star = u_star

        return RiemannState(h_star, u_star, (s_l, s_r, s_star))

    def sample_solution(
        self,
        h_l: float,
        u_l: float,
        h_r: float,
        u_r: float,
        x: NDArray[np.float64],
        t: float,
        x0: float = 0.0,
    ) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Sample exact solution at given points and time.

        Args:
            h_l: Left water depth [m]
            u_l: Left velocity [m/s]
            h_r: Right water depth [m]
            u_r: Right velocity [m/s]
            x: Spatial coordinates [m]
            t: Time [s]
            x0: Initial discontinuity position [m]

        Returns:
            Tuple of (h, u) arrays at each x position
        """
        if t <= 0:
            h = np.where(x < x0, h_l, h_r)
            u = np.where(x < x0, u_l, u_r)
            return h.astype(np.float64), u.astype(np.float64)

        state = self.solve(h_l, u_l, h_r, u_r)
        s_l, s_r, s_star = state.wave_speeds

        h = np.zeros_like(x, dtype=np.float64)
        u = np.zeros_like(x, dtype=np.float64)

        c_l = np.sqrt(self.g * h_l)
        c_r = np.sqrt(self.g * h_r)

        for i, xi in enumerate(x):
            s = (xi - x0) / t

            if s <= s_l:
                # Left state
                h[i] = h_l
                u[i] = u_l
            elif s >= s_r:
                # Right state
                h[i] = h_r
                u[i] = u_r
            elif s_star <= s and s <= s_r and h_r > 0:
                # Right rarefaction or shock
                if state.h > h_r:
                    # Shock
                    h[i] = state.h
                    u[i] = state.u
                else:
                    # Rarefaction
                    if s >= u_r + c_r:
                        h[i] = h_r
                        u[i] = u_r
                    else:
                        u_val = (u_r - 2.0 * c_r + 2.0 * s) / 3.0
                        c_val = (u_r + 2.0 * c_r - s) / 3.0
                        h[i] = c_val**2 / self.g
                        u[i] = u_val
            elif s_l <= s and s <= s_star and h_l > 0:
                # Left rarefaction or shock
                if state.h > h_l:
                    # Shock
                    h[i] = state.h
                    u[i] = state.u
                else:
                    # Rarefaction
                    if s <= u_l - c_l:
                        h[i] = h_l
                        u[i] = u_l
                    else:
                        u_val = (u_l + 2.0 * c_l + 2.0 * s) / 3.0
                        c_val = (-u_l + 2.0 * c_l + s) / 3.0
                        h[i] = c_val**2 / self.g
                        u[i] = u_val
            else:
                # Star region
                h[i] = state.h
                u[i] = state.u

        return h, u


class ExactRiemann:
    """Adapter class for frontend to compute exact Riemann solution.

    Provides the interface expected by frontend code:
    - Constructor takes DamBreakConfig
    - solve(config) returns the exact solution array
    """

    def __init__(self, config=None):
        """Initialize with optional config.

        Args:
            config: Optional DamBreakConfig object
        """
        self.config = config
        self.solver = ExactRiemannSolver()

    def solve(self, config=None):
        """Compute exact solution for the dam break problem.

        Args:
            config: DamBreakConfig object with simulation parameters

        Returns:
            NDArray[np.float64]: Array of shape (2, nx) containing h and u
        """
        if config is None:
            config = self.config

        if config is None:
            raise ValueError("No configuration provided")

        h_l = config.h_l
        u_l = config.u_l
        h_r = config.h_r
        u_r = config.u_r
        x = config.x
        t = config.t_end
        x0 = config.x_dam

        h, u = self.solver.sample_solution(h_l, u_l, h_r, u_r, x, t, x0)

        return np.vstack([h, u])
