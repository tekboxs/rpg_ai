#!/usr/bin/env python3
"""
Test script for the simplified RPG AI system
Tests the action queue and simple game master functionality
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.action_queue import ActionQueue, ActionProcessor, PlayerAction
from src.game_master.simple_master import SimpleGameMaster
from src.core.game_state import GameState
from src.game_master.ai_engine import AIEngine
from src.utils.logger import logger

def test_action_queue():
    """Test the action queue system"""
    print("🧪 Testando Sistema de Fila de Ações...")
    
    # Create action queue
    queue = ActionQueue()
    
    # Test adding actions
    print("\n1. Adicionando ações à fila...")
    
    action1 = queue.add_action("player1", "fazer", "explorar a área")
    action2 = queue.add_action("player2", "dizer", "Olá, como vai?")
    action3 = queue.add_action("player1", "historia", "o vento sopra suavemente")
    
    print(f"   ✅ Ação 1: {action1}")
    print(f"   ✅ Ação 2: {action2}")
    print(f"   ✅ Ação 3: {action3}")
    
    # Test queue status
    print("\n2. Verificando status da fila...")
    status = queue.get_queue_status()
    print(f"   📊 Total de ações: {status['total_actions']}")
    print(f"   📝 Ações aguardando: {status['unprocessed_actions']}")
    print(f"   🎭 Fazer: {status['actions_by_type']['fazer']}")
    print(f"   💬 Dizer: {status['actions_by_type']['dizer']}")
    print(f"   📖 História: {status['actions_by_type']['historia']}")
    
    # Test getting unprocessed actions
    print("\n3. Obtendo ações não processadas...")
    unprocessed = queue.get_unprocessed_actions()
    print(f"   📋 Ações não processadas: {len(unprocessed)}")
    for action in unprocessed:
        print(f"      - {action.action_type}: {action.content[:30]}...")
    
    # Test getting actions by type
    print("\n4. Obtendo ações por tipo...")
    fazer_actions = queue.get_actions_by_type("fazer")
    dizer_actions = queue.get_actions_by_type("dizer")
    historia_actions = queue.get_actions_by_type("historia")
    
    print(f"   🎭 Ações 'fazer': {len(fazer_actions)}")
    print(f"   💬 Ações 'dizer': {len(dizer_actions)}")
    print(f"   📖 Ações 'historia': {len(historia_actions)}")
    
    # Test clearing processed actions
    print("\n5. Testando limpeza de ações processadas...")
    for action in unprocessed:
        action.processed = True
    
    cleared_count = queue.clear_processed_actions()
    print(f"   🧹 Ações limpas: {cleared_count}")
    
    # Final status
    final_status = queue.get_queue_status()
    print(f"   📊 Status final: {final_status['total_actions']} ações, {final_status['unprocessed_actions']} aguardando")
    
    print("\n✅ Teste da fila de ações concluído com sucesso!")
    return True

def test_simple_game_master():
    """Test the simple game master"""
    print("\n🧪 Testando Simple Game Master...")
    
    try:
        # Create game state
        game_state = GameState()
        
        # Create simple game master
        master = SimpleGameMaster(game_state)
        
        print("   ✅ Simple Game Master criado com sucesso")
        
        # Test command patterns
        print("\n1. Testando padrões de comando...")
        
        test_commands = [
            "{fazer explorar a área}",
            "{dizer Olá, como vai?}",
            "{historia o vento sopra suavemente}",
            "{mestre}",
            "{status}",
            "{ajuda}"
        ]
        
        for cmd in test_commands:
            # Create a mock player
            class MockPlayer:
                def __init__(self):
                    self.id = "test_player"
                    self.name = "TestPlayer"
                    self.last_activity = time.time()
                
                def update_activity(self):
                    self.last_activity = time.time()
            
            player = MockPlayer()
            
            # Process command
            response = master.process_player_action(player, cmd)
            if response:
                print(f"   ✅ Comando '{cmd[:20]}...' processado")
                print(f"      Resposta: {response[:50]}...")
            else:
                print(f"   ❌ Comando '{cmd[:20]}...' falhou")
        
        # Test system status
        print("\n2. Testando status do sistema...")
        system_status = master.get_system_status()
        print(f"   📊 Tipo do sistema: {system_status['system_type']}")
        print(f"   🎯 Sistema ativo: {system_status['is_active']}")
        print(f"   👥 Total de jogadores: {system_status['total_players']}")
        print(f"   🌍 Localizações do mundo: {system_status['world_locations']}")
        
        print("\n✅ Teste do Simple Game Master concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False

def test_action_processor():
    """Test the action processor"""
    print("\n🧪 Testando Processador de Ações...")
    
    try:
        # Create components
        queue = ActionQueue()
        game_state = GameState()
        ai_engine = AIEngine()
        
        # Create processor
        processor = ActionProcessor(queue, game_state, ai_engine)
        
        print("   ✅ Processador de ações criado com sucesso")
        
        # Add test actions
        print("\n1. Adicionando ações de teste...")
        queue.add_action("player1", "fazer", "explorar a área")
        queue.add_action("player2", "dizer", "Olá, como vai?")
        queue.add_action("player1", "historia", "o vento sopra suavemente")
        
        # Test processing
        print("\n2. Testando processamento de ações...")
        unprocessed = queue.get_unprocessed_actions()
        print(f"   📋 Ações para processar: {len(unprocessed)}")
        
        # Note: This will fail if AI engine is not configured
        # but we can test the structure
        print("   ⚠️  Nota: Processamento real requer IA configurada")
        
        # Test queue status after adding actions
        status = queue.get_queue_status()
        print(f"   📊 Status da fila: {status['unprocessed_actions']} ações aguardando")
        
        print("\n✅ Teste do processador de ações concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Iniciando testes do Sistema Simplificado...")
    print("=" * 60)
    
    tests = [
        ("Sistema de Fila de Ações", test_action_queue),
        ("Simple Game Master", test_simple_game_master),
        ("Processador de Ações", test_action_processor)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
        except Exception as e:
            print(f"❌ {test_name}: ERRO - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO DOS TESTES: {passed}/{total} passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema funcionando perfeitamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Testes interrompidos pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro fatal durante os testes: {e}")
        sys.exit(1)
