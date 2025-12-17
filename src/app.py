# update parameters
# transmitter/receiver position
# post the movement of vehicle in a scene
# CIR at every step (endgoal)


from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from sionna_wrapper import Sionna

# 1. Global variable to hold our controller
sim_controller = None


# 2. Lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    global sim_controller
    print("Initializing Sionna Scene...")
    sim_controller = Sionna()
    sim_controller.load_simulation_scene()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


# 3. Endpoints
@app.get("/")
def read_root():
    return {"status": "Sionna API is running"}


@app.get("/scene/info")
def get_scene_info():
    if not sim_controller.scene:
        raise HTTPException(status_code=500, detail="Scene not loaded")

    return {
        "scene_path": sim_controller.scene_path,
        "object_count": sim_controller.get_object_count(),
        "objects": list(sim_controller.scene.objects.keys()),
    }


@app.post("/simulation/reset")
def reset_scene():
    sim_controller.load_simulation_scene()
    return {"message": "Scene reloaded successfully"}
