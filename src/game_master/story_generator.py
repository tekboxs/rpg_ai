"""
Story Generator System for RPG AI
Generates dynamic story beginnings and campaign scenarios
"""
from typing import Dict, List, Optional, Any
import random
from datetime import datetime
from ..utils.logger import logger
from ..utils.config import config
from .ai_engine import AIEngine

class StoryGenerator:
    """Generates dynamic story beginnings and campaign scenarios"""
    
    def __init__(self, ai_engine: AIEngine):
        self.ai_engine = ai_engine
        self.story_templates = self._load_story_templates()
        self.scenario_types = self._load_scenario_types()
        
        logger.info("Story Generator initialized")
    
    def _load_story_templates(self) -> Dict[str, Dict]:
        """Load base templates for different story beginnings"""
        return {
            'adventure_start': {
                'keywords': ['aventura', 'descoberta', 'chamado', 'destino', 'missão'],
                'locations': ['floresta', 'montanha', 'ruínas', 'vila', 'cidade', 'caverna', 'navio', 'caravana'],
                'triggers': ['encontro', 'descoberta', 'mensagem', 'visão', 'acidente', 'conflito'],
                'objectives': ['investigar', 'proteger', 'encontrar', 'libertar', 'explorar', 'defender']
            },
            'mystery_start': {
                'keywords': ['mistério', 'segredo', 'desaparecimento', 'pista', 'investigação'],
                'locations': ['mansão', 'biblioteca', 'templo', 'mercado', 'rua', 'casa', 'torre'],
                'triggers': ['descoberta', 'relato', 'evidência', 'testemunho', 'coincidência'],
                'objectives': ['descobrir', 'resolver', 'encontrar', 'provar', 'explicar']
            },
            'conflict_start': {
                'keywords': ['conflito', 'guerra', 'invasão', 'rebelião', 'disputa'],
                'locations': ['fortaleza', 'campo', 'vila', 'cidade', 'castelo', 'acampamento'],
                'triggers': ['ataque', 'ultimato', 'traição', 'aliança', 'negociação'],
                'objectives': ['defender', 'atacar', 'negociar', 'aliar', 'escapar']
            },
            'discovery_start': {
                'keywords': ['descoberta', 'tesouro', 'artefato', 'conhecimento', 'poder'],
                'locations': ['caverna', 'ruínas', 'templo', 'biblioteca', 'laboratório', 'crypta'],
                'triggers': ['exploração', 'acidente', 'mapa', 'lenda', 'sonho'],
                'objectives': ['explorar', 'recuperar', 'estudar', 'proteger', 'compartilhar']
            }
        }
    
    def _load_scenario_types(self) -> Dict[str, Dict]:
        """Load different types of campaign scenarios"""
        return {
            'epic_quest': {
                'scale': 'world',
                'duration': 'long',
                'complexity': 'high',
                'rewards': 'legendary',
                'description': 'Uma jornada épica que afeta todo o mundo'
            },
            'local_adventure': {
                'scale': 'region',
                'duration': 'medium',
                'complexity': 'medium',
                'rewards': 'substantial',
                'description': 'Uma aventura que afeta uma região específica'
            },
            'personal_journey': {
                'scale': 'personal',
                'duration': 'variable',
                'complexity': 'low',
                'rewards': 'personal',
                'description': 'Uma jornada pessoal de crescimento e descoberta'
            },
            'mystery_investigation': {
                'scale': 'community',
                'duration': 'medium',
                'complexity': 'high',
                'rewards': 'knowledge',
                'description': 'Uma investigação que revela segredos ocultos'
            }
        }
    
    def generate_story_beginning(self, player_count: int = 1, campaign_style: str = None) -> Dict[str, Any]:
        """Generate a dynamic story beginning"""
        
        if not campaign_style:
            campaign_style = random.choice(list(self.story_templates.keys()))
        
        template = self.story_templates[campaign_style]
        
        # Generate random elements
        location_type = random.choice(template['locations'])
        trigger = random.choice(template['triggers'])
        objective = random.choice(template['objectives'])
        
        # Generate story context
        story_context = f"""
        Tipo de Campanha: {campaign_style}
        Localização: {location_type}
        Gatilho: {trigger}
        Objetivo: {objective}
        Número de Jogadores: {player_count}
        Estilo: Dinâmico e envolvente
        """
        
        # Generate story using AI
        story_prompt = f"""
        Crie uma história inicial envolvente para uma campanha de RPG com as seguintes características:
        - Tipo: {campaign_style}
        - Localização: {location_type}
        - Gatilho: {trigger}
        - Objetivo: {objective}
        - Jogadores: {player_count}
        
        A história deve ser:
        - Criativa e única (não uma taverna padrão)
        - Imersiva e envolvente
        - Com elementos de mistério e aventura
        - Que motive os jogadores a agir
        - Com descrições sensoriais e atmosféricas
        
        Seja detalhado e criativo!
        """
        
        story = self.ai_engine.generate_world_building_response(story_prompt, story_context)
        
        if not story:
            # Fallback story
            story = self._generate_fallback_story(campaign_style, location_type, trigger, objective)
        
        # Generate initial situation
        situation = self._generate_initial_situation(campaign_style, location_type, player_count)
        
        # Generate NPCs for the beginning
        initial_npcs = self._generate_initial_npcs(campaign_style, location_type, player_count)
        
        story_data = {
            'campaign_type': campaign_style,
            'story_title': self._generate_story_title(campaign_style, location_type),
            'story_text': story,
            'initial_location': location_type,
            'initial_situation': situation,
            'initial_npcs': initial_npcs,
            'player_objectives': [objective],
            'campaign_scale': self._determine_campaign_scale(campaign_style),
            'generated_at': datetime.now().isoformat(),
            'player_count': player_count
        }
        
        logger.info(f"Generated story beginning: {story_data['story_title']}")
        return story_data
    
    def _generate_fallback_story(self, campaign_type: str, location: str, trigger: str, objective: str) -> str:
        """Generate a fallback story if AI generation fails"""
        
        fallback_stories = {
            'adventure_start': f"Uma {trigger} inesperada em {location} despertou o espírito aventureiro dos heróis. {objective} tornou-se necessário para proteger o que é importante.",
            'mystery_start': f"Um {trigger} misterioso em {location} deixou todos perplexos. Os heróis devem {objective} para desvendar a verdade por trás dos acontecimentos.",
            'conflict_start': f"Um {trigger} em {location} ameaça a paz da região. Os heróis precisam {objective} para evitar que a situação se agrave.",
            'discovery_start': f"Uma {trigger} em {location} revelou algo extraordinário. Os heróis devem {objective} para entender e proteger essa descoberta."
        }
        
        return fallback_stories.get(campaign_type, f"Uma aventura começa em {location} com {trigger}.")
    
    def _generate_initial_situation(self, campaign_type: str, location: str, player_count: int) -> Dict[str, Any]:
        """Generate the initial situation for players to react to"""
        
        situations = {
            'adventure_start': {
                'description': f"Os jogadores se encontram em {location} quando algo inesperado acontece.",
                'immediate_actions': ['investigar', 'ajudar', 'proteger', 'explorar'],
                'time_pressure': random.choice([True, False]),
                'danger_level': random.choice(['baixo', 'médio', 'alto']),
                'resources_available': random.choice(['limitados', 'adequados', 'abundantes'])
            },
            'mystery_start': {
                'description': f"Algo estranho está acontecendo em {location} e os jogadores são testemunhas.",
                'immediate_actions': ['observar', 'perguntar', 'investigar', 'documentar'],
                'time_pressure': random.choice([True, False]),
                'danger_level': random.choice(['baixo', 'médio', 'alto']),
                'resources_available': random.choice(['limitados', 'adequados', 'abundantes'])
            },
            'conflict_start': {
                'description': f"Um conflito irrompe em {location} e os jogadores estão no meio da situação.",
                'immediate_actions': ['mediar', 'defender', 'atacar', 'escapar'],
                'time_pressure': True,
                'danger_level': random.choice(['médio', 'alto', 'crítico']),
                'resources_available': random.choice(['limitados', 'adequados', 'abundantes'])
            },
            'discovery_start': {
                'description': f"Os jogadores fazem uma descoberta extraordinária em {location}.",
                'immediate_actions': ['estudar', 'proteger', 'compartilhar', 'esconder'],
                'time_pressure': random.choice([True, False]),
                'danger_level': random.choice(['baixo', 'médio', 'alto']),
                'resources_available': random.choice(['limitados', 'adequados', 'abundantes'])
            }
        }
        
        base_situation = situations.get(campaign_type, situations['adventure_start'])
        
        # Add dynamic elements
        base_situation['weather'] = random.choice(['ensolarado', 'nublado', 'chuvoso', 'tempestuoso', 'nebuloso'])
        base_situation['time_of_day'] = random.choice(['manhã', 'tarde', 'noite', 'madrugada'])
        base_situation['atmosphere'] = random.choice(['tensa', 'misteriosa', 'agitada', 'calma', 'perigosa'])
        
        return base_situation
    
    def _generate_initial_npcs(self, campaign_type: str, location: str, player_count: int) -> List[Dict[str, Any]]:
        """Generate initial NPCs for the story beginning"""
        
        npc_count = min(player_count + random.randint(1, 3), 6)
        npcs = []
        
        npc_roles = {
            'adventure_start': ['guia', 'mentor', 'informante', 'vítima', 'testemunha'],
            'mystery_start': ['investigador', 'suspeito', 'vítima', 'testemunha', 'autoridade'],
            'conflict_start': ['mediador', 'agressor', 'vítima', 'autoridade', 'bystander'],
            'discovery_start': ['especialista', 'guardião', 'explorador', 'estudioso', 'curioso']
        }
        
        available_roles = npc_roles.get(campaign_type, ['NPC', 'personagem'])
        
        for i in range(npc_count):
            role = random.choice(available_roles)
            npc = {
                'name': self._generate_npc_name(role),
                'role': role,
                'location': location,
                'attitude': random.choice(['amigável', 'neutro', 'hostil', 'desconfiado', 'curioso']),
                'knowledge': random.choice(['especialista', 'informado', 'leigo', 'ignorante']),
                'motivation': self._generate_npc_motivation(role, campaign_type)
            }
            npcs.append(npc)
        
        return npcs
    
    def _generate_npc_name(self, role: str) -> str:
        """Generate a name for an NPC"""
        name_templates = {
            'guia': ['Eldric', 'Mira', 'Thorne', 'Lyra'],
            'mentor': ['Merlin', 'Elara', 'Theo', 'Isolde'],
            'informante': ['Gareth', 'Sara', 'Marcus', 'Aria'],
            'vítima': ['Tom', 'Mary', 'John', 'Anna'],
            'testemunha': ['Peter', 'Emma', 'David', 'Sophia'],
            'investigador': ['Raven', 'Blade', 'Storm', 'Shadow'],
            'suspeito': ['Kael', 'Nyx', 'Vex', 'Zara'],
            'autoridade': ['Captain', 'Sheriff', 'Mayor', 'Commander'],
            'especialista': ['Professor', 'Scholar', 'Master', 'Expert']
        }
        
        base_names = name_templates.get(role, ['Alex', 'Sam', 'Jordan', 'Casey'])
        return random.choice(base_names)
    
    def _generate_npc_motivation(self, role: str, campaign_type: str) -> str:
        """Generate motivation for an NPC"""
        motivations = {
            'guia': 'ajudar os heróis em sua jornada',
            'mentor': 'passar conhecimento e sabedoria',
            'informante': 'compartilhar informações importantes',
            'vítima': 'encontrar ajuda e proteção',
            'testemunha': 'contar o que viu',
            'investigador': 'resolver o mistério',
            'suspeito': 'provar sua inocência',
            'autoridade': 'manter a ordem e justiça',
            'especialista': 'estudar e aprender'
        }
        
        return motivations.get(role, 'cumprir seu papel na história')
    
    def _generate_story_title(self, campaign_type: str, location: str) -> str:
        """Generate a title for the story"""
        titles = {
            'adventure_start': f'A Aventura de {location.title()}',
            'mystery_start': f'O Mistério de {location.title()}',
            'conflict_start': f'O Conflito de {location.title()}',
            'discovery_start': f'A Descoberta de {location.title()}'
        }
        
        return titles.get(campaign_type, f'A História de {location.title()}')
    
    def _determine_campaign_scale(self, campaign_type: str) -> str:
        """Determine the scale of the campaign"""
        scale_mapping = {
            'adventure_start': 'regional',
            'mystery_start': 'local',
            'conflict_start': 'regional',
            'discovery_start': 'mundial'
        }
        
        return scale_mapping.get(campaign_type, 'local')
    
    def get_story_variations(self) -> List[str]:
        """Get available story variations"""
        return list(self.story_templates.keys())
    
    def get_campaign_scenarios(self) -> List[str]:
        """Get available campaign scenario types"""
        return list(self.scenario_types.keys())
