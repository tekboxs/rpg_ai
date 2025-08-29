"""
Action Queue System for RPG AI
Handles player actions in a queue system with three input types:
- {fazer} - Player actions
- {dizer} - Player dialogue
- {historia} - Player story elements
- {mestre} - Process all queued actions
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re
from ..utils.logger import logger
from ..utils.config import config

class PlayerAction:
    """Represents a single player action in the queue"""
    
    def __init__(self, player_id: str, action_type: str, content: str, timestamp: datetime = None):
        self.player_id = player_id
        self.action_type = action_type  # 'fazer', 'dizer', 'historia'
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.processed = False
        self.result = None
        self.conflicts = []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary"""
        return {
            'player_id': self.player_id,
            'action_type': self.action_type,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'processed': self.processed,
            'result': self.result,
            'conflicts': self.conflicts
        }
    
    def __str__(self):
        return f"{self.action_type.upper()}: {self.content} (by {self.player_id})"

class ActionQueue:
    """Manages the queue of player actions"""
    
    def __init__(self):
        self.actions: List[PlayerAction] = []
        self.last_story_context: Optional[PlayerAction] = None
        self.processing_order = 'chronological'  # 'chronological', 'priority', 'random'
        self.tie_breaker = 'timestamp'  # 'timestamp', 'player_order', 'roll'
        
        logger.info("Action Queue System initialized")
    
    def add_action(self, player_id: str, action_type: str, content: str) -> PlayerAction:
        """Add a new action to the queue"""
        
        # Validate action type
        if action_type not in ['fazer', 'dizer', 'historia']:
            raise ValueError(f"Invalid action type: {action_type}")
        
        # Create action
        action = PlayerAction(player_id, action_type, content)
        
        # Special handling for historia actions
        if action_type == 'historia':
            self.last_story_context = action
        
        # Add to queue
        self.actions.append(action)
        
        logger.info(f"Added {action_type} action to queue: {content[:50]}...")
        return action
    
    def get_unprocessed_actions(self) -> List[PlayerAction]:
        """Get all unprocessed actions"""
        return [action for action in self.actions if not action.processed]
    
    def get_actions_by_type(self, action_type: str) -> List[PlayerAction]:
        """Get actions of a specific type"""
        return [action for action in self.actions if action.action_type == action_type]
    
    def get_recent_actions(self, limit: int = 10) -> List[PlayerAction]:
        """Get most recent actions"""
        sorted_actions = sorted(self.actions, key=lambda x: x.timestamp, reverse=True)
        return sorted_actions[:limit]
    
    def clear_processed_actions(self) -> int:
        """Remove all processed actions and return count"""
        initial_count = len(self.actions)
        self.actions = [action for action in self.actions if not action.processed]
        removed_count = initial_count - len(self.actions)
        
        if removed_count > 0:
            logger.info(f"Cleared {removed_count} processed actions")
        
        return removed_count
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        unprocessed = self.get_unprocessed_actions()
        
        return {
            'total_actions': len(self.actions),
            'unprocessed_actions': len(unprocessed),
            'actions_by_type': {
                'fazer': len(self.get_actions_by_type('fazer')),
                'dizer': len(self.get_actions_by_type('dizer')),
                'historia': len(self.get_actions_by_type('historia'))
            },
            'last_story_context': self.last_story_context.to_dict() if self.last_story_context else None,
            'processing_order': self.processing_order,
            'tie_breaker': self.tie_breaker
        }

