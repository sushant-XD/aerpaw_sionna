from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Position(BaseModel):
    x: float
    y: float
    z: float

    def to_tuple(self):
        return (self.x, self.y, self.z)


class DeviceCreate(BaseModel):
    name: str = Field(..., description="Unique identifier for the device")
    position: Position


class DeviceUpdate(BaseModel):
    position: Position


class DeviceResponse(BaseModel):
    name: str
    position: Position


class PathComputationRequest(BaseModel):
    max_depth: int = Field(
        3, ge=1, le=10, description="Maximum number of reflections/diffractions"
    )
    diffraction: bool = True
    scattering: bool = False


class CirResponse(BaseModel):
    # This structure depends on what main.get_cir() returns,
    # but generally CIR contains delays and complex gains.
    # Assuming a simplified dictionary return for now.
    timestamp: float
    paths: List[Dict[str, Any]]


class SceneInfoResponse(BaseModel):
    object_count: int
    objects: List[str]
    transmitter_count: int
    receiver_count: int
