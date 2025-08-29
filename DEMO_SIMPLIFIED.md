# 🎭 Demonstração do Sistema Simplificado

Este arquivo demonstra como usar o novo sistema de RPG AI que dá poder total ao jogador.

## 🚀 **Iniciando o Sistema**

### 1. **Iniciar o Servidor**
```bash
# Usar configuração simplificada
python main.py server --config config/simple_settings.yaml

# Ou usar configuração padrão
python main.py server
```

### 2. **Conectar como Cliente**
```bash
python main.py client
# Digite o IP do servidor (Radmin)
# Digite a porta (padrão: 5555)
```

## 🎮 **Demonstração Passo a Passo**

### **Cena 1: Chegada na Taverna**

```
🎲 **BEM-VINDO AO RPG AI SIMPLIFICADO, Aventureiro!**

📍 Taverna do Dragão Dourado
Uma taverna aconchegante com lareira crepitante e mesas de madeira antiga.

💡 **SISTEMA SIMPLIFICADO - COMANDOS RÁPIDOS:**
- {ajuda} - Ver todos os comandos
- {status} - Seu status e da fila de ações
- {explorar} - Explorar localização atual
- {fazer <ação>} - Adicionar ação à fila
- {dizer <fala>} - Adicionar fala à fila
- {historia <elemento>} - Adicionar elemento narrativo à fila
- {mestre} - Processar todas as ações em fila

🎯 **DICA:** Comece com {fazer explorar a área} e depois use {mestre}!
```

### **Passo 1: Explorar a Área**
```
> {fazer explorar a área da taverna, observando os clientes e a atmosfera}

✅ Ação 'explorar a área da taverna, observando os clientes e a atmosfera' adicionada à fila de processamento.
📝 Use {mestre} para processar todas as ações em fila.

📊 Status da fila: 1 ações aguardando
```

### **Passo 2: Adicionar Contexto Narrativo**
```
> {historia o cheiro de cerveja e comida caseira enche o ar

📖 Elemento de história 'o cheiro de cerveja e comida caseira enche o ar' adicionado à fila de processamento.
📝 Use {mestre} para processar todas as ações em fila.

📊 Status da fila: 2 ações aguardando
```

### **Passo 3: Interagir com NPCs**
```
> {dizer "Boa noite! Esta é uma taverna muito acolhedora."

💬 Fala 'Boa noite! Esta é uma taverna muito acolhedora.' adicionada à fila de processamento.
📝 Use {mestre} para processar todas as ações em fila.

📊 Status da fila: 3 ações aguardando
```

### **Passo 4: Processar Todas as Ações**
```
> {mestre}

🎭 **MESTRE PROCESSANDO 3 AÇÕES**

**FAZER** (Aventureiro):
_explorar a área da taverna, observando os clientes e a atmosfera_
➤ Você observa atentamente a taverna. A área principal é iluminada pela lareira, criando sombras dançantes nas paredes. Várias mesas estão ocupadas por viajantes e moradores locais, alguns conversando animadamente, outros absortos em suas bebidas. O ambiente é acolhedor e convidativo.

**HISTORIA** (Aventureiro):
_o cheiro de cerveja e comida caseira enche o ar_
➤ O aroma rico e reconfortante de cerveja artesanal e comida caseira permeia todo o ambiente. O cheiro de pão fresco assado e um guisado quente torna o lugar ainda mais acolhedor, sugerindo que a cozinha está ativa e preparando refeições para os clientes.

**DIZER** (Aventureiro):
_"Boa noite! Esta é uma taverna muito acolhedora."_
➤ Suas palavras ecoam pela taverna, chamando a atenção de alguns clientes. Um homem mais velho sentado próximo à lareira vira a cabeça e sorri, acenando com sua caneca. "Bem-vindo, viajante! Sim, é um lugar especial, esta taverna. O dono, Thorne, mantém tudo funcionando perfeitamente."

📖 **RESUMO FINAL:**
Após explorar a taverna, você descobre um ambiente acolhedor e movimentado. O cheiro de comida caseira e cerveja artesanal cria uma atmosfera convidativa. Sua saudação amigável é bem recebida pelos clientes locais, que compartilham informações sobre o dono da taverna, Thorne. A área está cheia de vida e história, com várias mesas ocupadas e uma lareira crepitante que ilumina o ambiente com uma luz quente e reconfortante.

🎯 **PRÓXIMOS PASSOS:**
• Use {fazer} para descrever ações
• Use {dizer} para falas e diálogos
• Use {historia} para elementos narrativos
• Use {mestre} para processar tudo novamente
```

