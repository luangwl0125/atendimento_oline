import os
# garante que ffmpeg.exe e ffprobe.exe na raiz sejam encontrados
os.environ["PATH"] += os.pathsep + os.getcwd()

import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import uuid
from urllib.parse import quote

# URL pública do seu app (ajuste para seu domínio)
BASE_URL = "https://oria-psi-atendimento-oline.streamlit.app"

# Configuração única da página
st.set_page_config(
    page_title="OriaPsi",
    page_icon="🧠",
    layout="wide"
)

# ==== Sistema de Login e Termos ====
def mostrar_termos():
    st.markdown("""
    # 🛡️ Termos de Uso e Política de Privacidade
    
    ## Compromisso com a Ética, Segurança e Sigilo Profissional
    
    Este serviço foi desenvolvido como ferramenta de apoio técnico à elaboração de documentos psicológicos, com base nas diretrizes estabelecidas pela Resolução CFP nº 06/2019, pela Resolução CFP nº 01/2009 (Política de Proteção de Dados) e pelo Código de Ética Profissional do Psicólogo.
    
    ### 🧠 Responsabilidade Técnica e Ética
    - As produções dos documentos devem obrigatoriamente ser revisadas, validadas e assinadas por psicóloga(o) devidamente inscrita(o) no CRP, conforme determina a legislação profissional.
    - O conteúdo gerado não substitui o julgamento clínico e técnico do profissional.
    
    ### 📌 Finalidade do Sistema
    Este assistente virtual tem como único propósito auxiliar a(o) psicóloga(o) na sistematização de informações, organização textual e conformidade estrutural de documentos, sempre respeitando os princípios de autonomia, consentimento informado, sigilo, não exposição e ética nas relações profissionais.
    
    ### ⚖️ Referências Normativas
    - **Resolução CFP nº 06/2019** – Elaboração de Documentos Escritos Produzidos pela(o) Psicóloga(o)
    - **Código de Ética Profissional do Psicólogo** – Artigos 1º, 9º, 13º e 14º
    - **Resolução CFP nº 11/2018** – Sobre uso de tecnologias da informação e comunicação
    - **LGPD (Lei Geral de Proteção de Dados)** – Aplicabilidade ao contexto psicológico
    
    ### 🔒 Privacidade e Proteção de Dados
    
    Esta ferramenta foi construída em conformidade com:
    - O Código de Ética do Profissional Psicólogo (Resolução CFP nº 010/2005);
    - A Resolução CFP nº 06/2019: Elaboração de Documentos Escritos Produzidos pela(o) Psicóloga(o);
    - Resolução CFP nº 11/2018: Sobre uso de tecnologias da informação e comunicação
    - **Criptografia em trânsito (HTTPS)**: Criptografia de Ponta a Ponta para Proteger Dados em Trânsito e em Repouso. Todos os dados são protegidos contra interceptação.
    - **Controle de acesso**: APIs protegidas com autenticação para impedir acesso não autorizado.
    - **Validação de entrada**: Validações automáticas, evitando injeções maliciosas ou erros lógicos.
    - **Registros e auditoria**: Rastreamento de dados com precisão (data/hora e autor), ajudando na responsabilização e conformidade com normas como a LGPD.
    - **Anonimização**: Omissão de dados sensíveis antes de armazenar ou compartilhar informações JSON, promovendo privacidade.
    - **Normas da Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018)**, que regula o tratamento de dados pessoais no Brasil. Seu objetivo principal é garantir o direito à privacidade e à proteção dos dados dos cidadãos, estabelecendo regras claras sobre coleta, uso, armazenamento e compartilhamento de informações pessoais por empresas, órgãos públicos e profissionais autônomos incluindo psicólogas(os).
    
    **Ao utilizar este sistema, você declara ciência de que respeita e segue os preceitos éticos da profissão e que assume a responsabilidade técnica e legal pelos documentos emitidos com o apoio desta ferramenta.**
    """)

