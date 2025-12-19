from typing import Dict, List, Optional, Tuple

from sionna_wrapper import Sionna
from utils import AntennaType

engine = Sionna()


def initialize(scene_path: Optional[str] = None) -> None:
    """Initialize the simulation engine with a scene."""
    engine.load_simulation_scene(scene_path)


def shutdown() -> None:
    """Shutdown and clean up the simulation engine."""
    engine.reset()


def get_scene_info() -> Dict:
    """Get information about the current scene."""
    return engine.get_scene_info()


def reset_scene() -> None:
    """Reset the scene to initial state."""
    engine.reset()


def add_transmitter(
    name: str,
    position: Tuple[float, float, float],
    orientation: Optional[Tuple[float, float, float]] = None,
) -> Dict:
    """Add a transmitter to the scene."""
    engine.add_transmitter(name, position, orientation)
    result = {"name": name, "position": position}
    if orientation:
        result["orientation"] = orientation
    return result


def update_transmitter_position(
    name: str, position: Tuple[float, float, float]
) -> Dict:
    """Update the position of an existing transmitter."""
    engine.update_ant_position(AntennaType.Receiver, name, position)
    return {"name": name, "position": position}


def get_transmitters() -> List[str]:
    """Get list of all transmitter names."""
    return list(engine.transmitters.keys())


def add_receiver(
    name: str,
    position: Tuple[float, float, float],
    orientation: Optional[Tuple[float, float, float]] = None,
) -> Dict:
    """Add a receiver to the scene."""
    engine.add_receiver(name, position, orientation)
    result = {"name": name, "position": position}
    if orientation:
        result["orientation"] = orientation
    return result


def update_receiver_position(name: str, position: Tuple[float, float, float]) -> Dict:
    """Update the position of an existing receiver."""
    engine.update_ant_position(AntennaType.Transmitter, name, position)
    return {"name": name, "position": position}


def get_receivers() -> List[str]:
    """Get list of all receiver names."""
    return list(engine.receivers.keys())


def set_array(
    ant_type: str,
    num_rows_cols: Tuple[int, int],
    vertical_horizontal_spacing: Tuple[float, float],
    pattern: str,
    polarization: str,
) -> Dict:
    """
    Set antenna array configuration for transmitter or receiver.

    Args:
        ant_type: Antenna type ('tx' or 'rx')
        num_rows_cols: Tuple of (num_rows, num_cols)
        vertical_horizontal_spacing: Tuple of (vertical_spacing, horizontal_spacing)
        pattern: Radiation pattern ('iso', 'dipole', or 'tr38901')
        polarization: Polarization type ('V', 'H', or 'cross')

    Returns:
        Dictionary with array configuration details
    """
    # Convert string to enum
    try:
        antenna_enum = AntennaType(ant_type)
    except ValueError:
        raise ValueError(f"Invalid antenna type: {ant_type}. Must be 'tx' or 'rx'")

    # Validate pattern
    try:
        RadiationPattern(pattern)
    except ValueError:
        raise ValueError(
            f"Invalid pattern: {pattern}. Must be 'iso', 'dipole', or 'tr38901'"
        )

    # Validate polarization
    try:
        PolarizationType(polarization)
    except ValueError:
        raise ValueError(
            f"Invalid polarization: {polarization}. Must be 'V', 'H', or 'cross'"
        )

    num_rows, num_cols = num_rows_cols
    vertical_spacing, horizontal_spacing = vertical_horizontal_spacing

    engine.set_array(
        antenna_enum,
        num_rows,
        num_cols,
        vertical_spacing,
        horizontal_spacing,
        pattern,
        polarization,
    )

    return {
        "antenna_type": ant_type,
        "num_rows": num_rows,
        "num_cols": num_cols,
        "vertical_spacing": vertical_spacing,
        "horizontal_spacing": horizontal_spacing,
        "pattern": pattern,
        "polarization": polarization,
    }


def compute_paths(max_depth: int = 3) -> Dict:
    """Compute propagation paths between transmitters and receivers."""
    return engine.compute_paths(max_depth)


def get_cir() -> Dict:
    """Get the Channel Impulse Response."""
    return engine.get_channel_impulse_response()
