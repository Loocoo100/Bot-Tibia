import os
import asyncio
import threading
import time
import random
import uuid
import json
import numpy as np
from PIL import Image, ImageDraw
import psutil
import websockets

# Mock GUI libraries for headless environment
class MockPyAutoGUI:
    FAILSAFE = False
    PAUSE = 0.01
    
    def screenshot(self):
        # Return a mock PIL image
        return Image.new('RGB', (1920, 1080), color='black')
    
    def position(self):
        return (500, 500)
    
    def moveTo(self, x, y):
        pass
    
    def click(self):
        pass
    
    def rightClick(self):
        pass
    
    def press(self, key):
        pass
    
    def hotkey(self, *keys):
        pass
    
    def mouseDown(self):
        pass
    
    def mouseUp(self):
        pass

class MockPyTesseract:
    def image_to_string(self, image, config=''):
        return "100/100"  # Mock HP/MP text

class MockCV2:
    COLOR_RGB2BGR = 4
    COLOR_BGR2GRAY = 6
    
    def cvtColor(self, img, code):
        return np.zeros((100, 100), dtype=np.uint8)

class MockPynput:
    class mouse:
        Button = type('Button', (), {'left': 1, 'right': 2})()
        Listener = lambda **kwargs: None
    
    class keyboard:
        Key = type('Key', (), {'space': 'space', 'ctrl': 'ctrl'})()
        Listener = lambda **kwargs: None

# Use mocks
pyautogui = MockPyAutoGUI()
pytesseract = MockPyTesseract()
cv2 = MockCV2()
mouse = MockPynput.mouse
keyboard = MockPynput.keyboard

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
from scipy import interpolate
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'otbot_database')

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Initialize FastAPI
app = FastAPI(title="OT Bot Indetectável", version="1.0.0")
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Disable pyautogui fail-safe for seamless operation
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.01  # Minimal pause between actions

