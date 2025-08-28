"""
NPC Memory System for RPG AI
Tracks conversations, interactions, and context to avoid repetition
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
from ..utils.logger import logger

class ConversationMemory:
    """Tracks conversation history and context for an NPC"""
    
    def __init__(self, npc_id: str, max_memory_size: int = 100):
        self.npc_id = npc_id
        self.max_memory_size = max_memory_size
        self.conversations = []  # List of conversation sessions
        self.player_interactions = {}  # Player-specific interaction history
        self.topic_memory = {}  # What topics have been discussed
        self.emotional_state = {
            'mood': 'neutral',
            'trust_level': 0,
            'interest_level': 0,
            'last_interaction': None
        }
        
        logger.info(f"Conversation memory initialized for NPC {npc_id}")
    
    def add_conversation(self, 
                        player_id: str, 
                        topic: str, 
                        player_message: str, 
                        npc_response: str,
                        context: str = None) -> None:
        """Add a new conversation to memory"""
        
        conversation_entry = {
            'timestamp': datetime.now().isoformat(),
            'player_id': player_id,
            'topic': topic,
            'player_message': player_message,
            'npc_response': npc_response,
            'context': context,
            'session_id': self._get_session_id(player_id)
        }
        
        self.conversations.append(conversation_entry)
        
        # Update player interactions
        if player_id not in self.player_interactions:
            self.player_interactions[player_id] = []
        
        self.player_interactions[player_id].append(conversation_entry)
        
        # Update topic memory
        if topic not in self.topic_memory:
            self.topic_memory[topic] = []
        
        self.topic_memory[topic].append(conversation_entry)
        
        # Update emotional state
        self._update_emotional_state(player_id, topic, player_message)
        
        # Clean up old memories if needed
        self._cleanup_old_memories()
        
        logger.debug(f"Added conversation to memory for NPC {self.npc_id}")
    
    def get_recent_conversations(self, 
                               player_id: str = None, 
                               topic: str = None, 
                               limit: int = 5) -> List[Dict]:
        """Get recent conversations, optionally filtered by player or topic"""
        
        if player_id and topic:
            # Filter by both player and topic
            filtered = [
                conv for conv in self.conversations
                if conv['player_id'] == player_id and conv['topic'] == topic
            ]
        elif player_id:
            # Filter by player only
            filtered = [
                conv for conv in self.conversations
                if conv['player_id'] == player_id
            ]
        elif topic:
            # Filter by topic only
            filtered = [
                conv for conv in self.conversations
                if conv['topic'] == topic
            ]
        else:
            # No filter
            filtered = self.conversations
        
        # Sort by timestamp and return most recent
        filtered.sort(key=lambda x: x['timestamp'], reverse=True)
        return filtered[:limit]
    
    def has_discussed_topic(self, 
                           player_id: str, 
                           topic: str, 
                           within_hours: int = 24) -> bool:
        """Check if a topic was recently discussed with a specific player"""
        
        if topic not in self.topic_memory:
            return False
        
        cutoff_time = datetime.now() - timedelta(hours=within_hours)
        
        for conv in self.topic_memory[topic]:
            if (conv['player_id'] == player_id and 
                datetime.fromisoformat(conv['timestamp']) > cutoff_time):
                return True
        
        return False
    
    def get_topic_summary(self, topic: str) -> str:
        """Get a summary of what has been discussed about a topic"""
        
        if topic not in self.topic_memory:
            return f"Não tenho informações sobre {topic}."
        
        conversations = self.topic_memory[topic]
        if not conversations:
            return f"Não tenho informações sobre {topic}."
        
        # Group by player to see who knows what
        player_knowledge = {}
        for conv in conversations:
            player_id = conv['player_id']
            if player_id not in player_knowledge:
                player_knowledge[player_id] = []
            player_knowledge[player_id].append(conv)
        
        summary = f"Já conversei sobre {topic} com {len(player_knowledge)} pessoa(s). "
        
        # Add specific details if there are recent conversations
        recent_conversations = [
            conv for conv in conversations
            if datetime.fromisoformat(conv['timestamp']) > 
            (datetime.now() - timedelta(hours=6))
        ]
        
        if recent_conversations:
            summary += f"Recentemente, discutimos sobre isso."
        
        return summary
    
    def get_player_relationship_context(self, player_id: str) -> Dict[str, Any]:
        """Get context about the relationship with a specific player"""
        
        if player_id not in self.player_interactions:
            return {
                'interaction_count': 0,
                'first_interaction': None,
                'last_interaction': None,
                'topics_discussed': [],
                'trust_level': 0,
                'mood_towards_player': 'neutral'
            }
        
        interactions = self.player_interactions[player_id]
        
        # Get topics discussed
        topics = list(set([conv['topic'] for conv in interactions]))
        
        # Calculate trust level based on interaction frequency and topics
        trust_level = min(len(interactions) * 2, 10)  # 0-10 scale
        
        # Determine mood towards player
        if trust_level >= 7:
            mood = 'friendly'
        elif trust_level >= 4:
            mood = 'neutral'
        else:
            mood = 'cautious'
        
        return {
            'interaction_count': len(interactions),
            'first_interaction': min([conv['timestamp'] for conv in interactions]),
            'last_interaction': max([conv['timestamp'] for conv in interactions]),
            'topics_discussed': topics,
            'trust_level': trust_level,
            'mood_towards_player': mood
        }
    
    def _get_session_id(self, player_id: str) -> str:
        """Generate a session ID for tracking conversation sessions"""
        return f"{player_id}_{datetime.now().strftime('%Y%m%d_%H')}"
    
    def _update_emotional_state(self, player_id: str, topic: str, message: str) -> None:
        """Update NPC's emotional state based on interaction"""
        
        # Update last interaction time
        self.emotional_state['last_interaction'] = datetime.now().isoformat()
        
        # Simple mood analysis based on message content
        positive_words = ['obrigado', 'obrigada', 'amigo', 'amiga', 'ajuda', 'bom', 'boa']
        negative_words = ['ruim', 'mau', 'má', 'problema', 'perigo', 'medo', 'raiva']
        
        message_lower = message.lower()
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            self.emotional_state['mood'] = 'positive'
            self.emotional_state['trust_level'] = min(10, self.emotional_state['trust_level'] + 1)
        elif negative_count > positive_count:
            self.emotional_state['mood'] = 'negative'
            self.emotional_state['trust_level'] = max(0, self.emotional_state['trust_level'] - 1)
        
        # Update interest level based on topic variety
        unique_topics = len(set([conv['topic'] for conv in self.conversations]))
        self.emotional_state['interest_level'] = min(10, unique_topics)
    
    def _cleanup_old_memories(self) -> None:
        """Remove old memories to prevent memory overflow"""
        
        if len(self.conversations) <= self.max_memory_size:
            return
        
        # Remove oldest conversations
        self.conversations.sort(key=lambda x: x['timestamp'])
        conversations_to_remove = len(self.conversations) - self.max_memory_size
        
        removed_conversations = self.conversations[:conversations_to_remove]
        self.conversations = self.conversations[conversations_to_remove:]
        
        # Clean up references in other data structures
        for conv in removed_conversations:
            player_id = conv['player_id']
            topic = conv['topic']
            
            # Remove from player interactions
            if player_id in self.player_interactions:
                self.player_interactions[player_id] = [
                    c for c in self.player_interactions[player_id]
                    if c['timestamp'] != conv['timestamp']
                ]
            
            # Remove from topic memory
            if topic in self.topic_memory:
                self.topic_memory[topic] = [
                    c for c in self.topic_memory[topic]
                    if c['timestamp'] != conv['timestamp']
                ]
        
        logger.debug(f"Cleaned up {conversations_to_remove} old conversations from NPC {self.npc_id}")
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of the NPC's memory state"""
        
        return {
            'total_conversations': len(self.conversations),
            'unique_players': len(self.player_interactions),
            'topics_discussed': list(self.topic_memory.keys()),
            'emotional_state': self.emotional_state,
            'memory_usage': len(self.conversations) / self.max_memory_size
        }
    
    def export_memory(self) -> Dict[str, Any]:
        """Export memory data for saving/loading"""
        
        return {
            'npc_id': self.npc_id,
            'max_memory_size': self.max_memory_size,
            'conversations': self.conversations,
            'player_interactions': self.player_interactions,
            'topic_memory': self.topic_memory,
            'emotional_state': self.emotional_state
        }
    
    def import_memory(self, memory_data: Dict[str, Any]) -> None:
        """Import memory data from saved state"""
        
        self.npc_id = memory_data.get('npc_id', self.npc_id)
        self.max_memory_size = memory_data.get('max_memory_size', self.max_memory_size)
        self.conversations = memory_data.get('conversations', [])
        self.player_interactions = memory_data.get('player_interactions', {})
        self.topic_memory = memory_data.get('topic_memory', {})
        self.emotional_state = memory_data.get('emotional_state', self.emotional_state)
        
        logger.info(f"Memory imported for NPC {self.npc_id}")

