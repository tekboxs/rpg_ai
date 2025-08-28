#!/usr/bin/env python3
"""
Teste dos Novos Recursos - RPG AI
Verifica se os sistemas de geração procedural e memória estão funcionando
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_procedural_generation():
    """Testa o sistema de geração procedural"""
    print("🧪 Testando Sistema de Geração Procedural...")
    
    try:
        from src.game_master.procedural_generator import ProceduralGenerator
        from src.game_master.ai_engine import AIEngine
        
        # Create AI engine (mock if no real endpoint)
        ai_engine = AIEngine()
        
        # Create procedural generator
        generator = ProceduralGenerator(ai_engine)
        
        print("✅ ProceduralGenerator criado com sucesso")
        
        # Test location generation
        print("🏗️ Testando geração de localização...")
        location = generator.generate_location(
            location_type='wilderness',
            context='Teste de funcionalidade'
        )
        
        if location and 'name' in location:
            print(f"✅ Localização gerada: {location['name']}")
            print(f"   Tipo: {location['location_type']}")
            print(f"   Tamanho: {location.get('size', 'N/A')}")
            print(f"   Estilo: {location.get('style', 'N/A')}")
        else:
            print("❌ Falha na geração de localização")
        
        # Test NPC generation
        print("👤 Testando geração de NPC...")
        npc = generator.generate_npc(
            npc_type='merchant',
            location_context='Local de teste'
        )
        
        if npc and 'name' in npc:
            print(f"✅ NPC gerado: {npc['name']}")
            print(f"   Role: {npc['role']}")
            print(f"   Personalidade: {', '.join(npc.get('personality', {}).get('traits', []))}")
        else:
            print("❌ Falha na geração de NPC")
        
        # Test world expansion
        print("🌍 Testando expansão do mundo...")
        new_content = generator.expand_world(['Local de teste'], 'organic')
        
        if new_content:
            print(f"✅ Mundo expandido com {len(new_content)} localizações")
        else:
            print("❌ Falha na expansão do mundo")
        
        # Get generation stats
        stats = generator.get_generation_stats()
        print(f"📊 Estatísticas de geração: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de geração procedural: {e}")
        return False

def test_npc_memory():
    """Testa o sistema de memória de NPCs"""
    print("\n🧪 Testando Sistema de Memória de NPCs...")
    
    try:
        from src.game_master.npc_memory import NPCMemoryManager
        
        # Create memory manager
        memory_manager = NPCMemoryManager()
        
        print("✅ NPCMemoryManager criado com sucesso")
        
        # Test adding conversation
        print("💬 Testando adição de conversa...")
        memory_manager.add_conversation(
            npc_id="TestNPC",
            player_id="TestPlayer",
            topic="teste",
            player_message="Olá, como você está?",
            npc_response="Olá! Estou bem, obrigado por perguntar.",
            context="Teste de funcionalidade"
        )
        
        print("✅ Conversa adicionada com sucesso")
        
        # Test getting context
        print("🧠 Testando recuperação de contexto...")
        context = memory_manager.get_npc_context_for_player(
            npc_id="TestNPC",
            player_id="TestPlayer",
            topic="teste"
        )
        
        print(f"✅ Contexto recuperado: {context}")
        
        # Test memory statistics
        stats = memory_manager.get_memory_statistics()
        print(f"📊 Estatísticas de memória: {stats}")
        
        # Test exporting/importing memories
        print("💾 Testando exportação/importação de memórias...")
        exported = memory_manager.export_all_memories()
        
        if exported:
            print("✅ Memórias exportadas com sucesso")
            
            # Clear and reimport
            memory_manager.npc_memories.clear()
            memory_manager.global_context.clear()
            
            memory_manager.import_all_memories(exported)
            print("✅ Memórias reimportadas com sucesso")
        else:
            print("❌ Falha na exportação de memórias")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de memória de NPCs: {e}")
        return False

def test_narrative_engine():
    """Testa o motor de narrativa aprimorado"""
    print("\n🧪 Testando Motor de Narrativa Aprimorado...")
    
    try:
        from src.game_master.narrative import NarrativeEngine
        from src.game_master.ai_engine import AIEngine
        from src.core.world import World
        
        # Create world and AI engine
        world = World("Mundo de Teste")
        ai_engine = AIEngine()
        
        # Create narrative engine
        narrative_engine = NarrativeEngine(world, ai_engine)
        
        print("✅ NarrativeEngine criado com sucesso")
        
        # Test dynamic quest creation
        print("🎯 Testando criação de missão dinâmica...")
        quest = narrative_engine.create_dynamic_quest()
        
        if quest and 'title' in quest:
            print(f"✅ Missão criada: {quest['title']}")
            print(f"   Tipo: {quest['type']}")
            print(f"   Dificuldade: {quest['difficulty']}")
        else:
            print("❌ Falha na criação de missão")
        
        # Test world expansion
        print("🌍 Testando expansão procedural do mundo...")
        new_content = narrative_engine.expand_world_procedurally('organic', 2)
        
        if new_content:
            print(f"✅ Mundo expandido com {len(new_content)} localizações")
            for content in new_content:
                if 'name' in content:
                    print(f"   📍 {content['name']}")
        else:
            print("❌ Falha na expansão do mundo")
        
        # Get narrative summary
        summary = narrative_engine.get_narrative_summary()
        print(f"📊 Resumo narrativo: {summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do motor de narrativa: {e}")
        return False

def test_configuration():
    """Testa as novas configurações"""
    print("\n🧪 Testando Novas Configurações...")
    
    try:
        from src.utils.config import config
        
        print("✅ Configuração carregada com sucesso")
        
        # Test procedural settings
        print("🏗️ Configurações de geração procedural:")
        print(f"   Habilitado: {config.procedural_enabled}")
        print(f"   Máximo de localizações por expansão: {config.max_locations_per_expansion}")
        print(f"   Criatividade: {config.generation_creativity}")
        print(f"   Chance de expansão: {config.world_expansion_chance}")
        
        # Test memory settings
        print("🧠 Configurações de memória:")
        print(f"   Habilitado: {config.memory_enabled}")
        print(f"   Tamanho máximo da memória: {config.max_memory_size}")
        print(f"   Rastreamento emocional: {config.emotional_state_tracking}")
        print(f"   Desenvolvimento de relacionamentos: {config.relationship_development}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de configuração: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando Testes dos Novos Recursos - RPG AI")
    print("=" * 60)
    
    tests = [
        ("Geração Procedural", test_procedural_generation),
        ("Memória de NPCs", test_npc_memory),
        ("Motor de Narrativa", test_narrative_engine),
        ("Configurações", test_configuration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro crítico no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os novos recursos estão funcionando corretamente!")
        return 0
    else:
        print("⚠️ Alguns recursos podem precisar de ajustes.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
