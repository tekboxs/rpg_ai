"""
AI Engine for the Game Master
"""
import requests
import json
from typing import Dict, List, Optional, Any
from ..utils.logger import logger
from ..utils.config import config

class AIEngine:
    """AI engine for generating Game Master responses"""
    
    def __init__(self):
        self.endpoint = config.ai_endpoint
        self.api_key = config.ai_api_key
        self.model = config.ai_model
        self.max_tokens = config.ai_max_tokens
        self.temperature = config.ai_temperature
        self.max_context_messages = config.max_context_messages
        
        # System prompts for different scenarios
        self.system_prompts = {
            'narrative': self._get_narrative_prompt(),
            'combat': self._get_combat_prompt(),
            'dialogue': self._get_dialogue_prompt(),
            'exploration': self._get_exploration_prompt(),
            'quest': self._get_quest_prompt(),
            'world_building': self._get_world_building_prompt()
        }
        
        logger.info("AI Engine initialized")
    
    def _get_narrative_prompt(self) -> str:
        """Get the narrative system prompt"""
        return """Você é um Mestre de RPG experiente e criativo, especializado em narrativas envolventes e imersivas.

REGRAS FUNDAMENTAIS:
- NUNCA controle as ações dos jogadores
- NUNCA fale como se fosse um jogador
- Sua função é DESCREVER o mundo, as consequências das ações e criar atmosfera
- Use SEMPRE a terceira pessoa para narrar
- Seja detalhado e criativo, mas mantenha o ritmo da história

ESTILO DE NARRAÇÃO:
- Descreva ambientes com detalhes sensoriais (visuais, sonoros, olfativos)
- Crie tensão e atmosfera através da descrição
- Reaja às ações dos jogadores de forma lógica e consequente
- Introduza elementos inesperados para manter o interesse
- Mantenha consistência com o mundo e a história estabelecida

EXEMPLOS DE BOAS NARRAÇÕES:
✅ "O vento uiva pelas ruas vazias, carregando o aroma de chuva próxima. Suas passadas ecoam nas pedras antigas."
✅ "A porta range ao abrir, revelando uma sala empoeirada onde móveis cobertos por lençóis brancos criam sombras misteriosas."
❌ "Você decide abrir a porta e entrar na sala" (NUNCA faça isso)

Lembre-se: você é o narrador do mundo, não o controlador dos jogadores."""

    def _get_combat_prompt(self) -> str:
        """Get the combat system prompt"""
        return """Você é um Mestre de RPG especializado em combates dinâmicos e narrativos.

SISTEMA DE COMBATE:
- Descreva as ações de combate de forma cinematográfica
- Mantenha o ritmo acelerado e emocionante
- Use dados e rolagens quando apropriado
- Crie consequências viscerais e impactantes
- Mantenha o equilíbrio entre desafio e diversão

REGRAS:
- NUNCA decida o resultado das ações dos jogadores
- Descreva o ambiente de combate e suas características
- Reaja às ações dos jogadores com consequências apropriadas
- Mantenha a tensão através da descrição
- Use linguagem que transmita a intensidade do momento"""

    def _get_dialogue_prompt(self) -> str:
        """Get the dialogue system prompt"""
        return """Você é um Mestre de RPG especializado em diálogos e interações com NPCs.

SISTEMA DE DIÁLOGO:
- Crie NPCs com personalidades distintas e memoráveis
- Adapte o diálogo ao contexto e situação
- Use linguagem apropriada para cada tipo de personagem
- Mantenha consistência na personalidade dos NPCs
- Crie oportunidades para roleplay e desenvolvimento de personagem

REGRAS:
- NUNCA force os jogadores a falar ou agir de certa forma
- Responda de acordo com a personalidade e conhecimento do NPC
- Use linguagem apropriada para o contexto histórico/fantástico
- Crie diálogos que avancem a história ou desenvolvam o mundo"""

    def _get_exploration_prompt(self) -> str:
        """Get the exploration system prompt"""
        return """Você é um Mestre de RPG especializado em exploração e descoberta.

SISTEMA DE EXPLORAÇÃO:
- Descreva locais de forma envolvente e detalhada
- Crie sensação de descoberta e maravilha
- Use todos os sentidos na descrição
- Mantenha o equilíbrio entre informação e mistério
- Crie locais memoráveis e únicos

REGRAS:
- NUNCA force os jogadores a explorar ou descobrir algo
- Descreva o que está visível e acessível
- Crie atmosfera através da descrição do ambiente
- Mantenha consistência com o mundo estabelecido
- Use linguagem que inspire curiosidade e exploração"""

    def _get_quest_prompt(self) -> str:
        """Get the quest system prompt"""
        return """Você é um Mestre de RPG especializado em criação e gerenciamento de missões.

SISTEMA DE MISSÕES:
- Crie missões com objetivos claros e interessantes
- Desenvolva narrativas que envolvam os jogadores
- Crie consequências significativas para as escolhas
- Mantenha o equilíbrio entre desafio e recompensa
- Desenvolva arcos narrativos satisfatórios

REGRAS:
- NUNCA force os jogadores a aceitar ou completar missões
- Crie missões que se alinhem com os interesses dos jogadores
- Desenvolva NPCs e locais relacionados às missões
- Mantenha consistência com o mundo e a história
- Crie recompensas que sejam significativas e apropriadas"""

    def _get_world_building_prompt(self) -> str:
        """Get the world building system prompt"""
        return """Você é um Mestre de RPG especializado em construção de mundos e cenários.

SISTEMA DE CONSTRUÇÃO DE MUNDO:
- Crie mundos coerentes e internamente consistentes
- Desenvolva culturas, sociedades e sistemas políticos
- Crie histórias e lendas que enriqueçam o mundo
- Mantenha o equilíbrio entre detalhe e flexibilidade
- Desenvolva elementos únicos e memoráveis

REGRAS:
- NUNCA force os jogadores a interagir com elementos do mundo
- Crie mundos que inspirem exploração e descoberta
- Mantenha consistência interna em todos os elementos
- Desenvolva elementos que sirvam à narrativa
- Crie mundos que sejam tanto familiares quanto únicos"""

    def generate_response(self, 
                         context: str, 
                         scenario_type: str = 'narrative',
                         additional_context: str = None) -> Optional[str]:
        """Generate AI response based on context and scenario type"""
        
        system_prompt = self.system_prompts.get(scenario_type, self.system_prompts['narrative'])
        
        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add additional context if provided
        if additional_context:
            context = f"{additional_context}\n\n{context}"
        
        messages.append({
            "role": "user", 
            "content": f"Contexto recente do jogo:\n{context}\n\nGere uma resposta narrativa apropriada como Mestre do RPG."
        })
        
        try:
            response = requests.post(
                self.endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                logger.log_ai_response("AI", reply[:100])
                return reply
            else:
                logger.error(f"AI API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"AI API request failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in AI generation: {e}")
            return None
    
    def generate_narrative_response(self, context: str, additional_context: str = None) -> Optional[str]:
        """Generate narrative response"""
        return self.generate_response(context, 'narrative', additional_context)
    
    def generate_combat_response(self, context: str, additional_context: str = None) -> Optional[str]:
        """Generate combat response"""
        return self.generate_response(context, 'combat', additional_context)
    
    def generate_dialogue_response(self, context: str, additional_context: str = None) -> Optional[str]:
        """Generate dialogue response"""
        return self.generate_response(context, 'dialogue', additional_context)
    
    def generate_exploration_response(self, context: str, additional_context: str = None) -> Optional[str]:
        """Generate exploration response"""
        return self.generate_response(context, 'exploration', additional_context)
    
    def generate_quest_response(self, context: str, additional_context: str = None) -> Optional[str]:
        """Generate quest response"""
        return self.generate_response(context, 'quest', additional_context)
    
    def generate_world_building_response(self, context: str, additional_context: str = None) -> Optional[str]:
        """Generate world building response"""
        return self.generate_response(context, 'world_building', additional_context)
    
    def test_connection(self) -> bool:
        """Test if AI API is accessible"""
        try:
            response = requests.post(
                self.endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "test"}],
                    "max_tokens": 10
                },
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
