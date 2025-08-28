"""
Narrative system for the Game Master
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import random
from ..utils.logger import logger
from ..core.world import World, Location, NPC

class NarrativeEngine:
    """Handles narrative generation and story progression"""
    
    def __init__(self, world: World):
        self.world = world
        self.story_arcs = []
        self.active_plots = []
        self.character_development = {}
        self.atmosphere_markers = []
        
        # Narrative templates and patterns
        self.narrative_patterns = self._load_narrative_patterns()
        self.atmosphere_descriptions = self._load_atmosphere_descriptions()
        
        logger.info("Narrative Engine initialized")
    
    def _load_narrative_patterns(self) -> Dict[str, List[str]]:
        """Load narrative patterns for different scenarios"""
        return {
            'arrival': [
                "O ar muda sutilmente conforme você se aproxima de {location}. {atmosphere}",
                "Uma sensação de {emotion} paira sobre {location}. {atmosphere}",
                "Os primeiros sinais de {location} aparecem à distância. {atmosphere}"
            ],
            'exploration': [
                "Cada passo revela novos detalhes sobre {location}. {atmosphere}",
                "A exploração de {location} revela {discovery}. {atmosphere}",
                "Conforme você investiga {location}, {observation} se torna aparente. {atmosphere}"
            ],
            'interaction': [
                "A presença de {npc} adiciona uma nova dimensão ao ambiente. {atmosphere}",
                "A interação com {npc} revela {insight}. {atmosphere}",
                "O diálogo com {npc} traz {information} à tona. {atmosphere}"
            ],
            'discovery': [
                "Uma descoberta inesperada aguarda em {location}. {atmosphere}",
                "O que você encontra em {location} supera suas expectativas. {atmosphere}",
                "Uma revelação surpreendente emerge de {location}. {atmosphere}"
            ]
        }
    
    def _load_atmosphere_descriptions(self) -> Dict[str, List[str]]:
        """Load atmospheric descriptions for different moods"""
        return {
            'mysterious': [
                "Uma aura de mistério envolve o local, fazendo com que até os sons mais familiares pareçam estranhos.",
                "Sombras dançam nas bordas da visão, criando formas que a mente insiste em interpretar.",
                "O silêncio aqui tem peso, carregando consigo a promessa de segredos por descobrir."
            ],
            'peaceful': [
                "Uma sensação de calma serena preenche o ar, como se o tempo aqui fluísse mais lentamente.",
                "O ambiente respira tranquilidade, oferecendo um refúgio dos problemas do mundo exterior.",
                "Uma paz natural permeia o local, convidando à contemplação e reflexão."
            ],
            'dangerous': [
                "Uma tensão palpável paira no ar, alertando os sentidos para possíveis ameaças.",
                "O ambiente carrega uma energia ameaçadora, fazendo com que cada som seja potencialmente perigoso.",
                "Uma sensação de perigo iminente faz com que os pelos da nuca se eriçem."
            ],
            'energetic': [
                "O local pulsa com energia vital, fazendo com que seja impossível não se sentir revigorado.",
                "Uma vibração positiva preenche o ar, contagiando todos que aqui chegam.",
                "O ambiente irradia entusiasmo e possibilidade, inspirando ação e criatividade."
            ],
            'melancholic': [
                "Uma melancolia sutil permeia o local, como se as paredes guardassem memórias tristes.",
                "O ar carrega o peso de histórias não contadas e sonhos não realizados.",
                "Uma nostalgia suave envolve o ambiente, convidando à reflexão sobre o passado."
            ]
        }
    
    def generate_location_description(self, location: Location, mood: str = None) -> str:
        """Generate a rich description for a location"""
        if not mood:
            mood = random.choice(list(self.atmosphere_descriptions.keys()))
        
        # Get base description
        base_desc = location.get_description(include_details=True)
        
        # Add atmospheric elements
        atmosphere = random.choice(self.atmosphere_descriptions.get(mood, self.atmosphere_descriptions['mysterious']))
        
        # Add time and weather context
        time_context = self._get_time_context()
        weather_context = self._get_weather_context()
        
        # Combine everything
        full_description = f"{base_desc}\n\n{atmosphere}\n\n{time_context}\n{weather_context}"
        
        return full_description
    
    def _get_time_context(self) -> str:
        """Generate time-based context"""
        time_of_day = self.world.time_of_day
        
        time_descriptions = {
            'madrugada': "A madrugada traz consigo um silêncio profundo, onde até os sons mais sutis ecoam com clareza cristalina.",
            'manhã': "A manhã banha o local com luz dourada, trazendo renovação e possibilidades para o novo dia.",
            'tarde': "A tarde traz consigo a energia do dia em pleno vigor, com atividade e movimento por todos os lados.",
            'noite': "A noite envolve o local em sombras misteriosas, onde a imaginação pode dar vida a qualquer som ou movimento."
        }
        
        return time_descriptions.get(time_of_day, "")
    
    def _get_weather_context(self) -> str:
        """Generate weather-based context"""
        weather = self.world.weather
        
        weather_descriptions = {
            'ensolarado': "O sol brilha intensamente, criando sombras nítidas e um calor que convida ao descanso.",
            'nublado': "Nuvens cinzentas cobrem o céu, criando uma atmosfera mais introspectiva e contemplativa.",
            'chuvoso': "A chuva cai suavemente, criando um som reconfortante e limpando o ar de poeira e tensão.",
            'tempestuoso': "Uma tempestade se aproxima, trazendo consigo eletricidade no ar e uma sensação de poder da natureza.",
            'nevando': "Flocos de neve dançam no ar, criando um cenário mágico e silencioso."
        }
        
        return weather_descriptions.get(weather, "")
    
    def create_story_arc(self, title: str, description: str, locations: List[str], 
                         npcs: List[str], quests: List[Dict]) -> Dict:
        """Create a new story arc"""
        story_arc = {
            'id': f"arc_{len(self.story_arcs) + 1}",
            'title': title,
            'description': description,
            'locations': locations,
            'npcs': npcs,
            'quests': quests,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'progress': 0.0,
            'milestones': []
        }
        
        self.story_arcs.append(story_arc)
        logger.info(f"New story arc created: {title}")
        
        return story_arc
    
    def advance_story_arc(self, arc_id: str, progress: float, milestone: str = None):
        """Advance the progress of a story arc"""
        for arc in self.story_arcs:
            if arc['id'] == arc_id:
                arc['progress'] = min(1.0, arc['progress'] + progress)
                
                if milestone:
                    arc['milestones'].append({
                        'description': milestone,
                        'timestamp': datetime.now().isoformat(),
                        'progress': arc['progress']
                    })
                
                if arc['progress'] >= 1.0:
                    arc['status'] = 'completed'
                    logger.info(f"Story arc completed: {arc['title']}")
                else:
                    logger.info(f"Story arc progress: {arc['title']} - {arc['progress']:.1%}")
                break
    
    def generate_npc_dialogue(self, npc: NPC, context: str, player_action: str) -> str:
        """Generate appropriate dialogue for an NPC based on context"""
        # Analyze the context and player action
        if 'saudação' in player_action.lower() or 'olá' in player_action.lower():
            return self._generate_greeting(npc)
        elif 'pergunta' in player_action.lower() or 'pergunt' in player_action.lower():
            return self._generate_informative_response(npc, context)
        elif 'ajuda' in player_action.lower() or 'socorro' in player_action.lower():
            return self._generate_helpful_response(npc)
        else:
            return self._generate_contextual_response(npc, context, player_action)
    
    def _generate_greeting(self, npc: NPC) -> str:
        """Generate a greeting response for an NPC"""
        greetings = [
            f"Olá, viajante! Bem-vindo à {npc.role.lower()}.",
            f"Saudações! É um prazer receber visitantes aqui.",
            f"Oi! Que bom ter você por aqui hoje.",
            f"Bem-vindo! Como posso ajudá-lo?"
        ]
        
        return random.choice(greetings)
    
    def _generate_informative_response(self, npc: NPC, context: str) -> str:
        """Generate an informative response based on NPC knowledge"""
        if npc.knowledge:
            # Find relevant knowledge
            relevant_knowledge = []
            for knowledge in npc.knowledge:
                if any(word in context.lower() for word in knowledge['topic'].lower().split()):
                    relevant_knowledge.append(knowledge)
            
            if relevant_knowledge:
                knowledge = random.choice(relevant_knowledge)
                return f"Ah, sobre {knowledge['topic']}? {knowledge['information']}"
        
        return "Hmm, não tenho certeza sobre isso. Talvez você possa perguntar a alguém mais experiente?"
    
    def _generate_helpful_response(self, npc: NPC) -> str:
        """Generate a helpful response for NPCs"""
        helpful_responses = [
            "Claro, estarei feliz em ajudar! O que você precisa?",
            "É para isso que estou aqui! Como posso ser útil?",
            "Sem problemas! Vamos resolver isso juntos.",
            "Estou à disposição para ajudar no que for possível."
        ]
        
        return random.choice(helpful_responses)
    
    def _generate_contextual_response(self, npc: NPC, context: str, player_action: str) -> str:
        """Generate a contextual response based on the situation"""
        # Analyze the player's action and generate appropriate response
        if 'combate' in player_action.lower() or 'luta' in player_action.lower():
            return "Cuidado com o combate! É sempre melhor resolver as coisas pacificamente quando possível."
        elif 'explorar' in player_action.lower() or 'investigar' in player_action.lower():
            return "Exploração é sempre uma boa ideia! Você nunca sabe o que pode descobrir."
        elif 'comprar' in player_action.lower() or 'vender' in player_action.lower():
            return "Ah, você está interessado em comércio? Posso ter algumas sugestões para você."
        else:
            return "Interessante! Continue explorando e descobrindo o que este mundo tem a oferecer."
    
    def create_atmospheric_event(self, location: Location, event_type: str = 'random') -> str:
        """Create an atmospheric event to enhance the narrative"""
        if event_type == 'random':
            event_type = random.choice(['sound', 'visual', 'environmental', 'social'])
        
        event_descriptions = {
            'sound': [
                "Um som distante ecoa pelas ruas, sua origem impossível de determinar.",
                "O vento sussurra através das frestas, criando uma melodia misteriosa.",
                "Passos distantes ressoam nas pedras, aproximando-se e depois afastando-se."
            ],
            'visual': [
                "Uma sombra se move rapidamente no canto da visão, desaparecendo antes que você possa focar nela.",
                "Luzes dançam nas janelas distantes, criando padrões que mudam constantemente.",
                "Reflexos na água criam imagens distorcidas que parecem se mover independentemente."
            ],
            'environmental': [
                "O ar muda sutilmente, trazendo consigo novos aromas e sensações.",
                "A temperatura flutua, criando uma sensação de mudança iminente.",
                "Elementos do ambiente se reorganizam sutilmente, como se o local tivesse vida própria."
            ],
            'social': [
                "Conversas distantes chegam aos seus ouvidos, palavras individuais impossíveis de distinguir.",
                "Risadas ecoam de algum lugar próximo, trazendo uma sensação de alegria e comunidade.",
                "O som de atividades diárias preenche o ar, criando uma sensação de vida e movimento."
            ]
        }
        
        description = random.choice(event_descriptions.get(event_type, event_descriptions['sound']))
        
        # Add location-specific context
        if location.location_type == 'tavern':
            description += " A atmosfera da taverna parece absorver e amplificar o evento."
        elif location.location_type == 'city':
            description += " A vida da cidade continua ao redor, aparentemente indiferente ao que aconteceu."
        
        return description
    
    def get_narrative_summary(self) -> Dict[str, Any]:
        """Get a summary of the current narrative state"""
        return {
            'active_story_arcs': len([arc for arc in self.story_arcs if arc['status'] == 'active']),
            'completed_story_arcs': len([arc for arc in self.story_arcs if arc['status'] == 'completed']),
            'total_story_arcs': len(self.story_arcs),
            'active_plots': len(self.active_plots),
            'character_development_entries': len(self.character_development),
            'atmosphere_markers': len(self.atmosphere_markers),
            'world_mood': self._determine_world_mood()
        }
    
    def _determine_world_mood(self) -> str:
        """Determine the overall mood of the world based on current events"""
        # This is a simplified version - in a real implementation, you'd analyze
        # various factors like recent events, player actions, story progress, etc.
        moods = ['peaceful', 'mysterious', 'dangerous', 'energetic', 'melancholic']
        return random.choice(moods)
