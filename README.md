# 🎲 RPG AI - Sistema de RPG Multiplayer com IA

Um sistema de RPG multiplayer inovador que utiliza inteligência artificial para criar um Game Master dinâmico e responsivo, oferecendo uma experiência de jogo imersiva e fiel a partidas reais de RPG.

## 🌟 Características Principais

### 🧠 Game Master com IA
- **Narrativa Dinâmica**: Gera descrições envolventes e contextualizadas
- **Respostas Inteligentes**: Adapta-se às ações dos jogadores em tempo real
- **Múltiplos Estilos**: Suporte para diferentes tipos de cenários (combate, exploração, diálogo)
- **Consistência de Mundo**: Mantém coerência na história e no universo do jogo

### 🏗️ Geração Procedural Avançada
- **Localizações Dinâmicas**: Cria novas áreas do mundo conforme necessário
- **NPCs Únicos**: Gera personagens com personalidades e histórias distintas
- **Missões Personalizadas**: Cria objetivos únicos baseados no contexto
- **Expansão Orgânica**: O mundo cresce de forma natural e coerente

### 🧠 Sistema de Memória para NPCs
- **Memória Persistente**: NPCs se lembram de conversas anteriores
- **Relacionamentos Dinâmicos**: Desenvolvem laços com jogadores ao longo do tempo
- **Personalidades Únicas**: Cada NPC tem traços e estilos de diálogo distintos
- **Contexto Inteligente**: Evitam repetir informações já compartilhadas

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
- `{falar} <NPC>` - Inicia conversa com um NPC específico (com memória!)
- `{combate} <alvo>` - Inicia uma sequência de combate

### Comandos do Sistema
- `{missao}` - Gerencia missões e objetivos
- `{inventario}` - Mostra seu inventário
- `{status}` - Mostra seu status atual
- `{ajuda}` - Mostra ajuda completa
- `{salvar}` - Salva o estado do jogo
- `{carregar}` - Carrega um estado salvo

### 🆕 Novos Comandos de Geração
- `{expandir} [tipo]` - Expande o mundo proceduralmente
  - Tipos: `organic`, `quest_driven`, `random`
- `{gerar} <tipo>` - Gera conteúdo específico
  - Tipos: `localização`, `npc`, `missão`

### Roleplay
- Digite qualquer texto para falar ou agir no jogo
- Use comandos especiais para interagir com o sistema
- Explore o mundo e crie sua própria história!

## 🆕 Novos Recursos em Destaque

### 🌍 Expansão Procedural do Mundo
O sistema agora pode expandir o mundo automaticamente:
- **Expansão Orgânica**: Novas localizações conectadas às existentes
- **Expansão por Missões**: Áreas criadas especificamente para objetivos
- **Geração Inteligente**: Cada localização é única e contextualizada

### 👥 NPCs com Memória e Personalidade
- **Memória Persistente**: Lembram de conversas e relacionamentos
- **Personalidades Únicas**: Cada NPC tem traços e estilos distintos
- **Desenvolvimento de Relacionamentos**: Laços que evoluem com o tempo
- **Contexto Inteligente**: Evitam repetir informações já compartilhadas

### 🎯 Missões Dinâmicas
- **Geração Automática**: Missões criadas pela IA conforme necessário
- **Contexto Personalizado**: Baseadas no estado atual do mundo
- **Objetivos Únicos**: Cada missão tem objetivos e recompensas distintas

## 📚 Documentação Adicional

- **[DEMO_NEW_FEATURES.md](DEMO_NEW_FEATURES.md)** - Demonstração detalhada dos novos recursos
- **[TIMEOUT_CONFIG.md](TIMEOUT_CONFIG.md)** - Configurações de timeout do sistema
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Status atual do projeto

## 🔧 Configurações Avançadas

### Geração Procedural
```yaml
procedural:
  enabled: true
  max_locations_per_expansion: 5
  generation_creativity: 0.8
  world_expansion_chance: 0.3
```

### Sistema de Memória
```yaml
memory:
  enabled: true
  max_memory_size: 100
  emotional_state_tracking: true
  relationship_development: true
```

## 🌟 Benefícios dos Novos Recursos

1. **Mundo Infinito**: O mundo se expande conforme necessário
2. **NPCs Inteligentes**: Personalidades únicas e memória persistente
3. **Conteúdo Único**: Cada sessão é diferente
4. **Imersão**: NPCs se lembram de você e desenvolvem relacionamentos
5. **Escalabilidade**: Sistema que cresce com o uso

## 🚀 Próximos Passos

- Teste os novos comandos de geração
- Explore o mundo expandido
- Converse com NPCs para desenvolver relacionamentos
- Aceite missões dinâmicas
- Monitore o crescimento do mundo

---

**🎉 Agora o RPG AI oferece uma experiência verdadeiramente dinâmica e imersiva, com um mundo que cresce e NPCs que se lembram de você!**
