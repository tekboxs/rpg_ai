"""
Game state management for RPG system
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from pathlib import Path
from .world import World
from .player import Player
from ..utils.logger import logger
from ..utils.config import config

class GameSession:
    """Represents a complete RPG game session"""
    
    def __init__(self, session_name: str = "Sessão RPG"):
        self.session_name = session_name
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.created_at = datetime.now()
        self.started_at = None
        self.ended_at = None
        self.is_active = False
        self.session_data = {}
        
        logger.info(f"New game session created: {session_name} (ID: {self.session_id})")
    
    def start_session(self):
        """Start the game session"""
        self.started_at = datetime.now()
        self.is_active = True
        logger.info(f"Game session started: {self.session_name}")
    
    def end_session(self):
        """End the game session"""
        self.ended_at = datetime.now()
        self.is_active = False
        logger.info(f"Game session ended: {self.session_name}")
    
    def get_duration(self) -> Optional[float]:
        """Get session duration in seconds"""
        if self.started_at and self.ended_at:
            return (self.ended_at - self.started_at).total_seconds()
        elif self.started_at:
            return (datetime.now() - self.started_at).total_seconds()
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary"""
        return {
            'session_id': self.session_id,
            'session_name': self.session_name,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'is_active': self.is_active,
            'duration': self.get_duration(),
            'session_data': self.session_data
        }

