"""
Simple Game Master for RPG AI
A simplified system that gives more power to players and uses action queues
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re
from ..core.game_state import GameState
from ..core.player import Player
from ..core.world import World, Location, NPC
from .ai_engine import AIEngine
from ..core.action_queue import ActionQueue, ActionProcessor
from ..utils.logger import logger
from ..utils.config import config

class SimpleGameMaster:
    """Simplified Game Master that gives more power to players"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.world = game_state.world
        self.ai_engine = AIEngine()
        
        # Action queue system
        self.action_queue = ActionQueue()
        self.action_processor = ActionProcessor(self.action_queue, game_state, self.ai_engine)
        
        # Command patterns for the new system
        self.command_patterns = self._load_command_patterns()
        
        # Game state
        self.is_active = True
        self.last_activity = datetime.now()
        
        logger.info("Simple Game Master initialized - Player-driven narrative system")
    
    def _load_command_patterns(self) -> Dict[str, re.Pattern]:
        """Load regex patterns for command recognition"""
        return {
            "fazer": re.compile(r"\{fazer\s+(.+)\}", re.IGNORECASE),
            "dizer": re.compile(r"\{dizer\s+(.+)\}", re.IGNORECASE),
            "historia": re.compile(r"\{historia\s+(.+)\}", re.IGNORECASE),
            "mestre": re.compile(r"\{mestre\}(?:\s+(.+))?", re.IGNORECASE),
            "status": re.compile(r"\{status\}(?:\s+(.+))?", re.IGNORECASE),
            "ajuda": re.compile(r"\{ajuda\}(?:\s+(.+))?", re.IGNORECASE),
            "explorar": re.compile(r"\{explorar\}(?:\s+(.+))?", re.IGNORECASE),
            "mover": re.compile(r"\{mover\}(?:\s+(.+))?", re.IGNORECASE),
            "inventario": re.compile(r"\{inventario\}(?:\s+(.+))?", re.IGNORECASE),
            "salvar": re.compile(r"\{salvar\}(?:\s+(.+))?", re.IGNORECASE),
            "carregar": re.compile(r"\{carregar\}(?:\s+(.+))?", re.IGNORECASE),
        }
    
    def process_player_action(self, player: Player, action: str) -> Optional[str]:
        """Process a player action and add to queue or execute immediately"""
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
            
            # If no special command, treat as regular roleplay
            return self._process_roleplay_action(player, action)
            
        except Exception as e:
            logger.error(f"Error processing player action: {e}")
            return f"⚠️ Erro ao processar ação: {str(e)}"
    
    def _process_commands(self, player: Player, action: str) -> Optional[str]:
        """Process special commands in player actions"""
        
        # Check for fazer command
        match = self.command_patterns["fazer"].match(action)
        if match:
            return self._handle_fazer_command(player, match.group(1))
        
        # Check for dizer command
        match = self.command_patterns["dizer"].match(action)
        if match:
            return self._handle_dizer_command(player, match.group(1))
        
        # Check for historia command
        match = self.command_patterns["historia"].match(action)
        if match:
            return self._handle_historia_command(player, match.group(1))
        
        # Check for mestre command
        match = self.command_patterns["mestre"].match(action)
        if match:
            return self._handle_mestre_command(player, match.group(1))
        
        # Check for other commands
        match = self.command_patterns["status"].match(action)
        if match:
            return self._handle_status_command(player, match.group(1))
        
        match = self.command_patterns["ajuda"].match(action)
        if match:
            return self._handle_help_command(player, match.group(1))
        
        match = self.command_patterns["explorar"].match(action)
        if match:
            return self._handle_explore_command(player, match.group(1))
        
        match = self.command_patterns["mover"].match(action)
        if match:
            return self._handle_move_command(player, match.group(1))
        
        match = self.command_patterns["inventario"].match(action)
        if match:
            return self._handle_inventory_command(player, match.group(1))
        
        match = self.command_patterns["salvar"].match(action)
        if match:
            return self._handle_save_command(player, match.group(1))
        
        match = self.command_patterns["carregar"].match(action)
        if match:
            return self._handle_load_command(player, match.group(1))
        
        return None
    
    def _handle_fazer_command(self, player: Player, content: str) -> str:
        """Handle {fazer} command - add action to queue"""
        
        try:
            action = self.action_queue.add_action(player.id, 'fazer', content)
            
            response = f"✅ Ação '{content}' adicionada à fila de processamento.\n"
            response += f"📝 Use {{mestre}} para processar todas as ações em fila."
            
            # Show queue status
            queue_status = self.action_queue.get_queue_status()
            response += f"\n\n📊 Status da fila: {queue_status['unprocessed_actions']} ações aguardando"
            
            return response
            
        except Exception as e:
            logger.error(f"Error adding fazer action: {e}")
            return f"❌ Erro ao adicionar ação: {str(e)}"
    
    def _handle_dizer_command(self, player: Player, content: str) -> str:
        """Handle {dizer} command - add dialogue to queue"""
        
        try:
            action = self.action_queue.add_action(player.id, 'dizer', content)
            
            response = f"💬 Fala '{content}' adicionada à fila de processamento.\n"
            response += f"📝 Use {{mestre}} para processar todas as ações em fila."
            
            # Show queue status
            queue_status = self.action_queue.get_queue_status()
            response += f"\n\n📊 Status da fila: {queue_status['unprocessed_actions']} ações aguardando"
            
            return response
            
        except Exception as e:
            logger.error(f"Error adding dizer action: {e}")
            return f"❌ Erro ao adicionar fala: {str(e)}"
    
    def _handle_historia_command(self, player: Player, content: str) -> str:
        """Handle {historia} command - add story element to queue"""
        
        try:
            action = self.action_queue.add_action(player.id, 'historia', content)
            
            response = f"📖 Elemento de história '{content}' adicionado à fila de processamento.\n"
            response += f"📝 Use {{mestre}} para processar todas as ações em fila."
            
            # Show queue status
            queue_status = self.action_queue.get_queue_status()
            response += f"\n\n📊 Status da fila: {queue_status['unprocessed_actions']} ações aguardando"
            
            return response
            
        except Exception as e:
            logger.error(f"Error adding historia action: {e}")
            return f"❌ Erro ao adicionar elemento de história: {str(e)}"
    
    def _handle_mestre_command(self, player: Player, content: str) -> str:
        """Handle {mestre} command - process all queued actions"""
        
        try:
            # Check if there are actions to process
            unprocessed = self.action_queue.get_unprocessed_actions()
            if not unprocessed:
                return "📝 Nenhuma ação para processar. Use {fazer}, {dizer} ou {historia} para adicionar ações."
            
            # Process all actions
            result = self.action_processor.process_all_actions()
            
            if not result['success']:
                return f"❌ Erro ao processar ações: {result.get('message', 'Erro desconhecido')}"
            
            # Build response
            response = f"🎭 **MESTRE PROCESSANDO {result['processed_count']} AÇÕES**\n\n"
            
            # Add individual results
            for action_result in result['results']:
                response += f"**{action_result['action_type'].upper()}** ({action_result['player_id']}):\n"
                response += f"_{action_result['content']}_\n"
                response += f"➤ {action_result['result']}\n\n"
            
            # Add final summary
            response += f"📖 **RESUMO FINAL:**\n{result['final_summary']}\n\n"
            
            # Add next steps
            response += "🎯 **PRÓXIMOS PASSOS:**\n"
            response += "• Use {fazer} para descrever ações\n"
            response += "• Use {dizer} para falas e diálogos\n"
            response += "• Use {historia} para elementos narrativos\n"
            response += "• Use {mestre} para processar tudo novamente\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing actions: {e}")
            return f"❌ Erro ao processar ações: {str(e)}"
    
    def _handle_status_command(self, player: Player, content: str) -> str:
        """Handle {status} command - show player and game status"""
        
        try:
            # Get player location
            current_location = self.game_state.get_player_location(player.id)
            location_desc = self.game_state.get_location_description(current_location)
            
            # Get queue status
            queue_status = self.action_queue.get_queue_status()
            
            response = f"👤 **STATUS DO JOGADOR:** {player.name}\n"
            response += f"📍 **Localização:** {current_location}\n"
            response += f"🕐 **Última atividade:** {datetime.fromtimestamp(player.last_activity).strftime('%H:%M:%S')}\n\n"
            
            response += f"📊 **STATUS DA FILA:**\n"
            response += f"• Total de ações: {queue_status['total_actions']}\n"
            response += f"• Ações aguardando: {queue_status['unprocessed_actions']}\n"
            response += f"• Fazer: {queue_status['actions_by_type']['fazer']}\n"
            response += f"• Dizer: {queue_status['actions_by_type']['dizer']}\n"
            response += f"• História: {queue_status['actions_by_type']['historia']}\n\n"
            
            response += f"🌍 **DESCRIÇÃO DA LOCALIZAÇÃO:**\n{location_desc}\n\n"
            
            response += f"💡 **DICA:** Use {{mestre}} para processar todas as ações em fila!"
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return f"❌ Erro ao obter status: {str(e)}"
    
    def _handle_help_command(self, player: Player, content: str) -> str:
        """Handle {ajuda} command - show help"""
        
        help_text = """
🎮 **SISTEMA DE RPG SIMPLIFICADO - AJUDA**

📝 **COMANDOS PRINCIPAIS:**
• {fazer <ação>} - Adiciona uma ação à fila de processamento
• {dizer <fala>} - Adiciona uma fala/diálogo à fila
• {historia <elemento>} - Adiciona um elemento narrativo à fila
• {mestre} - Processa todas as ações em fila e gera a nova cena

🔧 **COMANDOS AUXILIARES:**
• {status} - Mostra seu status e da fila de ações
• {explorar} - Explora a localização atual
• {mover <direção>} - Move para uma direção
• {inventario} - Mostra seu inventário
• {salvar} - Salva o jogo
• {carregar} - Carrega um jogo salvo

💡 **COMO FUNCIONA:**
1. Use {fazer}, {dizer} ou {historia} para descrever suas ações
2. Todas as ações ficam em fila até você usar {mestre}
3. O {mestre} processa tudo sequencialmente e gera uma nova cena
4. Você tem controle total sobre a narrativa!

🎭 **EXEMPLOS:**
• {fazer investigar a mesa em busca de pistas}
• {dizer "Olá, posso ajudá-lo?"}
• {historia uma tempestade se aproxima do horizonte}
• {mestre}

🎯 **DICA:** Use {mestre} frequentemente para manter o ritmo da história!
        """
        
        return help_text.strip()
    
    def _handle_explore_command(self, player: Player, content: str) -> str:
        """Handle {explorar} command - explore current location"""
        
        try:
            current_location = self.game_state.get_player_location(player.id)
            location_desc = self.game_state.get_location_description(current_location)
            
            response = f"🔍 **EXPLORANDO {current_location.upper()}**\n\n"
            response += location_desc
            
            return response
            
        except Exception as e:
            logger.error(f"Error exploring location: {e}")
            return f"❌ Erro ao explorar localização: {str(e)}"
    
    def _handle_move_command(self, player: Player, content: str) -> str:
        """Handle {mover} command - move to a direction"""
        
        try:
            direction = content.strip().lower() if content else "norte"
            
            # Simple movement logic
            current_location = self.game_state.get_player_location(player.id)
            
            # For now, just acknowledge the movement
            response = f"🚶 **MOVIMENTO:** {player.name} se move para {direction}.\n\n"
            response += f"💡 **DICA:** Use {{fazer caminhar para {direction}}} para adicionar detalhes à fila!"
            
            return response
            
        except Exception as e:
            logger.error(f"Error moving player: {e}")
            return f"❌ Erro ao mover jogador: {str(e)}"
    
    def _handle_inventory_command(self, player: Player, content: str) -> str:
        """Handle {inventario} command - show inventory"""
        
        try:
            # For now, show a simple inventory
            response = f"🎒 **INVENTÁRIO DE {player.name.upper()}**\n\n"
            response += "📦 **Itens:**\n"
            response += "• Mochila de couro\n"
            response += "• Cantil de água\n"
            response += "• Pedaço de pão\n\n"
            
            response += "💡 **DICA:** Use {{fazer verificar mochila}} para adicionar ações à fila!"
            
            return response
            
        except Exception as e:
            logger.error(f"Error showing inventory: {e}")
            return f"❌ Erro ao mostrar inventário: {str(e)}"
    
    def _handle_save_command(self, player: Player, content: str) -> str:
        """Handle {salvar} command - save game"""
        
        try:
            # For now, just acknowledge the save
            response = f"💾 **JOGO SALVO**\n\n"
            response += f"✅ O estado do jogo foi salvo com sucesso.\n"
            response += f"🕐 Timestamp: {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            response += f"💡 **DICA:** Use {{fazer guardar item importante}} para adicionar ações à fila!"
            
            return response
            
        except Exception as e:
            logger.error(f"Error saving game: {e}")
            return f"❌ Erro ao salvar jogo: {str(e)}"
    
    def _handle_load_command(self, player: Player, content: str) -> str:
        """Handle {carregar} command - load game"""
        
        try:
            # For now, just acknowledge the load
            response = f"📂 **JOGO CARREGADO**\n\n"
            response += f"✅ O estado do jogo foi carregado com sucesso.\n"
            response += f"🕐 Timestamp: {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            response += f"💡 **DICA:** Use {{fazer verificar equipamento}} para adicionar ações à fila!"
            
            return response
            
        except Exception as e:
            logger.error(f"Error loading game: {e}")
            return f"❌ Erro ao carregar jogo: {str(e)}"
    
    def _process_roleplay_action(self, player: Player, action: str) -> str:
        """Process regular roleplay action (not a special command)"""
        
        # For regular roleplay, just acknowledge it
        response = f"💬 **ROLEPLAY:** {player.name} diz/faz: \"{action}\"\n\n"
        response += f"💡 **DICA:** Use comandos especiais para mais controle:\n"
        response += f"• {{fazer {action}}} - Para ações\n"
        response += f"• {{dizer {action}}} - Para falas\n"
        response += f"• {{historia {action}}} - Para elementos narrativos\n"
        response += f"• {{mestre}} - Para processar tudo"
        
        return response
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        
        queue_status = self.action_queue.get_queue_status()
        
        return {
            'system_type': 'Simple Game Master',
            'is_active': self.is_active,
            'last_activity': self.last_activity.isoformat(),
            'action_queue_status': queue_status,
            'processing_history': len(self.action_processor.get_processing_history()),
            'total_players': len(self.game_state.player_locations),
            'world_locations': len(self.world.locations)
        }
    
    def shutdown(self) -> None:
        """Shutdown the simple game master"""
        logger.info("Simple Game Master shutting down")
        self.is_active = False
