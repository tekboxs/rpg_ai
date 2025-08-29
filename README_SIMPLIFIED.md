# 🎲 RPG AI - Sistema Simplificado

Um sistema de RPG multiplayer que **dá poder total ao jogador** sobre a narrativa, usando IA apenas como assistente para gerar respostas criativas.

## 🌟 **PRINCÍPIO FUNDAMENTAL**

**O jogador controla a história. A IA apenas ajuda a executá-la.**

## 🎯 **Como Funciona**

### 1. **Sistema de Fila de Ações**
- **{fazer}** - Adiciona ações à fila
- **{dizer}** - Adiciona falas à fila  
- **{historia}** - Adiciona elementos narrativos à fila
- **{mestre}** - Processa todas as ações em fila

### 2. **Fluxo de Jogo**
```
Jogador usa {fazer}, {dizer} ou {historia}
    ↓
Ação vai para fila de processamento
    ↓
Jogador usa {mestre}
    ↓
Sistema processa tudo sequencialmente
    ↓
Nova cena é gerada
    ↓
Jogador decide próximos passos
```

### 3. **Controle Total do Jogador**
- ✅ **Você decide** o que acontece
- ✅ **Você controla** o ritmo da história
- ✅ **Você cria** os elementos narrativos
- ✅ **A IA apenas executa** suas decisões

## 🚀 **Instalação e Configuração**

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
# Use config/simple_settings.yaml para o sistema simplificado
```

## 🎮 **Como Usar**

### Iniciando o Servidor
```bash
# Usando configuração simplificada
python main.py server --config config/simple_settings.yaml

# Com configurações personalizadas
python main.py server --port 6666 --host 0.0.0.0
```

### Conectando como Cliente
```bash
# Usando o arquivo principal
python main.py client

# Com host específico
python main.py client --host 192.168.1.100
```

## 📝 **Comandos do Sistema**

### **🎭 Comandos Principais**
- `{fazer <ação>}` - Adiciona uma ação à fila
  - Exemplo: `{fazer investigar a mesa em busca de pistas}`
  - Exemplo: `{fazer abrir a porta com cuidado}`
  - Exemplo: `{fazer atacar o goblin com minha espada}`

- `{dizer <fala>}` - Adiciona uma fala/diálogo à fila
  - Exemplo: `{dizer "Olá, posso ajudá-lo?"}`
  - Exemplo: `{dizer "Cuidado, há uma armadilha!"}`
  - Exemplo: `{dizer "Vamos negociar, não precisamos lutar"}`

- `{historia <elemento>}` - Adiciona um elemento narrativo à fila
  - Exemplo: `{historia uma tempestade se aproxima do horizonte}`
  - Exemplo: `{historia o ar fica mais denso e misterioso}`
  - Exemplo: `{historia uma luz azul brilha na distância}`

- `{mestre}` - Processa todas as ações em fila e gera nova cena

### **🔧 Comandos Auxiliares**
- `{status}` - Mostra seu status e da fila de ações
- `{explorar}` - Explora a localização atual
- `{mover <direção>}` - Move para uma direção
- `{inventario}` - Mostra seu inventário
- `{ajuda}` - Mostra ajuda completa
- `{salvar}` - Salva o jogo
- `{carregar}` - Carrega um jogo salvo

## 🎭 **Exemplos de Uso**

### **Cena de Exploração**
```
Jogador: {fazer examinar a parede em busca de entradas secretas}
Sistema: ✅ Ação 'examinar a parede em busca de entradas secretas' adicionada à fila de processamento.
        📝 Use {mestre} para processar todas as ações em fila.

Jogador: {dizer "Hmm, esta parede parece diferente..."
Sistema: 💬 Fala 'Hmm, esta parede parece diferente...' adicionada à fila de processamento.

Jogador: {historia uma brisa fria sopra de algum lugar
Sistema: 📖 Elemento de história 'uma brisa fria sopra de algum lugar' adicionado à fila de processamento.

Jogador: {mestre}
Sistema: 🎭 **MESTRE PROCESSANDO 3 AÇÕES**
        [Processa todas as ações e gera nova cena]
```

### **Cena de Combate**
```
Jogador: {fazer desembainhar minha espada e assumir posição de combate}
Jogador: {dizer "Você escolheu o caminho errado, bandido!"}
Jogador: {historia a tensão no ar é palpável
Jogador: {mestre}
Sistema: [Processa combate e gera resultado]
```

## 🌟 **Vantagens do Sistema Simplificado**

### **Para Jogadores**
- ✅ **Controle Total** - Você decide o que acontece
- ✅ **Narrativa Personalizada** - Sua história, suas regras
- ✅ **Ritmo Controlado** - Processe ações quando quiser
- ✅ **Criatividade Ilimitada** - Sem restrições da IA
- ✅ **Feedback Imediato** - Veja suas ações sendo processadas

### **Para Mestres**
- ✅ **Menos Preparação** - Sistema se adapta automaticamente
- ✅ **Foco na História** - Menos tempo com mecânicas
- ✅ **Flexibilidade Total** - Sistema se molda ao seu estilo
- ✅ **IA Assistente** - Ajuda sem controlar

### **Para Administradores**
- ✅ **Sistema Estável** - Menos complexidade = menos bugs
- ✅ **Configuração Simples** - Fácil de manter e modificar
- ✅ **Recursos Otimizados** - Menos uso de CPU/memória
- ✅ **Logs Limpos** - Sistema mais fácil de debugar

## 🔧 **Configurações Avançadas**

### **Fila de Ações**
```yaml
action_queue:
  max_actions_per_queue: 20  # Máximo de ações antes de forçar processamento
  processing_order: "chronological"  # Ordem de processamento
  auto_process_threshold: 10  # Processa automaticamente quando atinge este número
```

### **Sistema Simplificado**
```yaml
simplified:
  player_narrative_control: true  # Jogador controla a história
  ai_assistant_mode: true  # IA apenas ajuda
  immediate_feedback: true  # Feedback imediato nas ações
  story_context_tracking: true  # Rastreia contexto da história
```

## 🚀 **Próximos Passos**

### **Para Jogadores**
1. **Comece Simples** - Use `{fazer explorar a área}`
2. **Adicione Contexto** - Use `{historia` para atmosfera
3. **Processe Regularmente** - Use `{mestre}` para manter o ritmo
4. **Seja Criativo** - Não há limites para suas ações!

### **Para Mestres**
1. **Observe o Sistema** - Veja como os jogadores usam
2. **Ajuste Configurações** - Personalize para seu grupo
3. **Use a IA** - Aproveite para gerar respostas criativas
4. **Mantenha o Controle** - Sistema é ferramenta, não mestre

## 📚 **Documentação Adicional**

- **[README.md](README.md)** - Documentação do sistema completo
- **[config/simple_settings.yaml](config/simple_settings.yaml)** - Configuração simplificada
- **[src/game_master/simple_master.py](src/game_master/simple_master.py)** - Código do mestre simplificado

## 🎉 **Conclusão**

O **RPG AI Simplificado** coloca você no controle da sua história. A IA é sua assistente criativa, não sua controladora. Use os comandos `{fazer}`, `{dizer}`, `{historia}` e `{mestre}` para criar experiências únicas e memoráveis.

**🎯 Lembre-se: A história é sua. A IA apenas ajuda a contá-la.**

---

**🎲 Agora você tem o poder de criar suas próprias aventuras épicas!**
