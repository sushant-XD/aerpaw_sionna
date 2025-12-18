from typing import Dict, Optional, Tuple

try:
    import sionna.rt
except ImportError as e:
    import os

    os.system("pip install sionna-rt")
    import sionna.rt

# Other imports
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

no_preview = True  # Toggle to False to use the preview widget

# Import relevant components from Sionna RT
from sionna.rt import (
    Camera,
    PathSolver,
    PlanarArray,
    RadioMapSolver,
    Receiver,
    Transmitter,
    load_scene,
    subcarrier_frequencies,
)


class Sionna:
    def __init__(self):
        self.scene = None
        self.transmitters: Dict[str, sionna.rt.Transmitter] = {}
        self.receivers: Dict[str, sionna.rt.Receiver] = {}
        self._path_solver = None

    def load_simulation_scene(self, scene_path: Optional[str] = None):
        try:
            if scene_path is None:
                self.scene = load_scene(sionna.rt.scene.munich)
            else:
                self.scene = load_scene(scene_path)

            print(f"Successfully loaded scene: {scene_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load scene: {e}")

    def get_scene_info(self):
        if not self.scene:
            raise RuntimeError("No scene loaded")
        return {
            "object_count": len(self.scene.objects),
            "objects": list(self.scene.objects.keys()),
            "transmitter_count": len(self.transmitters),
            "receiver_count": len(self.receivers),
        }

    def add_transmitter(
        self,
        name: str,
        position: Tuple[float, float, float],
        orientation: Optional[Tuple[float, float, float]] = None,
    ) -> None:
        if not self.scene:
            raise RuntimeError("Scene not loaded")

        tx = sionna.rt.Transmitter(name=name, position=position)
        if orientation:
            tx.orientation = orientation

        self.scene.add(tx)
        self.transmitters[name] = tx

    def add_receiver(
        self,
        name: str,
        position: Tuple[float, float, float],
        orientation: Optional[Tuple[float, float, float]] = None,
    ) -> None:
        """Add a receiver to the scene."""
        if not self.scene:
            raise RuntimeError("Scene not loaded")

        rx = sionna.rt.Receiver(name=name, position=position)
        if orientation:
            rx.orientation = orientation

        self.scene.add(rx)
        self.receivers[name] = rx

    def update_transmitter_position(
        self, name: str, position: Tuple[float, float, float]
    ) -> None:
        """Update transmitter position."""
        if name not in self.transmitters:
            raise ValueError(f"Transmitter '{name}' not found")

        self.transmitters[name].position = position

    def update_receiver_position(
        self, name: str, position: Tuple[float, float, float]
    ) -> None:
        """Update receiver position."""
        if name not in self.receivers:
            raise ValueError(f"Receiver '{name}' not found")

        self.receivers[name].position = position

    def compute_paths(self, max_depth: int = 3) -> Dict:
        """Compute propagation paths between transmitters and receivers."""
        if not self.scene:
            raise RuntimeError("Scene not loaded")

        if not self.transmitters or not self.receivers:
            raise RuntimeError("No transmitters or receivers in scene")

        # Initialize path solver
        self._path_solver = sionna.rt.PathSolver(self.scene, solver="fibonacci")

        # Compute paths
        paths = self._path_solver.compute_paths(max_depth=max_depth)

        return {
            "path_count": len(paths.vertices),
            "max_depth": max_depth,
        }

    def get_channel_impulse_response(self) -> Dict:
        """Compute and return Channel Impulse Response (CIR)."""
        if not self._path_solver:
            raise RuntimeError("Paths not computed. Call compute_paths() first")

        # Get CIR from path solver
        paths = self._path_solver.compute_paths()

        return {
            "delays": paths.delays.numpy().tolist() if hasattr(paths, "delays") else [],
            "gains": paths.gains.numpy().tolist() if hasattr(paths, "gains") else [],
        }

    def reset(self) -> None:
        """Reset the simulation state."""
        self.transmitters.clear()
        self.receivers.clear()
        self._path_solver = None
