#!/usr/bin/env python3
"""
Teste dos Sistemas Avançados - RPG AI
Testa todos os novos recursos implementados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.config import config
from src.utils.logger import logger
from src.game_master.ai_engine import AIEngine
from src.game_master.story_generator import StoryGenerator
from src.game_master.dice_system import DiceSystem
from src.game_master.event_system import EventSystem
from src.game_master.ai_dungeon_master import AIDungeonMaster
from src.game_master.server_admin import ServerAdmin

def test_story_generator():
    """Testa o gerador de histórias"""
    print("🧪 Testando Gerador de Histórias...")
    
    try:
        ai_engine = AIEngine()
        story_gen = StoryGenerator(ai_engine)
        
        # Testar geração de história
        story_data = story_gen.generate_story_beginning(3, 'adventure_start')
        
        print(f"✅ História gerada: {story_data['story_title']}")
        print(f"   Tipo: {story_data['campaign_type']}")
        print(f"   Localização: {story_data['initial_location']}")
        print(f"   NPCs: {len(story_data['initial_npcs'])}")
        
        # Testar variações disponíveis
        variations = story_gen.get_story_variations()
        print(f"   Variações disponíveis: {', '.join(variations)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no gerador de histórias: {e}")
        return False

def test_dice_system():
    """Testa o sistema de dados"""
    print("\n🎲 Testando Sistema de Dados...")
    
    try:
        dice_sys = DiceSystem()
        
        # Testar rolagem básica
        roll = dice_sys.roll_dice("d20")
        print(f"✅ Rolagem d20: {roll['final_result']}")
        
        # Testar rolagem com modificador
        roll = dice_sys.roll_dice("d20", modifier=5)
        print(f"✅ Rolagem d20+5: {roll['final_result']}")
        
        # Testar rolagem com vantagem
        roll = dice_sys.roll_dice("d20", advantage=True)
        print(f"✅ Rolagem d20 com vantagem: {roll['final_result']}")
        
        # Testar verificação de habilidade
        check = dice_sys.roll_ability_check(16, 15)
        print(f"✅ Verificação de habilidade: {check['success']}")
        
        # Testar ataque
        attack = dice_sys.roll_attack(5, 18)
        print(f"✅ Ataque: {'Acertou' if attack['hit'] else 'Errou'}")
        
        # Testar dano
        damage = dice_sys.roll_damage("2d6", 3)
        print(f"✅ Dano: {damage['total_damage']}")
        
        # Testar evento aleatório
        event = dice_sys.roll_random_event("combat_encounter", "medium")
        print(f"✅ Evento aleatório: {event['outcome']}")
        
        # Verificar estatísticas
        stats = dice_sys.get_statistics()
        print(f"   Estatísticas: {stats['total_rolls']} rolagens")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de dados: {e}")
        return False

def test_event_system():
    """Testa o sistema de eventos"""
    print("\n🎭 Testando Sistema de Eventos...")
    
    try:
        ai_engine = AIEngine()
        dice_sys = DiceSystem()
        event_sys = EventSystem(ai_engine, dice_sys)
        
        # Testar disparo de evento
        event = event_sys.trigger_random_event('combat_encounter', 'medium', 'Teste')
        print(f"✅ Evento disparado: {event['event_type']}")
        print(f"   Resultado: {event['outcome']}")
        
        # Testar resposta de jogador
        success = event_sys.add_player_response(
            event['event_id'], 
            'player1', 
            'Vou atacar o inimigo', 
            'combat'
        )
        print(f"✅ Resposta de jogador adicionada: {success}")
        
        # Verificar estatísticas
        stats = event_sys.get_event_statistics()
        print(f"   Estatísticas: {stats['total_events']} eventos")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de eventos: {e}")
        return False

def test_ai_dungeon_master():
    """Testa a IA Mestre"""
    print("\n🤖 Testando IA Mestre...")
    
    try:
        ai_engine = AIEngine()
        story_gen = StoryGenerator(ai_engine)
        dice_sys = DiceSystem()
        event_sys = EventSystem(ai_engine, dice_sys)
        
        ai_master = AIDungeonMaster(ai_engine, story_gen, event_sys, dice_sys)
        
        # Testar início de campanha
        campaign = ai_master.start_new_campaign(3, 'mystery_start')
        print(f"✅ Campanha iniciada: {campaign['story_title']}")
        
        # Testar tomada de decisão
        decision = ai_master.make_campaign_decision(
            "Jogador tenta escalar uma montanha perigosa",
            [{'player_id': 'player1', 'action': 'escalar', 'action_type': 'exploration'}],
            "Exploração de montanha"
        )
        print(f"✅ Decisão tomada: {decision['action_type']}")
        
        # Verificar status da campanha
        status = ai_master.get_campaign_status()
        print(f"   Progresso: {status['story_progress']}")
        print(f"   Decisões: {status['recent_decisions']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na IA Mestre: {e}")
        return False

def test_server_admin():
    """Testa o sistema de administração"""
    print("\n🔧 Testando Sistema de Administração...")
    
    try:
        admin = ServerAdmin()
        
        # Testar comandos disponíveis
        commands = admin.get_available_commands('admin')
        print(f"✅ Comandos disponíveis: {len(commands)}")
        
        # Testar status do servidor
        status = admin.execute_admin_command('status_servidor', [], 'admin')
        print(f"✅ Status do servidor obtido: {status['success']}")
        
        # Testar criação de backup
        backup = admin.execute_admin_command('backup', ['test'], 'admin')
        print(f"✅ Backup criado: {backup['success']}")
        
        # Testar limpeza de logs
        logs = admin.execute_admin_command('limpar_logs', ['1'], 'admin')
        print(f"✅ Logs limpos: {logs['success']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de administração: {e}")
        return False

def test_configuration():
    """Testa as configurações"""
    print("\n⚙️ Testando Configurações...")
    
    try:
        # Verificar configurações básicas
        print(f"✅ Servidor: {config.server_host}:{config.server_port}")
        print(f"✅ Máximo de jogadores: {config.max_players}")
        print(f"✅ IA habilitada: {config.ai_enabled}")
        
        # Verificar configurações de geração procedural
        print(f"✅ Geração procedural: {config.procedural_enabled}")
        print(f"✅ Criatividade: {config.generation_creativity}")
        print(f"✅ Expansão mundial: {config.world_expansion_chance}")
        
        # Verificar configurações de memória
        print(f"✅ Sistema de memória: {config.memory_enabled}")
        print(f"✅ Tamanho da memória: {config.max_memory_size}")
        print(f"✅ Rastreamento emocional: {config.emotional_state_tracking}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas configurações: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Teste dos Sistemas Avançados - RPG AI")
    print("=" * 60)
    
    tests = [
        ("Gerador de Histórias", test_story_generator),
        ("Sistema de Dados", test_dice_system),
        ("Sistema de Eventos", test_event_system),
        ("IA Mestre", test_ai_dungeon_master),
        ("Administração do Servidor", test_server_admin),
        ("Configurações", test_configuration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Erro crítico em {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os sistemas avançados estão funcionando perfeitamente!")
        print("🚀 O RPG AI está pronto para uso com todos os recursos!")
    else:
        print("⚠️ Alguns sistemas precisam de atenção.")
        print("🔧 Verifique os logs para mais detalhes.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
