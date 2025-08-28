"""
Main Game Master class that coordinates all RPG systems
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re
from ..core.game_state import GameState
from ..core.player import Player
from ..core.world import World, Location, NPC
from .ai_engine import AIEngine
from .narrative import NarrativeEngine
from .procedural_generator import ProceduralGenerator
from .npc_memory import NPCMemoryManager
from ..utils.logger import logger
from ..utils.config import config
import random

class GameMaster:
    """Main Game Master class that coordinates all RPG systems"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.world = game_state.world
        self.ai_engine = AIEngine()
        self.narrative_engine = NarrativeEngine(self.world, self.ai_engine)
        self.procedural_generator = ProceduralGenerator(self.ai_engine)
        self.memory_manager = NPCMemoryManager()
        
        # Command patterns for different actions
        self.command_patterns = self._load_command_patterns()
        
        # Game Master state
        self.is_active = True
        self.last_activity = datetime.now()
        self.active_scenarios = []
        self.player_attention = {}  # Track what players are focused on
        
        logger.info("Enhanced Game Master initialized and ready")
    
    def _load_command_patterns(self) -> Dict[str, re.Pattern]:
        """Load regex patterns for command recognition"""
        return {
            'narrate': re.compile(r'\{narra\}(?:\s+(.+))?', re.IGNORECASE),
            'explore': re.compile(r'\{explorar\}(?:\s+(.+))?', re.IGNORECASE),
            'move': re.compile(r'\{mover\}(?:\s+(.+))?', re.IGNORECASE),
            'talk': re.compile(r'\{falar\}(?:\s+(.+))?', re.IGNORECASE),
            'combat': re.compile(r'\{combate\}(?:\s+(.+))?', re.IGNORECASE),
            'quest': re.compile(r'\{missao\}(?:\s+(.+))?', re.IGNORECASE),
            'inventory': re.compile(r'\{inventario\}(?:\s+(.+))?', re.IGNORECASE),
            'help': re.compile(r'\{ajuda\}(?:\s+(.+))?', re.IGNORECASE),
            'status': re.compile(r'\{status\}(?:\s+(.+))?', re.IGNORECASE),
            'save': re.compile(r'\{salvar\}(?:\s+(.+))?', re.IGNORECASE),
            'load': re.compile(r'\{carregar\}(?:\s+(.+))?', re.IGNORECASE),
            'expand': re.compile(r'\{expandir\}(?:\s+(.+))?', re.IGNORECASE),
            'generate': re.compile(r'\{gerar\}(?:\s+(.+))?', re.IGNORECASE)
        }
    
    def process_player_action(self, player: Player, action: str) -> Optional[str]:
        """Process a player action and generate appropriate response"""
        try:
            # Update player activity
            player.update_activity()
            self.last_activity = datetime.now()
            
            # Add action to game history
            self.game_state.add_to_history(player.name, action, "player")
            
            # Check for special commands
            command_response = self._process_commands(player, action)
            if command_response:
                return command_response
            
            # Process regular roleplay action
            return self._process_roleplay_action(player, action)
            
        except Exception as e:
            logger.error(f"Error processing player action: {e}")
            return f"⚠️ Erro ao processar ação: {str(e)}"
    
    def _process_commands(self, player: Player, action: str) -> Optional[str]:
        """Process special commands in player actions"""
        
        # Check for narrate command
        match = self.command_patterns['narrate'].match(action)
        if match:
            return self._handle_narrate_command(player, match.group(1))
        
        # Check for explore command
        match = self.command_patterns['explore'].match(action)
        if match:
            return self._handle_explore_command(player, match.group(1))
        
        # Check for move command
        match = self.command_patterns['move'].match(action)
        if match:
            return self._handle_move_command(player, match.group(1))
        
        # Check for talk command
        match = self.command_patterns['talk'].match(action)
        if match:
            return self._handle_talk_command(player, match.group(1))
        
        # Check for combat command
        match = self.command_patterns['combat'].match(action)
        if match:
            return self._handle_combat_command(player, match.group(1))
        
        # Check for quest command
        match = self.command_patterns['quest'].match(action)
        if match:
            return self._handle_quest_command(player, match.group(1))
        
        # Check for inventory command
        match = self.command_patterns['inventory'].match(action)
        if match:
            return self._handle_inventory_command(player, match.group(1))
        
        # Check for help command
        match = self.command_patterns['help'].match(action)
        if match:
            return self._handle_help_command(player, match.group(1))
        
        # Check for status command
        match = self.command_patterns['status'].match(action)
        if match:
            return self._handle_status_command(player, match.group(1))
        
        # Check for save command
        match = self.command_patterns['save'].match(action)
        if match:
            return self._handle_save_command(player, match.group(1))
        
        # Check for load command
        match = self.command_patterns['load'].match(action)
        if match:
            return self._handle_load_command(player, match.group(1))
        
        # Check for expand command
        match = self.command_patterns['expand'].match(action)
        if match:
            return self._handle_expand_command(player, match.group(1))
        
        # Check for generate command
        match = self.command_patterns['generate'].match(action)
        if match:
            return self._handle_generate_command(player, match.group(1))
        
        return None
    
    def _handle_narrate_command(self, player: Player, target: Optional[str]) -> str:
        """Handle the narrate command"""
        if not target:
            target = "o ambiente atual"
        
        # Get current context
        context = self.game_state.get_context()
        player_location = self.game_state.get_player_location(player.id)
        
        # Generate AI response
        response = self.ai_engine.generate_narrative_response(
            context, 
            f"Jogador {player.name} solicitou narração sobre {target} na localização {player_location}"
        )
        
        if response:
            # Add to game history
            self.game_state.add_to_history("Mestre", response, "gm")
            return response
        else:
            return "⚠️ Não foi possível gerar narração no momento. Tente novamente mais tarde."
    
    def _handle_explore_command(self, player: Player, target: Optional[str]) -> str:
        """Handle the explore command"""
        player_location = self.game_state.get_player_location(player.id)
        location = self.world.get_location(player_location)
        
        if not location:
            return f"⚠️ Localização '{player_location}' não encontrada."
        
        # Generate exploration description
        description = self.narrative_engine.generate_location_description(location)
        
        # Add atmospheric event
        atmospheric_event = self.narrative_engine.create_atmospheric_event(location)
        
        full_response = f"{description}\n\n{atmospheric_event}"
        
        # Add to game history
        self.game_state.add_to_history("Mestre", full_response, "gm")
        
        return full_response
    
    def _handle_move_command(self, player: Player, direction: Optional[str]) -> str:
        """Handle the move command"""
        if not direction:
            return "⚠️ Especifique uma direção para mover. Use: {mover} <direção>"
        
        player_location = self.game_state.get_player_location(player.id)
        current_location = self.world.get_location(player_location)
        
        if not current_location:
            return f"⚠️ Localização atual '{player_location}' não encontrada."
        
        # Check if direction is valid
        if direction not in current_location.connections:
            available_directions = list(current_location.connections.keys())
            return f"⚠️ Direção '{direction}' não disponível. Direções disponíveis: {', '.join(available_directions)}"
        
        # Get destination
        connection = current_location.connections[direction]
        destination_name = connection['location']
        destination = self.world.get_location(destination_name)
        
        if not destination:
            return f"⚠️ Destino '{destination_name}' não encontrado."
        
        # Move player
        old_location = player_location
        self.game_state.set_player_location(player.id, destination_name)
        
        # Generate movement description
        movement_desc = f"Você se move {direction} de {old_location} para {destination_name}."
        if connection.get('description'):
            movement_desc += f" {connection['description']}"
        
        # Add to game history
        self.game_state.add_to_history("Sistema", movement_desc, "movement")
        
        return f"{movement_desc}\n\n{destination.get_description(include_details=True)}"
    
    def _handle_talk_command(self, player: Player, target: Optional[str]) -> str:
        """Handle the talk command with enhanced NPC memory"""
        if not target:
            return "⚠️ Especifique com quem falar. Use: {falar} <nome do NPC>"
        
        player_location = self.game_state.get_player_location(player.id)
        location = self.world.get_location(player_location)
        
        if not location:
            return f"⚠️ Localização '{player_location}' não encontrada."
        
        # Find NPC in current location
        npc_data = None
        for npc in location.npcs:
            if target.lower() in npc['name'].lower():
                npc_data = npc
                break
        
        if not npc_data:
            available_npcs = [npc['name'] for npc in location.npcs]
            if available_npcs:
                return f"⚠️ NPC '{target}' não encontrado. NPCs disponíveis: {', '.join(available_npcs)}"
            else:
                return f"⚠️ Não há NPCs nesta localização para conversar."
        
        # Create NPC object and generate dialogue with memory
        npc = NPC(npc_data['name'], npc_data['role'], npc_data['description'])
        
        # Get conversation context from memory
        memory_context = self.memory_manager.get_npc_context_for_player(
            npc.name, player.id, "conversa"
        )
        
        # Generate dialogue considering memory
        dialogue = self.narrative_engine.generate_npc_dialogue(
            npc, 
            f"Jogador {player.name} conversando com {npc.name}. {memory_context}", 
            "conversa",
            player.id
        )
        
        # Add to game history
        self.game_state.add_to_history(f"{npc.name} ({npc.role})", dialogue, "npc")
        
        return f"💬 {npc.name} ({npc.role}): {dialogue}"
    
    def _handle_combat_command(self, player: Player, target: Optional[str]) -> str:
        """Handle the combat command"""
        if not target:
            return "⚠️ Especifique o alvo do combate. Use: {combate} <alvo>"
        
        # Get current context
        context = self.game_state.get_context()
        
        # Generate combat response
        response = self.ai_engine.generate_combat_response(
            context,
            f"Jogador {player.name} iniciou combate com {target}"
        )
        
        if response:
            # Add to game history
            self.game_state.add_to_history("Mestre", response, "combat")
            return response
        else:
            return "⚠️ Não foi possível gerar resposta de combate no momento."
    
    def _handle_quest_command(self, player: Player, action: Optional[str]) -> str:
        """Handle the quest command with procedural generation"""
        if not action:
            # Show available quests
            active_quests = self.game_state.active_quests
            if not active_quests:
                return "📋 Não há missões ativas no momento."
            
            quest_list = "\n".join([
                f"🎯 {quest['title']}: {quest.get('description', 'Sem descrição')}"
                for quest in active_quests
            ])
            
            return f"📋 Missões ativas:\n{quest_list}"
        
        # Handle specific quest actions
        if action.lower() in ['aceitar', 'pegar', 'iniciar']:
            # Generate a new procedural quest
            quest_data = self.narrative_engine.create_dynamic_quest()
            
            self.game_state.add_quest(quest_data)
            return f"🎯 Nova missão aceita: {quest_data['title']}\n\n{quest_data['description']}"
        
        return f"⚠️ Ação de missão '{action}' não reconhecida."
    
    def _handle_expand_command(self, player: Player, expansion_type: Optional[str]) -> str:
        """Handle the expand command for procedural world expansion"""
        if not expansion_type:
            expansion_type = 'organic'
        
        if expansion_type not in ['organic', 'quest_driven', 'random']:
            return "⚠️ Tipos de expansão válidos: organic, quest_driven, random"
        
        try:
            # Expand the world procedurally
            new_content = self.narrative_engine.expand_world_procedurally(
                expansion_type=expansion_type,
                num_locations=3
            )
            
            if new_content:
                location_names = [loc['name'] for loc in new_content if 'name' in loc]
                response = f"🌍 Mundo expandido com {len(new_content)} novas localizações:\n"
                response += "\n".join([f"📍 {name}" for name in location_names])
                
                # Add to game history
                self.game_state.add_to_history("Sistema", response, "world_expansion")
                
                return response
            else:
                return "⚠️ Não foi possível expandir o mundo no momento."
                
        except Exception as e:
            logger.error(f"Error expanding world: {e}")
            return f"⚠️ Erro ao expandir mundo: {str(e)}"
    
    def _handle_generate_command(self, player: Player, target: Optional[str]) -> str:
        """Handle the generate command for creating specific content"""
        if not target:
            return "⚠️ Especifique o que gerar. Use: {gerar} <localização|npc|missão>"
        
        try:
            if target.lower() in ['localização', 'location']:
                # Generate a random location
                new_location = self.procedural_generator.generate_location()
                
                # Add to world
                self.narrative_engine._add_generated_location_to_world(new_location)
                
                response = f"🏗️ Nova localização gerada: {new_location['name']}\n\n{new_location['description']}"
                
            elif target.lower() in ['npc', 'personagem']:
                # Generate a random NPC
                new_npc = self.procedural_generator.generate_npc()
                
                # Add to world
                self.world.add_npc(NPC(
                    new_npc['name'], 
                    new_npc['role'], 
                    new_npc['description']
                ))
                
                response = f"👤 Novo NPC gerado: {new_npc['name']} ({new_npc['role']})\n\n{new_npc['description']}"
                
            elif target.lower() in ['missão', 'quest']:
                # Generate a random quest
                new_quest = self.narrative_engine.create_dynamic_quest()
                
                response = f"🎯 Nova missão gerada: {new_quest['title']}\n\n{new_quest['description']}"
                
            else:
                return f"⚠️ Tipo de conteúdo '{target}' não reconhecido. Use: localização, npc, ou missão"
            
            # Add to game history
            self.game_state.add_to_history("Sistema", response, "content_generation")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return f"⚠️ Erro ao gerar conteúdo: {str(e)}"
    
    def _handle_inventory_command(self, player: Player, action: Optional[str]) -> str:
        """Handle the inventory command"""
        # For now, return a simple inventory message
        # In a full implementation, this would check actual player inventory
        return "🎒 Seu inventário está vazio. Explore o mundo para encontrar itens!"
    
    def _handle_help_command(self, player: Player, topic: Optional[str]) -> str:
        """Handle the help command with new features"""
        if not topic:
            help_text = """
🎮 **COMANDOS DISPONÍVEIS:**

**Narrativa:**
- {narra} [tema] - Solicita narração do Mestre sobre um tema específico
- {explorar} - Explora detalhadamente a localização atual

**Movimento:**
- {mover} <direção> - Move para uma direção específica (norte, sul, leste, oeste)

**Interação:**
- {falar} <NPC> - Inicia conversa com um NPC específico (com memória!)
- {combate} <alvo> - Inicia uma sequência de combate

**Sistema:**
- {missao} - Gerencia missões e objetivos
- {inventario} - Mostra seu inventário
- {status} - Mostra seu status atual
- {ajuda} [tema] - Mostra ajuda sobre um tema específico
- {salvar} - Salva o estado do jogo
- {carregar} - Carrega um estado salvo

**Novos Recursos:**
- {expandir} [tipo] - Expande o mundo proceduralmente
- {gerar} <tipo> - Gera conteúdo específico (localização, NPC, missão)

**Roleplay:**
- Digite qualquer texto para falar ou agir no jogo

💡 **DICA:** Use os comandos especiais para interagir com o sistema, mas principalmente use texto livre para criar sua história!

🆕 **NOVO:** NPCs agora têm memória e personalidades únicas! Eles se lembram de conversas anteriores e respondem de forma mais natural.
            """.strip()
        else:
            help_text = f"ℹ️ Ajuda sobre '{topic}': Este recurso está em desenvolvimento."
        
        return help_text
    
    def _handle_status_command(self, player: Player, target: Optional[str]) -> str:
        """Handle the status command with enhanced information"""
        if target and target.lower() != 'meu':
            return f"⚠️ Comando de status só funciona para seu próprio personagem."
        
        player_location = self.game_state.get_player_location(player.id)
        world_summary = self.game_state.get_world_summary()
        
        # Get procedural generation stats
        proc_stats = self.procedural_generator.get_generation_stats()
        memory_stats = self.memory_manager.get_memory_statistics()
        
        status_text = f"""
👤 **STATUS DO JOGADOR:**
**Nome:** {player.name}
**Localização:** {player_location}
**Sessão:** {world_summary['session_info']['session_name']}
**Tempo de jogo:** {world_summary['session_info']['duration']:.0f}s

🌍 **STATUS DO MUNDO:**
**Clima:** {world_summary['world_info']['weather']}
**Hora do dia:** {world_summary['world_info']['time_of_day']}
**Missões ativas:** {world_summary['active_quests']}
**Jogadores ativos:** {world_summary['active_players']}

🏗️ **GERAÇÃO PROCEDURAL:**
**Localizações geradas:** {proc_stats['locations_generated']}
**NPCs gerados:** {proc_stats['npcs_generated']}
**Total de conteúdo:** {proc_stats['total_generated']}

🧠 **SISTEMA DE MEMÓRIA:**
**NPCs com memória:** {memory_stats['total_npcs_with_memory']}
**Total de conversas:** {memory_stats['total_conversations']}
**Jogadores únicos:** {memory_stats['total_unique_players']}
        """.strip()
        
        return status_text
    
    def _handle_save_command(self, player: Player, filename: Optional[str]) -> str:
        """Handle the save command with memory data"""
        if not filename:
            filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            # Save game state
            self.game_state.save_game_state(f"saves/{filename}")
            
            # Save NPC memories
            memory_data = self.memory_manager.export_all_memories()
            memory_filename = f"saves/memory_{filename}"
            
            import json
            with open(memory_filename, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
            
            return f"💾 Jogo salvo com sucesso como '{filename}' (incluindo memórias dos NPCs)"
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return f"⚠️ Erro ao salvar jogo: {str(e)}"
    
    def _handle_load_command(self, player: Player, filename: Optional[str]) -> str:
        """Handle the load command with memory data"""
        if not filename:
            return "⚠️ Especifique o arquivo para carregar. Use: {carregar} <nome_do_arquivo>"
        
        try:
            # Load game state
            self.game_state.load_game_state(f"saves/{filename}")
            
            # Load NPC memories
            memory_filename = f"saves/memory_{filename}"
            try:
                import json
                with open(memory_filename, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                
                self.memory_manager.import_all_memories(memory_data)
            except FileNotFoundError:
                logger.warning(f"Memory file {memory_filename} not found, starting with empty memories")
            
            return f"📂 Jogo carregado com sucesso de '{filename}'"
        except Exception as e:
            logger.error(f"Failed to load game: {e}")
            return f"⚠️ Erro ao carregar jogo: {str(e)}"
    
    def _process_roleplay_action(self, player: Player, action: str) -> Optional[str]:
        """Process regular roleplay actions (non-command text)"""
        # For regular roleplay, we don't need to generate a response
        # The action is already added to history and broadcast to other players
        return None
    
    def create_dynamic_event(self, event_type: str = 'random') -> str:
        """Create a dynamic world event to keep the story interesting"""
        if event_type == 'random':
            event_type = random.choice(['weather_change', 'npc_arrival', 'mystery', 'opportunity', 'world_expansion'])
        
        if event_type == 'weather_change':
            new_weather = random.choice(['ensolarado', 'nublado', 'chuvoso', 'tempestuoso'])
            self.world.change_weather(new_weather)
            return f"🌤️ O clima mudou para {new_weather}!"
        
        elif event_type == 'npc_arrival':
            # Create a new NPC arriving at a random location
            locations = list(self.world.locations.keys())
            if locations:
                location_name = random.choice(locations)
                location = self.world.locations[location_name]
                
                # Generate a new NPC procedurally
                new_npc = self.procedural_generator.generate_npc(
                    location_context=location_name
                )
                
                location.add_npc(new_npc)
                
                return f"👤 {new_npc['name']}, um {new_npc['role'].lower()}, chegou a {location_name}!"
        
        elif event_type == 'world_expansion':
            # Expand the world procedurally
            try:
                new_content = self.narrative_engine.expand_world_procedurally('organic', 2)
                if new_content:
                    location_names = [loc['name'] for loc in new_content if 'name' in loc]
                    return f"🌍 O mundo se expandiu! Novas localizações descobertas: {', '.join(location_names)}"
            except Exception as e:
                logger.error(f"Error in dynamic world expansion: {e}")
                return "🌍 Algo interessante acontece no mundo..."
        
        elif event_type == 'mystery':
            return "🔍 Algo misterioso acontece no mundo... O que será?"
        
        elif event_type == 'opportunity':
            return "✨ Uma nova oportunidade se apresenta! Mantenha os olhos abertos!"
        
        return "🌍 Algo interessante acontece no mundo..."
    
    def get_game_master_status(self) -> Dict[str, Any]:
        """Get current Game Master status with new systems"""
        return {
            'is_active': self.is_active,
            'last_activity': self.last_activity.isoformat(),
            'active_scenarios': len(self.active_scenarios),
            'ai_engine_status': self.ai_engine.test_connection(),
            'narrative_summary': self.narrative_engine.get_narrative_summary(),
            'world_summary': self.game_state.get_world_summary(),
            'procedural_stats': self.procedural_generator.get_generation_stats(),
            'memory_stats': self.memory_manager.get_memory_statistics()
        }
    
    def shutdown(self):
        """Shutdown the Game Master"""
        self.is_active = False
        logger.info("Enhanced Game Master shutdown")
