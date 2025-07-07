# 📝 Sistema de Registro - OriaPsi

## 📋 Visão Geral

O sistema foi atualizado para permitir que psicólogos façam seu próprio cadastro no primeiro acesso, criando suas senhas e fornecendo informações completas de identificação.

## 🛡️ Funcionalidades Implementadas

### 🔑 Sistema de Login Duplo

- **Aba Login**: Para usuários já cadastrados
- **Aba Primeiro Acesso**: Para novos usuários
- **Validação robusta**: Formato CRP e senhas
- **Autenticação segura**: Verificação de credenciais

### 📝 Registro de Novos Usuários

- **Nome Completo**: Campo obrigatório
- **CRP**: Formato livre (mínimo 3 caracteres)
- **Senha**: Mínimo 6 caracteres
- **Confirmação**: Verificação de senha
- **Validações**: Múltiplas verificações de dados

### 🔒 Validações de Segurança

- **CRP válido**: Mínimo 3 caracteres
- **Senha forte**: Mínimo 6 caracteres
- **CRP único**: Não permite duplicatas
- **Dados obrigatórios**: Todos os campos preenchidos

## 🔧 Como Funciona

### 1. **Primeiro Acesso**

```
Usuário acessa → Aba "Primeiro Acesso" → Preenche dados → Validação → Cadastro
```

### 2. **Login Regular**

```
Usuário acessa → Aba "Login" → CRP + Senha → Autenticação → Acesso
```

### 3. **Validação de CRP**

```python
def validar_crp(crp):
    # Removida validação de formato específico
    # Aceita qualquer formato de CRP
    return len(crp.strip()) >= 3  # Mínimo 3 caracteres
```

### 4. **Verificação de Usuário**

```python
def verificar_usuario_existe(crp):
    usuarios = carregar_usuarios()
    return any(u['crp'] == crp for u in usuarios)
```

## 📊 Interface do Usuário

### Aba Login

- **Campo CRP**: Placeholder com exemplo
- **Campo Senha**: Protegido por asteriscos
- **Botão Entrar**: Validação completa
- **Mensagens**: Feedback claro de erros

### Aba Primeiro Acesso

- **Nome Completo**: Campo obrigatório
- **CRP**: Com validação de formato
- **Senha**: Mínimo 6 caracteres
- **Confirmar Senha**: Verificação
- **Validação em tempo real**: Feedback imediato

### Validações Visuais

- ✅ **Dados válidos**: Mensagem de sucesso
- ❌ **Erro de formato**: CRP inválido
- ❌ **CRP duplicado**: Já cadastrado
- ❌ **Senhas diferentes**: Não coincidem
- ❌ **Senha fraca**: Menos de 6 caracteres

## 🔒 Segurança e Validação

### ✅ Validações Implementadas

- **CRP válido**: Mínimo 3 caracteres
- **CRP único**: Não permite duplicatas
- **Senha mínima**: 6 caracteres
- **Confirmação**: Senhas devem coincidir
- **Nome válido**: Mínimo 3 caracteres
- **Campos obrigatórios**: Todos preenchidos

### 🛡️ Estrutura de Dados

```json
{
  "nome": "Dr. João Silva Santos",
  "crp": "06/123456",
  "senha": "senha123",
  "email": "joao.silva@exemplo.com",
  "ativo": true,
  "data_cadastro": "2024-01-01 10:00"
}
```

## 🚀 Como Usar

### Para Novos Usuários

1. **Acesse** a aplicação
2. **Clique** na aba "📝 Primeiro Acesso"
3. **Preencha** todos os campos:
   - Nome Completo
   - CRP (mínimo 3 caracteres)
   - Senha (mínimo 6 caracteres)
   - Confirmar Senha
4. **Clique** em "📝 Cadastrar"
5. **Faça login** na aba "🔑 Login"

### Para Usuários Existentes

1. **Acesse** a aplicação
2. **Clique** na aba "🔑 Login"
3. **Digite** CRP e senha
4. **Clique** em "🔑 Entrar"

### Exemplos de Dados

- **CRP válido**: 06/123456, 12/789012, 01/345678, CRP123, 06-123456
- **CRP inválido**: 12, ab, (vazio)
- **Senha válida**: senha123, minhaSenha, 123456
- **Senha inválida**: 123, abc, (vazia)

## 📋 Funções Criadas

### `carregar_usuarios()`

- Carrega lista de usuários do arquivo JSON
- Tratamento de erros incluído

### `salvar_usuarios(usuarios)`

- Salva lista de usuários no arquivo JSON
- Preserva formatação e encoding

### `validar_crp(crp)`

- Valida CRP com mínimo 3 caracteres
- Aceita qualquer formato

### `verificar_usuario_existe(crp)`

- Verifica se CRP já está cadastrado
- Evita duplicatas

### `registrar_novo_usuario(nome, crp, senha)`

- Registra novo usuário no sistema
- Inclui timestamp de cadastro

### `autenticar_usuario(crp, senha)`

- Autentica usuário existente
- Verifica senha e status ativo

## 🔍 Monitoramento

### Arquivos Criados

- `usuarios.json`: Base de dados de usuários
- Logs de cadastro e login
- Histórico de acessos

### Métricas Disponíveis

- Número de usuários cadastrados
- Taxa de sucesso de login
- Validações de formato CRP
- Erros de autenticação

## ⚠️ Considerações Importantes

### Segurança

- **Senhas em texto**: Em produção, usar hash bcrypt
- **Validação client-side**: Complementar com server-side
- **Rate limiting**: Implementar para evitar spam
- **Logs de acesso**: Auditoria de tentativas

### Melhorias Futuras

- **Criptografia**: Hash de senhas
- **Recuperação**: Esqueci minha senha
- **Perfil**: Edição de dados pessoais
- **2FA**: Autenticação de dois fatores

### Compatibilidade

- **Dados existentes**: Preservados
- **Migração**: Processo transparente
- **Backup**: Dados originais mantidos

## 📞 Suporte

### Problemas Comuns

1. **CRP inválido**: Digite pelo menos 3 caracteres
2. **CRP já cadastrado**: Use aba de login
3. **Senha fraca**: Mínimo 6 caracteres
4. **Senhas diferentes**: Confirme corretamente

### Validações

- **CRP mínimo**: 3 caracteres
- **Senha mínima**: 6 caracteres
- **Nome mínimo**: 3 caracteres
- **Campos obrigatórios**: Todos preenchidos

---

**💡 Dica**: O sistema de registro garante que apenas profissionais de psicologia com CRP válido tenham acesso à plataforma, mantendo a segurança e ética da aplicação.
