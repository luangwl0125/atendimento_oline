# 🎥 Guia de Videochamada - OriaPsi

## 📋 Opções de Videochamada Disponíveis

### 🎥 **Jitsi Meet (Recomendado)**

- **Totalmente gratuito** e de código aberto
- **Sem necessidade de conta** ou instalação
- **Privacidade garantida** - dados não são armazenados
- **Funciona em qualquer navegador**
- **Criptografia** de ponta a ponta

### 🎥 **Google Meet**

- **Mais confiável** e gratuito
- **Funciona em qualquer dispositivo**
- **Não precisa de conta Google**
- **Interface familiar**

### 🎥 **Zoom**

- **Interface familiar** para muitos usuários
- **Funciona em desktop e mobile**
- **Recursos avançados** disponíveis

### 📱 **WhatsApp Video**

- **Direto pelo celular**
- **Ideal para atendimentos rápidos**
- **Não precisa de link**

## 🔧 **Como funciona:**

1. **Psicólogo** seleciona um paciente no sistema
2. **Sistema** gera um link único para a videochamada
3. **Psicólogo** escolhe a plataforma (Jitsi Meet recomendado)
4. **Paciente** recebe o link via WhatsApp e clica para acessar
5. **Ambos** permitem acesso à câmera e microfone
6. **Conexão** é estabelecida automaticamente

## 🚀 **Instruções de Uso:**

#### Para o Psicólogo

1. Vá para "Atendimento On-line"
2. Selecione o paciente
3. **Escolha a plataforma** (Jitsi Meet recomendado)
4. Clique em "🎥 Criar [Plataforma]" para gerar o link
5. Clique em "Enviar link via WhatsApp" para compartilhar
6. Acesse o link gerado para iniciar a videochamada

#### Para o Paciente

1. Clique no link recebido via WhatsApp
2. Permita acesso à câmera e microfone quando solicitado
3. Aguarde a conexão ser estabelecida
4. A videochamada começará automaticamente

## 🎥 **Jitsi Meet - Configuração Especial**

### ✅ **Vantagens:**

- **100% gratuito** sem limitações
- **Sem anúncios** ou interrupções
- **Privacidade máxima** - dados não são armazenados
- **Conformidade** com LGPD
- **Código aberto** auditável

### 🔧 **Configuração:**

- **Navegador**: Chrome, Firefox, Safari, Edge
- **Internet**: Mínimo 1 Mbps
- **Dispositivo**: Câmera e microfone funcionando

### 📱 **Compatibilidade:**

- **Desktop**: Todos os navegadores modernos
- **Mobile**: Android e iOS
- **Tablet**: Qualquer dispositivo

## 🔍 **Solução de Problemas:**

#### Se cada um vê apenas a si mesmo

1. **Verifique o navegador**: Use Chrome, Firefox, Safari ou Edge atualizados
2. **Permissões**: Certifique-se de que câmera e microfone estão permitidos
3. **Conexão**: Verifique se a internet está estável
4. **Recarregue**: Tente recarregar a página se necessário

#### Se a conexão não funciona

1. **Firewall**: Verifique se o firewall não está bloqueando
2. **NAT**: Algumas redes corporativas podem bloquear WebRTC
3. **VPN**: Desative VPN se estiver usando
4. **Servidores STUN**: O sistema usa múltiplos servidores STUN do Google

#### Problemas específicos do Jitsi Meet

1. **Não consigo acessar**: Verifique se o link está correto
2. **Áudio não funciona**: Verifique permissões do navegador
3. **Vídeo travando**: Verifique a conexão de internet

## 📱 **Navegadores Suportados:**

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## 🌐 **Configuração de Rede:**

- **STUN Servers**: Google STUN servers (gratuitos)
- **TURN Servers**: Não configurados (requerem servidor próprio)
- **Portas**: 19302 (STUN), 3478 (TURN se configurado)

## 🔧 **Configuração Avançada:**

Se precisar de servidores TURN (para NATs restritivos):

1. Edite `webrtc_config.py`
2. Descomente a linha do servidor TURN
3. Adicione suas credenciais:

```python
{"urls": ["turn:seu-servidor.com:3478"], "username": "user", "credential": "pass"}
```

## 📊 **Monitoramento:**

- O sistema salva automaticamente as observações da sessão
- Histórico completo disponível em "Gerenciador de Pacientes" → "Histórico"

## 🆘 **Suporte:**

Se a videochamada não funcionar:

1. **Teste com Jitsi Meet** (mais confiável)
2. **Verifique as instruções** acima
3. **Teste com diferentes navegadores**
4. **Verifique a conexão** de internet
5. **Use WhatsApp Video** como alternativa

## 📚 **Documentação Adicional:**

- [Guia Completo Jitsi Meet](JITSI_MEET_GUIDE.md)
- [Solução de Videochamada](SOLUCAO_VIDEOCHAMADA.md)
- [Videochamada Final](VIDEOCHAMADA_FINAL.md)

---

**💡 Dica:** O Jitsi Meet é especialmente recomendado para sessões de psicologia devido à sua privacidade e simplicidade de uso.

**Desenvolvido por Luan Gama** 🧠
