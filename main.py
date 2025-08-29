#!/usr/bin/env python3
"""
RPG AI - Sistema de RPG multiplayer com IA
Arquivo principal para executar o sistema
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.network.server import start_server
from src.network.client import start_client
from src.utils.logger import logger
from src.utils.config import config


def main():
    """Main entry point for RPG AI system"""
    parser = argparse.ArgumentParser(
        description="RPG AI - Sistema de RPG multiplayer com IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py server          # Iniciar servidor
  python main.py client          # Iniciar cliente
  python main.py server --port 6666  # Servidor na porta 6666
  python main.py client --host 192.168.1.100  # Cliente conectando ao IP específico
        """,
    )

    parser.add_argument(
        "mode", choices=["server", "client"], help="Modo de execução: server ou client"
    )

    parser.add_argument(
        "--host",
        default=None,
        help="Host/IP para conectar (cliente) ou escutar (servidor)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Porta para conectar (cliente) ou escutar (servidor)",
    )

    parser.add_argument(
        "--config", help="Caminho para arquivo de configuração personalizado"
    )

    args = parser.parse_args()

    try:
        # Reload config if custom path provided
        if args.config:
            from src.utils.config import Config

            global config
            config = Config(args.config)
            logger.info(f"Configuração carregada de: {args.config}")

        if args.mode == "server":
            print("🚀 Iniciando servidor RPG AI...")
            print(f"📊 Configurações:")
            print(f"   Host: {args.host or config.server_host}")
            print(f"   Porta: {args.port or config.server_port}")
            print(f"   Máximo de jogadores: {config.max_players}")
            print(f"   Endpoint AI: {config.ai_endpoint}")
            print(f"   Modelo AI: {config.ai_model}")
            print()

            # Show new system information
            print("🆕 Sistema Simplificado Ativado:")
            print(f"   📝 Sistema de Fila de Ações: ✅")
            print(f"   🎭 Controle Total do Jogador: ✅")
            print(f"   🤖 IA Assistente (não controladora): ✅")
            print(f"   🔧 Administração do Servidor: ✅")
            print(f"   🎨 Criatividade AI: {config.generation_creativity:.1f}")
            print(f"   🌍 Mundo Dinâmico: ✅")
            print(f"   💾 Sistema de Histórico: ✅")
            print()

            start_server(args.host, args.port)

        elif args.mode == "client":
            print("🎮 Iniciando cliente RPG AI...")
            start_client()

    except KeyboardInterrupt:
        print("\n\n🛑 Sistema interrompido pelo usuário.")
        logger.info("System interrupted by user")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
