Overview





import asyncio
import logging
import cv2
try:
    from reachy_mini import ReachyMini
    from reachy_mini.utils import create_head_pose
    HAS_REACHY = True
except ImportError:
    HAS_REACHY = False
    logging.warning("reachy_mini package not found. Using mock fallback.")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class ReachyController:
    """Implementation of the Reachy Mini SDK for the Lite USB version."""
    def __init__(self):
        self.connected = False
        self.is_listening = False
        self.mini = None
    def _ensure_connected(self):
        if not self.mini and HAS_REACHY:
            try:
                # This connects to the daemon running on localhost (USB connection to Lite)
                self.mini = ReachyMini()
                self.connected = True
                logger.info("[REACHY] Connected successfully to physical robot.")
                
                # Automatically wiggle antennas to show connection success
                self.mini.goto_target(antennas=[0.5, -0.5], duration=0.5)
                return True
            except Exception as e:
                logger.error(f"[REACHY] Failed to connect to robot: {e}")
                return False
        return self.connected
    async def connect_robot(self):
        """Manually trigger connection from UI."""
        return self._ensure_connected()
    async def wake_word_detected(self):
        """Simulates the wake word 'Maggie' being detected."""
        logger.info("[WAKEWORD] Detected 'Maggie'. Animating antennas.")
        await self.animate_antennas("happy")
        self.is_listening = True
    async def animate_antennas(self, emotion: str):
        logger.info(f"[REACHY] Moving antennas to express: {emotion}")
        self._ensure_connected()
        if self.mini:
            # Example animation: wiggle antennas
            self.mini.goto_target(antennas=[0.6, -0.6], duration=0.3)
        await asyncio.sleep(0.5)
    async def look_at_user(self):
        logger.info("[REACHY] Directing 6-DOF head towards user.")
        self._ensure_connected()
        if self.mini:
            # Point head up/forward to look at user
            self.mini.goto_target(head=create_head_pose(z=15, degrees=True), duration=0.5)
        await asyncio.sleep(1)
        
    async def capture_photo(self) -> str:
        logger.info("[REACHY] Capturing high-resolution photo from wide-angle camera.")
        await self.look_at_user()
        
        self._ensure_connected()
        if self.mini:
            # Use robot camera frame
            # frame = self.mini.cameras.main.last_frame
            # cv2.imwrite("mock_photo_data.jpg", frame)
            pass
            
        await asyncio.sleep(1)
        return "mock_photo_data.jpg"
    async def speak(self, text: str):
        logger.info(f"[REACHY] Speaking via 5W speaker: {text}")
        # Add TTS integration here if sending directly to Reachy speakers
        await asyncio.sleep(1)
    def turn_off(self):
        """Turn off Maggie's motors (compliant mode)."""
        logger.info("[REACHY] Turning off motors to compliant state.")
        self._ensure_connected()
        if self.mini:
            self.mini.turn_off()
            
    def get_video_frame(self):
        """Fetch the latest camera frame and encode as JPEG."""
        if not self._ensure_connected() or not self.mini:
            return None
        try:
            # Reachy Mini Lite exposes main camera frames
            frame = self.mini.cameras.main.last_frame
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    return buffer.tobytes()
        except Exception as e:
            logger.error(f"[REACHY] Error capturing video frame: {e}")
        return None
reachy = ReachyController()
