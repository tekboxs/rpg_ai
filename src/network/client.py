"""
Network client for RPG AI system
"""
import socket
import threading
import time
import sys
from typing import Optional
from ..utils.logger import logger

class RPGGameClient:
    """RPG game client"""
    
    def __init__(self):
        self.socket = None
        self.is_connected = False
        self.player_name = None
        self.receive_thread = None
        self.server_host = None
        self.server_port = None
        
        # Client state
        self.last_message_time = time.time()
        self.message_count = 0
        
        logger.info("RPG Game Client initialized")
    
    def connect_to_server(self, host: str, port: int = 5555) -> bool:
        """Connect to the RPG server"""
        try:
            self.server_host = host
            self.server_port = port
            
            logger.info(f"Conectando ao servidor {host}:{port}...")
            
            # Create socket and connect
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            from ..utils.config import config
            timeout_value = config.get('server.connection_timeout', 0)
            self.socket.settimeout(timeout_value if timeout_value > 0 else None)
            self.socket.connect((host, port))
            
            # Get player name from server
            player_name = self._get_player_name_from_server()
            if not player_name:
                return False
            
            self.player_name = player_name
            self.is_connected = True
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
            self.receive_thread.start()
            
            logger.info(f"Conectado ao servidor como {player_name}")
            return True
            
        except socket.timeout:
            logger.error("Timeout ao conectar ao servidor")
            return False
        except ConnectionRefusedError:
            logger.error("Conexão recusada pelo servidor")
            return False
        except Exception as e:
            logger.error(f"Erro ao conectar: {e}")
            return False
    
    def _get_player_name_from_server(self) -> Optional[str]:
        """Get player name prompt from server and send response"""
        try:
            # Wait for server prompt
            data = self.socket.recv(1024)
            if not data:
                return None
            
            prompt = data.decode('utf-8').strip()
            print(f"\n{prompt}")
            
            # Get player name from user
            while True:
                name = input("> ").strip()
                if name and len(name) <= 20:
                    # Send name to server with explicit UTF-8 encoding
                    self.socket.sendall(name.encode('utf-8'))
                    
                    # Wait for confirmation or error
                    response = self.socket.recv(1024)
                    if response:
                        response_text = response.decode('utf-8').strip()
                        if "❌" in response_text:
                            print(response_text)
                            continue
                        else:
                            return name
                    break
                else:
                    print("❌ Nome deve ter entre 1 e 20 caracteres.")
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting player name: {e}")
            return None
    
    def _receive_messages(self):
        """Receive messages from server"""
        while self.is_connected and self.socket:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                
                message = data.decode().strip()
                if message:
                    self._display_message(message)
                    self.last_message_time = time.time()
                    
            except socket.timeout:
                continue
            except Exception as e:
                if self.is_connected:
                    logger.error(f"Error receiving message: {e}")
                break
        
        # Connection lost
        if self.is_connected:
            self._handle_connection_lost()
    
    def _display_message(self, message: str):
        """Display received message"""
        # Clear line and display message
        sys.stdout.write(f"\r{message}\n> ")
        sys.stdout.flush()
    
    def _handle_connection_lost(self):
        """Handle lost connection"""
        self.is_connected = False
        print("\n❌ Conexão perdida com o servidor.")
        print("Pressione Enter para sair...")
    
    def send_message(self, message: str) -> bool:
        """Send message to server"""
        if not self.is_connected or not self.socket:
            return False
        
        try:
            self.socket.sendall(message.encode('utf-8'))
            self.message_count += 1
            return True
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        self.is_connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        logger.info("Disconnected from server")
    
    def get_connection_status(self) -> dict:
        """Get current connection status"""
        return {
            'is_connected': self.is_connected,
            'server_host': self.server_host,
            'server_port': self.server_port,
            'player_name': self.player_name,
            'message_count': self.message_count,
            'last_message_time': self.last_message_time
        }

def start_client():
    """Start the RPG client"""
    print("🎲 RPG AI - Cliente")
    print("=" * 40)
    
    # Get server connection info
    host = input("Digite o IP do servidor (Radmin): ").strip()
    if not host:
        print("❌ IP do servidor é obrigatório.")
        return
    
    port_input = input("Digite a porta do servidor [5555]: ").strip()
    port = int(port_input) if port_input else 5555
    
    # Create and start client
    client = RPGGameClient()
    
    try:
        # Connect to server
        if not client.connect_to_server(host, port):
            print("❌ Falha ao conectar ao servidor.")
            return
        
        print("\n🎮 Conectado ao RPG!")
        print("\n💡 **COMANDOS DISPONÍVEIS:**")
        print("**Narrativa:**")
        print("- {narra} [tema] - Solicita narração do Mestre")
        print("- {explorar} - Explora localização atual")
        print("\n**Movimento:**")
        print("- {mover} <direção> - Move para uma direção")
        print("\n**Interação:**")
        print("- {falar} <NPC> - Inicia conversa com NPC")
        print("- {combate} <alvo> - Inicia combate")
        print("\n**Sistema:**")
        print("- {missao} - Gerencia missões")
        print("- {inventario} - Mostra inventário")
        print("- {status} - Mostra status atual")
        print("- {ajuda} - Mostra ajuda completa")
        print("- {salvar} - Salva o jogo")
        print("- {carregar} - Carrega jogo salvo")
        print("\n**Roleplay:**")
        print("- Digite qualquer texto para falar ou agir")
        print("\nDigite 'sair' para encerrar.")
        print("\n" + "=" * 40)
        
        # Main client loop
        while client.is_connected:
            try:
                message = input("> ").strip()
                
                if not message:
                    continue
                
                if message.lower() == 'sair':
                    break
                
                # Send message to server
                if not client.send_message(message):
                    print("❌ Erro ao enviar mensagem.")
                    break
                
            except KeyboardInterrupt:
                print("\n\n🛑 Interrupção solicitada pelo usuário.")
                break
            except EOFError:
                break
        
    except Exception as e:
        logger.error(f"Client error: {e}")
        print(f"❌ Erro no cliente: {e}")
    
    finally:
        # Cleanup
        client.disconnect()
        print("\n👋 Cliente encerrado.")

if __name__ == "__main__":
    start_client()
