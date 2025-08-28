# ⏰ Configurações de Timeout - RPG AI

## 📋 Visão Geral

O sistema RPG AI foi configurado para **eliminar timeouts automáticos** que poderiam interromper conexões ou respostas da IA. Isso é especialmente importante para:

- **Respostas lentas da IA** que podem demorar para gerar narrativas
- **Conexões estáveis** dos jogadores sem desconexão automática
- **Sessões persistentes** que não expiram por inatividade

## 🔧 Configurações Implementadas

### 1. **Servidor (`server`)**
```yaml
server:
  timeout: 0                    # Timeout geral do servidor (0 = ilimitado)
  connection_timeout: 0          # Timeout de conexão (0 = ilimitado)
  player_name_timeout: 0         # Timeout para nome do jogador (0 = ilimitado)
```

**Explicação:**
- `timeout: 0` - Remove timeout geral do servidor
- `connection_timeout: 0` - Conexões de clientes nunca expiram
- `player_name_timeout: 0` - Jogadores podem demorar para digitar o nome

### 2. **IA (`ai`)**
```yaml
ai:
  request_timeout: 0             # Timeout de requisição para IA (0 = ilimitado)
  connection_timeout: 0          # Timeout de conexão com IA (0 = ilimitado)
```

**Explicação:**
- `request_timeout: 0` - Requisições para IA nunca expiram
- `connection_timeout: 0` - Conexão com servidor de IA é mantida
- **Importante:** Permite que a IA demore o tempo necessário para gerar respostas

### 3. **Jogo (`game`)**
```yaml
game:
  session_timeout: 0             # Timeout de sessão (0 = ilimitado)
```

**Explicação:**
- `session_timeout: 0` - Jogadores nunca são desconectados por inatividade
- Sessões permanecem ativas indefinidamente
- Útil para jogos longos ou pausas durante a sessão

## 🚀 Como Funciona

### **Antes (com timeouts):**
```python
# Timeout de 30 segundos para nome do jogador
conn.settimeout(30)

# Timeout de 30 segundos para requisições da IA
response = requests.post(url, json=data, timeout=30)

# Jogadores expiravam após 5 minutos de inatividade
def is_active(self, timeout_minutes=5):
    return delta.total_seconds() < (timeout_minutes * 60)
```

### **Agora (sem timeouts):**
```python
# Sem timeout para nome do jogador
timeout_value = config.get('server.player_name_timeout', 0)
conn.settimeout(timeout_value if timeout_value > 0 else None)

# Sem timeout para requisições da IA
timeout = config.get('ai.request_timeout', 0) or None
response = requests.post(url, json=data, timeout=timeout)

# Jogadores nunca expiram se session_timeout = 0
def is_active(self, timeout_minutes=None):
    if timeout_minutes is None or timeout_minutes <= 0:
        return True  # Sempre ativo
```

## 📊 Benefícios

### ✅ **Para a IA:**
- Pode demorar o tempo necessário para gerar respostas complexas
- Não há interrupção de conexão durante processamento
- Respostas mais elaboradas e contextuais

### ✅ **Para os Jogadores:**
- Conexões estáveis sem desconexão automática
- Podem fazer pausas durante o jogo
- Sessões persistentes entre jogadas

### ✅ **Para o Sistema:**
- Maior estabilidade de conexões
- Melhor experiência do usuário
- Menos problemas de reconexão

## ⚠️ Considerações

### **Segurança:**
- Conexões ilimitadas podem ser usadas para ataques de DoS
- Considere implementar rate limiting se necessário
- Monitore conexões ativas para detectar abusos

### **Recursos:**
- Conexões persistentes consomem mais memória
- Monitore uso de recursos do servidor
- Implemente limpeza manual se necessário

### **Configuração:**
- Para reativar timeouts, altere os valores de `0` para segundos/minutos
- Exemplo: `timeout: 300` para 5 minutos
- Reinicie o servidor após alterações

## 🔄 Como Alterar

### **Para Reativar Timeouts:**
```yaml
# Exemplo: timeout de 5 minutos
server:
  timeout: 300
  connection_timeout: 300
  player_name_timeout: 60

ai:
  request_timeout: 120          # 2 minutos para IA
  connection_timeout: 60        # 1 minuto para conexão

game:
  session_timeout: 30           # 30 minutos de sessão
```

### **Para Timeouts Personalizados:**
```yaml
# Exemplo: configurações balanceadas
server:
  timeout: 600                  # 10 minutos geral
  connection_timeout: 300       # 5 minutos conexão
  player_name_timeout: 120      # 2 minutos para nome

ai:
  request_timeout: 300          # 5 minutos para IA
  connection_timeout: 120       # 2 minutos conexão IA

game:
  session_timeout: 60           # 1 hora de sessão
```

## 📝 Logs e Monitoramento

### **Verificar Configurações:**
```bash
# Testar configurações de timeout
python -c "
from src.utils.config import config
print(f'Server timeout: {config.get(\"server.timeout\")}')
print(f'AI timeout: {config.get(\"ai.request_timeout\")}')
print(f'Session timeout: {config.get(\"game.session_timeout\")}')
"
```

### **Monitorar Conexões:**
- Verifique logs do servidor para conexões ativas
- Monitore tempo de resposta da IA
- Acompanhe duração das sessões

## 🎯 Recomendações

### **Para Desenvolvimento:**
- Mantenha timeouts ilimitados durante testes
- Facilita debugging e desenvolvimento
- Permite testar cenários complexos

### **Para Produção:**
- Configure timeouts apropriados para seu ambiente
- Balanceie entre estabilidade e segurança
- Monitore performance e recursos

### **Para Jogos Longos:**
- Use `session_timeout: 0` para sessões persistentes
- Configure `ai.request_timeout: 0` para respostas complexas
- Mantenha `connection_timeout: 0` para estabilidade

---

**Nota:** As configurações atuais (timeouts = 0) são ideais para desenvolvimento e jogos casuais. Para ambientes de produção com muitos usuários, considere implementar timeouts apropriados baseados nos seus requisitos de segurança e recursos.
