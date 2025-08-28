"""
AI Dungeon Master System for RPG AI
An autonomous AI that makes campaign decisions and manages the story
"""
from typing import Dict, List, Optional, Any
import random
from datetime import datetime
from ..utils.logger import logger
from .ai_engine import AIEngine
from .story_generator import StoryGenerator
from .event_system import EventSystem
from .dice_system import DiceSystem

class AIDungeonMaster:
    """Autonomous AI that manages the campaign and makes decisions"""
    
    def __init__(self, ai_engine: AIEngine, story_generator: StoryGenerator, event_system: EventSystem, dice_system: DiceSystem):
        self.ai_engine = ai_engine
        self.story_generator = story_generator
        self.event_system = event_system
        self.dice_system = dice_system
        
        # Campaign state
        self.campaign_state = {
            'current_story': None,
            'story_progress': 0.0,  # 0.0 to 1.0
            'active_plot_threads': [],
            'player_achievements': [],
            'world_state': {},
            'npc_relationships': {},
            'campaign_mood': 'neutral',
            'difficulty_curve': 'balanced'
        }
        
        # AI personality and decision making
        self.ai_personality = {
            'storytelling_style': 'immersive',
            'difficulty_preference': 'adaptive',
            'pacing_style': 'dynamic',
            'player_agency_respect': 'high',
            'creativity_level': 'high'
        }
        
        # Decision making parameters
        self.decision_weights = {
            'player_choice': 0.4,
            'story_coherence': 0.3,
            'dramatic_tension': 0.2,
            'world_consistency': 0.1
        }
        
        logger.info("AI Dungeon Master initialized")
    
    def start_new_campaign(self, player_count: int, campaign_style: str = None) -> Dict[str, Any]:
        """Start a new campaign with AI-generated story"""
        
        logger.info(f"Starting new campaign with {player_count} players")
        
        # Generate story beginning
        story_data = self.story_generator.generate_story_beginning(player_count, campaign_style)
        
        # Initialize campaign state
        self.campaign_state.update({
            'current_story': story_data,
            'story_progress': 0.0,
            'active_plot_threads': [story_data['story_title']],
            'player_achievements': [],
            'world_state': {
                'weather': story_data['initial_situation']['weather'],
                'time_of_day': story_data['initial_situation']['time_of_day'],
                'atmosphere': story_data['initial_situation']['atmosphere'],
                'danger_level': story_data['initial_situation']['danger_level']
            },
            'campaign_mood': 'adventure',
            'difficulty_curve': 'balanced'
        })
        
        # Generate initial world state
        self._generate_initial_world_state(story_data)
        
        logger.info(f"Campaign started: {story_data['story_title']}")
        return story_data
    
    def _generate_initial_world_state(self, story_data: Dict) -> None:
        """Generate initial world state based on story"""
        
        # Generate world context using AI
        world_prompt = f"""
        Crie um estado inicial do mundo para uma campanha de RPG com as seguintes características:
        
        História: {story_data['story_title']}
        Tipo: {story_data['campaign_type']}
        Localização: {story_data['initial_location']}
        Atmosfera: {story_data['initial_situation']['atmosphere']}
        
        O estado do mundo deve incluir:
        - Condições ambientais
        - Estado político/social
        - Eventos recentes importantes
        - Tensões ou conflitos existentes
        - Oportunidades para os jogadores
        
        Seja criativo e detalhado!
        """
        
        world_state = self.ai_engine.generate_world_building_response(world_prompt)
        
        if world_state:
            self.campaign_state['world_state']['description'] = world_state
        else:
            # Fallback world state
            self.campaign_state['world_state']['description'] = f"O mundo está em um estado de {story_data['initial_situation']['atmosphere']} com oportunidades para aventura."
    
    def make_campaign_decision(self, situation: str, player_actions: List[Dict], context: str = None) -> Dict[str, Any]:
        """Make a campaign decision based on current situation and player actions"""
        
        logger.info(f"AI Dungeon Master making decision for: {situation}")
        
        # Analyze player actions and situation
        analysis = self._analyze_situation(situation, player_actions, context)
        
        # Generate decision options
        decision_options = self._generate_decision_options(situation, analysis)
        
        # Evaluate options and make decision
        decision = self._evaluate_and_choose_option(decision_options, analysis)
        
        # Execute decision
        result = self._execute_decision(decision, analysis)
        
        # Update campaign state
        self._update_campaign_state(decision, result)
        
        logger.info(f"Decision made: {decision['type']} - {decision['description']}")
        return result
    
    def _analyze_situation(self, situation: str, player_actions: List[Dict], context: str = None) -> Dict[str, Any]:
        """Analyze the current situation and player actions"""
        
        analysis = {
            'situation_type': self._classify_situation(situation),
            'player_engagement': self._assess_player_engagement(player_actions),
            'story_coherence': self._assess_story_coherence(situation),
            'dramatic_potential': self._assess_dramatic_potential(situation),
            'world_impact': self._assess_world_impact(situation),
            'context': context or 'Situação geral'
        }
        
        # Use AI to enhance analysis
        ai_analysis = self._get_ai_situation_analysis(situation, player_actions, context)
        if ai_analysis:
            analysis.update(ai_analysis)
        
        return analysis
    
    def _classify_situation(self, situation: str) -> str:
        """Classify the type of situation"""
        situation_keywords = {
            'combat': ['luta', 'batalha', 'ataque', 'defesa', 'combate'],
            'exploration': ['explorar', 'investigar', 'descobrir', 'mapear'],
            'social': ['conversa', 'negociação', 'diplomacia', 'persuasão'],
            'puzzle': ['enigma', 'puzzle', 'mistério', 'segredo', 'desafio'],
            'survival': ['sobrevivência', 'ambiente', 'recursos', 'perigo'],
            'plot': ['história', 'trama', 'missão', 'objetivo', 'destino']
        }
        
        situation_lower = situation.lower()
        for category, keywords in situation_keywords.items():
            if any(keyword in situation_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def _assess_player_engagement(self, player_actions: List[Dict]) -> Dict[str, Any]:
        """Assess how engaged players are"""
        if not player_actions:
            return {'level': 'low', 'actions_count': 0, 'variety': 'none'}
        
        actions_count = len(player_actions)
        action_types = set(action.get('action_type', 'unknown') for action in player_actions)
        
        # Analyze action variety and creativity
        variety_score = len(action_types) / max(len(player_actions), 1)
        
        if actions_count >= 5 and variety_score >= 0.6:
            engagement_level = 'high'
        elif actions_count >= 3 and variety_score >= 0.4:
            engagement_level = 'medium'
        else:
            engagement_level = 'low'
        
        return {
            'level': engagement_level,
            'actions_count': actions_count,
            'variety': variety_score,
            'action_types': list(action_types)
        }
    
    def _assess_story_coherence(self, situation: str) -> Dict[str, Any]:
        """Assess how coherent the story is"""
        # Simple coherence assessment - can be enhanced
        current_story = self.campaign_state.get('current_story')
        if not current_story:
            return {'coherence': 'unknown', 'consistency': 'unknown'}
        
        # Check if situation aligns with campaign type
        campaign_type = current_story.get('campaign_type', 'unknown')
        situation_alignment = self._check_situation_alignment(situation, campaign_type)
        
        return {
            'coherence': situation_alignment,
            'consistency': 'good' if situation_alignment in ['high', 'medium'] else 'poor',
            'campaign_alignment': situation_alignment
        }
    
    def _check_situation_alignment(self, situation: str, campaign_type: str) -> str:
        """Check how well a situation aligns with campaign type"""
        alignment_keywords = {
            'adventure_start': ['aventura', 'exploração', 'descoberta', 'ação'],
            'mystery_start': ['mistério', 'investigação', 'segredo', 'pista'],
            'conflict_start': ['conflito', 'batalha', 'disputa', 'tensão'],
            'discovery_start': ['descoberta', 'tesouro', 'conhecimento', 'artefato']
        }
        
        keywords = alignment_keywords.get(campaign_type, [])
        situation_lower = situation.lower()
        
        matches = sum(1 for keyword in keywords if keyword in situation_lower)
        
        if matches >= 2:
            return 'high'
        elif matches >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _assess_dramatic_potential(self, situation: str) -> Dict[str, Any]:
        """Assess the dramatic potential of a situation"""
        dramatic_keywords = ['perigo', 'urgência', 'conflito', 'mistério', 'descoberta', 'traição', 'aliança']
        situation_lower = situation.lower()
        
        dramatic_elements = [keyword for keyword in dramatic_keywords if keyword in situation_lower]
        
        if len(dramatic_elements) >= 3:
            potential = 'very_high'
        elif len(dramatic_elements) >= 2:
            potential = 'high'
        elif len(dramatic_elements) >= 1:
            potential = 'medium'
        else:
            potential = 'low'
        
        return {
            'level': potential,
            'elements': dramatic_elements,
            'enhancement_opportunities': len(dramatic_elements) < 2
        }
    
    def _assess_world_impact(self, situation: str) -> Dict[str, Any]:
        """Assess the potential impact on the world"""
        impact_keywords = {
            'high': ['mundo', 'reino', 'cidade', 'civilização', 'destino'],
            'medium': ['região', 'comunidade', 'guilda', 'família'],
            'low': ['local', 'pessoal', 'temporário']
        }
        
        situation_lower = situation.lower()
        
        for impact_level, keywords in impact_keywords.items():
            if any(keyword in situation_lower for keyword in keywords):
                return {'level': impact_level, 'scope': keywords}
        
        return {'level': 'unknown', 'scope': []}
    
    def _get_ai_situation_analysis(self, situation: str, player_actions: List[Dict], context: str = None) -> Optional[Dict[str, Any]]:
        """Get AI-enhanced situation analysis"""
        
        prompt = f"""
        Analise a seguinte situação de RPG e forneça insights sobre:
        
        Situação: {situation}
        Ações dos Jogadores: {len(player_actions)} ações
        Contexto: {context or 'Situação geral'}
        
        Forneça análise sobre:
        - Complexidade da situação
        - Oportunidades para desenvolvimento
        - Riscos e recompensas
        - Recomendações para o mestre
        
        Seja conciso e prático.
        """
        
        analysis = self.ai_engine.generate_world_building_response(prompt)
        
        if analysis:
            return {'ai_insights': analysis}
        
        return None
    
    def _generate_decision_options(self, situation: str, analysis: Dict) -> List[Dict[str, Any]]:
        """Generate possible decision options for the situation"""
        
        options = []
        
        # Generate options based on situation type
        situation_type = analysis.get('situation_type', 'general')
        
        if situation_type == 'combat':
            options.extend(self._generate_combat_options(analysis))
        elif situation_type == 'exploration':
            options.extend(self._generate_exploration_options(analysis))
        elif situation_type == 'social':
            options.extend(self._generate_social_options(analysis))
        elif situation_type == 'puzzle':
            options.extend(self._generate_puzzle_options(analysis))
        else:
            options.extend(self._generate_general_options(analysis))
        
        # Add AI-generated options
        ai_options = self._get_ai_decision_options(situation, analysis)
        if ai_options:
            options.extend(ai_options)
        
        return options
    
    def _generate_combat_options(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Generate combat-related decision options"""
        return [
            {
                'type': 'escalate_combat',
                'description': 'Aumentar a intensidade do combate',
                'impact': 'high',
                'risk': 'medium',
                'reward': 'high'
            },
            {
                'type': 'deescalate_combat',
                'description': 'Reduzir a intensidade do combate',
                'impact': 'medium',
                'risk': 'low',
                'reward': 'medium'
            },
            {
                'type': 'introduce_complication',
                'description': 'Adicionar complicação ao combate',
                'impact': 'medium',
                'risk': 'medium',
                'reward': 'medium'
            }
        ]
    
    def _generate_exploration_options(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Generate exploration-related decision options"""
        return [
            {
                'type': 'reveal_discovery',
                'description': 'Revelar uma descoberta importante',
                'impact': 'medium',
                'risk': 'low',
                'reward': 'high'
            },
            {
                'type': 'create_obstacle',
                'description': 'Criar um obstáculo para superar',
                'impact': 'medium',
                'risk': 'low',
                'reward': 'medium'
            },
            {
                'type': 'expand_area',
                'description': 'Expandir a área explorável',
                'impact': 'high',
                'risk': 'low',
                'reward': 'high'
            }
        ]
    
    def _generate_social_options(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Generate social interaction decision options"""
        return [
            {
                'type': 'deepen_relationship',
                'description': 'Aprofundar relacionamento com NPC',
                'impact': 'medium',
                'risk': 'low',
                'reward': 'medium'
            },
            {
                'type': 'create_conflict',
                'description': 'Criar conflito social',
                'impact': 'medium',
                'risk': 'medium',
                'reward': 'high'
            },
            {
                'type': 'reveal_information',
                'description': 'Revelar informação importante',
                'impact': 'medium',
                'risk': 'low',
                'reward': 'medium'
            }
        ]
    
    def _generate_puzzle_options(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Generate puzzle/challenge decision options"""
        return [
            {
                'type': 'provide_hint',
                'description': 'Fornecer dica para o desafio',
                'impact': 'low',
                'risk': 'low',
                'reward': 'medium'
            },
            {
                'type': 'escalate_challenge',
                'description': 'Aumentar dificuldade do desafio',
                'impact': 'medium',
                'risk': 'medium',
                'reward': 'high'
            },
            {
                'type': 'introduce_time_pressure',
                'description': 'Adicionar pressão de tempo',
                'impact': 'medium',
                'risk': 'medium',
                'reward': 'medium'
            }
        ]
    
    def _generate_general_options(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Generate general decision options"""
        return [
            {
                'type': 'advance_plot',
                'description': 'Avançar a trama principal',
                'impact': 'high',
                'risk': 'low',
                'reward': 'high'
            },
            {
                'type': 'create_side_quest',
                'description': 'Criar missão secundária',
                'impact': 'medium',
                'risk': 'low',
                'reward': 'medium'
            },
            {
                'type': 'world_event',
                'description': 'Disparar evento mundial',
                'impact': 'high',
                'risk': 'medium',
                'reward': 'high'
            }
        ]
    
    def _get_ai_decision_options(self, situation: str, analysis: Dict) -> List[Dict[str, Any]]:
        """Get AI-generated decision options"""
        
        prompt = f"""
        Para a situação: {situation}
        
        Análise:
        - Tipo: {analysis.get('situation_type', 'unknown')}
        - Engajamento: {analysis.get('player_engagement', {}).get('level', 'unknown')}
        - Potencial dramático: {analysis.get('dramatic_potential', {}).get('level', 'unknown')}
        
        Sugira 2-3 opções criativas de decisão para o mestre, incluindo:
        - Tipo de ação
        - Descrição
        - Impacto esperado
        - Riscos e recompensas
        
        Seja criativo e específico!
        """
        
        ai_response = self.ai_engine.generate_world_building_response(prompt)
        
        if ai_response:
            # Parse AI response into structured options
            # This is a simplified parser - can be enhanced
            return [{
                'type': 'ai_suggested',
                'description': ai_response[:100] + '...' if len(ai_response) > 100 else ai_response,
                'impact': 'medium',
                'risk': 'medium',
                'reward': 'medium',
                'ai_generated': True
            }]
        
        return []
    
    def _evaluate_and_choose_option(self, options: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """Evaluate options and choose the best one"""
        
        if not options:
            return {'type': 'no_action', 'description': 'Nenhuma ação tomada'}
        
        # Score each option
        scored_options = []
        for option in options:
            score = self._score_option(option, analysis)
            scored_options.append((option, score))
        
        # Sort by score (highest first)
        scored_options.sort(key=lambda x: x[1], reverse=True)
        
        # Choose the best option
        chosen_option = scored_options[0][0]
        
        # Add decision metadata
        chosen_option.update({
            'decision_timestamp': datetime.now().isoformat(),
            'analysis_basis': analysis,
            'other_options_considered': len(options) - 1
        })
        
        return chosen_option
    
    def _score_option(self, option: Dict, analysis: Dict) -> float:
        """Score a decision option based on various factors"""
        
        score = 0.0
        
        # Base score from impact
        impact_scores = {'low': 1.0, 'medium': 2.0, 'high': 3.0}
        score += impact_scores.get(option.get('impact', 'medium'), 2.0)
        
        # Adjust for player engagement
        engagement = analysis.get('player_engagement', {}).get('level', 'medium')
        if engagement == 'high' and option.get('impact') == 'high':
            score += 1.0
        elif engagement == 'low' and option.get('impact') == 'low':
            score += 0.5
        
        # Adjust for story coherence
        coherence = analysis.get('story_coherence', {}).get('coherence', 'medium')
        if coherence in ['high', 'medium']:
            score += 0.5
        
        # Adjust for dramatic potential
        dramatic = analysis.get('dramatic_potential', {}).get('level', 'medium')
        if dramatic in ['high', 'very_high']:
            score += 1.0
        
        # Random factor for unpredictability
        score += random.uniform(-0.5, 0.5)
        
        return score
    
    def _execute_decision(self, decision: Dict, analysis: Dict) -> Dict[str, Any]:
        """Execute the chosen decision"""
        
        decision_type = decision.get('type', 'unknown')
        
        if decision_type == 'escalate_combat':
            result = self._execute_combat_escalation(decision, analysis)
        elif decision_type == 'reveal_discovery':
            result = self._execute_discovery_revelation(decision, analysis)
        elif decision_type == 'advance_plot':
            result = self._execute_plot_advancement(decision, analysis)
        elif decision_type == 'world_event':
            result = self._execute_world_event(decision, analysis)
        else:
            result = self._execute_general_decision(decision, analysis)
        
        # Add execution metadata
        result.update({
            'decision_executed': decision,
            'execution_timestamp': datetime.now().isoformat(),
            'ai_master_notes': self._generate_ai_master_notes(decision, result)
        })
        
        return result
    
    def _execute_combat_escalation(self, decision: Dict, analysis: Dict) -> Dict[str, Any]:
        """Execute combat escalation decision"""
        
        # Trigger a combat event
        event = self.event_system.trigger_random_event(
            'combat_encounter',
            difficulty='hard',
            context='Escalação de combate por decisão da IA'
        )
        
        return {
            'action_type': 'combat_escalation',
            'description': f"O combate se intensifica com {event.get('description', 'novos desafios')}",
            'event_triggered': event,
            'impact': 'high',
            'immediate_effects': ['Dificuldade aumentada', 'Novos inimigos', 'Ambiente hostil']
        }
    
    def _execute_discovery_revelation(self, decision: Dict, analysis: Dict) -> Dict[str, Any]:
        """Execute discovery revelation decision"""
        
        # Trigger a treasure discovery event
        event = self.event_system.trigger_random_event(
            'treasure_discovery',
            difficulty='medium',
            context='Revelação de descoberta por decisão da IA'
        )
        
        return {
            'action_type': 'discovery_revelation',
            'description': f"Uma descoberta importante é revelada: {event.get('description', 'tesouro encontrado')}",
            'event_triggered': event,
            'impact': 'medium',
            'immediate_effects': ['Tesouro descoberto', 'Informação revelada', 'Novo objetivo']
        }
    
    def _execute_plot_advancement(self, decision: Dict, analysis: Dict) -> Dict[str, Any]:
        """Execute plot advancement decision"""
        
        # Advance story progress
        current_progress = self.campaign_state.get('story_progress', 0.0)
        new_progress = min(1.0, current_progress + random.uniform(0.1, 0.3))
        
        self.campaign_state['story_progress'] = new_progress
        
        # Generate plot advancement description
        prompt = f"""
        A trama da campanha avança significativamente. 
        Progresso atual: {new_progress:.1%}
        
        Descreva como a história evolui e o que isso significa para os jogadores.
        Seja dramático e envolvente!
        """
        
        advancement_description = self.ai_engine.generate_world_building_response(prompt)
        
        return {
            'action_type': 'plot_advancement',
            'description': advancement_description or "A trama avança significativamente!",
            'progress_change': new_progress - current_progress,
            'new_progress': new_progress,
            'impact': 'high',
            'immediate_effects': ['História avança', 'Novos objetivos', 'Mundo evolui']
        }
    
    def _execute_world_event(self, decision: Dict, analysis: Dict) -> Dict[str, Any]:
        """Execute world event decision"""
        
        # Trigger a plot development event
        event = self.event_system.trigger_random_event(
            'plot_development',
            difficulty='medium',
            context='Evento mundial por decisão da IA'
        )
        
        return {
            'action_type': 'world_event',
            'description': f"Um evento mundial acontece: {event.get('description', 'mudança significativa')}",
            'event_triggered': event,
            'impact': 'high',
            'immediate_effects': ['Mundo muda', 'Novas oportunidades', 'Desafios globais']
        }
    
    def _execute_general_decision(self, decision: Dict, analysis: Dict) -> Dict[str, Any]:
        """Execute a general decision"""
        
        return {
            'action_type': decision.get('type', 'general'),
            'description': decision.get('description', 'Ação executada'),
            'impact': decision.get('impact', 'medium'),
            'immediate_effects': ['Situação evolui', 'Novas possibilidades']
        }
    
    def _generate_ai_master_notes(self, decision: Dict, result: Dict) -> str:
        """Generate notes from the AI master about the decision"""
        
        prompt = f"""
        Como Mestre de RPG, comente sobre a decisão tomada:
        
        Decisão: {decision.get('description', 'N/A')}
        Resultado: {result.get('description', 'N/A')}
        Impacto: {result.get('impact', 'N/A')}
        
        Forneça:
        - Justificativa para a decisão
        - Expectativas para o futuro
        - Conselhos para os jogadores
        
        Seja sábio e misterioso!
        """
        
        notes = self.ai_engine.generate_world_building_response(prompt)
        
        return notes or "A decisão foi tomada com sabedoria. O destino dos jogadores está em suas mãos."
    
    def _update_campaign_state(self, decision: Dict, result: Dict) -> None:
        """Update campaign state based on decision and result"""
        
        # Update story progress
        if result.get('action_type') == 'plot_advancement':
            # Already updated in execution
            pass
        
        # Update campaign mood
        impact = result.get('impact', 'medium')
        if impact == 'high':
            self.campaign_state['campaign_mood'] = 'intense'
        elif impact == 'low':
            self.campaign_state['campaign_mood'] = 'calm'
        
        # Update active plot threads
        if result.get('action_type') in ['plot_advancement', 'world_event']:
            self.campaign_state['active_plot_threads'].append(f"Evento: {result.get('description', 'N/A')}")
        
        # Update world state
        if result.get('immediate_effects'):
            self.campaign_state['world_state']['recent_events'] = result.get('immediate_effects')
        
        logger.debug(f"Campaign state updated: {result.get('action_type')}")
    
    def get_campaign_status(self) -> Dict[str, Any]:
        """Get current campaign status"""
        return {
            'campaign_state': self.campaign_state,
            'ai_personality': self.ai_personality,
            'decision_weights': self.decision_weights,
            'recent_decisions': len(self.campaign_state.get('active_plot_threads', [])),
            'story_progress': f"{self.campaign_state.get('story_progress', 0.0):.1%}"
        }
    
    def adapt_difficulty(self, player_performance: Dict) -> None:
        """Adapt campaign difficulty based on player performance"""
        
        # Analyze player performance
        success_rate = player_performance.get('success_rate', 0.5)
        engagement_level = player_performance.get('engagement_level', 'medium')
        
        # Adjust difficulty curve
        if success_rate < 0.3:  # Players struggling
            self.campaign_state['difficulty_curve'] = 'easier'
            logger.info("AI Master reducing difficulty - players struggling")
        elif success_rate > 0.8:  # Players excelling
            self.campaign_state['difficulty_curve'] = 'harder'
            logger.info("AI Master increasing difficulty - players excelling")
        else:
            self.campaign_state['difficulty_curve'] = 'balanced'
        
        # Adjust decision weights based on engagement
        if engagement_level == 'low':
            self.decision_weights['dramatic_tension'] += 0.1
            self.decision_weights['player_choice'] -= 0.05
        elif engagement_level == 'high':
            self.decision_weights['player_choice'] += 0.05
            self.decision_weights['story_coherence'] += 0.05
    
    def shutdown(self) -> None:
        """Shutdown the AI Dungeon Master"""
        logger.info("AI Dungeon Master shutting down")
        
        # Save final campaign state
        final_state = {
            'campaign_state': self.campaign_state,
            'final_timestamp': datetime.now().isoformat(),
            'total_decisions_made': len(self.campaign_state.get('active_plot_threads', [])),
            'final_story_progress': self.campaign_state.get('story_progress', 0.0)
        }
        
        # Could save to file here
        logger.info(f"Final campaign state: {final_state}")