## 🎭 **Demonstração de Combate**

### **Cena 2: Encontro com Bandidos**

```
> {fazer desembainhar minha espada e assumir posição defensiva}

✅ Ação 'desembainhar minha espada e assumir posição defensiva' adicionada à fila de processamento.

> {dizer "Vocês escolheram o caminho errado, bandidos!"

💬 Fala 'Vocês escolheram o caminho errado, bandidos!' adicionada à fila de processamento.

> {historia a tensão no ar é palpável, o vento carrega o som de metal contra metal

📖 Elemento de história 'a tensão no ar é palpável, o vento carrega o som de metal contra metal' adicionado à fila de processamento.

> {mestre}

🎭 **MESTRE PROCESSANDO 3 AÇÕES**

**FAZER** (Aventureiro):
_desembainhar minha espada e assumir posição defensiva_
➤ Com movimentos fluidos e treinados, você desembainha sua espada. A lâmina brilha sob a luz do sol, refletindo sua determinação. Você assume uma postura defensiva sólida, pernas firmemente plantadas no chão, espada erguida em posição de guarda. Sua experiência em combate é evidente na confiança de seus movimentos.

**DIZER** (Aventureiro):
_"Vocês escolheram o caminho errado, bandidos!"_
➤ Suas palavras ecoam pela estrada, carregando autoridade e confiança. Os bandidos trocam olhares nervosos, alguns recuando um passo. Sua voz firme e a postura de combate deixam claro que não são um alvo fácil. Um dos bandidos, aparentemente o líder, franze a testa e aperta o punho em sua arma.

**HISTORIA** (Aventureiro):
_a tensão no ar é palpável, o vento carrega o som de metal contra metal_
➤ O ar fica eletricamente carregado com a tensão do momento. O vento, antes suave, agora carrega o som metálico de armas sendo desembainhadas e ajustadas. O silêncio pesado é quebrado apenas pelo som de passos cautelosos na terra seca e o rangido de couro e metal. Todos os presentes sabem que o combate é iminente.

📖 **RESUMO FINAL:**
O confronto se intensifica dramaticamente. Sua postura de combate experiente e palavras determinadas fazem os bandidos hesitarem. A tensão no ar é eletrizante, com o som de armas sendo preparadas ecoando pelo vento. O ambiente está carregado de expectativa, e todos sabem que o combate é inevitável. Sua preparação e confiança são evidentes, criando uma presença intimidante que faz os bandidos reconsiderarem sua posição.

🎯 **PRÓXIMOS PASSOS:**
• Use {fazer} para descrever ações
• Use {dizer} para falas e diálogos
• Use {historia} para elementos narrativos
• Use {mestre} para processar tudo novamente
```

## 🔍 **Demonstração de Exploração**

### **Cena 3: Investigando Ruínas Antigas**

