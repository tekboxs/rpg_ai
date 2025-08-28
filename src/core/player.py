"""
Player management for RPG system
"""
from typing import Dict, List, Optional
from datetime import datetime
import uuid
from ..utils.logger import logger

class Player:
    """Represents a player in the RPG session"""
    
    def __init__(self, name: str, connection=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.connection = connection
        self.joined_at = datetime.now()
        self.last_activity = datetime.now()
        self.character = None
        self.is_ready = False
        self.is_gm = False  # Game Master flag
        
        # Player stats and preferences
        self.preferences = {
            'narrative_style': 'descriptive',  # descriptive, concise, dramatic
            'combat_style': 'tactical',        # tactical, narrative, cinematic
            'roleplay_level': 'medium'         # low, medium, high
        }
        
        logger.info(f"New player created: {name} (ID: {self.id})")
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def is_active(self, timeout_minutes: int = None) -> bool:
        """Check if player is still active"""
        # Se timeout_minutes for 0 ou None, jogador nunca expira
        if timeout_minutes is None or timeout_minutes <= 0:
            return True
        
        delta = datetime.now() - self.last_activity
        return delta.total_seconds() < (timeout_minutes * 60)
    
    def send_message(self, message: str) -> bool:
        """Send message to player's connection"""
        if self.connection:
            try:
                self.connection.sendall(message.encode('utf-8'))
                return True
            except Exception as e:
                logger.error(f"Failed to send message to {self.name}: {e}")
                return False
        return False
    
    def set_character(self, character_data: Dict):
        """Set player's character"""
        self.character = character_data
        logger.info(f"Character set for {self.name}: {character_data.get('name', 'Unknown')}")
    
    def get_status(self) -> Dict:
        """Get player status information"""
        return {
            'id': self.id,
            'name': self.name,
            'joined_at': self.joined_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'is_ready': self.is_ready,
            'is_gm': self.is_gm,
            'has_character': self.character is not None,
            'character_name': self.character.get('name') if self.character else None
        }
    
    def __str__(self):
        return f"Player({self.name}, ID: {self.id})"
    
    def __repr__(self):
        return self.__str__()

class PlayerManager:
    """Manages all players in the RPG session"""
    
    def __init__(self, max_players: int = 8):
        self.max_players = max_players
        self.players: Dict[str, Player] = {}
        self.players_by_connection = {}
        logger.info(f"PlayerManager initialized with max {max_players} players")
    
    def add_player(self, name: str, connection) -> Optional[Player]:
        """Add a new player to the session"""
        if len(self.players) >= self.max_players:
            logger.warning(f"Cannot add player {name}: session is full")
            return None
        
        # Generate unique name if duplicate
        original_name = name
        counter = 1
        while name in [p.name for p in self.players.values()]:
            name = f"{original_name}_{counter}"
            counter += 1
        
        player = Player(name, connection)
        self.players[player.id] = player
        self.players_by_connection[connection] = player
        
        logger.info(f"Player {name} added to session (Total: {len(self.players)})")
        return player
    
    def remove_player(self, player_id: str) -> bool:
        """Remove a player from the session"""
        if player_id in self.players:
            player = self.players[player_id]
            if player.connection in self.players_by_connection:
                del self.players_by_connection[player.connection]
            del self.players[player_id]
            logger.info(f"Player {player.name} removed from session")
            return True
        return False
    
    def get_player_by_connection(self, connection) -> Optional[Player]:
        """Get player by their connection object"""
        return self.players_by_connection.get(connection)
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """Get player by name"""
        for player in self.players.values():
            if player.name == name:
                return player
        return None
    
    def get_active_players(self) -> List[Player]:
        """Get list of currently active players"""
        from ..utils.config import config
        timeout_minutes = config.get('game.session_timeout', 0)
        return [p for p in self.players.values() if p.is_active(timeout_minutes)]
    
    def broadcast_message(self, message: str, exclude_player: Optional[Player] = None):
        """Send message to all players"""
        for player in self.players.values():
            if player != exclude_player:
                player.send_message(message)
    
    def get_session_info(self) -> Dict:
        """Get information about the current session"""
        return {
            'total_players': len(self.players),
            'active_players': len(self.get_active_players()),
            'max_players': self.max_players,
            'players': [p.get_status() for p in self.players.values()]
        }
