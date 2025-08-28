#!/usr/bin/env python3
"""
Teste de Conexão Simples - RPG AI
Testa a conexão básica com o servidor para verificar se o problema de codificação foi resolvido
"""

import socket
import time

def test_server_connection(host='127.0.0.1', port=5555):
    """Testa a conexão com o servidor"""
    print(f"🧪 Testando conexão com {host}:{port}")
    
    try:
        # Criar socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 segundos de timeout
        
        print("📡 Conectando ao servidor...")
        sock.connect((host, port))
        print("✅ Conectado com sucesso!")
        
        # Aguardar prompt do servidor
        print("⏳ Aguardando prompt do servidor...")
        data = sock.recv(1024)
        
        if data:
            try:
                prompt = data.decode('utf-8')
                print(f"📨 Servidor disse: {prompt}")
            except UnicodeDecodeError as e:
                print(f"❌ Erro de decodificação: {e}")
                print(f"📊 Dados brutos: {data}")
                return False
        
        # Enviar nome de teste
        test_name = "TestPlayer"
        print(f"📤 Enviando nome: {test_name}")
        sock.sendall(test_name.encode('utf-8'))
        
        # Aguardar resposta
        print("⏳ Aguardando resposta...")
        response = sock.recv(1024)
        
        if response:
            try:
                response_text = response.decode('utf-8')
                print(f"📨 Resposta do servidor: {response_text}")
                
                if "❌" in response_text:
                    print("⚠️ Servidor retornou erro")
                    return False
                else:
                    print("✅ Conexão funcionando perfeitamente!")
                    return True
                    
            except UnicodeDecodeError as e:
                print(f"❌ Erro de decodificação na resposta: {e}")
                print(f"📊 Dados brutos: {response}")
                return False
        
        # Fechar conexão
        sock.close()
        print("🔌 Conexão fechada")
        return True
        
    except ConnectionRefusedError:
        print("❌ Conexão recusada. Servidor não está rodando?")
        return False
    except socket.timeout:
        print("❌ Timeout na conexão")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Teste de Conexão - RPG AI")
    print("=" * 40)
    
    # Testar conexão local
    success = test_server_connection()
    
    if success:
        print("\n🎉 Teste de conexão PASSOU!")
        print("✅ O problema de codificação foi resolvido")
    else:
        print("\n❌ Teste de conexão FALHOU!")
        print("⚠️ Ainda há problemas de codificação")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    main()
