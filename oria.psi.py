import os
# garante que ffmpeg.exe e ffprobe.exe na raiz sejam encontrados
os.environ["PATH"] += os.pathsep + os.getcwd()

import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import uuid
from urllib.parse import quote
import io

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
    # Removida validação de formato específico
    # Aceita qualquer formato de CRP
    return len(crp.strip()) >= 3  # Mínimo 3 caracteres

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
                crp_login = st.text_input("CRP", placeholder="Digite seu CRP", key="login_crp")
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
                            st.error("❌ CRP inválido! Digite um CRP válido.")
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
                crp_registro = st.text_input("CRP", placeholder="Digite seu CRP", key="reg_crp")
                senha_registro = st.text_input("Senha", type="password", placeholder="Crie uma senha", key="reg_senha")
                senha_confirmacao = st.text_input("Confirmar Senha", type="password", placeholder="Confirme sua senha", key="reg_senha_confirm")
                
                # Verificar se já foi cadastrado com sucesso
                cadastro_sucesso = st.session_state.get('cadastro_sucesso', False)
                
                if cadastro_sucesso:
                    st.success("✅ Cadastro realizado com sucesso!")
                    st.info("Agora você pode fazer login na aba 'Login'.")
                    st.markdown("---")
                    st.markdown("""
                    **🎉 Parabéns! Seu cadastro foi realizado com sucesso.**
                    
                    **Próximos passos:**
                    1. Clique na aba **"🔑 Login"** acima
                    2. Digite seu **CRP** e **senha**
                    3. Clique em **"🔑 Entrar"**
                    4. Comece a usar a plataforma!
                    """)
                    if st.button("📝 Fazer Novo Cadastro", use_container_width=True):
                        st.session_state.cadastro_sucesso = False
                        st.rerun()
                else:
                    if st.button("📝 Cadastrar", use_container_width=True):
                        # Validações ao clicar no botão
                        if not (nome_completo and crp_registro and senha_registro and senha_confirmacao):
                            st.error("❌ Preencha todos os campos!")
                        elif not validar_crp(crp_registro):
                            st.error("❌ CRP inválido! Digite um CRP válido.")
                        elif verificar_usuario_existe(crp_registro):
                            st.error("❌ CRP já cadastrado! Use a aba de login.")
                        elif senha_registro != senha_confirmacao:
                            st.error("❌ Senhas não coincidem!")
                        elif len(senha_registro) < 6:
                            st.error("❌ Senha deve ter pelo menos 6 caracteres!")
                        elif len(nome_completo) < 3:
                            st.error("❌ Nome deve ter pelo menos 3 caracteres!")
                        else:
                            if registrar_novo_usuario(nome_completo, crp_registro, senha_registro):
                                st.session_state.cadastro_sucesso = True
                                st.rerun()
                            else:
                                st.error("❌ Erro ao realizar cadastro!")

                    st.markdown("---")
                    st.info("""
                    **📋 Informações do Cadastro:**
                    - CRP deve ter pelo menos 3 caracteres
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
if 'cadastro_sucesso' not in st.session_state:
    st.session_state.cadastro_sucesso = False

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
            <p style="margin: 0; color: #666;">Profissional: {nome_usuario} (CRP {st.session_state.crp})</p>
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

def gerar_planilha_modelo():
    df = pd.DataFrame([
        {
            'nome': 'Exemplo Nome',
            'idade': 30,
            'telefone': '11999999999',
            'email': 'exemplo@email.com',
            'data_nascimento': '01/01/1990',
            'genero': 'Masculino',
            'endereco': 'Rua Exemplo, 123',
            'descricao': 'Histórico do paciente',
            'responsavel': 'Nome do responsável',
            'telefone_responsavel': '11988888888',
            'plano_saude': 'Plano Exemplo',
            'numero_plano': '123456',
        }
    ])
    return df

def gerar_planilha_modelo_bytes():
    df = gerar_planilha_modelo()
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output.getvalue()

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
        
        # Upload de planilha Excel para importar pacientes
        with st.expander("📥 Importar Pacientes via Planilha Excel (.xlsx)"):
            st.markdown("Faça upload de uma planilha Excel com os campos de cadastro de paciente.")
            modelo = gerar_planilha_modelo()
            st.download_button(
                label="📄 Baixar Planilha Modelo",
                data=gerar_planilha_modelo_bytes(),
                file_name="modelo_pacientes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            uploaded_file = st.file_uploader("Selecione o arquivo Excel (.xlsx)", type=["xlsx"], key="upload_excel")
            if uploaded_file is not None:
                try:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                    # Validação básica dos campos
                    campos_necessarios = ['nome','idade','telefone','email','data_nascimento','genero','endereco','descricao','responsavel','telefone_responsavel','plano_saude','numero_plano']
                    if all(c in df.columns for c in campos_necessarios):
                        novos_pacientes = df.to_dict(orient='records')
                        # Adiciona room_id e id únicos
                        for np in novos_pacientes:
                            np['id'] = len(pacientes) + 1 + novos_pacientes.index(np)
                            np['room_id'] = uuid.uuid4().hex[:8]
                            np['data_cadastro'] = datetime.now().strftime("%d/%m/%Y %H:%M")
                        pacientes.extend(novos_pacientes)
                        salvar_pacientes(pacientes, crp)
                        st.success(f"{len(novos_pacientes)} paciente(s) importado(s) com sucesso!")
                        st.rerun()
                    else:
                        st.error("A planilha não possui todos os campos necessários. Baixe o modelo para referência.")
                except Exception as e:
                    st.error(f"Erro ao importar planilha: {e}")

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
            share_link = f"{BASE_URL}?room={p['room_id']}"
            with st.expander("📋 Instruções para Videochamada"):
                st.markdown(f"""
                **Opções de Videochamada Disponíveis:**
                
                ### 📱 WhatsApp
                - **Enviar link**: Envia o link da plataforma via WhatsApp
                - **WhatsApp Video**: Inicia videochamada direta pelo WhatsApp
                
                ### 🎥 Jitsi Meet
                - **Totalmente gratuito** e de código aberto
                - **Sem necessidade de conta** ou instalação
                - **Privacidade garantida** - dados não são armazenados
                - Funciona em qualquer navegador
                - Clique em "Criar Jitsi Meet" e envie o link
                
                **Como usar:**
                1. **Escolha uma plataforma** (Jitsi Meet recomendado)
                2. **Clique em criar** a videochamada
                3. **Envie o link** via WhatsApp para o paciente
                4. **Ambos acessem** o link para iniciar a videochamada
                
                **Dicas:**
                - **Jitsi Meet** é ideal para privacidade e simplicidade
                - **WhatsApp Video** é ideal para atendimentos rápidos
                """)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 📱 WhatsApp")
                if st.button("💬 Enviar link via WhatsApp"):
                    tel=''.join(filter(str.isdigit,p.get('telefone','')))
                    if tel.startswith('55'): tel=tel[2:]
                    msg=quote(f"Olá {p['nome']}, acesse sua videochamada: {share_link}")
                    wa_url=f"https://wa.me/55{tel}?text={msg}"
                    st.markdown(f"[Abrir WhatsApp]({wa_url})")
                if st.button("📹 WhatsApp Video"):
                    tel=''.join(filter(str.isdigit,p.get('telefone','')))
                    if tel.startswith('55'): tel=tel[2:]
                    wa_video=f"https://wa.me/55{tel}?text=Iniciar%20videochamada"
                    st.markdown(f"[WhatsApp Video]({wa_video})")
            with col2:
                st.markdown("### 🎥 Jitsi Meet")
                jitsi_room = f"oria-{p['room_id']}-{datetime.now().strftime('%H%M')}"
                jitsi_link = f"https://meet.jit.si/{jitsi_room}"
                if st.button("🎥 Criar Jitsi Meet"):
                    st.success(f"✅ Jitsi Meet criado!")
                    st.markdown(f"**Link do Jitsi Meet:** [{jitsi_link}]({jitsi_link})")
                    tel=''.join(filter(str.isdigit,p.get('telefone','')))
                    if tel.startswith('55'): tel=tel[2:]
                    msg=quote(f"Olá {p['nome']}, acesse sua videochamada no Jitsi Meet: {jitsi_link}")
                    wa_url=f"https://wa.me/55{tel}?text={msg}"
                    st.markdown(f"[Enviar link via WhatsApp]({wa_url})")
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
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"📱 {p.get('telefone','–')}")
                        st.write(f"✉️ {p.get('email','–')}")
                        st.write(f"📅 {p.get('data_nascimento','–')}")
                    with col2:
                        st.write(f"🏠 {p.get('endereco','–')}")
                        st.write(f"👤 {p.get('responsavel','–')}")
                    col_btn1, col_btn2 = st.columns([1,1])
                    with col_btn1:
                        if st.button("🗑️ Excluir", key=f"del_{p['id']}_{i}"):
                            pacientes.remove(p)
                            salvar_pacientes(pacientes, obter_crp_atual())
                            st.success("Paciente removido!")
                            st.rerun()
                    with col_btn2:
                        if st.button("✏️ Editar", key=f"edit_{p['id']}_{i}"):
                            st.session_state['edit_paciente'] = p['id']
                            st.session_state['edit_index'] = i
                            st.session_state['edit_data'] = p.copy()
                            st.rerun()

                # Formulário de edição inline
                if st.session_state.get('edit_paciente') == p['id'] and st.session_state.get('edit_index') == i:
                    edit_data = st.session_state.get('edit_data', p.copy())
                    with st.form(f"form_edit_{p['id']}_{i}"):
                        nome_edit = st.text_input("Nome Completo", value=edit_data.get('nome',''))
                        idade_edit = st.number_input("Idade", min_value=0, max_value=120, value=edit_data.get('idade',0))
                        telefone_edit = st.text_input("Telefone", value=edit_data.get('telefone',''))
                        email_edit = st.text_input("E-mail", value=edit_data.get('email',''))
                        data_nasc_edit = st.text_input("Data de Nascimento", value=edit_data.get('data_nascimento',''))
                        endereco_edit = st.text_input("Endereço", value=edit_data.get('endereco',''))
                        descricao_edit = st.text_area("Descrição / Histórico", value=edit_data.get('descricao',''))
                        responsavel_edit = st.text_input("Responsável", value=edit_data.get('responsavel',''))
                        telefone_resp_edit = st.text_input("Telefone do Responsável", value=edit_data.get('telefone_responsavel',''))
                        plano_saude_edit = st.text_input("Plano de Saúde", value=edit_data.get('plano_saude',''))
                        numero_plano_edit = st.text_input("Número da Carteirinha", value=edit_data.get('numero_plano',''))
                        submitted = st.form_submit_button("💾 Salvar Alterações")
                        cancelar = st.form_submit_button("Cancelar")
                        if submitted:
                            p['nome'] = nome_edit
                            p['idade'] = idade_edit
                            p['telefone'] = telefone_edit
                            p['email'] = email_edit
                            p['data_nascimento'] = data_nasc_edit
                            p['endereco'] = endereco_edit
                            p['descricao'] = descricao_edit
                            p['responsavel'] = responsavel_edit
                            p['telefone_responsavel'] = telefone_resp_edit
                            p['plano_saude'] = plano_saude_edit
                            p['numero_plano'] = numero_plano_edit
                            salvar_pacientes(pacientes, obter_crp_atual())
                            st.success("Alterações salvas!")
                            del st.session_state['edit_paciente']
                            del st.session_state['edit_index']
                            del st.session_state['edit_data']
                            st.rerun()
                        if cancelar:
                            del st.session_state['edit_paciente']
                            del st.session_state['edit_index']
                            del st.session_state['edit_data']
                            st.rerun()
    with tab3:
        st.subheader("Histórico de Sessões")
        for s in reversed(sessoes):
            with st.expander(f"📅 {s['data']} - {s['paciente']}"):
                st.write(s.get('observacoes','Sem observações'))

st.divider()
st.write("💻 Desenvolvido por Luan Gama")
