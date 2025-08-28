# 🎲 RPG AI - Sistema de RPG Multiplayer com IA

Um sistema de RPG multiplayer inovador que utiliza inteligência artificial para criar um Game Master dinâmico e responsivo, oferecendo uma experiência de jogo imersiva e fiel a partidas reais de RPG.

## 🌟 Características Principais

### 🧠 Game Master com IA
- **Narrativa Dinâmica**: Gera descrições envolventes e contextualizadas
- **Respostas Inteligentes**: Adapta-se às ações dos jogadores em tempo real
- **Múltiplos Estilos**: Suporte para diferentes tipos de cenários (combate, exploração, diálogo)
- **Consistência de Mundo**: Mantém coerência na história e no universo do jogo

### 🎮 Sistema de Jogo Robusto
- **Gerenciamento de Jogadores**: Sistema completo de sessões e personagens
- **Mundo Dinâmico**: Localizações, NPCs e eventos que evoluem com o tempo
- **Sistema de Missões**: Criação e gerenciamento de objetivos dinâmicos
- **Persistência**: Sistema de salvamento automático e manual

### 🌐 Multiplayer via Radmin
- **Conexão LAN**: Otimizado para redes locais via Radmin
- **Múltiplos Jogadores**: Suporte para até 8 jogadores simultâneos
- **Sincronização em Tempo Real**: Todas as ações são transmitidas instantaneamente
- **Interface Intuitiva**: Cliente simples e responsivo

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.7 ou superior
- Conexão de rede local (Radmin recomendado)
- Servidor K-Bold ou similar para IA

### Instalação
1. Clone o repositório:
```bash
git clone <repository-url>
cd rpg_ai
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o arquivo de configuração:
```bash
# Edite config/settings.yaml com suas configurações
# Especialmente o endpoint da IA e chave da API
```

## 🎯 Como Usar

### Iniciando o Servidor
```bash
# Usando o arquivo principal
python main.py server

# Com configurações personalizadas
python main.py server --port 6666 --host 0.0.0.0

# Usando o servidor diretamente
python -m src.network.server
```

### Conectando como Cliente
```bash
# Usando o arquivo principal
python main.py client

# Com host específico
python main.py client --host 192.168.1.100

# Usando o cliente diretamente
python -m src.network.client
```

## 🎮 Comandos do Jogo

### Comandos de Narrativa
- `{narra} [tema]` - Solicita narração do Mestre sobre um tema específico
- `{explorar}` - Explora detalhadamente a localização atual

### Comandos de Movimento
- `{mover} <direção>` - Move para uma direção específica (norte, sul, leste, oeste)

### Comandos de Interação
- `{falar} <NPC>` - Inicia conversa com um NPC específico
- `{combate} <alvo>` - Inicia uma sequência de combate

### Comandos do Sistema
- `{missao}` - Gerencia missões e objetivos
- `{inventario}` - Mostra seu inventário
- `{status}` - Mostra seu status atual
- `{ajuda}` - Mostra ajuda completa
- `{salvar}` - Salva o estado do jogo
- `{carregar}` - Carrega um estado salvo

### Roleplay
- Digite qualquer texto para falar ou agir no jogo
- Use comandos especiais para interagir com o sistema
- Explore o mundo e crie sua própria história!

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios
```
rpg_ai/
├── src/
│   ├── core/           # Componentes principais do jogo
│   │   ├── game_state.py    # Estado global do jogo
│   │   ├── player.py        # Gerenciamento de jogadores
│   │   └── world.py         # Mundo e localizações
│   ├── game_master/    # Sistema do Game Master
│   │   ├── master.py        # Classe principal do GM
│   │   ├── ai_engine.py     # Motor de IA
│   │   └── narrative.py     # Sistema de narrativa
│   ├── network/        # Comunicação em rede
│   │   ├── server.py        # Servidor do jogo
│   │   └── client.py        # Cliente do jogo
│   └── utils/          # Utilitários
│       ├── config.py        # Gerenciamento de configuração
│       └── logger.py        # Sistema de logging
├── config/
│   └── settings.yaml   # Configurações do sistema
├── main.py             # Ponto de entrada principal
└── requirements.txt    # Dependências Python
```

### Componentes Principais

#### 🎭 Game Master
- **Master**: Coordena todos os sistemas do jogo
- **AI Engine**: Gera respostas inteligentes usando IA
- **Narrative Engine**: Cria narrativas envolventes e atmosféricas

#### 🌍 Mundo do Jogo
- **World**: Gerencia o universo do jogo
- **Location**: Representa locais específicos
- **NPC**: Personagens não-jogadores com personalidades únicas

#### 👥 Sistema de Jogadores
- **Player**: Representa um jogador individual
- **PlayerManager**: Gerencia todos os jogadores da sessão
- **GameSession**: Controla sessões individuais do jogo

## ⚙️ Configuração

### Arquivo de Configuração (config/settings.yaml)
```yaml
# Server Settings
server:
  host: "0.0.0.0"
  port: 5555
  max_players: 8
  timeout: 30

# AI Settings
ai:
  endpoint: "http://localhost:5001/v1/chat/completions"
  api_key: ""
  model: "kb-gpt-neo"
  max_tokens: 600
  temperature: 0.8
  max_context_messages: 15

# Game Settings
game:
  session_timeout: 300
  max_history: 100
  auto_save_interval: 60

# World Settings
world:
  default_location: "Taverna do Dragão Dourado"
  starting_scenario: "Uma noite tempestuosa na taverna..."

# Logging
logging:
  level: "INFO"
  file: "rpg_ai.log"
  max_size: "10MB"
  backup_count: 5
```

## 🔧 Desenvolvimento

### Executando Testes
```bash
# Testar conexão com IA
python -c "from src.game_master.ai_engine import AIEngine; print(AIEngine().test_connection())"

# Verificar configuração
python -c "from src.utils.config import config; print(config.get_world_summary())"
```

### Estrutura de Logs
O sistema gera logs detalhados em:
- **Console**: Informações em tempo real
- **Arquivo**: Logs persistentes em `rpg_ai.log`
- **Rotação**: Logs são rotacionados automaticamente

### Extensibilidade
O sistema foi projetado para ser facilmente extensível:
- **Novos Comandos**: Adicione padrões regex em `GameMaster._load_command_patterns()`
- **Novos Tipos de IA**: Estenda `AIEngine` com novos prompts
- **Novos Elementos de Mundo**: Crie subclasses de `Location` e `NPC`

## 🌟 Recursos Avançados

### Sistema de Missões
- Criação dinâmica de objetivos
- Progresso automático baseado em ações
- Recompensas e consequências

### Eventos Dinâmicos
- Mudanças de clima automáticas
- Chegada de novos NPCs
- Eventos atmosféricos aleatórios

### Persistência de Dados
- Salvamento automático a cada minuto
- Salvamento manual via comando
- Carregamento de estados salvos

## 🤝 Contribuindo

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
- Use type hints em todas as funções
- Documente todas as classes e métodos
- Siga o padrão PEP 8
- Mantenha a cobertura de testes alta

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Comunidade RPG por inspiração
- Desenvolvedores de IA por ferramentas poderosas
- Testadores beta por feedback valioso

## 📞 Suporte

Para suporte, dúvidas ou sugestões:
- Abra uma issue no GitHub
- Entre em contato via email
- Participe da comunidade Discord

---

**🎲 Divirta-se e boa aventura no mundo do RPG AI!** 🚀
