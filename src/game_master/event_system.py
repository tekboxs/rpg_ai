"""
Event System for RPG AI
Handles dynamic events that require dice rolling and player decisions
"""
from typing import Dict, List, Optional, Any
import random
from datetime import datetime
from ..utils.logger import logger
from .dice_system import DiceSystem
from .ai_engine import AIEngine

class EventSystem:
    """Handles dynamic events and their outcomes"""
    
    def __init__(self, ai_engine: AIEngine, dice_system: DiceSystem):
        self.ai_engine = ai_engine
        self.dice_system = dice_system
        self.active_events = {}
        self.event_history = []
        self.event_templates = self._load_event_templates()
        
        logger.info("Event System initialized")
    
    def _load_event_templates(self) -> Dict[str, Dict]:
        """Load templates for different types of events"""
        return {
            'combat_encounter': {
                'triggers': ['exploração', 'movimento', 'interação', 'tempo'],
                'difficulty_modifiers': ['baixo', 'médio', 'alto'],
                'requires_roll': True,
                'roll_type': 'random_event',
                'outcomes': {
                    'legendary_success': 'Encontro fácil com recompensas extras',
                    'amazing_success': 'Encontro controlável com vantagens',
                    'great_success': 'Encontro padrão com pequenas vantagens',
                    'success': 'Encontro padrão',
                    'partial_success': 'Encontro desafiador',
                    'failure': 'Encontro difícil',
                    'bad_failure': 'Encontro muito difícil',
                    'catastrophic_failure': 'Encontro extremamente perigoso'
                }
            },
            'treasure_discovery': {
                'triggers': ['exploração', 'investigação', 'combate', 'tempo'],
                'difficulty_modifiers': ['baixo', 'médio', 'alto'],
                'requires_roll': True,
                'roll_type': 'random_event',
                'outcomes': {
                    'legendary_success': 'Tesouro lendário descoberto',
                    'amazing_success': 'Tesouro muito valioso',
                    'great_success': 'Tesouro valioso',
                    'success': 'Tesouro padrão',
                    'partial_success': 'Pequeno tesouro',
                    'failure': 'Nada encontrado',
                    'bad_failure': 'Armadilha ativada',
                    'catastrophic_failure': 'Perigo mortal despertado'
                }
            },
            'social_encounter': {
                'triggers': ['interação', 'movimento', 'tempo'],
                'difficulty_modifiers': ['baixo', 'médio', 'alto'],
                'requires_roll': True,
                'roll_type': 'random_event',
                'outcomes': {
                    'legendary_success': 'Aliança poderosa formada',
                    'amazing_success': 'Informação valiosa obtida',
                    'great_success': 'Relacionamento positivo',
                    'success': 'Interação bem-sucedida',
                    'partial_success': 'Interação neutra',
                    'failure': 'Interação tensa',
                    'bad_failure': 'Conflito iniciado',
                    'catastrophic_failure': 'Inimizade criada'
                }
            },
            'environmental_hazard': {
                'triggers': ['movimento', 'exploração', 'tempo'],
                'difficulty_modifiers': ['baixo', 'médio', 'alto'],
                'requires_roll': True,
                'roll_type': 'random_event',
                'outcomes': {
                    'legendary_success': 'Hazard completamente evitado',
                    'amazing_success': 'Hazard facilmente superado',
                    'great_success': 'Hazard superado com vantagem',
                    'success': 'Hazard superado',
                    'partial_success': 'Hazard parcialmente superado',
                    'failure': 'Hazard causa dano',
                    'bad_failure': 'Hazard causa dano significativo',
                    'catastrophic_failure': 'Hazard causa dano crítico'
                }
            },
            'plot_development': {
                'triggers': ['tempo', 'ação_jogador', 'progresso'],
                'difficulty_modifiers': ['baixo', 'médio', 'alto'],
                'requires_roll': False,
                'roll_type': None,
                'outcomes': {
                    'plot_advance': 'A história avança significativamente',
                    'plot_complication': 'Nova complicação surge',
                    'plot_revelation': 'Segredo importante é revelado',
                    'plot_redirection': 'A história toma nova direção'
                }
            }
        }
    
    def trigger_random_event(self, event_type: str = None, difficulty: str = "medium", context: str = None) -> Dict[str, Any]:
        """Trigger a random event of the specified type"""
        
        if not event_type:
            event_type = random.choice(list(self.event_templates.keys()))
        
        if event_type not in self.event_templates:
            logger.error(f"Unknown event type: {event_type}")
            return {}
        
        template = self.event_templates[event_type]
        
        # Generate event details
        event_id = f"event_{len(self.active_events) + 1}_{datetime.now().strftime('%H%M%S')}"
        
        if template['requires_roll']:
            # Roll for event outcome
            roll_result = self.dice_system.roll_random_event(event_type, difficulty)
            outcome = roll_result['outcome']
            outcome_description = template['outcomes'].get(outcome, 'Resultado inesperado')
        else:
            # No roll needed for plot events
            outcome = random.choice(list(template['outcomes'].keys()))
            outcome_description = template['outcomes'][outcome]
            roll_result = None
        
        # Generate event description using AI
        event_description = self._generate_event_description(event_type, outcome, context, roll_result)
        
        # Create event data
        event_data = {
            'event_id': event_id,
            'event_type': event_type,
            'difficulty': difficulty,
            'outcome': outcome,
            'outcome_description': outcome_description,
            'description': event_description,
            'context': context,
            'roll_result': roll_result,
            'timestamp': datetime.now().isoformat(),
            'status': 'active',
            'player_responses': [],
            'resolution': None
        }
        
        # Store event
        self.active_events[event_id] = event_data
        self.event_history.append(event_data)
        
        logger.info(f"Random event triggered: {event_type} - {outcome}")
        return event_data
    
    def _generate_event_description(self, event_type: str, outcome: str, context: str, roll_result: Dict = None) -> str:
        """Generate a description of the event using AI"""
        
        prompt = f"""
        Descreva um evento de {event_type} em um RPG com o seguinte resultado: {outcome}
        
        Contexto: {context or 'Situação geral do jogo'}
        
        A descrição deve ser:
        - Imersiva e envolvente
        - Com detalhes sensoriais
        - Que motive os jogadores a reagir
        - Apropriada para o resultado obtido
        
        Seja criativo e detalhado!
        """
        
        if roll_result and roll_result.get('critical_type'):
            prompt += f"\n\nResultado especial: {roll_result['critical_type']}"
        
        description = self.ai_engine.generate_world_building_response(prompt)
        
        if not description:
            # Fallback description
            description = self._generate_fallback_description(event_type, outcome, context)
        
        return description
    
    def _generate_fallback_description(self, event_type: str, outcome: str, context: str) -> str:
        """Generate a fallback description if AI generation fails"""
        
        fallback_descriptions = {
            'combat_encounter': f"Um encontro de combate surge inesperadamente. {outcome}.",
            'treasure_discovery': f"Uma oportunidade de descoberta de tesouro se apresenta. {outcome}.",
            'social_encounter': f"Uma interação social interessante se desenvolve. {outcome}.",
            'environmental_hazard': f"Um perigo ambiental ameaça os jogadores. {outcome}.",
            'plot_development': f"A trama da história se desenvolve de forma inesperada. {outcome}."
        }
        
        return fallback_descriptions.get(event_type, f"Um evento de {event_type} acontece. {outcome}.")
    
    def add_player_response(self, event_id: str, player_id: str, response: str, action_type: str = "general") -> bool:
        """Add a player response to an active event"""
        
        if event_id not in self.active_events:
            logger.warning(f"Event {event_id} not found")
            return False
        
        event = self.active_events[event_id]
        
        player_response = {
            'player_id': player_id,
            'response': response,
            'action_type': action_type,
            'timestamp': datetime.now().isoformat()
        }
        
        event['player_responses'].append(player_response)
        
        # Check if event should be resolved
        if self._should_resolve_event(event):
            self._resolve_event(event_id)
        
        logger.debug(f"Player response added to event {event_id}")
        return True
    
    def _should_resolve_event(self, event: Dict) -> bool:
        """Determine if an event should be resolved based on player responses"""
        
        # Simple resolution logic - can be enhanced
        if event['event_type'] == 'plot_development':
            return len(event['player_responses']) >= 1
        elif event['event_type'] in ['combat_encounter', 'treasure_discovery']:
            return len(event['player_responses']) >= 2
        else:
            return len(event['player_responses']) >= 1
    
    def _resolve_event(self, event_id: str) -> None:
        """Resolve an event and determine final outcome"""
        
        event = self.active_events[event_id]
        
        # Generate resolution using AI
        resolution = self._generate_event_resolution(event)
        
        event['resolution'] = resolution
        event['status'] = 'resolved'
        
        # Remove from active events
        del self.active_events[event_id]
        
        logger.info(f"Event {event_id} resolved: {resolution}")
    
    def _generate_event_resolution(self, event: Dict) -> str:
        """Generate a resolution description for the event"""
        
        prompt = f"""
        Resolva um evento de RPG com as seguintes características:
        
        Tipo: {event['event_type']}
        Resultado: {event['outcome']}
        Descrição: {event['description']}
        
        Respostas dos jogadores:
        {chr(10).join([f"- {r['player_id']}: {r['response']}" for r in event['player_responses']])}
        
        A resolução deve:
        - Concluir o evento de forma satisfatória
        - Considerar as ações dos jogadores
        - Ser apropriada para o resultado obtido
        - Avançar a história de forma interessante
        
        Seja criativo e conclusivo!
        """
        
        resolution = self.ai_engine.generate_world_building_response(prompt)
        
        if not resolution:
            # Fallback resolution
            resolution = self._generate_fallback_resolution(event)
        
        return resolution
    
    def _generate_fallback_resolution(self, event: Dict) -> str:
        """Generate a fallback resolution if AI generation fails"""
        
        base_resolution = f"O evento de {event['event_type']} é concluído com {event['outcome']}."
        
        if event['player_responses']:
            base_resolution += f" As ações dos jogadores influenciaram o resultado."
        
        return base_resolution
    
    def get_active_events(self) -> List[Dict[str, Any]]:
        """Get all currently active events"""
        return list(self.active_events.values())
    
    def get_event_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent event history"""
        return self.event_history[-limit:] if self.event_history else []
    
    def clear_event_history(self) -> None:
        """Clear event history"""
        self.event_history.clear()
        self.active_events.clear()
        logger.info("Event history cleared")
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """Get statistics about events"""
        if not self.event_history:
            return {'total_events': 0}
        
        total_events = len(self.event_history)
        resolved_events = len([e for e in self.event_history if e['status'] == 'resolved'])
        active_events = len(self.active_events)
        
        # Count by type
        event_types = {}
        for event in self.event_history:
            event_type = event['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        return {
            'total_events': total_events,
            'resolved_events': resolved_events,
            'active_events': active_events,
            'events_by_type': event_types,
            'resolution_rate': resolved_events / total_events if total_events > 0 else 0
        }
