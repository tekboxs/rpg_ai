"""
Configuration management for RPG AI
"""
import os
import yaml
from typing import Dict, Any
from pathlib import Path

class Config:
    """Configuration manager for the RPG system"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # Look for config in current directory or parent directories
            current_dir = Path.cwd()
            config_path = current_dir / "config" / "settings.yaml"
            
            if not config_path.exists():
                # Try to find config in parent directories
                for parent in current_dir.parents:
                    potential_config = parent / "config" / "settings.yaml"
                    if potential_config.exists():
                        config_path = potential_config
                        break
        
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'server.port')"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def reload(self):
        """Reload configuration from file"""
        self._config = self._load_config()
    
    @property
    def server_host(self) -> str:
        return self.get('server.host', '0.0.0.0')
    
    @property
    def server_port(self) -> int:
        return self.get('server.port', 5555)
    
    @property
    def max_players(self) -> int:
        return self.get('server.max_players', 8)
    
    @property
    def ai_endpoint(self) -> str:
        return self.get('ai.endpoint', 'http://localhost:5001/v1/chat/completions')
    
    @property
    def ai_api_key(self) -> str:
        return self.get('ai.api_key', '')
    
    @property
    def ai_enabled(self) -> bool:
        return self.get('ai.enabled', True)
    
    @property
    def ai_model(self) -> str:
        return self.get('ai.model', 'kb-gpt-neo')
    
    @property
    def ai_max_tokens(self) -> int:
        return self.get('ai.max_tokens', 600)
    
    @property
    def ai_temperature(self) -> float:
        return self.get('ai.temperature', 0.8)
    
    @property
    def max_context_messages(self) -> int:
        return self.get('ai.max_context_messages', 15)
    
    @property
    def world_default_location(self) -> str:
        return self.get('world.default_location', 'Taverna do Dragão Dourado')
    
    @property
    def world_starting_scenario(self) -> str:
        return self.get('world.starting_scenario', 'Uma noite tempestuosa na taverna...')
    
    # Procedural Generation Properties
    @property
    def procedural_enabled(self) -> bool:
        return self.get('procedural.enabled', True)
    
    @property
    def max_locations_per_expansion(self) -> int:
        return self.get('procedural.max_locations_per_expansion', 5)
    
    @property
    def max_npcs_per_location(self) -> int:
        return self.get('procedural.max_npcs_per_location', 4)
    
    @property
    def location_name_max_length(self) -> int:
        return self.get('procedural.location_name_max_length', 50)
    
    @property
    def npc_name_max_length(self) -> int:
        return self.get('procedural.npc_name_max_length', 30)
    
    @property
    def generation_creativity(self) -> float:
        return self.get('procedural.generation_creativity', 0.8)
    
    @property
    def world_expansion_chance(self) -> float:
        return self.get('procedural.world_expansion_chance', 0.3)
    
    # NPC Memory Properties
    @property
    def memory_enabled(self) -> bool:
        return self.get('memory.enabled', True)
    
    @property
    def max_memory_size(self) -> int:
        return self.get('memory.max_memory_size', 100)
    
    @property
    def memory_cleanup_interval(self) -> int:
        return self.get('memory.memory_cleanup_interval', 24)
    
    @property
    def emotional_state_tracking(self) -> bool:
        return self.get('memory.emotional_state_tracking', True)
    
    @property
    def relationship_development(self) -> bool:
        return self.get('memory.relationship_development', True)
    
    @property
    def topic_memory_enabled(self) -> bool:
        return self.get('memory.topic_memory_enabled', True)
    
    @property
    def player_interaction_history(self) -> bool:
        return self.get('memory.player_interaction_history', True)

# Global configuration instance
config = Config()
