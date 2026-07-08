Overview





from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
app = FastAPI()
# Enable cross-origin resource sharing so Vite can call your backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryPayload(BaseModel):
    text: str
    agent: str
import subprocess
import asyncio
import threading
# --- REACHY ROBOT SETUP ---
try:
    from reachy_mini import ReachyMini
    HAS_REACHY = True
except ImportError:
    HAS_REACHY = False
    print("WARNING: reachy_mini not installed.")
mini_robot = None
daemon_process = None
async def maintain_robot_connection():
    global mini_robot, daemon_process
    while True:
        # 1. Ensure daemon is running
        if daemon_process is None or daemon_process.poll() is not None:
            print("[AUTO-CONNECT] Starting reachy-mini-daemon...")
            try:
                daemon_process = subprocess.Popen(["reachy-mini-daemon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"[AUTO-CONNECT] Failed to start daemon: {e}")
        
        # 2. Try to connect if not connected
        if HAS_REACHY and not mini_robot:
            try:
                temp_robot = ReachyMini()
                # Wiggle antennas to show it woke up automatically
                temp_robot.goto_target(antennas=[0.5, -0.5], duration=0.5)
                mini_robot = temp_robot
                print("[AUTO-CONNECT] Successfully connected and woke up Maggie!")
            except Exception:
                # Normal if robot isn't plugged in yet or still booting
                mini_robot = None
                
        await asyncio.sleep(5) # poll every 5 seconds
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(maintain_robot_connection())
@app.post("/api/robot/connect")
def connect_robot():
    global mini_robot
    if not HAS_REACHY:
        return {"status": "error", "message": "reachy_mini Python package not found."}
    
    try:
        if not mini_robot:
            mini_robot = ReachyMini()
        
        # Wiggle antennas to show connection success
        mini_robot.goto_target(antennas=[0.5, -0.5], duration=0.5)
        
        return {"status": "success", "message": "Connected to Reachy Mini"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
@app.post("/api/robot/disconnect")
def disconnect_robot():
    global mini_robot
    if not mini_robot:
        return {"status": "error", "message": "Robot is not connected."}
    try:
        mini_robot.turn_off() # This makes all motors compliant/limp
        return {"status": "success", "message": "Maggie has been turned off."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
# --------------------------
@app.post("/api/agent/listen")
def handle_hardware_listen():
    try:
        # 1. Animate Maggie's antennas / head via reachy_mini library to signify listening state
        # example: robot.head.look_at(x=1, y=0, z=0)
        
        # 2. Capture voice sample and parse with Whisper engine
        simulated_text = "Where is the main campus IT service desk located?"
        
        return {
            "status": "success",
            "transcription": simulated_text,
            "next_step": "WIKI_LOOKUP_AGENT"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/api/agent/query")
def handle_agent_routing(payload: QueryPayload):
    print(f"Executing payload routing for: {payload.text} using {payload.agent}")
    
    # Run the corresponding sub-agent process
    if payload.agent == "WIKI_LOOKUP_AGENT":
        response_msg = "The main IT desk is on the second floor of the Murdock Library."
    else:
        response_msg = "Task routed successfully."
        
    return {"status": "complete", "output": response_msg}
