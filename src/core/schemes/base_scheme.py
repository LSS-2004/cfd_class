"""Abstract base class for finite volume schemes.

Provides the template method pattern for all numerical schemes,
ensuring consistent structure and interface across implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable

import numpy as np
from numpy.typing import NDArray


class SimulationResult:
    """Container for simulation results.

    Attributes:
        t: Time array [s]
        h: Water depth history [m]
        u: Velocity history [m/s]
        snapshots: Dictionary of {time: (h, u)} for specific times
    """

    def __init__(
        self,
        t: NDArray[np.float64],
        h: NDArray[np.float64],
        u: NDArray[np.float64],
        snapshots: Optional[Dict[float, tuple]] = None,
    ):
        self.t = t
        self.h = h
        self.u = u
        self.snapshots = snapshots or {}


class BaseScheme(ABC):
    """Abstract base class for all FVM schemes.

    Defines the common interface that all numerical schemes must implement.
    Uses the Template Method pattern to enforce consistent structure.

    Attributes:
        name: Scheme name
        order: Spatial accuracy order
        g: Gravitational acceleration [m/s^2]
    """

    def __init__(self, name: str, order: int, g: float = 9.81):
        """Initialize scheme.

        Args:
            name: Scheme name
            order: Spatial accuracy order (1 or 2)
            g: Gravitational acceleration [m/s^2]
        """
        self.name = name
        self.order = order
        self.g = g

    @abstractmethod
    def compute_flux(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Compute numerical flux at cell interfaces.

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]

        Returns:
            Tuple of (mass_flux, momentum_flux) at interfaces
        """
        pass

    @abstractmethod
    def compute_time_step(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
        cfl: float,
        dx: float,
    ) -> float:
        """Compute adaptive time step based on CFL condition.

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]
            cfl: CFL stability number
            dx: Grid spacing [m]

        Returns:
            Time step [s]
        """
        pass

    def apply_boundary_conditions(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Apply transmissive boundary conditions.

        Args:
            h: Water depth array [m]
            u: Velocity array [m/s]

        Returns:
            Tuple of (h, u) with boundary conditions applied
        """
        h_bc = h.copy()
        u_bc = u.copy()

        # Transmissive (zero-gradient) boundaries
        if len(h) > 1:
            h_bc[0] = h[1]
            h_bc[-1] = h[-2]
            u_bc[0] = u[1]
            u_bc[-1] = u[-2]

        return h_bc, u_bc

    def advance(
        self,
        h: NDArray[np.float64],
        u: NDArray[np.float64],
        dt: float,
        dx: float,
    ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        """Advance solution by one time step.

        Template method that calls compute_flux and updates conserved variables.

        Args:
            h: Current water depth [m]
            u: Current velocity [m/s]
            dt: Time step [s]
            dx: Grid spacing [m]

        Returns:
            Tuple of (h_new, u_new) at next time level
        """
        # Compute fluxes
        mass_flux, mom_flux = self.compute_flux(h, u)

        # Update conserved variables
        h_new = h - dt / dx * (mass_flux[1:] - mass_flux[:-1])
        hu = h * u
        hu_new = hu - dt / dx * (mom_flux[1:] - mom_flux[:-1])

        # Positivity preservation
        eps_h = 1e-12
        h_new = np.maximum(h_new, eps_h)

        # Compute velocity
        u_new = np.where(h_new > eps_h, hu_new / h_new, 0.0)

        # Apply boundary conditions
        h_new, u_new = self.apply_boundary_conditions(h_new, u_new)

        return h_new, u_new

    def evolve(
        self,
        config: Any,
        progress_callback: Optional[Callable[[float, float], None]] = None,
    ) -> Dict[float, NDArray[np.float64]]:
        """Run full simulation using the configuration.

        Args:
            config: DamBreakConfig object with simulation parameters
            progress_callback: Optional callback for progress reporting

        Returns:
            Dictionary mapping time values to solution arrays
        """
        h0, u0 = config.initial_condition()
        dx = config.dx
        
        result = self.run_simulation(
            h0=h0,
            u0=u0,
            cfl=config.cfl,
            dx=dx,
            t_end=config.t_end,
            progress_callback=lambda p: progress_callback(p, config.t_end) if progress_callback else None,
        )
        
        output = {}
        for i, t in enumerate(result.t):
            h = result.h[i]
            u = result.u[i]
            output[round(float(t), 6)] = np.vstack([h, u])
        
        return output

    def run_simulation(
        self,
        h0: NDArray[np.float64],
        u0: NDArray[np.float64],
        cfl: float,
        dx: float,
        t_end: float,
        progress_callback: Optional[Callable[[float], None]] = None,
        snapshot_times: Optional[list] = None,
    ) -> SimulationResult:
        """Run full simulation from t=0 to t=t_end.

        Args:
            h0: Initial water depth [m]
            u0: Initial velocity [m/s]
            cfl: CFL stability number
            dx: Grid spacing [m]
            t_end: End time [s]
            progress_callback: Optional callback(t) for progress reporting
            snapshot_times: Optional list of times to save snapshots

        Returns:
            SimulationResult with full time history
        """
        h = h0.copy()
        u = u0.copy()
        t = 0.0

        # Storage
        t_history = [t]
        h_history = [h.copy()]
        u_history = [u.copy()]
        snapshots = {}

        if snapshot_times:
            snapshot_times = sorted(snapshot_times)
            next_snapshot_idx = 0

        while t < t_end:
            # Compute time step
            dt = self.compute_time_step(h, u, cfl, dx)

            # Don't overshoot t_end
            if t + dt > t_end:
                dt = t_end - t

            # Advance
            h, u = self.advance(h, u, dt, dx)
            t += dt

            # Store
            t_history.append(t)
            h_history.append(h.copy())
            u_history.append(u.copy())

            # Save snapshots
            if snapshot_times and next_snapshot_idx < len(snapshot_times):
                if t >= snapshot_times[next_snapshot_idx]:
                    st = snapshot_times[next_snapshot_idx]
                    snapshots[st] = (h.copy(), u.copy())
                    next_snapshot_idx += 1

            # Progress callback
            if progress_callback:
                progress_callback(t / t_end)

        return SimulationResult(
            t=np.array(t_history, dtype=np.float64),
            h=np.array(h_history, dtype=np.float64),
            u=np.array(u_history, dtype=np.float64),
            snapshots=snapshots,
        )
