"""
Network server for RPG AI system
"""
import socket
import threading
import time
from typing import Dict, Optional
from pathlib import Path
from ..core.game_state import GameState
from ..core.player import Player, PlayerManager
from ..game_master.simple_master import SimpleGameMaster
from ..utils.logger import logger
from ..utils.config import config

class RPGGameServer:
    """Main RPG game server"""
    
    def __init__(self):
        self.game_state = GameState()
        self.player_manager = PlayerManager(max_players=config.max_players)
        self.game_master = SimpleGameMaster(self.game_state)
        
        # Server state
        self.is_running = False
        self.server_socket = None
        self.auto_save_thread = None
        
        # Create saves directory
        Path("saves").mkdir(exist_ok=True)
        
        logger.info("RPG Game Server initialized")
    
    def start_server(self, host: str = None, port: int = None):
        """Start the RPG server"""
        if self.is_running:
            logger.warning("Server is already running")
            return
        
        host = host or config.server_host
        port = port or config.server_port
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((host, port))
            self.server_socket.listen(config.max_players)
            
            self.is_running = True
            
            # Start auto-save thread
            self.auto_save_thread = threading.Thread(target=self._auto_save_loop, daemon=True)
            self.auto_save_thread.start()
            
            # Start the game session
            self.game_state.start_new_session("Sessão Principal")
            
            logger.info(f"🚀 Servidor RPG iniciado em {host}:{port}")
            logger.info(f"📊 Máximo de jogadores: {config.max_players}")
            logger.info(f"🌍 Mundo: {self.game_state.world.name}")
            
            # Main server loop
            self._accept_connections()
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            self.shutdown()
    
    def _accept_connections(self):
        """Accept incoming client connections"""
        try:
            while self.is_running:
                try:
                    conn, addr = self.server_socket.accept()
                    logger.info(f"Nova conexão de {addr}")
                    
                    # Start client handler thread
                    client_thread = threading.Thread(
                        target=self._handle_client, 
                        args=(conn, addr), 
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error:
                    if self.is_running:
                        logger.error("Socket error in accept loop")
                    break
                    
        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
            self.shutdown()
    
    def _handle_client(self, conn: socket.socket, addr):
        """Handle individual client connection"""
        player = None
        
        try:
            # Set socket options for better handling
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            
            # Get player name
            player_name = self._get_player_name(conn)
            if not player_name:
                logger.warning(f"Failed to get player name from {addr}")
                return
            
            # Create player
            player = self.player_manager.add_player(player_name, conn)
            if not player:
                conn.sendall("❌ Servidor cheio ou erro ao criar jogador.".encode('utf-8'))
                return
            
            # Set initial location
            self.game_state.set_player_location(player.id, config.world_default_location)
            
            # Send welcome message
            welcome_msg = self._create_welcome_message(player)
            player.send_message(welcome_msg)
            
            # Broadcast player arrival
            self.player_manager.broadcast_message(
                f"✨ {player.name} entrou no jogo!",
                exclude_player=player
            )
            
            # Add to game history
            self.game_state.add_to_history(
                "Sistema", 
                f"{player.name} entrou no jogo", 
                "system"
            )
            
            logger.info(f"Player {player.name} successfully connected from {addr}")
            
            # Main client loop
            self._client_message_loop(player, conn)
            
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
            # Try to send error message to client
            try:
                if conn:
                    conn.sendall("❌ Erro interno do servidor.".encode('utf-8'))
            except:
                pass
        finally:
            if player:
                self._handle_player_disconnect(player)
            try:
                conn.close()
            except:
                pass
    
    def _get_player_name(self, conn: socket.socket) -> Optional[str]:
        """Get player name from client"""
        try:
            # Send name request
            conn.sendall("🎮 Digite seu nome de jogador: ".encode('utf-8'))
            
            # Wait for response (sem timeout - ilimitado)
            timeout_value = config.get('server.player_name_timeout', 0)
            conn.settimeout(timeout_value if timeout_value > 0 else None)
            data = conn.recv(1024)
            
            if data:
                # Try multiple encoding strategies
                name = None
                encoding_attempts = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                
                for encoding in encoding_attempts:
                    try:
                        name = data.decode(encoding).strip()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if name is None:
                    # If all encodings fail, use error handling
                    name = data.decode('utf-8', errors='ignore').strip()
                if name and len(name) <= 20:
                    return name
                else:
                    conn.sendall("❌ Nome inválido. Deve ter entre 1 e 20 caracteres.".encode('utf-8'))
                    return None
            
            return None
            
        except socket.timeout:
            conn.sendall("❌ Timeout ao aguardar nome.".encode('utf-8'))
            return None
        except Exception as e:
            logger.error(f"Error getting player name: {e}")
            return None
    
    def _create_welcome_message(self, player: Player) -> str:
        """Create welcome message for new player"""
        current_location = self.game_state.get_player_location(player.id)
        location_desc = self.game_state.get_location_description(current_location)
        
        welcome_msg = f"""
🎲 **BEM-VINDO AO RPG AI SIMPLIFICADO, {player.name}!**

{location_desc}

💡 **SISTEMA SIMPLIFICADO - COMANDOS RÁPIDOS:**
- {{ajuda}} - Ver todos os comandos
- {{status}} - Seu status e da fila de ações
- {{explorar}} - Explorar localização atual
- {{fazer <ação>}} - Adicionar ação à fila
- {{dizer <fala>}} - Adicionar fala à fila
- {{historia <elemento>}} - Adicionar elemento narrativo à fila
- {{mestre}} - Processar todas as ações em fila

🎭 **COMO FUNCIONA:**
- Use {{fazer}}, {{dizer}} ou {{historia}} para suas ações
- Todas ficam em fila até usar {{mestre}}
- O {{mestre}} processa tudo e gera nova cena
- Você tem controle total sobre a narrativa!

🌍 **MUNDO ATUAL:**
- Clima: {self.game_state.world.weather}
- Hora: {self.game_state.world.time_of_day}
- Jogadores online: {len(self.player_manager.players)}

🎯 **DICA:** Comece com {{fazer explorar a área}} e depois use {{mestre}}!

Divirta-se e boa aventura!
        """.strip()
        
        return welcome_msg
    
    def _client_message_loop(self, player: Player, conn: socket.socket):
        """Main loop for handling client messages"""
        while self.is_running and player.is_active(config.get('game.session_timeout', 0)):
            try:
                data = conn.recv(4096)
                if not data:
                    break
                
                # Try multiple encoding strategies for message decoding
                message = None
                encoding_attempts = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                
                for encoding in encoding_attempts:
                    try:
                        message = data.decode(encoding).strip()
                        break
                    except UnicodeDecodeError:
                        continue
                
                if message is None:
                    # If all encodings fail, use error handling
                    message = data.decode('utf-8', errors='ignore').strip()
                if not message:
                    continue
                
                # Clean the message of any invalid characters
                message = ''.join(char for char in message if char.isprintable())
                if not message:
                    continue
                
                # Process message through Game Master
                response = self.game_master.process_player_action(player, message)
                
                # Broadcast player action to all players
                if response:
                    # Game Master provided a response
                    broadcast_msg = f"\n👤 {player.name}: {message}\n📜 Mestre: {response}\n"
                else:
                    # Regular roleplay action
                    broadcast_msg = f"\n👤 {player.name}: {message}\n"
                
                self.player_manager.broadcast_message(broadcast_msg)
                
                # Update player activity
                player.update_activity()
                
            except socket.timeout:
                continue  # Continue on timeout
            except Exception as e:
                logger.error(f"Error in client message loop for {player.name}: {e}")
                break
    
    def _handle_player_disconnect(self, player: Player):
        """Handle player disconnection"""
        try:
            # Remove player from manager
            self.player_manager.remove_player(player.id)
            
            # Remove from game state
            if player.id in self.game_state.player_locations:
                del self.game_state.player_locations[player.id]
            
            # Broadcast departure
            self.player_manager.broadcast_message(f"❌ {player.name} saiu do jogo.")
            
            # Add to game history
            self.game_state.add_to_history(
                "Sistema", 
                f"{player.name} saiu do jogo", 
                "system"
            )
            
            logger.info(f"Player {player.name} disconnected")
            
        except Exception as e:
            logger.error(f"Error handling player disconnect: {e}")
    
    def _auto_save_loop(self):
        """Auto-save game state periodically"""
        while self.is_running:
            try:
                time.sleep(config.get('game.auto_save_interval', 60))
                
                if self.is_running:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"saves/auto_save_{timestamp}.json"
                    
                    self.game_state.save_game_state(filename)
                    logger.info(f"Auto-save completed: {filename}")
                    
            except Exception as e:
                logger.error(f"Auto-save failed: {e}")
    
    def get_server_status(self) -> Dict:
        """Get current server status"""
        return {
            'is_running': self.is_running,
            'total_players': len(self.player_manager.players),
            'active_players': len(self.player_manager.get_active_players()),
            'max_players': config.max_players,
            'game_master_status': self.game_master.get_game_master_status(),
            'world_summary': self.game_state.get_world_summary()
        }
    
    def shutdown(self):
        """Shutdown the server"""
        logger.info("Shutting down RPG server...")
        
        self.is_running = False
        
        # Save final game state
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"saves/final_save_{timestamp}.json"
            self.game_state.save_game_state(filename)
            logger.info(f"Final save completed: {filename}")
        except Exception as e:
            logger.error(f"Final save failed: {e}")
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        # Shutdown game master
        if self.game_master:
            self.game_master.shutdown()
        
        logger.info("RPG server shutdown complete")

def start_server(host: str = None, port: int = None):
    """Start the RPG server (convenience function)"""
    server = RPGGameServer()
    try:
        server.start_server(host, port)
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    finally:
        server.shutdown()

if __name__ == "__main__":
    start_server()
