# update parameters
# transmitter/receiver position
# post the movement of vehicle in a scene
# CIR at every step (endgoal)


from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

import main
from schemas import *

# 1. Global variable to hold our controller
sim_controller = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Sionna simulation...")
    main.initialize()
    yield
    print("Shutting down...")
    main.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/scene", response_model=SceneInfoResponse)
def get_scene():
    try:
        return main.get_scene_info()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scene/reset")
def reset_scene():
    try:
        main.reset_scene()
        return {"message": "scene reset"}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transmitters", response_model=DeviceResponse)
def add_tx(device: DeviceCreate):
    try:
        main.add_transmitter(device.name, device.position.to_tuple())
        return DeviceResponse(name=device.name, position=device.position)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/transmitters", response_model=List[DeviceResponse])
def list_tx():
    try:
        return main.get_transmitters()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/transmitters/{name}", response_model=DeviceResponse)
def update_tx(name: str, update_data: DeviceUpdate):
    try:
        main.update_transmitter_position(name, update_data.position.to_tuple())
        return DeviceResponse(name=name, position=update_data.position)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/receivers", response_model=DeviceResponse)
def add_rx(device: DeviceCreate):
    try:
        return main.add_receiver(device.name, device.position.to_tuple())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/receivers", response_model=List[DeviceResponse])
def list_rx():
    try:
        return main.get_receivers()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/receivers/{name}", response_model=DeviceResponse)
def update_rx(name: str, update_data: DeviceUpdate):
    try:
        return main.update_receiver_position(name, update_data.position.to_tuple())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/simulation/paths")
def compute_paths(params: PathComputationRequest):
    try:
        return main.compute_paths(params.max_depth)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/simulation/cir", response_model=CirResponse, tags=["Simulation"])
def get_cir():
    """
    Retrieve the Channel Impulse Response (CIR) for the current step.
    """
    try:
        return simulation_engine.get_cir()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
