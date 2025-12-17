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
    def __init__(self, scene_path=None):
        self.scene_path = scene_path if scene_path else sionna.rt.scene.munich
        self.scene = None
        self.tx = None
        self.rx = None

    def load_simulation_scene(self):
        try:
            self.scene = load_scene(self.scene_path)
            print(f"Successfully loaded scene: {self.scene_path}")
            print(f"Objects in scene: {len(self.scene.objects)}")
            return self.scene
        except Exception as e:
            print(f"Error loading scene: {e}")
            return None

    def display_info(self):
        if self.scene:
            for name, obj in self.scene.objects.items():
                print(f"Object: {name}")
        else:
            print("No scene loaded yet.")

    def get_object_count(self):
        if self.scene and hasattr(self.scene, "objects"):
            return len(self.scene.objects)
        return 0