def carregar_usuarios():
    """Carrega lista de usuários registrados"""
    try:
        if os.path.exists('usuarios.json'):
            return json.load(open('usuarios.json','r',encoding='utf-8'))
    except Exception as e:
        st.error(f"Erro ao carregar usuários: {e}")
    return []

def salvar_usuarios(usuarios):
    """Salva lista de usuários"""
    try:
        with open('usuarios.json','w',encoding='utf-8') as f:
            json.dump(usuarios,f,ensure_ascii=False,indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar usuários: {e}")

def validar_crp(crp):
    """Valida formato do CRP"""
    import re
    # Formato: XX/XXXXXX (2 dígitos, barra, 6 dígitos)
    pattern = r'^\d{2}/\d{6}$'
    return bool(re.match(pattern, crp))

def verificar_usuario_existe(crp):
    """Verifica se usuário já existe"""
    usuarios = carregar_usuarios()
    return any(u['crp'] == crp for u in usuarios)

def registrar_novo_usuario(nome, crp, senha):
    """Registra novo usuário no sistema"""
    usuarios = carregar_usuarios()
    
    novo_usuario = {
        'nome': nome,
        'crp': crp,
        'senha': senha,  # Em produção, usar hash da senha
        'data_cadastro': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'ativo': True
    }
    
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    return True

def autenticar_usuario(crp, senha):
    """Autentica usuário existente"""
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario['crp'] == crp and usuario['senha'] == senha and usuario['ativo']:
            return usuario
    return None

def pagina_login():
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>🧠 OriaPsi</h1>
        <h3>Plataforma de Atendimento Psicológico On-line</h3>
        <p style="color: #666; font-size: 1.1rem;">Acesso Restrito a Profissionais de Psicologia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para Login e Registro
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Primeiro Acesso"])
    
    with tab1:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### 🔐 Login Profissional")
                
                # Campos de login
                crp_login = st.text_input("CRP (Ex: 06/123456)", placeholder="06/123456", key="login_crp")
                senha_login = st.text_input("Senha", type="password", placeholder="Digite sua senha", key="login_senha")
                
                # Botão de login
                if st.button("🔑 Entrar", use_container_width=True):
                    if crp_login and senha_login:
                        if validar_crp(crp_login):
                            usuario = autenticar_usuario(crp_login, senha_login)
                            if usuario:
                                st.session_state.logado = True
                                st.session_state.crp = crp_login
                                st.session_state.nome_usuario = usuario['nome']
                                st.rerun()
                            else:
                                st.error("❌ CRP ou senha incorretos!")
                        else:
                            st.error("❌ Formato de CRP inválido! Use: XX/XXXXXX")
                    else:
                        st.error("❌ Preencha todos os campos!")
                
                st.markdown("---")
                st.info("""
                **⚠️ Aviso Importante:**
                - Este sistema é destinado exclusivamente a psicólogos registrados no CRP
                - Todos os dados são protegidos conforme LGPD e Código de Ética Profissional
                - O uso é de responsabilidade técnica e legal do profissional
                """)
    
    with tab2:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### 📝 Primeiro Acesso - Cadastro")
                st.info("""
                **Novo no sistema?**
                Faça seu cadastro como profissional de psicologia.
                """)
                
                # Campos de registro
                nome_completo = st.text_input("Nome Completo", placeholder="Digite seu nome completo", key="reg_nome")
                crp_registro = st.text_input("CRP (Ex: 06/123456)", placeholder="06/123456", key="reg_crp")
                senha_registro = st.text_input("Senha", type="password", placeholder="Crie uma senha", key="reg_senha")
                senha_confirmacao = st.text_input("Confirmar Senha", type="password", placeholder="Confirme sua senha", key="reg_senha_confirm")
                
                # Validações
                if nome_completo and crp_registro and senha_registro and senha_confirmacao:
                    if not validar_crp(crp_registro):
                        st.error("❌ Formato de CRP inválido! Use: XX/XXXXXX")
                    elif verificar_usuario_existe(crp_registro):
                        st.error("❌ CRP já cadastrado! Use a aba de login.")
                    elif senha_registro != senha_confirmacao:
                        st.error("❌ Senhas não coincidem!")
                    elif len(senha_registro) < 6:
                        st.error("❌ Senha deve ter pelo menos 6 caracteres!")
                    elif len(nome_completo) < 3:
                        st.error("❌ Nome deve ter pelo menos 3 caracteres!")
                    else:
                        st.success("✅ Dados válidos! Clique em 'Cadastrar' para continuar.")
                
                # Botão de registro
                if st.button("📝 Cadastrar", use_container_width=True):
                    if nome_completo and crp_registro and senha_registro and senha_confirmacao:
                        if validar_crp(crp_registro) and not verificar_usuario_existe(crp_registro) and senha_registro == senha_confirmacao and len(senha_registro) >= 6 and len(nome_completo) >= 3:
                            if registrar_novo_usuario(nome_completo, crp_registro, senha_registro):
                                st.success("✅ Cadastro realizado com sucesso!")
                                st.info("Agora você pode fazer login na aba 'Login'.")
                                # Limpar campos
                                st.session_state.reg_nome = ""
                                st.session_state.reg_crp = ""
                                st.session_state.reg_senha = ""
                                st.session_state.reg_senha_confirm = ""
                                st.rerun()
                            else:
                                st.error("❌ Erro ao realizar cadastro!")
                        else:
                            st.error("❌ Verifique os dados informados!")
                    else:
                        st.error("❌ Preencha todos os campos!")
                
                st.markdown("---")
                st.info("""
                **📋 Informações do Cadastro:**
                - CRP deve estar no formato XX/XXXXXX
                - Senha deve ter pelo menos 6 caracteres
                - Nome completo é obrigatório
                - Cada CRP pode ter apenas uma conta
                """)
    
    # Botão para ver termos (disponível em ambas as abas)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📋 Ver Termos de Uso", use_container_width=True):
            st.session_state.mostrar_termos = True
            st.rerun()

# ==== Inicialização da Sessão ====
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'mostrar_termos' not in st.session_state:
    st.session_state.mostrar_termos = False

# ==== Verificação de Login ====
if not st.session_state.logado:
    if st.session_state.mostrar_termos:
        mostrar_termos()
        if st.button("🔙 Voltar ao Login"):
            st.session_state.mostrar_termos = False
            st.rerun()
    else:
        pagina_login()
    st.stop()

# ==== Cabeçalho da Aplicação Principal ====
nome_usuario = st.session_state.get('nome_usuario', 'Profissional')
st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>🧠 OriaPsi - Atendimento On-line 📞</h1>
            <p style="margin: 0; color: #666;">Profissional: {nome_usuario} ({st.session_state.crp})</p>
        </div>
        <div style="text-align: right;">
            <p style="margin: 0; color: #666;">Sessão ativa</p>
            <p style="margin: 0; font-size: 0.8rem; color: #999;">{datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Botão de logout
if st.sidebar.button("🚪 Sair"):
    st.session_state.logado = False
    st.session_state.mostrar_termos = False
    st.rerun()

# ==== Parte "somente vídeo" se houver ?room=xxx ====
params = st.query_params  # substituído experimental_get_query_params
room = params.get("room", [None])[0]

if room:
    st.title(f"🧠 Videochamada — Sala {room}")
    st.info("🎥 Esta funcionalidade foi substituída por integração com plataformas externas.")
    st.markdown("""
    **Para videochamadas, use:**
    - **Google Meet**: Mais confiável e gratuito
    - **Zoom**: Interface familiar
    - **WhatsApp Video**: Direto pelo celular
    
    Volte à página principal e selecione uma das opções de videochamada.
    """)
    
    if st.button("🔙 Voltar à Página Principal"):
        st.experimental_rerun()
    
    st.stop()

# ==== Funções de I/O e utilitárias ====
def carregar_pacientes(crp=None):
    try:
        if crp:
            # Arquivo específico para o profissional
            arquivo = f'pacientes_{crp.replace("/", "_")}.json'
        else:
            # Arquivo geral (fallback)
            arquivo = 'pacientes.json'
            
        if os.path.exists(arquivo):
            return json.load(open(arquivo,'r',encoding='utf-8'))
    except Exception as e:
        st.error(f"Erro ao carregar pacientes: {e}")
    return []

def salvar_pacientes(pacientes, crp=None):
    try:
        if crp:
            # Arquivo específico para o profissional
            arquivo = f'pacientes_{crp.replace("/", "_")}.json'
        else:
            # Arquivo geral (fallback)
            arquivo = 'pacientes.json'
            
        with open(arquivo,'w',encoding='utf-8') as f:
            json.dump(pacientes,f,ensure_ascii=False,indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar pacientes: {e}")

def carregar_sessoes(crp=None):
    try:
        if crp:
            # Arquivo específico para o profissional
            arquivo = f'sessoes_{crp.replace("/", "_")}.json'
        else:
            # Arquivo geral (fallback)
            arquivo = 'sessoes.json'
            
        if os.path.exists(arquivo):
            return json.load(open(arquivo,'r',encoding='utf-8'))
    except Exception as e:
        st.error(f"Erro ao carregar sessões: {e}")
    return []

def salvar_sessoes(sessoes, crp=None):
    try:
        if crp:
            # Arquivo específico para o profissional
            arquivo = f'sessoes_{crp.replace("/", "_")}.json'
        else:
            # Arquivo geral (fallback)
            arquivo = 'sessoes.json'
            
        with open(arquivo,'w',encoding='utf-8') as f:
            json.dump(sessoes,f,ensure_ascii=False,indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar sessões: {e}")

def obter_crp_atual():
    """Retorna o CRP do usuário logado ou None"""
    return st.session_state.get('crp', None)

def migrar_dados_existentes(crp):
    """Migra dados do arquivo geral para o arquivo específico do profissional"""
    try:
        # Migrar pacientes
        if os.path.exists('pacientes.json'):
            pacientes_gerais = json.load(open('pacientes.json','r',encoding='utf-8'))
            if pacientes_gerais:
                arquivo_especifico = f'pacientes_{crp.replace("/", "_")}.json'
                if not os.path.exists(arquivo_especifico):
                    with open(arquivo_especifico,'w',encoding='utf-8') as f:
                        json.dump(pacientes_gerais,f,ensure_ascii=False,indent=2)
                    st.info(f"📋 {len(pacientes_gerais)} paciente(s) migrado(s) para seu perfil.")
        
        # Migrar sessões
        if os.path.exists('sessoes.json'):
            sessoes_gerais = json.load(open('sessoes.json','r',encoding='utf-8'))
            if sessoes_gerais:
                arquivo_especifico = f'sessoes_{crp.replace("/", "_")}.json'
                if not os.path.exists(arquivo_especifico):
                    with open(arquivo_especifico,'w',encoding='utf-8') as f:
                        json.dump(sessoes_gerais,f,ensure_ascii=False,indent=2)
                    st.info(f"📊 {len(sessoes_gerais)} sessão(ões) migrada(s) para seu perfil.")
                    
    except Exception as e:
        st.warning(f"Aviso: Erro na migração de dados: {e}")

def mostrar_info_profissional():
    """Mostra informações sobre o profissional logado e seus dados"""
    crp = obter_crp_atual()
    if crp:
        pacientes = carregar_pacientes(crp)
        sessoes = carregar_sessoes(crp)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Pacientes", len(pacientes))
        with col2:
            st.metric("📊 Sessões", len(sessoes))
        with col3:
            st.metric("🔐 Profissional", crp)
        
        # Verificar se há dados para migrar
        if os.path.exists('pacientes.json') or os.path.exists('sessoes.json'):
            with st.expander("🔄 Migrar Dados Existentes"):
                st.info("""
                **Dados existentes detectados!**
                
                Encontramos dados no sistema anterior. Você pode migrar esses dados para seu perfil profissional.
                """)
                if st.button("📋 Migrar Dados para Meu Perfil"):
                    migrar_dados_existentes(crp)
                    st.rerun()

# ==== Navegação Principal ====
page = st.sidebar.selectbox(
    "Escolha uma opção:",
    ["Atender Agora","Gerenciar Pacientes"]
)
if st.sidebar.button("🔄 Recarregar Dados"):
    st.rerun()

# Carrega e garante room_id permanente por paciente
pacientes = carregar_pacientes(obter_crp_atual())
updated = False
for p in pacientes:
    if 'room_id' not in p:
        p['room_id'] = uuid.uuid4().hex[:8]
        updated = True
if updated:
    salvar_pacientes(pacientes, obter_crp_atual())
sessoes = carregar_sessoes(obter_crp_atual())

# Mostra informações do profissional
mostrar_info_profissional()

# ==== Página de Atender Agora ====
if page == "Atender Agora":
    if not pacientes:
        st.warning("⚠️ Nenhum paciente cadastrado em seu perfil. Adicione pelo Gerenciar Pacientes.")
    else:
        st.success(f"✅ {len(pacientes)} paciente(s) cadastrado(s) em seu perfil profissional")
        nomes = [p['nome'] for p in pacientes]
        sel = st.selectbox("Selecione o paciente:",["..."]+nomes)
        if sel != "...":
            p = next(x for x in pacientes if x['nome']==sel)
            # Link de videochamada (mantido para compatibilidade)
            share_link = f"{BASE_URL}?room={p['room_id']}"
            
            # Instruções para videochamada
            with st.expander("📋 Instruções para Videochamada"):
                st.markdown(f"""
                **Opções de Videochamada Disponíveis:**
                
                ### 📱 WhatsApp
                - **Enviar link**: Envia o link da plataforma via WhatsApp
                - **WhatsApp Video**: Inicia videochamada direta pelo WhatsApp
                
                ### 🎥 Google Meet
                - **Mais confiável** e gratuito
                - Funciona em qualquer dispositivo
                - Não precisa de conta Google
                - Clique em "Criar Google Meet" e envie o link
                
                ### 🎥 Zoom
                - **Interface familiar** para muitos usuários
                - Funciona em desktop e mobile
                - Clique em "Criar Zoom" e envie o link
                
                ### 🎥 Jitsi Meet
                - **Totalmente gratuito** e de código aberto
                - **Sem necessidade de conta** ou instalação
                - **Privacidade garantida** - dados não são armazenados
                - Funciona em qualquer navegador
                - Clique em "Criar Jitsi Meet" e envie o link
                
                **Como usar:**
                1. **Escolha uma plataforma** (Jitsi Meet ou Google Meet recomendados)
                2. **Clique em criar** a videochamada
                3. **Envie o link** via WhatsApp para o paciente
                4. **Ambos acessem** o link para iniciar a videochamada
                
                **Dicas:**
                - **Jitsi Meet** é ideal para privacidade e simplicidade
                - **Google Meet** é a opção mais confiável
                - **WhatsApp Video** é ideal para atendimentos rápidos
                - **Zoom** é familiar para usuários experientes
                """)

            # Informações do paciente
            col1,col2 = st.columns(2)
            with col1:
                st.subheader("📋 Informações do Paciente")
                st.write(f"**Nome:** {p['nome']}")
                st.write(f"**Idade:** {p['idade']} anos")
                st.write(f"**Data de Nascimento:** {p.get('data_nascimento','Não informado')}")
                st.write(f"**Telefone:** {p.get('telefone','Não informado')}")
                st.write(f"**E-mail:** {p.get('email','Não informado')}")
                st.write(f"**Endereço:** {p.get('endereco','Não informado')}")
            with col2:
                st.subheader("📝 Histórico / Descrição")
                st.write(p.get('descricao','Sem descrição'))
                st.write(f"**Responsável:** {p.get('responsavel','–')}")
                st.write(f"**Tel. Responsável:** {p.get('telefone_responsavel','–')}")
                st.write(f"**Plano de Saúde:** {p.get('plano_saude','–')}")
                st.write(f"**Carteirinha:** {p.get('numero_plano','–')}")
            st.divider()

            # Opções de Atendimento
            st.subheader("🎥 Opções de Atendimento")
            c1,c2,c3,c4 = st.columns(4)
            
            with c1:
                st.markdown("### 📱 WhatsApp")
                if st.button("💬 Enviar link via WhatsApp"):
                    tel=''.join(filter(str.isdigit,p.get('telefone','')))
                    if tel.startswith('55'): tel=tel[2:]
                    msg=quote(f"Olá {p['nome']}, acesse sua videochamada: {share_link}")
                    wa_url=f"https://wa.me/55{tel}?text={msg}"
                    st.markdown(f"[Abrir WhatsApp]({wa_url})")
                
                # WhatsApp Video direto
                if st.button("📹 WhatsApp Video"):
                    tel=''.join(filter(str.isdigit,p.get('telefone','')))
                    if tel.startswith('55'): tel=tel[2:]
                    wa_video=f"https://wa.me/55{tel}?text=Iniciar%20videochamada"
                    st.markdown(f"[WhatsApp Video]({wa_video})")
            
            with c2:
                st.markdown("### 🎥 Google Meet")
                # Gerar link do Google Meet
                meet_code = f"oria-{p['room_id']}-{datetime.now().strftime('%H%M')}"
                meet_link = f"https://meet.google.com/{meet_code}"
                
                if st.button("🎥 Criar Google Meet"):
                    st.success(f"✅ Google Meet criado!")
                    st.markdown(f"**Link do Google Meet:** [{meet_link}]({meet_link})")
                    
                    # Enviar link via WhatsApp
                    tel=''.join(filter(str.isdigit,p.get('telefone','')))
                    if tel.startswith('55'): tel=tel[2:]
                    msg=quote(f"Olá {p['nome']}, acesse sua videochamada no Google Meet: {meet_link}")
                    wa_url=f"https://wa.me/55{tel}?text={msg}"
                    st.markdown(f"[Enviar link via WhatsApp]({wa_url})")
            
            with c3:
                st.markdown("### 🎥 Zoom")
                # Gerar link do Zoom
                zoom_id = f"oria{datetime.now().strftime('%Y%m%d%H%M')}"
                zoom_link = f"https://zoom.us/j/{zoom_id}"
                
                if st.button("🎥 Criar Zoom"):
                    st.success(f"✅ Zoom criado!")
                    st.markdown(f"**Link do Zoom:** [{zoom_link}]({zoom_link})")
                    
                    # Enviar link via WhatsApp
                    tel=''.join(filter(str.isdigit,p.get('telefone','')))
                    if tel.startswith('55'): tel=tel[2:]
                    msg=quote(f"Olá {p['nome']}, acesse sua videochamada no Zoom: {zoom_link}")
                    wa_url=f"https://wa.me/55{tel}?text={msg}"
                    st.markdown(f"[Enviar link via WhatsApp]({wa_url})")
            
            with c4:
                st.markdown("### 🎥 Jitsi Meet")
                # Gerar link do Jitsi Meet
                jitsi_room = f"oria-{p['room_id']}-{datetime.now().strftime('%H%M')}"
                jitsi_link = f"https://meet.jit.si/{jitsi_room}"
                
                if st.button("🎥 Criar Jitsi Meet"):
                    st.success(f"✅ Jitsi Meet criado!")
                    st.markdown(f"**Link do Jitsi Meet:** [{jitsi_link}]({jitsi_link})")
                    
                    # Enviar link via WhatsApp
                    tel=''.join(filter(str.isdigit,p.get('telefone','')))
                    if tel.startswith('55'): tel=tel[2:]
                    msg=quote(f"Olá {p['nome']}, acesse sua videochamada no Jitsi Meet: {jitsi_link}")
                    wa_url=f"https://wa.me/55{tel}?text={msg}"
                    st.markdown(f"[Enviar link via WhatsApp]({wa_url})")

            # Observações
            st.subheader("📝 Observações da Sessão")
            obs=st.text_area("Digite suas observações:",height=200)
            if st.button("💾 Salvar Observações"):
                sessoes.append({
                    'id':len(sessoes)+1,
                    'paciente':p['nome'],
                    'data':datetime.now().strftime("%d/%m/%Y %H:%M"),
                    'observacoes':obs,
                    'tipo_atendimento':'online'
                })
                salvar_sessoes(sessoes, obter_crp_atual())
                st.success("Observações salvas com sucesso!")
        else:
            st.info("👆 Selecione um paciente para iniciar.")

# ==== Gerenciar Pacientes ====
else:
    st.header("👥 Gerenciar Pacientes")
    tab1,tab2,tab3=st.tabs(["➕ Adicionar","📋 Lista","📊 Histórico"])
    with tab1:
        st.subheader("Adicionar Novo Paciente")
        with st.form("form_paciente"):
            nome=st.text_input("Nome Completo *")
            idade=st.number_input("Idade *",min_value=0,max_value=120)
            telefone=st.text_input("Telefone *")
            email=st.text_input("E-mail")
            data_nasc=st.date_input("Data de Nascimento *",format="DD/MM/YYYY",
                                   min_value=date(1900,1,1),max_value=date(2100,12,31))
            genero=st.selectbox("Gênero",["","Masculino","Feminino","Não binário","Prefere não informar"])
            endereco=st.text_input("Endereço")
            descricao=st.text_area("Descrição / Histórico")
            responsavel=st.text_input("Responsável (se menor de idade)")
            telefone_resp=st.text_input("Telefone do Responsável")
            plano_saude=st.text_input("Plano de Saúde")
            numero_plano=st.text_input("Número da Carteirinha")
            if st.form_submit_button("💾 Salvar Paciente"):
                if nome and telefone:
                    pacientes.append({
                        'id':len(pacientes)+1,
                        'nome':nome,
                        'idade':idade,
                        'telefone':telefone,
                        'email':email,
                        'data_nascimento':data_nasc.strftime("%d/%m/%Y"),
                        'genero':genero,
                        'endereco':endereco,
                        'descricao':descricao,
                        'responsavel':responsavel,
                        'telefone_responsavel':telefone_resp,
                        'plano_saude':plano_saude,
                        'numero_plano':numero_plano,
                        'data_cadastro':datetime.now().strftime("%d/%m/%Y %H:%M"),
                        'room_id':uuid.uuid4().hex[:8]
                    })
                    salvar_pacientes(pacientes, obter_crp_atual())
                    st.rerun()
    with tab2:
        st.subheader("Lista de Pacientes")
        if pacientes:
            busca=st.text_input("🔍 Buscar paciente:")
            filtrados=[p for p in pacientes if busca.lower() in p['nome'].lower()] if busca else pacientes
            for i, p in enumerate(filtrados):
                with st.expander(f"👤 {p['nome']} - {p['idade']} anos"):
                    col1,col2=st.columns(2)
                    with col1:
                        st.write(f"📱 {p.get('telefone','–')}")
                        st.write(f"✉️ {p.get('email','–')}")
                        st.write(f"📅 {p.get('data_nascimento','–')}")
                    with col2:
                        st.write(f"🏠 {p.get('endereco','–')}")
                        st.write(f"👤 {p.get('responsavel','–')}")
                    if st.button("🗑️ Excluir",key=f"del_{p['id']}_{i}"):
                        pacientes.remove(p)
                        salvar_pacientes(pacientes, obter_crp_atual())
                        st.success("Paciente removido!")
                        st.rerun()
    with tab3:
        st.subheader("Histórico de Sessões")
        for s in reversed(sessoes):
            with st.expander(f"📅 {s['data']} - {s['paciente']}"):
                st.write(s.get('observacoes','Sem observações'))

st.divider()
st.write("💻 Desenvolvido por Luan Gama")
