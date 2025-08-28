# 🎲 RPG AI - Sistema de RPG Multiplayer com IA

Um sistema de RPG multiplayer inovador que utiliza inteligência artificial para criar um Game Master dinâmico e responsivo, oferecendo uma experiência de jogo imersiva e fiel a partidas reais de RPG.

## 🌟 Características Principais

### 🤖 IA Mestre Autônoma
- **Tomada de Decisões**: A IA toma decisões da campanha independentemente
- **Análise de Situações**: Analisa contexto, ações dos jogadores e estado da campanha
- **Adaptação Dinâmica**: Ajusta dificuldade e ritmo baseado no desempenho dos jogadores
- **Consistência de Mundo**: Mantém coerência na história e no universo do jogo

### 🎲 Sistema de Dados Completo
- **Rolagem Avançada**: Suporte para d20, d6, d100, vantagem/desvantagem
- **Sucessos Críticos**: Sistema completo de sucessos e falhas críticas
- **Eventos Baseados em Dados**: Eventos de combate, tesouro e interação social
- **Graus de Sucesso**: Sucesso excepcional, grande sucesso, sucesso, falha

### 🎭 Geração Procedural de Histórias
- **Histórias Únicas**: Cada campanha é diferente e contextualizada
- **Localizações Variadas**: Florestas, montanhas, ruínas, vilas, cidades, cavernas
- **Situações Iniciais**: Atmosfera dinâmica com clima, tempo e nível de perigo
- **NPCs Contextuais**: Guias, mentores, informantes com motivações únicas

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

### 🔧 Sistema de Administração Avançado
- **Comandos Administrativos**: Reiniciar, deletar dados, backup, restauração
- **Backup Inteligente**: Sistema automático de backup antes de operações críticas
- **Monitoramento Completo**: Status detalhado de todos os sistemas
- **Gerenciamento de Logs**: Limpeza automática e manutenção de logs

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

### 🎭 Comandos de Narrativa e Campanha
- `{narra} [tema]` - Solicita narração do Mestre sobre um tema específico
- `{explorar}` - Explora detalhadamente a localização atual
- `{historia} [estilo]` - Inicia/gerencia campanha com IA Mestre
- `{acao} <descrição>` - Descreve ação para a IA Mestre processar

### 🎲 Comandos de Dados e Eventos
- `{dados} <tipo>` - Rola dados (ex: d20, 2d6, d100)
- `{evento} [tipo]` - Dispara evento aleatório (combate, tesouro, social)

### 🚶 Comandos de Movimento
- `{mover} <direção>` - Move para uma direção específica (norte, sul, leste, oeste)

### 💬 Comandos de Interação
- `{falar} <NPC>` - Inicia conversa com um NPC específico (com memória!)
- `{combate} <alvo>` - Inicia uma sequência de combate

### 🔧 Comandos Administrativos
- `{admin} reiniciar` - Reinicia o servidor com backup automático
- `{admin} deletar_dados` - Remove todos os dados (com backup de segurança)
- `{admin} backup` - Cria backup completo do servidor
- `{admin} status_servidor` - Mostra status detalhado do servidor

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

### **Para Jogadores**
- **Histórias Únicas**: Cada campanha é diferente e contextualizada
- **Ações Significativas**: Suas escolhas moldam o mundo e a história
- **Imersão Profunda**: Sistema de dados realista e eventos dinâmicos
- **NPCs Inteligentes**: Personagens que se lembram e evoluem
- **IA Mestre Responsiva**: Sistema que se adapta às suas ações

### **Para Mestres**
- **Automação Inteligente**: A IA toma decisões baseadas em regras e contexto
- **Flexibilidade Total**: Sistema se adapta ao estilo de jogo automaticamente
- **Redução de Preparação**: Conteúdo é gerado dinamicamente
- **Foco na Narrativa**: Menos tempo com mecânicas, mais com história
- **Decisões Contextuais**: IA analisa situações e toma decisões apropriadas

### **Para Administradores**
- **Controle Total**: Comandos administrativos poderosos e seguros
- **Segurança de Dados**: Sistema de backup robusto e automático
- **Monitoramento Completo**: Visibilidade de todos os sistemas
- **Manutenção Simplificada**: Ferramentas para todas as operações
- **Backup Inteligente**: Sistema que protege dados automaticamente

## 🚀 Próximos Passos

### **Para Jogadores**
- Use `{historia}` para iniciar uma nova campanha
- Experimente `{acao} <sua ação>` para interagir com a IA Mestre
- Role dados com `{dados} d20` para ações importantes
- Dispare eventos com `{evento}` para situações dinâmicas

### **Para Mestres**
- Observe como a IA toma decisões baseadas nas ações dos jogadores
- Monitore o progresso da campanha com `{status}`
- Use `{admin} status_servidor` para ver estatísticas completas

### **Para Administradores**
- Teste os comandos administrativos com `{admin} backup`
- Monitore o sistema com `{admin} status_servidor`
- Use `{admin} limpar_logs` para manutenção regular

---

**🎉 Agora o RPG AI é um sistema verdadeiramente revolucionário com IA Mestre autônoma, sistema de dados completo e administração avançada!**

## 📚 Documentação Completa

- **[DEMO_AVANCADO.md](DEMO_AVANCADO.md)** - Demonstração dos recursos avançados
- **[DEMO_NEW_FEATURES.md](DEMO_NEW_FEATURES.md)** - Recursos básicos implementados
- **[TIMEOUT_CONFIG.md](TIMEOUT_CONFIG.md)** - Configurações de timeout
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Status do projeto
