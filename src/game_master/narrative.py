"""
Enhanced Narrative Engine for RPG AI
Integrates with procedural generation and NPC memory systems
"""
from typing import Dict, List, Optional, Any, Tuple
import random
from datetime import datetime
from ..core.world import World, Location, NPC
from .ai_engine import AIEngine
from .procedural_generator import ProceduralGenerator
from .npc_memory import NPCMemoryManager
from ..utils.logger import logger

class NarrativeEngine:
    """Enhanced narrative engine with procedural generation and memory"""
    
    def __init__(self, world: World, ai_engine: AIEngine):
        self.world = world
        self.ai_engine = ai_engine
        self.procedural_generator = ProceduralGenerator(ai_engine)
        self.memory_manager = NPCMemoryManager()
        
        # Narrative state tracking
        self.narrative_themes = []
        self.active_storylines = []
        self.world_events = []
        
        logger.info("Enhanced Narrative Engine initialized")
    
    def generate_location_description(self, location: Location) -> str:
        """Generate enhanced location description using AI"""
        
        # Check if location was procedurally generated
        if hasattr(location, 'generated_at'):
            # Use existing AI-generated description
            base_description = location.description
        else:
            # Generate new description for existing locations
            base_description = self.ai_engine.generate_world_building_response(
                f"Descreva detalhadamente a localização {location.name} "
                f"do tipo {location.location_type}. "
                f"Seja criativo e envolvente, criando uma atmosfera imersiva.",
                f"Localização: {location.name}\nTipo: {location.location_type}\n"
                f"NPCs: {len(location.npcs)}\nItens: {len(location.items)}"
            )
            
            if not base_description:
                base_description = location.description
        
        # Add dynamic elements based on time, weather, and events
        dynamic_elements = self._generate_dynamic_elements(location)
        
        # Combine base description with dynamic elements
        full_description = f"{base_description}\n\n{dynamic_elements}"
        
        return full_description
    
    def _generate_dynamic_elements(self, location: Location) -> str:
        """Generate dynamic elements for location description"""
        
        dynamic_parts = []
        
        # Add weather effects
        weather = self.world.weather if hasattr(self.world, 'weather') else 'ensolarado'
        if weather != 'ensolarado':
            weather_effects = {
                'chuvoso': f"O som da chuva caindo sobre {location.name} cria uma atmosfera melancólica.",
                'nublado': f"Nuvens pesadas pairam sobre {location.name}, criando sombras misteriosas.",
                'tempestuoso': f"O vento uiva através de {location.name}, carregando o aroma de tempestade."
            }
            if weather in weather_effects:
                dynamic_parts.append(weather_effects[weather])
        
        # Add time of day effects
        time_of_day = self.world.time_of_day if hasattr(self.world, 'time_of_day') else 'dia'
        if time_of_day != 'dia':
            time_effects = {
                'noite': f"À noite, {location.name} ganha um ar mais misterioso e intimidador.",
                'madrugada': f"Na madrugada, {location.name} está envolta em névoa e silêncio.",
                'tarde': f"O sol da tarde ilumina {location.name} com uma luz dourada e quente."
            }
            if time_of_day in time_effects:
                dynamic_parts.append(time_effects[time_of_day])
        
        # Add NPC activity descriptions
        if location.npcs:
            npc_activity = self._generate_npc_activity_description(location)
            if npc_activity:
                dynamic_parts.append(npc_activity)
        
        # Add recent events
        if hasattr(location, 'events') and location.events:
            recent_events = [
                event for event in location.events
                if hasattr(event, 'timestamp') and 
                (datetime.now() - datetime.fromisoformat(event['timestamp'])).days < 1
            ]
            if recent_events:
                event_desc = f"Recentemente, {recent_events[0].get('description', 'algo interessante aconteceu aqui')}."
                dynamic_parts.append(event_desc)
        
        return " ".join(dynamic_parts) if dynamic_parts else ""
    
    def _generate_npc_activity_description(self, location: Location) -> str:
        """Generate description of NPC activities in a location"""
        
        if not location.npcs:
            return ""
        
        # Select a random NPC to describe their activity
        npc = random.choice(location.npcs)
        npc_name = npc.get('name', 'Um NPC')
        npc_role = npc.get('role', 'residente')
        
        activities = {
            'merchant': f"{npc_name} está organizando suas mercadorias e atendendo clientes.",
            'guard': f"{npc_name} mantém vigilância, observando os arredores com atenção.",
            'scholar': f"{npc_name} está absorto em seus estudos, folheando livros antigos.",
            'adventurer': f"{npc_name} compartilha histórias de suas aventuras com outros viajantes.",
            'commoner': f"{npc_name} realiza suas tarefas diárias com dedicação."
        }
        
        # Use AI to generate more specific activity descriptions
        activity_prompt = f"Descreva brevemente o que {npc_name}, um {npc_role}, "
        activity_prompt += f"está fazendo em {location.name}. Seja específico e envolvente."
        
        ai_activity = self.ai_engine.generate_world_building_response(activity_prompt)
        
        if ai_activity:
            return ai_activity
        else:
            # Fallback to template-based description
            return activities.get(npc_role.lower(), f"{npc_name} está ocupado com suas atividades.")
    
    def generate_npc_dialogue(self, 
                             npc: NPC, 
                             context: str, 
                             action: str,
                             player_id: str = None) -> str:
        """Generate NPC dialogue with memory and personality"""
        
        # Get NPC memory context
        npc_id = npc.name
        memory_context = ""
        
        if player_id:
            memory_context = self.memory_manager.get_npc_context_for_player(
                npc_id, player_id, action
            )
        
        # Determine dialogue topic and style
        dialogue_topic = self._determine_dialogue_topic(action, context)
        dialogue_style = self._get_npc_dialogue_style(npc)
        
        # Generate dialogue using AI with memory context
        dialogue_prompt = f"""
        NPC: {npc.name} ({npc.role})
        Personalidade: {self._get_npc_personality_summary(npc)}
        Estilo de diálogo: {dialogue_style}
        Tópico: {dialogue_topic}
        Contexto da memória: {memory_context}
        Ação do jogador: {action}
        
        Gere uma resposta natural e apropriada para este NPC, considerando sua personalidade, 
        o contexto da conversa e o que ele já sabe sobre o jogador. Seja criativo e evite repetição.
        """
        
        dialogue = self.ai_engine.generate_dialogue_response(dialogue_prompt)
        
        if not dialogue:
            # Fallback to template-based dialogue
            dialogue = self._generate_fallback_dialogue(npc, dialogue_topic, action)
        
        # Store conversation in memory
        if player_id:
            self.memory_manager.add_conversation(
                npc_id, player_id, dialogue_topic, action, dialogue, context
            )
        
        return dialogue
    
    def _determine_dialogue_topic(self, action: str, context: str) -> str:
        """Determine the main topic of the dialogue"""
        
        # Analyze action and context to determine topic
        action_lower = action.lower()
        
        if any(word in action_lower for word in ['ajuda', 'ajudar', 'problema']):
            return 'help'
        elif any(word in action_lower for word in ['história', 'passado', 'origem']):
            return 'background'
        elif any(word in action_lower for word in ['missão', 'trabalho', 'tarefa']):
            return 'quest'
        elif any(word in action_lower for word in ['rumores', 'notícias', 'informação']):
            return 'gossip'
        elif any(word in action_lower for word in ['comércio', 'venda', 'compra']):
            return 'trade'
        else:
            return 'general'
    
    def _get_npc_dialogue_style(self, npc: NPC) -> str:
        """Get the dialogue style for an NPC"""
        
        if hasattr(npc, 'personality') and npc.personality:
            return npc.personality.get('dialogue_style', 'neutral')
        
        # Determine style based on role
        role_styles = {
            'merchant': 'persuasivo',
            'guard': 'autoritário',
            'scholar': 'erudito',
            'adventurer': 'dramático',
            'commoner': 'casual'
        }
        
        return role_styles.get(npc.role.lower(), 'neutral')
    
    def _get_npc_personality_summary(self, npc: NPC) -> str:
        """Get a summary of NPC personality traits"""
        
        if hasattr(npc, 'personality') and npc.personality:
            traits = npc.personality.get('traits', [])
            if traits:
                return ', '.join(traits)
        
        # Generate personality based on role
        role_personalities = {
            'merchant': 'ambicioso, amigável, conhecedor de negócios',
            'guard': 'vigilante, disciplinado, protetor',
            'scholar': 'curioso, sábio, distraído',
            'adventurer': 'corajoso, experiente, contador de histórias',
            'commoner': 'trabalhador, curioso, amigável'
        }
        
        return role_personalities.get(npc.role.lower(), 'neutro')
    
    def _generate_fallback_dialogue(self, npc: NPC, topic: str, action: str) -> str:
        """Generate fallback dialogue when AI generation fails"""
        
        topic_responses = {
            'help': f"Claro, posso ajudar! O que você precisa?",
            'background': f"Ah, minha história? Bem, sou {npc.role} aqui em {npc.name}.",
            'quest': f"Missões? Sempre há algo interessante acontecendo por aqui.",
            'gossip': f"Rumores? Deixe-me pensar... Ah sim, ouvi algo interessante.",
            'trade': f"Comércio? Tenho algumas coisas que podem interessar você.",
            'general': f"Olá! Como posso ajudá-lo hoje?"
        }
        
        return topic_responses.get(topic, f"Olá! Sou {npc.name}, {npc.role}.")
    
    def create_atmospheric_event(self, location: Location) -> str:
        """Create atmospheric events for locations"""
        
        # Use AI to generate atmospheric events
        event_prompt = f"""
        Localização: {location.name}
        Tipo: {location.location_type}
        Clima: {getattr(self.world, 'weather', 'ensolarado')}
        Hora: {getattr(self.world, 'time_of_day', 'dia')}
        
        Crie um evento atmosférico pequeno e envolvente para esta localização. 
        Pode ser um som, uma mudança de luz, um movimento, ou algo similar. 
        Seja criativo mas sutil, para não distrair da narrativa principal.
        """
        
        atmospheric_event = self.ai_engine.generate_world_building_response(event_prompt)
        
        if not atmospheric_event:
            # Fallback atmospheric events
            fallback_events = [
                f"Uma brisa suave passa por {location.name}, carregando aromas familiares.",
                f"O som distante de passos ecoa pelas ruas próximas.",
                f"Uma sombra passa rapidamente, criando um momento de mistério.",
                f"O ar se torna mais denso, como se algo importante estivesse prestes a acontecer."
            ]
            atmospheric_event = random.choice(fallback_events)
        
        return atmospheric_event
    
    def expand_world_procedurally(self, 
                                expansion_type: str = 'organic',
                                num_locations: int = 3) -> List[Dict[str, Any]]:
        """Expand the world using procedural generation"""
        
        current_locations = list(self.world.locations.keys())
        
        if expansion_type == 'organic':
            # Expand organically based on existing locations
            new_content = self.procedural_generator.expand_world(
                current_locations, 'organic'
            )
        else:
            # Create specific types of locations
            new_content = []
            for _ in range(num_locations):
                location_type = random.choice(['city', 'wilderness', 'dungeon', 'tavern'])
                new_location = self.procedural_generator.generate_location(
                    location_type=location_type,
                    context=f"Expansão {expansion_type} do mundo"
                )
                
                # Add NPCs to the new location
                num_npcs = random.randint(1, 3)
                for _ in range(num_npcs):
                    npc_type = random.choice(['merchant', 'guard', 'scholar', 'adventurer', 'commoner'])
                    new_npc = self.procedural_generator.generate_npc(
                        npc_type=npc_type,
                        location_context=new_location['name']
                    )
                    new_location['npcs'].append(new_npc)
                
                new_content.append(new_location)
        
        # Add new content to the world
        for content in new_content:
            if 'name' in content:  # It's a location
                self._add_generated_location_to_world(content)
        
        logger.info(f"World expanded with {len(new_content)} new locations")
        return new_content
    
    def _add_generated_location_to_world(self, location_data: Dict[str, Any]) -> None:
        """Add a procedurally generated location to the world"""
        
        # Create Location object
        location = Location(
            location_data['name'],
            location_data['description'],
            location_data['location_type']
        )
        
        # Set additional properties
        location.ambiance = location_data.get('ambiance', '')
        location.size = location_data.get('size', 'médio')
        location.style = location_data.get('style', 'padrão')
        location.features = location_data.get('features', [])
        
        # Add NPCs
        for npc_data in location_data.get('npcs', []):
            npc = NPC(
                npc_data['name'],
                npc_data['role'],
                npc_data['description']
            )
            
            # Set personality and knowledge
            if 'personality' in npc_data:
                npc.personality = npc_data['personality']
            
            if 'knowledge' in npc_data:
                npc.knowledge = npc_data['knowledge']
            
            if 'dialogue_options' in npc_data:
                npc.dialogue_options = npc_data['dialogue_options']
            
            # Add to location
            location.add_npc(npc_data)
            
            # Add to world NPCs
            self.world.add_npc(npc)
        
        # Add to world
        self.world.add_location(location)
        
        logger.info(f"Added generated location '{location.name}' to world")
    
    def create_dynamic_quest(self, 
                           quest_type: str = None,
                           target_location: str = None) -> Dict[str, Any]:
        """Create dynamic quests using AI"""
        
        if not quest_type:
            quest_types = ['exploration', 'collection', 'escort', 'investigation', 'combat']
            quest_type = random.choice(quest_types)
        
        # Generate quest using AI
        quest_prompt = f"""
        Crie uma missão do tipo {quest_type} para um RPG. 
        A missão deve ser interessante, com objetivos claros e recompensas apropriadas.
        
        Inclua:
        - Título da missão
        - Descrição detalhada
        - Objetivos específicos
        - Recompensas
        - Dificuldade estimada
        - Dicas ou pistas
        
        Seja criativo e envolvente.
        """
        
        quest_description = self.ai_engine.generate_quest_response(quest_prompt)
        
        if not quest_description:
            # Fallback quest generation
            quest_description = self._generate_fallback_quest(quest_type)
        
        # Create quest data structure
        quest_data = {
            'title': f"Missão de {quest_type.title()}",
            'description': quest_description,
            'type': quest_type,
            'objectives': self._generate_quest_objectives(quest_type),
            'rewards': self._generate_quest_rewards(quest_type),
            'difficulty': random.choice(['fácil', 'médio', 'difícil', 'épico']),
            'target_location': target_location,
            'created_at': datetime.now().isoformat(),
            'status': 'available'
        }
        
        return quest_data
    
    def _generate_fallback_quest(self, quest_type: str) -> str:
        """Generate fallback quest when AI generation fails"""
        
        quest_templates = {
            'exploration': "Explore uma área desconhecida e descubra seus segredos.",
            'collection': "Colete itens específicos espalhados pelo mundo.",
            'escort': "Proteja um NPC importante durante uma jornada perigosa.",
            'investigation': "Investigue um mistério que está assombrando a região.",
            'combat': "Enfrente um inimigo poderoso que ameaça a paz local."
        }
        
        return quest_templates.get(quest_type, "Complete uma missão desafiadora.")
    
    def _generate_quest_objectives(self, quest_type: str) -> List[str]:
        """Generate quest objectives based on type"""
        
        objective_templates = {
            'exploration': [
                "Explorar a área designada",
                "Descobrir pontos de interesse",
                "Mapear o território",
                "Retornar com informações"
            ],
            'collection': [
                "Encontrar todos os itens necessários",
                "Verificar a qualidade dos itens",
                "Entregar os itens ao solicitante"
            ],
            'escort': [
                "Proteger o NPC durante a viagem",
                "Evitar perigos no caminho",
                "Chegar ao destino com segurança"
            ],
            'investigation': [
                "Coletar evidências",
                "Entrevistar testemunhas",
                "Analisar pistas",
                "Resolver o mistério"
            ],
            'combat': [
                "Localizar o inimigo",
                "Preparar-se para o combate",
                "Derrotar o oponente",
                "Confirmar a eliminação"
            ]
        }
        
        return objective_templates.get(quest_type, ["Completar a missão"])
    
    def _generate_quest_rewards(self, quest_type: str) -> List[str]:
        """Generate quest rewards based on type"""
        
        reward_templates = {
            'exploration': ["Experiência", "Conhecimento local", "Itens únicos"],
            'collection': ["Ouro", "Itens raros", "Fama"],
            'escort': ["Gratidão", "Recompensa monetária", "Aliados"],
            'investigation': ["Informações valiosas", "Reconhecimento", "Acesso a áreas restritas"],
            'combat': ["Experiência de combate", "Equipamento do inimigo", "Glória"]
        }
        
        return reward_templates.get(quest_type, ["Recompensa padrão"])
    
    def get_narrative_summary(self) -> Dict[str, Any]:
        """Get a summary of the narrative state"""
        
        return {
            'active_storylines': len(self.active_storylines),
            'world_events': len(self.world_events),
            'narrative_themes': self.narrative_themes,
            'procedural_stats': self.procedural_generator.get_generation_stats(),
            'memory_stats': self.memory_manager.get_memory_statistics(),
            'world_locations': len(self.world.locations),
            'world_npcs': len(self.world.npcs)
        }