```
> {fazer examinar as paredes em busca de entradas secretas ou inscrições}

✅ Ação 'examinar as paredes em busca de entradas secretas ou inscrições' adicionada à fila de processamento.

> {historia a luz das tochas cria sombras misteriosas que parecem se mover

📖 Elemento de história 'a luz das tochas cria sombras misteriosas que parecem se mover' adicionado à fila de processamento.

> {dizer "Hmm, estas paredes parecem ter algo escondido..."

💬 Fala 'Hmm, estas paredes parecem ter algo escondido...' adicionada à fila de processamento.

> {mestre}

🎭 **MESTRE PROCESSANDO 3 AÇÕES**

**FAZER** (Aventureiro):
_examinar as paredes em busca de entradas secretas ou inscrições_
➤ Você examina cuidadosamente as paredes das ruínas, suas mãos experientes deslizando sobre a pedra antiga. Sua busca meticulosa revela pequenas irregularidades e marcas que poderiam ser pistas. Sua atenção aos detalhes é meticulosa, e você não deixa nenhuma área sem verificar.

**HISTORIA** (Aventureiro):
_a luz das tochas cria sombras misteriosas que parecem se mover_
➤ A luz das tochas dança pelas paredes antigas, criando um espetáculo de sombras que parece dar vida própria às ruínas. As sombras se contorcem e se movem de forma inquietante, como se as próprias paredes estivessem vivas e observando sua investigação. O efeito é ao mesmo tempo hipnotizante e levemente perturbador.

**DIZER** (Aventureiro):
_"Hmm, estas paredes parecem ter algo escondido..."_
➤ Suas palavras sussurradas ecoam pelas ruínas, carregando uma mistura de curiosidade e cautela. O tom de sua voz revela que você detectou algo interessante, algo que merece investigação mais profunda. Sua observação atrai a atenção de seus companheiros, que se aproximam para ver o que você descobriu.

📖 **RESUMO FINAL:**
Sua investigação cuidadosa das ruínas revela pistas promissoras. A luz das tochas cria um ambiente misterioso e atmosférico, com sombras que parecem ter vida própria. Sua observação sobre as paredes esconderem algo desperta o interesse de todos, sugerindo que vocês estão no caminho certo para descobrir os segredos das ruínas antigas.

🎯 **PRÓXIMOS PASSOS:**
• Use {fazer} para descrever ações
• Use {dizer} para falas e diálogos
• Use {historia} para elementos narrativos
• Use {mestre} para processar tudo novamente
```

## 💡 **Dicas de Uso**

### **1. Seja Específico**
- ❌ `{fazer lutar}`
- ✅ `{fazer desembainhar minha espada e atacar o goblin com um golpe lateral`

### **2. Use Contexto**
- ❌ `{historia algo acontece`
- ✅ `{historia o ar fica mais denso e o vento para de soprar`

### **3. Processe Regularmente**
- Não deixe muitas ações na fila
- Use `{mestre}` para manter o ritmo da história
- Ideal: 3-5 ações por processamento

### **4. Combine Tipos de Ações**
- Use `{fazer}` para ações físicas
- Use `{dizer}` para diálogo e interação
- Use `{historia}` para atmosfera e contexto

## 🎯 **Exemplos de Comandos Criativos**

### **Combate Dinâmico**
```
{fazer rolar para o lado e levantar rapidamente, espada em posição de ataque}
{dizer "Você vai precisar de mais que isso para me derrotar!"}
{historia a poeira se levanta do chão, criando uma cortina momentânea}
```

### **Exploração Detalhada**
```
{fazer examinar o chão em busca de pegadas ou marcas de arrastar}
{dizer "Estas marcas parecem recentes... alguém passou por aqui."
{historia o ar fica mais frio conforme avançamos, como se algo estivesse observando}
```

### **Interação Social**
```
{fazer aproximar-me do NPC com postura amigável e mãos visíveis}
{dizer "Olá, viajante. Posso ajudá-lo com alguma coisa?"
{historia o NPC relaxa visivelmente, reconhecendo que não sou uma ameaça}
```

## 🚀 **Próximo Passo**

Agora que você viu como funciona o sistema, **teste você mesmo!**

1. **Conecte ao servidor**
2. **Use {fazer explorar a área}**
3. **Adicione contexto com {historia}**
4. **Processe com {mestre}**
5. **Continue a história como quiser!**

**🎭 Lembre-se: A história é sua. A IA apenas ajuda a contá-la!**