# Pydantic models
class BotConfig(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    auto_heal: bool = True
    auto_food: bool = True
    auto_attack: bool = True
    auto_walk: bool = False
    auto_loot: bool = True
    heal_spell: str = "exura"
    heal_at_hp: int = 70
    heal_mana_spell: str = "exura gran"
    heal_at_mp: int = 50
    attack_spell: str = "exori"
    food_type: str = "ham"
    food_at: int = 90
    waypoints: List[Dict[str, Any]] = []
    waypoint_mode: str = "loop"  # loop, back_and_forth, once
    waypoint_delay: int = 1000  # milliseconds between waypoints
    target_creatures: List[str] = ["rat", "rotworm", "cyclops"]
    loot_items: List[str] = ["gold coin", "platinum coin", "crystal coin"]
    discard_items: List[str] = ["leather armor", "studded armor", "chain armor"]
    loot_all_and_filter: bool = True  # True for free acc, False for premium
    loot_range: int = 3  # Squares from player
    anti_idle: bool = True
    emergency_logout_hp: int = 10
    enabled: bool = False

class BotStats(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    exp_gained: int = 0
    time_running: int = 0
    heals_used: int = 0
    food_used: int = 0
    attacks_made: int = 0
    creatures_killed: int = 0
    items_looted: int = 0
    items_discarded: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Waypoint(BaseModel):
    name: str
    x: int
    y: int
    description: Optional[str] = ""

# Global bot instance
class TibiaBot:
    def __init__(self):
        self.config = None
        self.is_running = False
        self.is_paused = False
        self.session_id = str(uuid.uuid4())
        self.stats = BotStats(session_id=self.session_id, created_at=datetime.utcnow())
        self.game_window = None
        self.screen_capture = None
        self.last_action_time = 0
        self.websocket_connections = set()
        
        # Anti-detection variables
        self.human_delays = {
            'min_action_delay': 0.1,
            'max_action_delay': 0.8,
            'typing_delay': (0.05, 0.15),
            'mouse_move_duration': (0.3, 1.2),
            'micro_pause_chance': 0.15,
            'micro_pause_duration': (0.05, 0.3)
        }
        
        self.last_positions = []
        self.action_patterns = []
        
    async def broadcast_stats(self):
        """Broadcast current stats to all connected websockets"""
        if self.websocket_connections:
            stats_data = {
                "type": "stats_update",
                "data": {
                    "session_id": self.stats.session_id,
                    "exp_gained": self.stats.exp_gained,
                    "time_running": self.stats.time_running,
                    "heals_used": self.stats.heals_used,
                    "food_used": self.stats.food_used,
                    "attacks_made": self.stats.attacks_made,
                    "creatures_killed": self.stats.creatures_killed,
                    "items_looted": self.stats.items_looted,
                    "items_discarded": self.stats.items_discarded,
                    "is_running": self.is_running,
                    "is_paused": self.is_paused
                }
            }
            
            disconnected = set()
            for websocket in self.websocket_connections:
                try:
                    await websocket.send_text(json.dumps(stats_data))
                except:
                    disconnected.add(websocket)
            
            # Remove disconnected websockets
            self.websocket_connections -= disconnected
    
    def find_tibia_window(self):
        """Find Tibia game window"""
        try:
            # Get all windows
            for proc in psutil.process_iter(['pid', 'name']):
                if 'tibia' in proc.info['name'].lower() or 'otclient' in proc.info['name'].lower():
                    return proc.info['pid']
        except:
            pass
        return None
    
    def human_delay(self, min_delay=None, max_delay=None):
        """Generate human-like delay with micro-pauses"""
        if min_delay is None:
            min_delay = self.human_delays['min_action_delay']
        if max_delay is None:
            max_delay = self.human_delays['max_action_delay']
        
        # Base delay
        delay = random.uniform(min_delay, max_delay)
        
        # Add micro-pause chance
        if random.random() < self.human_delays['micro_pause_chance']:
            micro_pause = random.uniform(*self.human_delays['micro_pause_duration'])
            delay += micro_pause
        
        time.sleep(delay)
    
    def bezier_mouse_move(self, start_pos, end_pos, duration=None):
        """Move mouse using Bezier curve for natural movement"""
        if duration is None:
            duration = random.uniform(*self.human_delays['mouse_move_duration'])
        
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Create control points for Bezier curve
        control_x = random.uniform(min(x1, x2), max(x1, x2))
        control_y = random.uniform(min(y1, y2), max(y1, y2))
        
        # Generate points along Bezier curve
        steps = int(duration * 60)  # 60 steps per second
        for i in range(steps + 1):
            t = i / steps
            
            # Bezier curve formula
            x = (1-t)**2 * x1 + 2*(1-t)*t * control_x + t**2 * x2
            y = (1-t)**2 * y1 + 2*(1-t)*t * control_y + t**2 * y2
            
            pyautogui.moveTo(int(x), int(y))
            time.sleep(duration / steps)
    
    def capture_game_area(self):
        """Capture game screen area"""
        try:
            screenshot = pyautogui.screenshot()
            # Convert to OpenCV format
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
        except Exception as e:
            logger.error(f"Error capturing screen: {e}")
            return None
    
    def detect_hp_mp(self, screenshot):
        """Detect HP and MP using OCR"""
        try:
            # Simulate HP/MP detection
            hp_current = random.randint(50, 100)
            hp_max = 100
            mp_current = random.randint(30, 100)  
            mp_max = 100
            
            return {
                'hp_current': hp_current,
                'hp_max': hp_max,
                'hp_percent': (hp_current / hp_max) * 100 if hp_max > 0 else 100,
                'mp_current': mp_current,
                'mp_max': mp_max,
                'mp_percent': (mp_current / mp_max) * 100 if mp_max > 0 else 100
            }
        except Exception as e:
            logger.error(f"Error detecting HP/MP: {e}")
            return {'hp_percent': 100, 'mp_percent': 100}
    
    def detect_creatures(self, screenshot):
        """Detect creatures on screen"""
        creatures = []
        try:
            # Simulate creature detection
            for creature_name in self.config.target_creatures:
                if random.random() < 0.3:  # 30% chance to find creature
                    x = random.randint(300, 700)
                    y = random.randint(200, 500)
                    creatures.append({
                        'name': creature_name,
                        'x': x,
                        'y': y,
                        'distance': random.randint(1, 5)
                    })
        except Exception as e:
            logger.error(f"Error detecting creatures: {e}")
        
        return creatures
    
    def cast_healing_spell(self):
        """Cast healing spell with human-like behavior"""
        try:
            self.human_delay(0.1, 0.3)
            
            # Type healing spell
            for char in self.config.heal_spell:
                pyautogui.press(char)
                time.sleep(random.uniform(*self.human_delays['typing_delay']))
            
            pyautogui.press('enter')
            self.stats.heals_used += 1
            
            logger.info(f"Cast healing spell: {self.config.heal_spell}")
            
        except Exception as e:
            logger.error(f"Error casting healing spell: {e}")
    
    def use_food(self):
        """Use food with human-like behavior"""
        try:
            self.human_delay(0.2, 0.5)
            self.stats.food_used += 1
            logger.info("Used food")
        except Exception as e:
            logger.error(f"Error using food: {e}")
    
    def attack_creature(self, creature):
        """Attack a detected creature"""
        try:
            self.human_delay(0.2, 0.5)
            self.stats.attacks_made += 1
            
            # Chance to kill creature
            if random.random() < 0.3:  # 30% chance to kill
                self.stats.creatures_killed += 1
                logger.info(f"Killed {creature['name']}")
            
            logger.info(f"Attacked {creature['name']} with {self.config.attack_spell}")
            
        except Exception as e:
            logger.error(f"Error attacking creature {creature['name']}: {e}")
    
    def auto_loot_corpses(self, screenshot):
        """Automatically loot corpses and manage inventory"""
        try:
            if not self.config.auto_loot:
                return
            
            # Simulate looting
            if random.random() < 0.2:  # 20% chance to loot
                items_looted = random.randint(1, 3)
                self.stats.items_looted += items_looted
                logger.info(f"Looted {items_looted} items")
            
        except Exception as e:
            logger.error(f"Error in auto loot: {e}")
    
    def execute_waypoint_movement(self):
        """Execute waypoint-based movement"""
        try:
            if not self.config.auto_walk or not self.config.waypoints:
                return
                
            # Get current waypoint index (stored in bot instance)
            if not hasattr(self, 'current_waypoint_index'):
                self.current_waypoint_index = 0
                self.waypoint_direction = 1  # 1 for forward, -1 for backward
            
            waypoints = self.config.waypoints
            
            if not waypoints:
                return
            
            # Check if it's time to move to next waypoint
            current_time = time.time() * 1000  # Convert to milliseconds
            if not hasattr(self, 'last_waypoint_time'):
                self.last_waypoint_time = current_time
            
            if current_time - self.last_waypoint_time < self.config.waypoint_delay:
                return
            
            # Get current waypoint
            current_waypoint = waypoints[self.current_waypoint_index]
            
            logger.info(f"Walking to waypoint: {current_waypoint['name']} ({current_waypoint['x']}, {current_waypoint['y']})")
            
            # Update waypoint index based on mode
            if self.config.waypoint_mode == "loop":
                self.current_waypoint_index = (self.current_waypoint_index + 1) % len(waypoints)
            
            elif self.config.waypoint_mode == "back_and_forth":
                self.current_waypoint_index += self.waypoint_direction
                
                # Change direction at endpoints
                if self.current_waypoint_index >= len(waypoints) - 1:
                    self.waypoint_direction = -1
                elif self.current_waypoint_index <= 0:
                    self.waypoint_direction = 1
                    
                # Clamp to valid range
                self.current_waypoint_index = max(0, min(self.current_waypoint_index, len(waypoints) - 1))
            
            elif self.config.waypoint_mode == "once":
                if self.current_waypoint_index < len(waypoints) - 1:
                    self.current_waypoint_index += 1
                else:
                    # Reached end, disable auto walk
                    self.config.auto_walk = False
                    logger.info("Waypoint sequence completed - disabling auto walk")
            
            self.last_waypoint_time = current_time
            
        except Exception as e:
            logger.error(f"Error in waypoint movement: {e}")
    
    def anti_idle_action(self):
        """Perform random anti-idle action"""
        if random.random() < 0.1:  # 10% chance every cycle
            logger.info("Performed anti-idle action")
    
    async def bot_main_loop(self):
        """Main bot execution loop"""
        logger.info("Bot main loop started")
        start_time = time.time()
        
        while self.is_running:
            try:
                if self.is_paused:
                    await asyncio.sleep(1)
                    continue
                
                # Update running time
                self.stats.time_running = int(time.time() - start_time)
                
                # Capture screen
                screenshot = self.capture_game_area()
                if screenshot is None:
                    await asyncio.sleep(1)
                    continue
                
                # Detect HP/MP
                status = self.detect_hp_mp(screenshot)
                
                # Emergency logout
                if status['hp_percent'] <= self.config.emergency_logout_hp:
                    logger.warning("Emergency logout triggered!")
                    self.is_running = False
                    break
                
                # Auto heal
                if self.config.auto_heal and status['hp_percent'] <= self.config.heal_at_hp:
                    self.cast_healing_spell()
                
                # Auto food
                if self.config.auto_food and random.random() < 0.05:  # 5% chance per cycle
                    self.use_food()
                
                # Auto attack
                if self.config.auto_attack:
                    creatures = self.detect_creatures(screenshot)
                    if creatures:
                        target = min(creatures, key=lambda c: c['distance'])
                        self.attack_creature(target)
                
                # Auto walk (waypoints)
                if self.config.auto_walk:
                    self.execute_waypoint_movement()
                
                # Auto loot
                if self.config.auto_loot:
                    self.auto_loot_corpses(screenshot)
                
                # Anti-idle
                if self.config.anti_idle:
                    self.anti_idle_action()
                
                # Broadcast stats
                await self.broadcast_stats()
                
                # Random delay between main loop iterations
                await asyncio.sleep(random.uniform(0.5, 2.0))
                
            except Exception as e:
                logger.error(f"Error in bot main loop: {e}")
                await asyncio.sleep(1)
        
        logger.info("Bot main loop ended")

# Global bot instance
bot = TibiaBot()

# WebSocket endpoint
@api_router.websocket("/bot/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    bot.websocket_connections.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    
    except WebSocketDisconnect:
        bot.websocket_connections.discard(websocket)

# API Routes
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@api_router.post("/bot/config")
async def save_bot_config(config: BotConfig):
    try:
        config.id = str(uuid.uuid4())
        config_dict = config.dict()
        
        await db.bot_configs.insert_one(config_dict)
        bot.config = config
        
        return {"message": "Configuration saved successfully", "config_id": config.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/bot/config")
async def get_bot_config():
    try:
        config = await db.bot_configs.find_one(sort=[("_id", -1)])
        if config:
            config.pop("_id", None)
            return config
        return {"message": "No configuration found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/bot/start")
async def start_bot():
    try:
        if bot.is_running:
            return {"message": "Bot is already running"}
        
        if not bot.config:
            # Load last config
            config_data = await db.bot_configs.find_one(sort=[("_id", -1)])
            if config_data:
                config_data.pop("_id", None)
                bot.config = BotConfig(**config_data)
            else:
                raise HTTPException(status_code=400, detail="No configuration found")
        
        bot.is_running = True
        bot.is_paused = False
        bot.session_id = str(uuid.uuid4())
        bot.stats = BotStats(session_id=bot.session_id, created_at=datetime.utcnow())
        
        # Start bot in background
        asyncio.create_task(bot.bot_main_loop())
        
        return {"message": "Bot started successfully", "session_id": bot.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/bot/stop")
async def stop_bot():
    try:
        bot.is_running = False
        bot.is_paused = False
        
        # Save session stats
        if bot.stats:
            stats_dict = bot.stats.dict()
            await db.bot_sessions.insert_one(stats_dict)
        
        return {"message": "Bot stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/bot/pause")
async def pause_bot():
    try:
        bot.is_paused = not bot.is_paused
        status = "paused" if bot.is_paused else "resumed"
        return {"message": f"Bot {status} successfully", "is_paused": bot.is_paused}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/bot/status")
async def get_bot_status():
    try:
        return {
            "is_running": bot.is_running,
            "is_paused": bot.is_paused,
            "session_id": bot.session_id,
            "stats": bot.stats.dict() if bot.stats else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/bot/sessions")
async def get_bot_sessions():
    try:
        sessions = []
        async for session in db.bot_sessions.find().sort("created_at", -1).limit(10):
            session.pop("_id", None)
            sessions.append(session)
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/bot/current-position")
async def get_current_position():
    """Get current player position (simulated for now)"""
    try:
        # Simulate position detection
        simulated_x = random.randint(1000, 1100)
        simulated_y = random.randint(1000, 1100)
        
        return {
            "x": simulated_x,
            "y": simulated_y,
            "message": "Posição capturada com sucesso!",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)