class ActionProcessor:
    """Processes queued actions when {mestre} command is called"""
    
    def __init__(self, action_queue: ActionQueue, game_state, ai_engine):
        self.action_queue = action_queue
        self.game_state = game_state
        self.ai_engine = ai_engine
        self.processing_history = []
        
        logger.info("Action Processor initialized")
    
    def process_all_actions(self) -> Dict[str, Any]:
        """Process all unprocessed actions in the queue"""
        
        unprocessed_actions = self.action_queue.get_unprocessed_actions()
        
        if not unprocessed_actions:
            return {
                'success': True,
                'message': 'Nenhuma ação para processar',
                'processed_count': 0,
                'results': []
            }
        
        logger.info(f"Processing {len(unprocessed_actions)} queued actions")
        
        # Get story context
        story_context = self._get_story_context()
        
        # Sort actions by processing order
        sorted_actions = self._sort_actions_for_processing(unprocessed_actions)
        
        # Process actions sequentially
        results = []
        game_state_updates = []
        
        for action in sorted_actions:
            try:
                result = self._process_single_action(action, story_context, game_state_updates)
                results.append(result)
                
                # Update game state after each action
                if result['success']:
                    game_state_updates.extend(result.get('game_state_updates', []))
                
            except Exception as e:
                logger.error(f"Error processing action {action.id}: {e}")
                result = {
                    'action_id': getattr(action, 'id', 'unknown'),
                    'success': False,
                    'error': str(e),
                    'result': 'Erro ao processar ação'
                }
                results.append(result)
        
        # Apply all game state updates
        self._apply_game_state_updates(game_state_updates)
        
        # Mark actions as processed
        for action in unprocessed_actions:
            action.processed = True
        
        # Generate final summary
        final_summary = self._generate_final_summary(results, story_context)
        
        # Add to processing history
        self.processing_history.append({
            'timestamp': datetime.now().isoformat(),
            'actions_processed': len(unprocessed_actions),
            'results': results,
            'summary': final_summary
        })
        
        return {
            'success': True,
            'processed_count': len(unprocessed_actions),
            'results': results,
            'final_summary': final_summary,
            'game_state_updates': game_state_updates
        }
    
    def _get_story_context(self) -> Optional[str]:
        """Get the most recent story context"""
        if self.action_queue.last_story_context:
            return self.action_queue.last_story_context.content
        return None
    
    def _sort_actions_for_processing(self, actions: List[PlayerAction]) -> List[PlayerAction]:
        """Sort actions based on processing order and tie breaker"""
        
        if self.action_queue.processing_order == 'chronological':
            # Sort by timestamp
            sorted_actions = sorted(actions, key=lambda x: x.timestamp)
        elif self.action_queue.processing_order == 'priority':
            # Sort by type priority: historia > fazer > dizer
            type_priority = {'historia': 3, 'fazer': 2, 'dizer': 1}
            sorted_actions = sorted(actions, key=lambda x: (type_priority[x.action_type], x.timestamp))
        else:  # random
            import random
            sorted_actions = actions.copy()
            random.shuffle(sorted_actions)
        
        # Apply tie breaker if needed
        if self.action_queue.tie_breaker == 'player_order':
            # Sort by player order (first player first)
            player_order = {}
            for i, action in enumerate(sorted_actions):
                if action.player_id not in player_order:
                    player_order[action.player_id] = i
            
            sorted_actions.sort(key=lambda x: (x.timestamp, player_order.get(x.player_id, 999)))
        
        return sorted_actions
    
    def _process_single_action(self, action: PlayerAction, story_context: str, game_state_updates: List) -> Dict[str, Any]:
        """Process a single action"""
        
        logger.debug(f"Processing action: {action.action_type} - {action.content}")
        
        if action.action_type == 'fazer':
            result = self._process_fazer_action(action, story_context)
        elif action.action_type == 'dizer':
            result = self._process_dizer_action(action, story_context)
        elif action.action_type == 'historia':
            result = self._process_historia_action(action, story_context)
        else:
            result = {
                'success': False,
                'error': f'Unknown action type: {action.action_type}',
                'result': 'Tipo de ação desconhecido'
            }
        
        # Add action metadata
        result.update({
            'action_type': action.action_type,
            'player_id': action.player_id,
            'content': action.content,
            'timestamp': action.timestamp.isoformat()
        })
        
        # Store result in action
        action.result = result
        
        return result
    
    def _process_fazer_action(self, action: PlayerAction, story_context: str) -> Dict[str, Any]:
        """Process a 'fazer' (do) action"""
        
        # Use AI to determine action outcome
        prompt = f"""
        Contexto da história: {story_context or 'Situação geral'}
        
        Ação do jogador: {action.content}
        
        Determine o resultado desta ação considerando:
        - Sucesso/Falha/Parcial
        - Consequências imediatas
        - Impacto no mundo
        - Eventos adicionais que podem surgir
        
        Seja criativo e consequente com as ações anteriores.
        """
        
        ai_response = self.ai_engine.generate_response(prompt, 'narrative')
        
        if not ai_response:
            # Fallback response
            ai_response = f"A ação '{action.content}' é executada com sucesso moderado."
        
        # Generate game state updates
        game_state_updates = self._generate_game_state_updates_for_action(action, ai_response)
        
        return {
            'success': True,
            'result': ai_response,
            'action_outcome': 'success',  # Can be enhanced with AI analysis
            'game_state_updates': game_state_updates
        }
    
    def _process_dizer_action(self, action: PlayerAction, story_context: str) -> Dict[str, Any]:
        """Process a 'dizer' (say) action"""
        
        # Use AI to generate NPC responses or world reactions
        prompt = f"""
        Contexto da história: {story_context or 'Situação geral'}
        
        Fala do jogador: {action.content}
        
        Gere respostas de NPCs ou reações do mundo a esta fala.
        Considere:
        - Quem pode estar ouvindo
        - Como diferentes NPCs reagiriam
        - Mudanças na atmosfera ou situação
        - Possíveis consequências sociais
        
        Seja natural e apropriado ao contexto.
        """
        
        ai_response = self.ai_engine.generate_response(prompt, 'dialogue')
        
        if not ai_response:
            # Fallback response
            ai_response = f"Suas palavras ecoam pela área, chamando a atenção de alguns NPCs."
        
        # Generate game state updates
        game_state_updates = self._generate_game_state_updates_for_action(action, ai_response)
        
        return {
            'success': True,
            'result': ai_response,
            'action_outcome': 'success',
            'game_state_updates': game_state_updates
        }
    
    def _process_historia_action(self, action: PlayerAction, story_context: str) -> Dict[str, Any]:
        """Process a 'historia' (story) action"""
        
        # Use AI to expand or modify the story
        prompt = f"""
        Contexto atual da história: {story_context or 'Situação geral'}
        
        Elemento de história do jogador: {action.content}
        
        Integre este elemento à narrativa existente:
        - Como isso se conecta ao que já aconteceu
        - Que mudanças isso traz ao mundo
        - Novas possibilidades que se abrem
        - Elementos atmosféricos ou ambientais
        
        Seja criativo e mantenha a coerência da história.
        """
        
        ai_response = self.ai_engine.generate_response(prompt, 'world_building')
        
        if not ai_response:
            # Fallback response
            ai_response = f"O elemento '{action.content}' é integrado à narrativa, expandindo o mundo da história."
        
        # Generate game state updates
        game_state_updates = self._generate_game_state_updates_for_action(action, ai_response)
        
        return {
            'success': True,
            'result': ai_response,
            'action_outcome': 'success',
            'game_state_updates': game_state_updates
        }
    
    def _generate_game_state_updates_for_action(self, action: PlayerAction, ai_response: str) -> List[Dict[str, Any]]:
        """Generate game state updates based on action and AI response"""
        
        updates = []
        
        # Add action to game history
        updates.append({
            'type': 'add_to_history',
            'player_id': action.player_id,
            'action_type': action.action_type,
            'content': action.content,
            'ai_response': ai_response,
            'timestamp': action.timestamp.isoformat()
        })
        
        # Update world state if action has significant impact
        if action.action_type in ['fazer', 'historia']:
            updates.append({
                'type': 'update_world_state',
                'action': action.content,
                'impact': 'moderate',
                'timestamp': action.timestamp.isoformat()
            })
        
        return updates
    
    def _apply_game_state_updates(self, updates: List[Dict[str, Any]]) -> None:
        """Apply all game state updates"""
        
        for update in updates:
            try:
                if update['type'] == 'add_to_history':
                    self.game_state.add_to_history(
                        update['player_id'],
                        f"{update['action_type']}: {update['content']}",
                        'player_action'
                    )
                
                elif update['type'] == 'update_world_state':
                    # Update world state based on action
                    self._update_world_state(update)
                
            except Exception as e:
                logger.error(f"Error applying game state update: {e}")
    
    def _update_world_state(self, update: Dict[str, Any]) -> None:
        """Update world state based on action"""
        
        # This can be enhanced to actually modify the world
        # For now, just log the update
        logger.info(f"World state updated: {update['action']}")
    
    def _generate_final_summary(self, results: List[Dict[str, Any]], story_context: str) -> str:
        """Generate a final summary of all processed actions"""
        
        # Use AI to generate a coherent summary
        prompt = f"""
        Contexto da história: {story_context or 'Situação geral'}
        
        Ações processadas:
        {chr(10).join([f"- {r['action_type']}: {r['content']} -> {r['result'][:100]}..." for r in results])}
        
        Gere um resumo coerente da nova cena que emerge dessas ações.
        Inclua:
        - O que mudou no mundo
        - Novas situações ou possibilidades
        - Ganchos para próximas ações dos jogadores
        - Estado atual da narrativa
        
        Seja envolvente e motive os jogadores a continuar.
        """
        
        ai_summary = self.ai_engine.generate_response(prompt, 'narrative')
        
        if not ai_summary:
            # Fallback summary
            ai_summary = f"Após processar {len(results)} ações, a situação evoluiu significativamente. Novas possibilidades se abrem para os jogadores."
        
        return ai_summary
    
    def get_processing_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent processing history"""
        return self.processing_history[-limit:] if self.processing_history else []
    
    def clear_processing_history(self) -> None:
        """Clear processing history"""
        self.processing_history.clear()
        logger.info("Processing history cleared")
