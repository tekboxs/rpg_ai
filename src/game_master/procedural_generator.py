"""
Procedural Generation System for RPG AI
Generates locations, NPCs, and content dynamically using AI
"""
from typing import Dict, List, Optional, Any, Tuple
import random
from datetime import datetime
from ..utils.logger import logger
from ..utils.config import config
from .ai_engine import AIEngine

class ProceduralGenerator:
    """Generates procedural content using AI"""
    
    def __init__(self, ai_engine: AIEngine):
        self.ai_engine = ai_engine
        self.generated_content = {}  # Track generated content to avoid repetition
        self.location_templates = self._load_location_templates()
        self.npc_templates = self._load_npc_templates()
        
        logger.info("Procedural Generator initialized")
    
    def _load_location_templates(self) -> Dict[str, Dict]:
        """Load base templates for different location types"""
        return {
            'city': {
                'keywords': ['cidade', 'urbano', 'civilização', 'comércio', 'pessoas'],
                'size_variations': ['pequena', 'média', 'grande', 'enorme'],
                'style_variations': ['medieval', 'renascentista', 'fantástica', 'antiga', 'moderna'],
                'features': ['mercado', 'praça', 'templo', 'castelo', 'porto', 'bairro']
            },
            'wilderness': {
                'keywords': ['selvagem', 'natureza', 'isolado', 'perigoso', 'desconhecido'],
                'size_variations': ['clareira', 'vale', 'planície', 'montanha', 'floresta'],
                'style_variations': ['densa', 'aberta', 'rochosa', 'pantanosa', 'montanhosa'],
                'features': ['rio', 'lago', 'caverna', 'ruínas', 'árvore antiga', 'pedra sagrada']
            },
            'dungeon': {
                'keywords': ['subterrâneo', 'escuro', 'perigoso', 'antigo', 'misterioso'],
                'size_variations': ['pequeno', 'médio', 'grande', 'complexo', 'labiríntico'],
                'style_variations': ['natural', 'artificial', 'mágico', 'corrompido', 'sagrado'],
                'features': ['sala', 'corredor', 'armadilha', 'tesouro', 'monstro', 'portal']
            },
            'tavern': {
                'keywords': ['social', 'bebida', 'comida', 'conversa', 'informação'],
                'size_variations': ['pequena', 'média', 'grande', 'luxuosa', 'modesta'],
                'style_variations': ['rústica', 'elegante', 'misteriosa', 'familiar', 'exótica'],
                'features': ['bar', 'mesas', 'lareira', 'palco', 'quarto', 'adega']
            }
        }
    
    def _load_npc_templates(self) -> Dict[str, Dict]:
        """Load base templates for different NPC types"""
        return {
            'merchant': {
                'personality_traits': ['ambicioso', 'honesto', 'desconfiado', 'amigável', 'guloso'],
                'knowledge_domains': ['comércio', 'preços', 'rumores', 'história local', 'guildas'],
                'dialogue_style': ['formal', 'casual', 'persuasivo', 'reservado', 'extrovertido']
            },
            'guard': {
                'personality_traits': ['vigilante', 'corajoso', 'disciplinado', 'suspicaz', 'leal'],
                'knowledge_domains': ['segurança', 'leis', 'criminosos', 'patrulhas', 'autoridades'],
                'dialogue_style': ['direto', 'autoritário', 'cauteloso', 'protetor', 'rígido']
            },
            'scholar': {
                'personality_traits': ['curioso', 'sábio', 'distraído', 'entusiasta', 'cético'],
                'knowledge_domains': ['história', 'magia', 'ciência', 'lendas', 'arte'],
                'dialogue_style': ['erudito', 'explicativo', 'contemplativo', 'apaixonado', 'preciso']
            },
            'adventurer': {
                'personality_traits': ['corajoso', 'impulsivo', 'experiente', 'cauteloso', 'ambicioso'],
                'knowledge_domains': ['combate', 'exploração', 'monstros', 'tesouros', 'perigos'],
                'dialogue_style': ['direto', 'dramático', 'modesto', 'exagerado', 'sério']
            },
            'commoner': {
                'personality_traits': ['trabalhador', 'curioso', 'medroso', 'amigável', 'desconfiado'],
                'knowledge_domains': ['vida cotidiana', 'rumores locais', 'trabalho', 'família', 'história pessoal'],
                'dialogue_style': ['simples', 'casual', 'nervoso', 'acolhedor', 'reservado']
            }
        }
    
    def generate_location(self, 
                         location_type: str = None, 
                         context: str = None,
                         size: str = None) -> Dict[str, Any]:
        """Generate a new location procedurally"""
        
        if not location_type:
            location_type = random.choice(list(self.location_templates.keys()))
        
        if not size:
            size = random.choice(self.location_templates[location_type]['size_variations'])
        
        style = random.choice(self.location_templates[location_type]['style_variations'])
        features = random.sample(
            self.location_templates[location_type]['features'], 
            random.randint(2, 4)
        )
        
        # Generate unique name
        name = self._generate_location_name(location_type, style, size)
        
        # Generate description using AI
        description_context = f"""
        Tipo: {location_type}
        Tamanho: {size}
        Estilo: {style}
        Características: {', '.join(features)}
        Contexto: {context or 'Nova localização no mundo'}
        """
        
        description = self.ai_engine.generate_world_building_response(
            f"Descreva uma localização de {location_type} com estilo {style} e tamanho {size}. "
            f"Inclua as características: {', '.join(features)}. "
            f"Seja criativo e detalhado, criando uma atmosfera envolvente.",
            description_context
        )
        
        if not description:
            description = f"Uma {size} {location_type} com estilo {style}."
        
        # Generate ambiance
        ambiance = self.ai_engine.generate_world_building_response(
            f"Descreva a atmosfera e sensação desta localização: {name}. "
            f"Use linguagem sensorial e emocional para criar imersão.",
            description_context
        )
        
        if not ambiance:
            ambiance = f"A atmosfera desta localização é {random.choice(['misteriosa', 'acolhedora', 'intimidante', 'pacífica'])}."
        
        location_data = {
            'name': name,
            'description': description,
            'location_type': location_type,
            'size': size,
            'style': style,
            'features': features,
            'ambiance': ambiance,
            'connections': {},
            'npcs': [],
            'items': [],
            'events': [],
            'generated_at': datetime.now().isoformat(),
            'generation_context': context
        }
        
        # Track generated content
        self.generated_content[f"location_{name}"] = location_data
        
        logger.info(f"Generated new location: {name}")
        return location_data
    
    def generate_npc(self, 
                    npc_type: str = None, 
                    location_context: str = None,
                    personality_focus: str = None) -> Dict[str, Any]:
        """Generate a new NPC procedurally"""
        
        if not npc_type:
            npc_type = random.choice(list(self.npc_templates.keys()))
        
        template = self.npc_templates[npc_type]
        
        # Generate personality
        personality_traits = random.sample(
            template['personality_traits'], 
            random.randint(2, 4)
        )
        
        if personality_focus:
            personality_traits.insert(0, personality_focus)
        
        # Generate knowledge
        knowledge_domains = random.sample(
            template['knowledge_domains'], 
            random.randint(2, 3)
        )
        
        # Generate dialogue style
        dialogue_style = random.choice(template['dialogue_style'])
        
        # Generate unique name
        name = self._generate_npc_name(npc_type, personality_traits[0])
        
        # Generate appearance and background
        appearance_context = f"""
        Tipo: {npc_type}
        Personalidade: {', '.join(personality_traits)}
        Estilo de diálogo: {dialogue_style}
        Localização: {location_context or 'Mundo em geral'}
        """
        
        appearance = self.ai_engine.generate_world_building_response(
            f"Descreva a aparência física e visual de um {npc_type} com personalidade {personality_traits[0]}. "
            f"Seja detalhado e criativo, incluindo roupas, características faciais e postura.",
            appearance_context
        )
        
        if not appearance:
            appearance = f"Um {npc_type} com aparência típica de sua profissão."
        
        # Generate background story
        background = self.ai_engine.generate_world_building_response(
            f"Crie uma breve história de fundo para {name}, um {npc_type}. "
            f"Inclua sua origem, motivações e uma experiência marcante de sua vida.",
            appearance_context
        )
        
        if not background:
            background = f"{name} tem uma história interessante como {npc_type}."
        
        # Generate dialogue examples
        dialogue_examples = self._generate_dialogue_examples(
            npc_type, personality_traits, dialogue_style
        )
        
        npc_data = {
            'name': name,
            'role': npc_type,
            'description': appearance,
            'personality': {
                'traits': personality_traits,
                'dialogue_style': dialogue_style,
                'focus': personality_focus
            },
            'knowledge': {
                'domains': knowledge_domains,
                'expertise_level': random.choice(['iniciante', 'intermediário', 'especialista', 'mestre']),
                'background': background
            },
            'dialogue_options': dialogue_examples,
            'quests': [],
            'relationships': {},
            'memory': {
                'conversations': [],
                'player_interactions': [],
                'world_events': []
            },
            'generated_at': datetime.now().isoformat(),
            'generation_context': location_context
        }
        
        # Track generated content
        self.generated_content[f"npc_{name}"] = npc_data
        
        logger.info(f"Generated new NPC: {name} ({npc_type})")
        return npc_data
    
    def _generate_location_name(self, location_type: str, style: str, size: str) -> str:
        """Generate a unique location name"""
        
        # Use AI to generate creative names
        name_prompt = f"Gere um nome criativo e memorável para uma localização de {location_type} "
        name_prompt += f"com estilo {style} e tamanho {size}. "
        name_prompt += "Use apenas o nome, sem descrições adicionais."
        
        name = self.ai_engine.generate_world_building_response(name_prompt)
        
        if not name or len(name) > 50:
            # Fallback to template-based generation
            prefixes = {
                'city': ['Cidade', 'Vila', 'Burg', 'Metrópole'],
                'wilderness': ['Vale', 'Floresta', 'Montanha', 'Planície'],
                'dungeon': ['Caverna', 'Ruínas', 'Catacumbas', 'Labirinto'],
                'tavern': ['Taverna', 'Pousada', 'Estalagem', 'Taberna']
            }
            
            suffixes = {
                'city': ['do Norte', 'dos Ventos', 'das Sombras', 'do Ouro'],
                'wilderness': ['Eterna', 'Misteriosa', 'Perdida', 'Sagrada'],
                'dungeon': ['Antiga', 'Maldita', 'Esquecida', 'Proibida'],
                'tavern': ['do Dragão', 'dos Viajantes', 'das Histórias', 'do Fogo']
            }
            
            prefix = random.choice(prefixes.get(location_type, ['Local']))
            suffix = random.choice(suffixes.get(location_type, ['Misterioso']))
            name = f"{prefix} {suffix}"
        
        return name.strip()
    
    def _generate_npc_name(self, npc_type: str, personality: str) -> str:
        """Generate a unique NPC name"""
        
        # Use AI to generate creative names
        name_prompt = f"Gere um nome criativo e memorável para um {npc_type} "
        name_prompt += f"com personalidade {personality}. "
        name_prompt += "Use apenas o nome, sem descrições adicionais."
        
        name = self.ai_engine.generate_world_building_response(name_prompt)
        
        if not name or len(name) > 30:
            # Fallback to template-based generation
            name_templates = {
                'merchant': ['Gareth', 'Mira', 'Thorne', 'Lyra', 'Kael'],
                'guard': ['Marcus', 'Aria', 'Duncan', 'Sara', 'Roland'],
                'scholar': ['Merlin', 'Elara', 'Theo', 'Isolde', 'Aldric'],
                'adventurer': ['Raven', 'Blade', 'Storm', 'Shadow', 'Phoenix'],
                'commoner': ['Tom', 'Mary', 'John', 'Anna', 'Peter']
            }
            
            base_names = name_templates.get(npc_type, ['Alex', 'Sam', 'Jordan', 'Casey'])
            name = random.choice(base_names)
        
        return name.strip()
    
    def _generate_dialogue_examples(self, 
                                  npc_type: str, 
                                  personality_traits: List[str], 
                                  dialogue_style: str) -> Dict[str, str]:
        """Generate example dialogue responses for the NPC"""
        
        dialogue_examples = {}
        
        # Generate greetings
        greeting_prompt = f"Como um {npc_type} com personalidade {personality_traits[0]} "
        greeting_prompt += f"e estilo de diálogo {dialogue_style} cumprimentaria alguém?"
        
        greeting = self.ai_engine.generate_dialogue_response(greeting_prompt)
        if greeting:
            dialogue_examples['greeting'] = greeting
        
        # Generate responses to common topics
        common_topics = ['weather', 'news', 'help', 'trade', 'gossip']
        
        for topic in common_topics:
            topic_prompt = f"Como um {npc_type} com personalidade {personality_traits[0]} "
            topic_prompt += f"responderia a uma pergunta sobre {topic}?"
            
            response = self.ai_engine.generate_dialogue_response(topic_prompt)
            if response:
                dialogue_examples[topic] = response
        
        return dialogue_examples
    
    def expand_world(self, 
                    current_locations: List[str], 
                    expansion_type: str = 'organic') -> List[Dict[str, Any]]:
        """Expand the world with new locations and NPCs"""
        
        new_content = []
        
        if expansion_type == 'organic':
            # Add locations that make sense based on existing ones
            for location_name in current_locations:
                # Generate 1-2 connected locations
                num_connections = random.randint(1, 2)
                
                for _ in range(num_connections):
                    # Determine connection type based on current location
                    connection_types = ['city', 'wilderness', 'dungeon', 'tavern']
                    
                    # Weight the selection based on what would make sense
                    weights = [0.3, 0.4, 0.2, 0.1]  # Favor wilderness and cities
                    
                    new_type = random.choices(connection_types, weights=weights)[0]
                    
                    # Generate new location
                    new_location = self.generate_location(
                        location_type=new_type,
                        context=f"Conectado a {location_name}"
                    )
                    
                    # Generate NPCs for the new location
                    num_npcs = random.randint(1, 3)
                    for _ in range(num_npcs):
                        npc_type = random.choice(list(self.npc_templates.keys()))
                        new_npc = self.generate_npc(
                            npc_type=npc_type,
                            location_context=new_location['name']
                        )
                        new_location['npcs'].append(new_npc)
                    
                    new_content.append(new_location)
        
        elif expansion_type == 'quest_driven':
            # Add locations specifically for quest purposes
            quest_locations = ['dungeon', 'wilderness', 'city']
            
            for loc_type in quest_locations:
                new_location = self.generate_location(
                    location_type=loc_type,
                    context="Localização criada para missões e aventuras"
                )
                
                # Add quest-related NPCs
                if loc_type == 'dungeon':
                    npc = self.generate_npc(
                        npc_type='adventurer',
                        location_context=new_location['name'],
                        personality_focus='corajoso'
                    )
                else:
                    npc = self.generate_npc(
                        npc_type=random.choice(['merchant', 'scholar', 'guard']),
                        location_context=new_location['name']
                    )
                
                new_location['npcs'].append(npc)
                new_content.append(new_location)
        
        logger.info(f"Expanded world with {len(new_content)} new locations")
        return new_content
    
    def get_generation_stats(self) -> Dict[str, Any]:
        """Get statistics about generated content"""
        location_count = len([k for k in self.generated_content.keys() if k.startswith('location_')])
        npc_count = len([k for k in self.generated_content.keys() if k.startswith('npc_')])
        
        return {
            'total_generated': len(self.generated_content),
            'locations_generated': location_count,
            'npcs_generated': npc_count,
            'last_generation': max(
                [content.get('generated_at', '') for content in self.generated_content.values()]
            ) if self.generated_content else None
        }
