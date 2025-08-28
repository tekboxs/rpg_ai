"""
World management for RPG system
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from pathlib import Path
from ..utils.logger import logger

class Location:
    """Represents a location in the game world"""
    
    def __init__(self, name: str, description: str, location_type: str = "area"):
        self.name = name
        self.description = description
        self.location_type = location_type  # area, city, dungeon, tavern, etc.
        self.connections = {}  # connections to other locations
        self.npcs = []        # NPCs present in this location
        self.items = []       # items available in this location
        self.events = []      # events that can happen here
        self.ambiance = ""    # atmospheric description
        
    def add_connection(self, direction: str, location_name: str, description: str = ""):
        """Add a connection to another location"""
        self.connections[direction] = {
            'location': location_name,
            'description': description
        }
    
    def add_npc(self, npc_data: Dict):
        """Add an NPC to this location"""
        self.npcs.append(npc_data)
    
    def add_item(self, item_data: Dict):
        """Add an item to this location"""
        self.items.append(item_data)
    
    def get_description(self, include_details: bool = True) -> str:
        """Get location description with optional details"""
        desc = f"📍 {self.name}\n{self.description}"
        
        if include_details and self.ambiance:
            desc += f"\n\n{self.ambiance}"
        
        if include_details and self.npcs:
            desc += f"\n\n👥 NPCs presentes: {', '.join([npc['name'] for npc in self.npcs])}"
        
        if include_details and self.items:
            desc += f"\n\n📦 Itens visíveis: {', '.join([item['name'] for item in self.items])}"
        
        if include_details and self.connections:
            desc += f"\n\n🛣️ Direções disponíveis: {', '.join(self.connections.keys())}"
        
        return desc

class NPC:
    """Represents a Non-Player Character"""
    
    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description
        self.personality = {}
        self.knowledge = []
        self.quests = []
        self.dialogue_options = {}
        
    def add_personality_trait(self, trait: str, value: str):
        """Add a personality trait"""
        self.personality[trait] = value
    
    def add_knowledge(self, topic: str, information: str):
        """Add knowledge about a topic"""
        self.knowledge.append({
            'topic': topic,
            'information': information
        })
    
    def add_quest(self, quest_data: Dict):
        """Add a quest this NPC can offer"""
        self.quests.append(quest_data)
    
    def get_dialogue_response(self, topic: str) -> Optional[str]:
        """Get NPC response to a topic"""
        return self.dialogue_options.get(topic, "Não tenho muito a dizer sobre isso.")

class World:
    """Manages the game world and its locations"""
    
    def __init__(self, world_name: str = "Mundo Fantástico"):
        self.name = world_name
        self.locations: Dict[str, Location] = {}
        self.npcs: Dict[str, NPC] = {}
        self.current_events = []
        self.world_history = []
        self.weather = "ensolarado"
        self.time_of_day = "dia"
        self.season = "verão"
        
        # Initialize default world
        self._create_default_world()
        logger.info(f"World '{world_name}' initialized")
    
    def _create_default_world(self):
        """Create a basic world structure"""
        # Create starting tavern
        tavern = Location(
            "Taverna do Dragão Dourado",
            "Uma acolhedora taverna no coração da cidade. O ar está impregnado com o aroma de cerveja e comida caseira.",
            "tavern"
        )
        tavern.ambiance = "A lareira crepita suavemente no canto, iluminando o ambiente com uma luz dourada. Músicos tocam uma melodia suave ao fundo."
        
        # Add some NPCs
        tavern.add_npc({
            'name': 'Gareth, o Taverneiro',
            'role': 'Proprietário da taverna',
            'description': 'Um homem robusto de meia-idade com barba grisalha e olhos bondosos.'
        })
        
        tavern.add_npc({
            'name': 'Lyra, a Barda',
            'role': 'Música itinerante',
            'description': 'Uma jovem elfa com cabelos prateados, sempre com sua harpa nas mãos.'
        })
        
        # Add some items
        tavern.add_item({
            'name': 'Cerveja da Casa',
            'description': 'Uma cerveja artesanal, especialidade da taverna.',
            'type': 'bebida'
        })
        
        tavern.add_item({
            'name': 'Pergaminho de Missão',
            'description': 'Um pergaminho com missões disponíveis na cidade.',
            'type': 'quest'
        })
        
        self.add_location(tavern)
        
        # Create city square
        square = Location(
            "Praça Central",
            "O coração pulsante da cidade, onde comerciantes vendem suas mercadorias e viajantes compartilham notícias.",
            "city"
        )
        square.ambiance = "O sol brilha sobre as pedras antigas da praça. O som de conversas e negociações preenche o ar."
        
        # Connect locations
        tavern.add_connection("norte", "Praça Central", "Uma rua movimentada leva à praça central da cidade.")
        square.add_connection("sul", "Taverna do Dragão Dourado", "Uma rua movimentada leva à taverna.")
        
        self.add_location(square)
    
    def add_location(self, location: Location):
        """Add a location to the world"""
        self.locations[location.name] = location
        logger.info(f"Location '{location.name}' added to world")
    
    def get_location(self, name: str) -> Optional[Location]:
        """Get a location by name"""
        return self.locations.get(name)
    
    def add_npc(self, npc: NPC):
        """Add an NPC to the world"""
        self.npcs[npc.name] = npc
        logger.info(f"NPC '{npc.name}' added to world")
    
    def get_npc(self, name: str) -> Optional[NPC]:
        """Get an NPC by name"""
        return self.npcs.get(name)
    
    def add_event(self, event_data: Dict):
        """Add a world event"""
        event_data['timestamp'] = datetime.now().isoformat()
        self.current_events.append(event_data)
        self.world_history.append(event_data)
        logger.info(f"World event added: {event_data.get('title', 'Unknown event')}")
    
    def get_world_state(self) -> Dict[str, Any]:
        """Get current world state"""
        return {
            'name': self.name,
            'weather': self.weather,
            'time_of_day': self.time_of_day,
            'season': self.season,
            'total_locations': len(self.locations),
            'total_npcs': len(self.npcs),
            'current_events': len(self.current_events),
            'locations': list(self.locations.keys())
        }
    
    def change_weather(self, new_weather: str):
        """Change world weather"""
        old_weather = self.weather
        self.weather = new_weather
        self.add_event({
            'title': 'Mudança de Clima',
            'description': f'O clima mudou de {old_weather} para {new_weather}.',
            'type': 'environment'
        })
        logger.info(f"Weather changed from {old_weather} to {new_weather}")
    
    def advance_time(self):
        """Advance time of day"""
        time_cycle = ['madrugada', 'manhã', 'tarde', 'noite']
        current_index = time_cycle.index(self.time_of_day)
        next_index = (current_index + 1) % len(time_cycle)
        self.time_of_day = time_cycle[next_index]
        
        self.add_event({
            'title': 'Mudança de Tempo',
            'description': f'O tempo avançou para {self.time_of_day}.',
            'type': 'time'
        })
        logger.info(f"Time advanced to {self.time_of_day}")
    
    def save_world(self, filepath: str):
        """Save world state to file"""
        try:
            world_data = {
                'name': self.name,
                'locations': {name: self._location_to_dict(loc) for name, loc in self.locations.items()},
                'npcs': {name: self._npc_to_dict(npc) for name, npc in self.npcs.items()},
                'current_events': self.current_events,
                'world_history': self.world_history,
                'weather': self.weather,
                'time_of_day': self.time_of_day,
                'season': self.season
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(world_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"World saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save world: {e}")
    
    def _location_to_dict(self, location: Location) -> Dict:
        """Convert location to dictionary for serialization"""
        return {
            'name': location.name,
            'description': location.description,
            'location_type': location.location_type,
            'connections': location.connections,
            'npcs': location.npcs,
            'items': location.items,
            'events': location.events,
            'ambiance': location.ambiance
        }
    
    def _npc_to_dict(self, npc: NPC) -> Dict:
        """Convert NPC to dictionary for serialization"""
        return {
            'name': npc.name,
            'role': npc.role,
            'description': npc.description,
            'personality': npc.personality,
            'knowledge': npc.knowledge,
            'quests': npc.quests,
            'dialogue_options': npc.dialogue_options
        }