class NPCMemoryManager:
    """Manages memory for all NPCs in the world"""
    
    def __init__(self):
        self.npc_memories = {}  # npc_id -> ConversationMemory
        self.global_context = {}  # World-level context that affects all NPCs
        self.logger = logger
        
        logger.info("NPC Memory Manager initialized")
    
    def get_npc_memory(self, npc_id: str) -> ConversationMemory:
        """Get or create memory for an NPC"""
        
        if npc_id not in self.npc_memories:
            self.npc_memories[npc_id] = ConversationMemory(npc_id)
        
        return self.npc_memories[npc_id]
    
    def add_conversation(self, 
                        npc_id: str, 
                        player_id: str, 
                        topic: str, 
                        player_message: str, 
                        npc_response: str,
                        context: str = None) -> None:
        """Add a conversation to an NPC's memory"""
        
        memory = self.get_npc_memory(npc_id)
        memory.add_conversation(player_id, topic, player_message, npc_response, context)
    
    def get_npc_context_for_player(self, 
                                 npc_id: str, 
                                 player_id: str, 
                                 topic: str = None) -> str:
        """Get context about what an NPC knows about a player and topic"""
        
        memory = self.get_npc_memory(npc_id)
        
        # Check if topic was recently discussed
        if topic and memory.has_discussed_topic(player_id, topic):
            return f"Já conversamos sobre {topic} recentemente. "
        
        # Get relationship context
        relationship = memory.get_player_relationship_context(player_id)
        
        context_parts = []
        
        if relationship['interaction_count'] == 0:
            context_parts.append("É nossa primeira conversa.")
        else:
            context_parts.append(f"Já conversamos {relationship['interaction_count']} vez(es) antes.")
            
            if relationship['mood_towards_player'] == 'friendly':
                context_parts.append("Considero você um amigo.")
            elif relationship['mood_towards_player'] == 'cautious':
                context_parts.append("Ainda estou conhecendo você.")
        
        # Add topic context if available
        if topic:
            topic_summary = memory.get_topic_summary(topic)
            context_parts.append(topic_summary)
        
        return " ".join(context_parts)
    
    def update_global_context(self, event_type: str, description: str) -> None:
        """Update global context that affects all NPCs"""
        
        self.global_context[event_type] = {
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Global context updated: {event_type}")
    
    def get_global_context_summary(self) -> str:
        """Get a summary of recent global events"""
        
        if not self.global_context:
            return "O mundo está em um estado normal."
        
        recent_events = []
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        for event_type, event_data in self.global_context.items():
            event_time = datetime.fromisoformat(event_data['timestamp'])
            if event_time > cutoff_time:
                recent_events.append(f"{event_type}: {event_data['description']}")
        
        if recent_events:
            return "Eventos recentes no mundo: " + "; ".join(recent_events)
        else:
            return "O mundo está em um estado normal."
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get statistics about all NPC memories"""
        
        total_conversations = sum(
            len(memory.conversations) for memory in self.npc_memories.values()
        )
        
        total_players = set()
        for memory in self.npc_memories.values():
            total_players.update(memory.player_interactions.keys())
        
        return {
            'total_npcs_with_memory': len(self.npc_memories),
            'total_conversations': total_conversations,
            'total_unique_players': len(total_players),
            'global_context_events': len(self.global_context),
            'memory_usage_per_npc': {
                npc_id: memory.get_memory_summary()['memory_usage']
                for npc_id, memory in self.npc_memories.items()
            }
        }
    
    def export_all_memories(self) -> Dict[str, Any]:
        """Export all NPC memories for saving"""
        
        return {
            'npc_memories': {
                npc_id: memory.export_memory()
                for npc_id, memory in self.npc_memories.items()
            },
            'global_context': self.global_context
        }
    
    def import_all_memories(self, memory_data: Dict[str, Any]) -> None:
        """Import all NPC memories from saved state"""
        
        # Import NPC memories
        for npc_id, memory_data in memory_data.get('npc_memories', {}).items():
            memory = ConversationMemory(npc_id)
            memory.import_memory(memory_data)
            self.npc_memories[npc_id] = memory
        
        # Import global context
        self.global_context = memory_data.get('global_context', {})
        
        logger.info(f"Imported memories for {len(self.npc_memories)} NPCs")
