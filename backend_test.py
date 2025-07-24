#!/usr/bin/env python3
"""
Comprehensive Backend Test Suite for OT Cavebot System
Tests all API endpoints and WebSocket functionality
"""

import asyncio
import json
import time
import requests
import websockets
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"
WS_URL = f"{BACKEND_URL.replace('http', 'ws')}/api/bot/ws"

print(f"Testing backend at: {API_BASE}")
print(f"WebSocket URL: {WS_URL}")

class OTCavebotTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message="", details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test("Health Check", True, "Backend is healthy")
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_bot_configuration(self):
        """Test bot configuration save and retrieve"""
        # Test configuration data for OT Cavebot
        test_config = {
            "name": "Venore Coryms Hunter",
            "auto_heal": True,
            "auto_food": True,
            "auto_attack": True,
            "auto_walk": True,
            "auto_loot": True,
            "heal_spell": "exura gran",
            "heal_at_hp": 65,
            "heal_mana_spell": "exura gran mas res",
            "heal_at_mp": 40,
            "attack_spell": "exori gran",
            "food_type": "brown mushroom",
            "food_at": 85,
            "waypoints": [
                {"name": "Entrance", "x": 1032, "y": 1024, "description": "Cave entrance"},
                {"name": "Hunting Spot 1", "x": 1045, "y": 1038, "description": "First corym spawn"},
                {"name": "Hunting Spot 2", "x": 1058, "y": 1052, "description": "Second corym spawn"},
                {"name": "Depot", "x": 1032, "y": 1018, "description": "Return to depot"}
            ],
            "waypoint_mode": "loop",
            "waypoint_delay": 1500,
            "target_creatures": ["corym charlatan", "corym skirmisher", "corym vanguard"],
            "loot_items": ["gold coin", "platinum coin", "crystal coin", "corym dagger", "power ring"],
            "discard_items": ["leather boots", "leather helmet", "studded armor"],
            "loot_all_and_filter": True,
            "loot_range": 4,
            "anti_idle": True,
            "emergency_logout_hp": 15,
            "enabled": True
        }
        
        try:
            # Test saving configuration
            response = self.session.post(f"{API_BASE}/bot/config", json=test_config, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "config_id" in data:
                    self.log_test("Save Bot Config", True, f"Config saved with ID: {data['config_id']}")
                    
                    # Test retrieving configuration
                    get_response = self.session.get(f"{API_BASE}/bot/config", timeout=10)
                    
                    if get_response.status_code == 200:
                        retrieved_config = get_response.json()
                        
                        # Verify key fields
                        if (retrieved_config.get("name") == test_config["name"] and
                            retrieved_config.get("heal_spell") == test_config["heal_spell"] and
                            len(retrieved_config.get("waypoints", [])) == len(test_config["waypoints"])):
                            
                            self.log_test("Retrieve Bot Config", True, "Configuration retrieved and verified")
                            return True
                        else:
                            self.log_test("Retrieve Bot Config", False, "Retrieved config doesn't match saved config")
                            return False
                    else:
                        self.log_test("Retrieve Bot Config", False, f"HTTP {get_response.status_code}")
                        return False
                else:
                    self.log_test("Save Bot Config", False, f"No config_id in response: {data}")
                    return False
            else:
                self.log_test("Save Bot Config", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Bot Configuration", False, f"Error: {str(e)}")
            return False
    
    def test_bot_control_endpoints(self):
        """Test bot start, pause, stop functionality"""
        try:
            # Test starting bot
            start_response = self.session.post(f"{API_BASE}/bot/start", timeout=10)
            
            if start_response.status_code == 200:
                start_data = start_response.json()
                if "session_id" in start_data:
                    session_id = start_data["session_id"]
                    self.log_test("Start Bot", True, f"Bot started with session: {session_id}")
                    
                    # Wait a moment for bot to initialize
                    time.sleep(2)
                    
                    # Test bot status
                    status_response = self.session.get(f"{API_BASE}/bot/status", timeout=10)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        if status_data.get("is_running") == True:
                            self.log_test("Bot Status Check", True, "Bot is running")
                            
                            # Test pause functionality
                            pause_response = self.session.post(f"{API_BASE}/bot/pause", timeout=10)
                            if pause_response.status_code == 200:
                                pause_data = pause_response.json()
                                if pause_data.get("is_paused") == True:
                                    self.log_test("Pause Bot", True, "Bot paused successfully")
                                    
                                    # Test resume (pause again)
                                    resume_response = self.session.post(f"{API_BASE}/bot/pause", timeout=10)
                                    if resume_response.status_code == 200:
                                        resume_data = resume_response.json()
                                        if resume_data.get("is_paused") == False:
                                            self.log_test("Resume Bot", True, "Bot resumed successfully")
                                        else:
                                            self.log_test("Resume Bot", False, "Bot not resumed")
                                    else:
                                        self.log_test("Resume Bot", False, f"HTTP {resume_response.status_code}")
                                else:
                                    self.log_test("Pause Bot", False, "Bot not paused")
                            else:
                                self.log_test("Pause Bot", False, f"HTTP {pause_response.status_code}")
                            
                            # Test stopping bot
                            stop_response = self.session.post(f"{API_BASE}/bot/stop", timeout=10)
                            if stop_response.status_code == 200:
                                self.log_test("Stop Bot", True, "Bot stopped successfully")
                                
                                # Verify bot is stopped
                                final_status = self.session.get(f"{API_BASE}/bot/status", timeout=10)
                                if final_status.status_code == 200:
                                    final_data = final_status.json()
                                    if final_data.get("is_running") == False:
                                        self.log_test("Verify Bot Stopped", True, "Bot confirmed stopped")
                                        return True
                                    else:
                                        self.log_test("Verify Bot Stopped", False, "Bot still running")
                                        return False
                            else:
                                self.log_test("Stop Bot", False, f"HTTP {stop_response.status_code}")
                                return False
                        else:
                            self.log_test("Bot Status Check", False, "Bot not running after start")
                            return False
                    else:
                        self.log_test("Bot Status Check", False, f"HTTP {status_response.status_code}")
                        return False
                else:
                    self.log_test("Start Bot", False, "No session_id in response")
                    return False
            else:
                self.log_test("Start Bot", False, f"HTTP {start_response.status_code}: {start_response.text}")
                return False
                
        except Exception as e:
            self.log_test("Bot Control", False, f"Error: {str(e)}")
            return False
    
    def test_session_history(self):
        """Test session history retrieval"""
        try:
            response = self.session.get(f"{API_BASE}/bot/sessions", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "sessions" in data:
                    sessions = data["sessions"]
                    self.log_test("Session History", True, f"Retrieved {len(sessions)} sessions")
                    
                    # If we have sessions, verify structure
                    if sessions:
                        session = sessions[0]
                        required_fields = ["session_id", "exp_gained", "time_running", "heals_used", "attacks_made"]
                        if all(field in session for field in required_fields):
                            self.log_test("Session Data Structure", True, "Session data has required fields")
                            return True
                        else:
                            self.log_test("Session Data Structure", False, "Missing required fields in session data")
                            return False
                    else:
                        self.log_test("Session History", True, "No sessions found (expected for new system)")
                        return True
                else:
                    self.log_test("Session History", False, "No 'sessions' key in response")
                    return False
            else:
                self.log_test("Session History", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Session History", False, f"Error: {str(e)}")
            return False
    
    def test_current_position(self):
        """Test current position capture"""
        try:
            response = self.session.get(f"{API_BASE}/bot/current-position", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "x" in data and "y" in data:
                    x, y = data["x"], data["y"]
                    if isinstance(x, int) and isinstance(y, int):
                        self.log_test("Current Position", True, f"Position captured: ({x}, {y})")
                        return True
                    else:
                        self.log_test("Current Position", False, "Invalid coordinate types")
                        return False
                else:
                    self.log_test("Current Position", False, "Missing x or y coordinates")
                    return False
            else:
                self.log_test("Current Position", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Current Position", False, f"Error: {str(e)}")
            return False
    
    async def test_websocket_connection(self):
        """Test WebSocket real-time updates"""
        try:
            # Connect to WebSocket
            async with websockets.connect(WS_URL, timeout=10) as websocket:
                self.log_test("WebSocket Connection", True, "Connected successfully")
                
                # Send ping message
                ping_message = {"type": "ping"}
                await websocket.send(json.dumps(ping_message))
                
                # Wait for pong response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    data = json.loads(response)
                    
                    if data.get("type") == "pong":
                        self.log_test("WebSocket Ping/Pong", True, "Ping/Pong working")
                        return True
                    else:
                        self.log_test("WebSocket Ping/Pong", False, f"Unexpected response: {data}")
                        return False
                        
                except asyncio.TimeoutError:
                    self.log_test("WebSocket Ping/Pong", False, "No response to ping")
                    return False
                    
        except Exception as e:
            self.log_test("WebSocket Connection", False, f"Connection error: {str(e)}")
            return False
    
    async def test_websocket_stats_broadcast(self):
        """Test WebSocket stats broadcasting during bot operation"""
        try:
            # First start the bot
            start_response = self.session.post(f"{API_BASE}/bot/start", timeout=10)
            if start_response.status_code != 200:
                self.log_test("WebSocket Stats Setup", False, "Could not start bot for stats test")
                return False
            
            # Connect to WebSocket
            async with websockets.connect(WS_URL, timeout=10) as websocket:
                self.log_test("WebSocket Stats Connection", True, "Connected for stats test")
                
                # Wait for stats update
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10)
                    data = json.loads(response)
                    
                    if data.get("type") == "stats_update":
                        stats_data = data.get("data", {})
                        required_stats = ["session_id", "exp_gained", "time_running", "is_running"]
                        
                        if all(field in stats_data for field in required_stats):
                            self.log_test("WebSocket Stats Broadcast", True, "Received valid stats update")
                            
                            # Stop the bot
                            self.session.post(f"{API_BASE}/bot/stop", timeout=10)
                            return True
                        else:
                            self.log_test("WebSocket Stats Broadcast", False, "Missing required stats fields")
                            self.session.post(f"{API_BASE}/bot/stop", timeout=10)
                            return False
                    else:
                        self.log_test("WebSocket Stats Broadcast", False, f"Unexpected message type: {data.get('type')}")
                        self.session.post(f"{API_BASE}/bot/stop", timeout=10)
                        return False
                        
                except asyncio.TimeoutError:
                    self.log_test("WebSocket Stats Broadcast", False, "No stats update received")
                    self.session.post(f"{API_BASE}/bot/stop", timeout=10)
                    return False
                    
        except Exception as e:
            self.log_test("WebSocket Stats Broadcast", False, f"Error: {str(e)}")
            # Ensure bot is stopped
            try:
                self.session.post(f"{API_BASE}/bot/stop", timeout=5)
            except:
                pass
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 60)
        print("🤖 OT CAVEBOT BACKEND TEST SUITE")
        print("=" * 60)
        
        # Synchronous tests
        tests = [
            self.test_health_check,
            self.test_bot_configuration,
            self.test_bot_control_endpoints,
            self.test_session_history,
            self.test_current_position,
        ]
        
        sync_results = []
        for test in tests:
            try:
                result = test()
                sync_results.append(result)
            except Exception as e:
                print(f"❌ Test failed with exception: {str(e)}")
                sync_results.append(False)
        
        # Asynchronous WebSocket tests
        async def run_async_tests():
            ws_results = []
            try:
                result1 = await self.test_websocket_connection()
                ws_results.append(result1)
                
                result2 = await self.test_websocket_stats_broadcast()
                ws_results.append(result2)
            except Exception as e:
                print(f"❌ WebSocket tests failed: {str(e)}")
                ws_results = [False, False]
            
            return ws_results
        
        # Run async tests
        ws_results = asyncio.run(run_async_tests())
        
        # Combine results
        all_results = sync_results + ws_results
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in all_results if result)
        total = len(all_results)
        
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  Some tests failed - check logs above")
        
        # Print detailed results
        print("\nDetailed Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
        
        return passed == total

if __name__ == "__main__":
    tester = OTCavebotTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 Backend is ready for production!")
        exit(0)
    else:
        print("\n🔧 Backend needs attention before deployment")
        exit(1)