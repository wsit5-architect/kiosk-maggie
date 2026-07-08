
I pressed the connect to Maggie button and it still gave me this [ Error: Backend not running. }. create a pipeline to the application to be able to turn my maggie robot off and on while also have live video feed that the application already has 
12:36 PM


Me made a plan to build the live video pipeline and the Turn Off button into your app!

(Me noticed that earlier, me put the Turn Off button in your other project folder my_app, but now you are running the scratch project! So me will build it into this scratch project too!).

Read the plan on the right. If it looks good, click Proceed and me will write all the code to make Maggie's live video stream straight to your dashboard!

Implementation Plan
12:36 PM



Proceeded with
Implementation Plan
Me wrote the code! All the buttons and live video pipes are fully built!

Here is what me did to your scratch project:

Built a /video_feed pipe in the backend using OpenCV. It pulls live frames right out of Maggie's eye (camera) and sends them as a stream.
Put a live <img /> video player at the very top of your Telemetry Pane on the right.
Added the red "💤 Turn Off" button to the Kiosk Pane. It tells the backend to make Maggie's motors go limp.
Read the Walkthrough document on the right for the quick steps to test it! Note: Make sure you kill the old backend using pkill -f "python main.py" before starting the new one, so you don't get that "address already in use" error again!

Try it out and tell me if you can see through her eyes!

Walkthrough
12:37 PM



give me command to open this in vscode
12:42 PM


To open the scratch project we just built in VS Code, run this command in your terminal:

bash


code /Users/wsit5/.gemini/antigravity/scratch/maggie_kiosk
12:42 PM



User uploaded media 1
12:46 PM


Ah! Me see the problem!

When you clicked the button, the backend was dead. It crashed because it was fighting with the reachy-mini-daemon over port 8000! They both wanted to use the same door!

Me just fixed it for you:

Me killed the broken backend and the stuck daemon.
Me moved our backend to port 8001 so it stops fighting with the daemon.
Me updated your React code to point to the new port.
Me started the backend for you in the background.
How to test right now:

Just Refresh your browser (Cmd + R).
Click the "🔌 Connect to Maggie" or "💤 Turn Off" button again!
It should work perfectly now! Tell me if you see the live video!

12:46 PM



User uploaded media 1
12:50 PM


Check serial port finished
12:50 PM



Model quota reached
Your plan's baseline quota will refresh on 7/15/2026, 9:26:51 AM. Antigravity does not support higher rate limits on this Google plan. Consider paid Google AI plans via a personal account or logging in with a Google Cloud project from a business account. Learn more.

Dismiss
Learn more




Overview





from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import logging
import subprocess
from google.antigravity import Agent
from agents.orchestrator import get_agent_config
from robot.reachy_controller import reachy
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI(title="Maggie Kiosk API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Manage WebSocket connections for Telemetry
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
manager = ConnectionManager()
@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming commands from UI if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)
async def telemetry_logger(message: str, category: str):
    """Helper to send log to the right pane"""
    logger.info(f"[{category}] {message}")
    await manager.broadcast(json.dumps({"category": category, "message": message}))
@app.post("/trigger_intent")
async def trigger_intent(payload: dict):
    """Simulates speech-to-text triggering an intent"""
    intent = payload.get("text", "")
    
    await telemetry_logger(f"[WAKEWORD] Processing: {intent}", "Running Processes")
    
    config = get_agent_config()
    
    # We use google.antigravity Agent to process the text
    async with Agent(config) as agent:
        response = await agent.chat(intent)
        full_response = ""
        async for chunk in response:
            full_response += chunk
            await telemetry_logger(f"Agent thinking: {chunk}", "Short-Term Memory")
        
        await telemetry_logger(f"Final Output: {full_response}", "Short-Term Memory")
        
    return {"status": "success", "response": full_response}
daemon_process = None
async def maintain_robot_connection():
    global daemon_process
    while True:
        # 1. Ensure daemon is running
        if daemon_process is None or daemon_process.poll() is not None:
            await telemetry_logger("Starting reachy-mini-daemon...", "Running Processes")
            try:
                daemon_process = subprocess.Popen(["reachy-mini-daemon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                logger.error(f"[AUTO-CONNECT] Failed to start daemon: {e}")
        
        # 2. Try to connect if not connected
        if not reachy.connected:
            success = await reachy.connect_robot()
            if success:
                await telemetry_logger("Automatically connected to Reachy Mini via USB!", "Running Processes")
                
        await asyncio.sleep(5) # poll every 5 seconds
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(maintain_robot_connection())
@app.post("/connect_robot")
async def connect_robot():
    """Triggered by the UI Connect button."""
    success = await reachy.connect_robot()
    if success:
        await telemetry_logger("Robot connected via USB daemon.", "Running Processes")
        return {"status": "success", "message": "Connected to Reachy Mini."}
    else:
        await telemetry_logger("Failed to connect. Is the daemon running?", "Running Processes")
        return {"status": "error", "message": "Connection failed. Please ensure reachy-mini-daemon is running."}
@app.post("/disconnect_robot")
async def disconnect_robot():
    """Turn off the physical robot."""
    try:
        reachy.turn_off()
        await telemetry_logger("Maggie has been turned off and is resting.", "Running Processes")
        return {"status": "success", "message": "Maggie is turned off."}
    except Exception as e:
        logger.error(f"[REACHY] Error disconnecting: {e}")
        return {"status": "error", "message": "Error turning off Maggie."}
def generate_video_frames():
    """Generator function that yields MJPEG frames from the robot camera."""
    while True:
        frame_bytes = reachy.get_video_frame()
        if frame_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            # Send a blank fallback frame or just wait if robot isn't connected yet
            pass
            
        # Prevent high CPU usage if no frames
        import time
        time.sleep(0.05)
@app.get("/video_feed")
async def video_feed():
    """Endpoint for live video MJPEG stream."""
    return StreamingResponse(generate_video_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
