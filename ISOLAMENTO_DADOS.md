# 🔒 Sistema de Isolamento de Dados - OriaPsi

## 📋 Visão Geral

O sistema foi modificado para garantir que cada profissional de psicologia tenha acesso apenas aos seus próprios dados (pacientes e sessões), mantendo total isolamento e privacidade entre diferentes usuários.

## 🛡️ Funcionalidades Implementadas

### 🔐 Isolamento por CRP

- **Arquivos separados**: Cada profissional tem seus próprios arquivos JSON
- **Nomenclatura**: `pacientes_CRP.json` e `sessoes_CRP.json`
- **Segurança**: Dados completamente isolados entre profissionais
- **Privacidade**: Nenhum acesso cruzado entre usuários

### 📁 Estrutura de Arquivos

#### Antes (Sistema Geral)

```
pacientes.json     # Dados de todos os usuários
sessoes.json       # Sessões de todos os usuários
```

#### Agora (Sistema Isolado)

```
pacientes_06_123456.json    # Dados do CRP 06/123456
sessoes_06_123456.json      # Sessões do CRP 06/123456
pacientes_06_789012.json    # Dados do CRP 06/789012
sessoes_06_789012.json      # Sessões do CRP 06/789012
```

### 🔄 Migração de Dados

- **Detecção automática**: Sistema identifica dados existentes
- **Migração opcional**: Profissional pode migrar dados antigos
- **Preservação**: Dados originais mantidos como backup
- **Notificação**: Interface informa sobre dados disponíveis

## 🔧 Como Funciona

### 1. **Login do Profissional**

- Usuário faz login com CRP
- Sistema identifica o profissional
- Carrega apenas dados específicos do CRP

### 2. **Carregamento de Dados**

```python
def carregar_pacientes(crp=None):
    if crp:
        arquivo = f'pacientes_{crp.replace("/", "_")}.json'
    else:
        arquivo = 'pacientes.json'
```

### 3. **Salvamento de Dados**

```python
def salvar_pacientes(pacientes, crp=None):
    if crp:
        arquivo = f'pacientes_{crp.replace("/", "_")}.json'
    else:
        arquivo = 'pacientes.json'
```

### 4. **Isolamento Garantido**

- Cada profissional vê apenas seus dados
- Não há acesso cruzado entre usuários
- Dados são salvos em arquivos separados

## 📊 Interface do Usuário

### Dashboard Profissional

- **Métricas**: Número de pacientes e sessões do profissional
- **Identificação**: CRP do usuário logado
- **Migração**: Opção para migrar dados existentes

### Mensagens Contextuais

- "Nenhum paciente cadastrado **em seu perfil**"
- "X paciente(s) cadastrado(s) **em seu perfil profissional**"
- "Dados específicos do CRP: XX/XXXXXX"

## 🔒 Segurança e Privacidade

### ✅ Implementado

- **Isolamento total**: Dados separados por CRP
- **Validação de acesso**: Apenas dados do usuário logado
- **Migração segura**: Dados antigos preservados
- **Interface clara**: Identificação do profissional

### 🛡️ Benefícios

- **LGPD**: Conformidade com proteção de dados
- **Ética**: Sigilo profissional garantido
- **Segurança**: Sem acesso cruzado entre usuários
- **Auditoria**: Rastreabilidade por profissional

## 🚀 Como Usar

### Para Novos Usuários

1. **Faça login** com seu CRP
2. **Cadastre pacientes** normalmente
3. **Dados salvos** automaticamente em seu perfil
4. **Acesso restrito** apenas aos seus dados

### Para Usuários Existentes

1. **Faça login** com seu CRP
2. **Sistema detecta** dados antigos
3. **Clique em "Migrar"** se desejar
4. **Dados transferidos** para seu perfil

### Para Administradores

1. **Verifique arquivos**: `pacientes_CRP.json`
2. **Backup**: Dados originais preservados
3. **Auditoria**: Rastreabilidade por profissional

## 📋 Funções Modificadas

### `carregar_pacientes(crp=None)`

- Carrega dados específicos do profissional
- Fallback para arquivo geral se necessário

### `salvar_pacientes(pacientes, crp=None)`

- Salva dados no arquivo específico do profissional
- Garante isolamento de dados

### `carregar_sessoes(crp=None)`

- Carrega sessões específicas do profissional
- Mantém histórico isolado

### `salvar_sessoes(sessoes, crp=None)`

- Salva sessões no arquivo específico do profissional
- Preserva privacidade

### `migrar_dados_existentes(crp)`

- Migra dados antigos para perfil específico
- Preserva dados originais

### `mostrar_info_profissional()`

- Exibe métricas do profissional
- Oferece opção de migração

## 🔍 Monitoramento

### Arquivos Criados

- `pacientes_CRP.json`: Pacientes do profissional
- `sessoes_CRP.json`: Sessões do profissional
- Logs de migração (se aplicável)

### Métricas Disponíveis

- Número de pacientes por profissional
- Número de sessões por profissional
- Status de migração de dados

## ⚠️ Considerações Importantes

### Backup

- **Dados originais**: Preservados como backup
- **Migração**: Opcional e controlada
- **Recuperação**: Possível restaurar dados antigos

### Compatibilidade

- **Sistema anterior**: Funciona normalmente
- **Novos usuários**: Isolamento automático
- **Migração**: Processo transparente

### Segurança

- **Isolamento**: Garantido por design
- **Validação**: CRP verificado em cada operação
- **Auditoria**: Rastreabilidade completa

## 📞 Suporte

### Problemas Comuns

1. **Dados não aparecem**: Verifique se está logado com CRP correto
2. **Migração falhou**: Dados originais preservados
3. **Arquivo não encontrado**: Sistema cria automaticamente

### Contato

- **Logs**: Verifique console para erros
- **Backup**: Dados originais sempre preservados
- **Recuperação**: Processo de migração reversível

---

**💡 Dica**: O sistema de isolamento garante que cada profissional tenha acesso apenas aos seus dados, mantendo total privacidade e conformidade com a LGPD e Código de Ética Profissional.