class GameState:
    """Manages the overall state of the RPG game"""
    
    def __init__(self):
        self.world = World()
        self.current_session = GameSession()
        self.game_history = []
        self.player_locations = {}  # player_id -> current_location
        self.active_quests = []
        self.completed_quests = []
        self.game_rules = self._load_default_rules()
        self.metadata = {
            'version': '2.0.0',
            'last_save': None,
            'total_sessions': 0,
            'total_playtime': 0
        }
        
        # Initialize with starting scenario
        self._initialize_starting_scenario()
        logger.info("GameState initialized")
    
    def _load_default_rules(self) -> Dict[str, Any]:
        """Load default game rules"""
        return {
            'combat_system': 'narrative',
            'magic_system': 'freeform',
            'inventory_limit': 20,
            'gold_starting': 100,
            'experience_system': 'milestone',
            'death_consequences': 'respawn',
            'pvp_allowed': False,
            'auto_save': True
        }
    
    def _initialize_starting_scenario(self):
        """Initialize the starting scenario for new players"""
        starting_message = f"""
🌍 {self.world.name} desperta!

        📍 Localização atual: {config.world_default_location}

        {config.world_starting_scenario}

🎭 Você está prestes a embarcar em uma aventura épica. 
   Use seus comandos para explorar, interagir e criar sua história!
        """.strip()
        
        self.add_to_history("Sistema", starting_message, "system")
    
    def add_to_history(self, player_name: str, message: str, message_type: str = "player"):
        """Add a message to the game history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'player': player_name,
            'message': message,
            'type': message_type,  # player, system, gm, combat, etc.
            'session_id': self.current_session.session_id
        }
        
        self.game_history.append(entry)
        
        # Limit history size
        max_history = config.get('game.max_history', 100)
        if len(self.game_history) > max_history:
            self.game_history = self.game_history[-max_history:]
        
        logger.log_game_event(message_type, player_name, message[:100])
    
    def get_context(self, last_n: int = None) -> str:
        """Get recent game context for AI processing"""
        if last_n is None:
            last_n = config.get('ai.max_context_messages', 15)
        
        recent_entries = self.game_history[-last_n:]
        context_lines = []
        
        for entry in recent_entries:
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%H:%M')
            context_lines.append(f"[{timestamp}] {entry['player']}: {entry['message']}")
        
        return "\n".join(context_lines)
    
    def get_player_location(self, player_id: str) -> Optional[str]:
        """Get current location of a player"""
        return self.player_locations.get(player_id, config.world_default_location)
    
    def set_player_location(self, player_id: str, location_name: str):
        """Set player's current location"""
        old_location = self.player_locations.get(player_id)
        self.player_locations[player_id] = location_name
        
        if old_location != location_name:
            self.add_to_history(
                "Sistema", 
                f"Jogador mudou de {old_location or 'local desconhecido'} para {location_name}",
                "movement"
            )
            logger.info(f"Player {player_id} moved from {old_location} to {location_name}")
    
    def get_location_description(self, location_name: str, include_details: bool = True) -> str:
        """Get description of a specific location"""
        location = self.world.get_location(location_name)
        if location:
            return location.get_description(include_details)
        return f"📍 {location_name}\nLocalização não encontrada."
    
    def add_quest(self, quest_data: Dict):
        """Add a new quest to the game"""
        quest_data['id'] = f"quest_{len(self.active_quests) + 1}"
        quest_data['created_at'] = datetime.now().isoformat()
        quest_data['status'] = 'active'
        self.active_quests.append(quest_data)
        
        self.add_to_history(
            "Sistema",
            f"🎯 Nova missão disponível: {quest_data.get('title', 'Missão')}",
            "quest"
        )
        logger.info(f"New quest added: {quest_data.get('title', 'Unknown quest')}")
    
    def complete_quest(self, quest_id: str, player_name: str):
        """Mark a quest as completed"""
        for quest in self.active_quests:
            if quest['id'] == quest_id:
                quest['status'] = 'completed'
                quest['completed_by'] = player_name
                quest['completed_at'] = datetime.now().isoformat()
                
                self.completed_quests.append(quest)
                self.active_quests.remove(quest)
                
                self.add_to_history(
                    "Sistema",
                    f"✅ Missão completada por {player_name}: {quest.get('title', 'Missão')}",
                    "quest"
                )
                logger.info(f"Quest completed by {player_name}: {quest.get('title', 'Unknown quest')}")
                break
    
    def get_world_summary(self) -> Dict[str, Any]:
        """Get a summary of the current world state"""
        return {
            'world_info': self.world.get_world_state(),
            'session_info': self.current_session.to_dict(),
            'active_players': len(self.player_locations),
            'active_quests': len(self.active_quests),
            'completed_quests': len(self.completed_quests),
            'total_history_entries': len(self.game_history),
            'game_rules': self.game_rules,
            'metadata': self.metadata
        }
    
    def save_game_state(self, filepath: str):
        """Save the complete game state to file"""
        try:
            game_data = {
                'world': self.world,
                'current_session': self.current_session.to_dict(),
                'game_history': self.game_history,
                'player_locations': self.player_locations,
                'active_quests': self.active_quests,
                'completed_quests': self.completed_quests,
                'game_rules': self.game_rules,
                'metadata': self.metadata
            }
            
            # Update metadata
            self.metadata['last_save'] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Game state saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save game state: {e}")
    
    def load_game_state(self, filepath: str):
        """Load game state from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                game_data = json.load(f)
            
            # Restore game state
            # Note: This is a simplified version - in production you'd want more robust deserialization
            self.game_history = game_data.get('game_history', [])
            self.player_locations = game_data.get('player_locations', {})
            self.active_quests = game_data.get('active_quests', [])
            self.completed_quests = game_data.get('completed_quests', [])
            self.game_rules = game_data.get('game_rules', self.game_rules)
            self.metadata = game_data.get('metadata', self.metadata)
            
            logger.info(f"Game state loaded from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load game state: {e}")
    
    def start_new_session(self, session_name: str = None):
        """Start a new game session"""
        if self.current_session.is_active:
            self.current_session.end_session()
        
        if session_name is None:
            session_name = f"Sessão {self.metadata['total_sessions'] + 1}"
        
        self.current_session = GameSession(session_name)
        self.current_session.start_session()
        self.metadata['total_sessions'] += 1
        
        # Clear some session-specific data
        self.player_locations.clear()
        self.active_quests.clear()
        
        # Initialize new session
        self._initialize_starting_scenario()
        logger.info(f"New session started: {session_name}")
    
    def get_recent_activity(self, minutes: int = 30) -> List[Dict]:
        """Get recent game activity within specified time"""
        cutoff_time = datetime.now().timestamp() - (minutes * 60)
        recent_entries = []
        
        for entry in reversed(self.game_history):
            entry_time = datetime.fromisoformat(entry['timestamp']).timestamp()
            if entry_time >= cutoff_time:
                recent_entries.append(entry)
            else:
                break
        
        return list(reversed(recent_entries))
