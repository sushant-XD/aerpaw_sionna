from typing import Dict, List, Optional, Tuple

from sionna_wrapper import Sionna

engine = Sionna()


def initialize(scene_path: Optional[str] = None) -> None:
    engine.load_simulation_scene(scene_path)


def shutdown() -> None:
    engine.reset()


def get_scene_info() -> Dict:
    return engine.get_scene_info()


def reset_scene() -> None:
    engine.reset()


def add_transmitter(
    name: str,
    position: Tuple[float, float, float],
    orientation: Optional[Tuple[float, float, float]] = None,
) -> Dict:
    """Add a transmitter to the scene."""
    engine.add_transmitter(name, position, orientation)
    return {"name": name, "position": position}


def update_transmitter_position(
    name: str, position: Tuple[float, float, float]
) -> Dict:
    engine.update_transmitter_position(name, position)
    return {"name": name, "position": position}


def get_transmitters() -> List[str]:
    return list(engine.transmitters.keys())


def add_receiver(
    name: str,
    position: Tuple[float, float, float],
    orientation: Optional[Tuple[float, float, float]] = None,
) -> Dict:
    """Add a receiver to the scene."""
    engine.add_receiver(name, position, orientation)
    return {"name": name, "position": position}


def update_receiver_position(name: str, position: Tuple[float, float, float]) -> Dict:
    engine.update_receiver_position(name, position)
    return {"name": name, "position": position}


def get_receivers() -> List[str]:
    return list(engine.receivers.keys())


def compute_paths(max_depth: int = 3) -> Dict:
    return engine.compute_paths(max_depth)


def get_cir() -> Dict:
    return engine.get_channel_impulse_response()
