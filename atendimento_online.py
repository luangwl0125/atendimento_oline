import os
# garante que ffmpeg.exe e ffprobe.exe na raiz sejam encontrados
os.environ["PATH"] += os.pathsep + os.getcwd()

from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import streamlit as st
import pandas as pd
from datetime import datetime, date
import json

# Configuração da página
st.set_page_config(
    page_title="OriaPsi",
    page_icon="🧠",
    layout="wide"
)

# Função para carregar dados dos pacientes
def carregar_pacientes():
    try:
        if os.path.exists('pacientes.json'):
            with open('pacientes.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return dados
        return []
    except Exception as e:
        st.error(f"Erro ao carregar pacientes: {e}")
        return []

# Função para salvar dados dos pacientes
def salvar_pacientes(pacientes):
    try:
        with open('pacientes.json', 'w', encoding='utf-8') as f:
            json.dump(pacientes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar pacientes: {e}")

# Função para carregar sessões
def carregar_sessoes():
    try:
        if os.path.exists('sessoes.json'):
            with open('sessoes.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Erro ao carregar sessões: {e}")
        return []

# Função para salvar sessões
def salvar_sessoes(sessoes):
    try:
        with open('sessoes.json', 'w', encoding='utf-8') as f:
            json.dump(sessoes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar sessões: {e}")

# Função para converter data de formato brasileiro para objeto date
def converter_data_br_para_date(data_br):
    """Converte data no formato DD/MM/YYYY para objeto date"""
    if not data_br or data_br == "":
        return None
    try:
        return datetime.strptime(data_br, '%d/%m/%Y').date()
    except ValueError:
        return None

# Função para converter objeto date para formato brasileiro
def converter_date_para_br(data_obj):
    """Converte objeto date para formato DD/MM/YYYY"""
    if not data_obj:
        return ""
    try:
        return data_obj.strftime('%d/%m/%Y')
    except:
        return ""

# Título da Plataforma
st.title("🧠 Plataforma de Psicologia")

# Menu de Navegação
page = st.sidebar.selectbox(
    "Escolha uma opção:", 
    ["Atendimento On-line", "Gerenciador de Pacientes"]
)

# Botão para recarregar dados
if st.sidebar.button("🔄 Recarregar Dados"):
    st.rerun()

# Carregar dados
pacientes = carregar_pacientes()
sessoes = carregar_sessoes()

# Página de Atendimento On-line
if page == "Atendimento On-line":
    st.header("📞 Atendimento On-line")
    
    # Carregar dados novamente para garantir que estão atualizados
    pacientes = carregar_pacientes()
    
    # Seleção do paciente
    if pacientes:
        nomes_pacientes = [p['nome'] for p in pacientes]
        st.success(f"✅ {len(pacientes)} paciente(s) cadastrado(s)")
        
        paciente_selecionado = st.selectbox(
            "Selecione o paciente:",
            ["Selecione um paciente..."] + nomes_pacientes
        )
        
        if paciente_selecionado != "Selecione um paciente...":
            paciente = next(p for p in pacientes if p['nome'] == paciente_selecionado)
            
            # Informações do paciente
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📋 Informações do Paciente")
                st.write(f"**Nome:** {paciente['nome']}")
                st.write(f"**Idade:** {paciente['idade']} anos")
                st.write(f"**Data de Nascimento:** {paciente.get('data_nascimento', 'Não informado')}")
                st.write(f"**Telefone:** {paciente.get('telefone', 'Não informado')}")
            
            with col2:
                st.subheader("📝 Descrição")
                st.write(paciente.get('descricao', 'Sem descrição'))
            
            st.divider()
            
            # Opções de atendimento
            st.subheader("🎥 Opções de Atendimento")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📱 WhatsApp")
                if st.button("💬 Abrir WhatsApp", key="whatsapp"):
                    telefone = paciente.get('telefone', '')
                    if telefone:
                        # Remove caracteres especiais do telefone
                        telefone_limpo = ''.join(filter(str.isdigit, telefone))
                        if telefone_limpo.startswith('55'):
                            telefone_limpo = telefone_limpo[2:]
                        if not telefone_limpo.startswith('0'):
                            telefone_limpo = '0' + telefone_limpo
                        
                        url_whatsapp = f"https://wa.me/55{telefone_limpo}"
                        st.markdown(f"[Clique aqui para abrir WhatsApp]({url_whatsapp})")
                        st.success("WhatsApp aberto! Inicie a videochamada.")
                    else:
                        st.error("Telefone não cadastrado para este paciente.")
            
            with col2:
                st.markdown("### 🎥 Videochamada (WebRTC)")
                # configuração de ICE/STUN
                rtc_config = RTCConfiguration({
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                })
                # inicializa o componente WebRTC
                webrtc_streamer(
                    key="video_call",
                    rtc_configuration=rtc_config,
                    media_stream_constraints={"video": True, "audio": True}
                )
            
            st.divider()
            
            # Área de observações
            st.subheader("📝 Área de Trabalho")
            
            observacoes = st.text_area(
                "Observações da Sessão:",
                height=200,
                placeholder="Digite suas observações durante a sessão..."
            )
            
            if st.button("💾 Salvar Observações"):
                nova_sessao = {
                    'id': len(sessoes) + 1,
                    'paciente': paciente['nome'],
                    'data': datetime.now().strftime("%d/%m/%Y %H:%M"),
                    'observacoes': observacoes,
                    'tipo_atendimento': 'online'
                }
                sessoes.append(nova_sessao)
                salvar_sessoes(sessoes)
                st.success("Observações salvas com sucesso!")
        
        else:
            st.info("👆 Selecione um paciente para iniciar o atendimento.")
    
    else:
        st.warning("⚠️ Nenhum paciente cadastrado. Adicione pacientes no Gerenciador de Pacientes primeiro.")
        st.info("💡 Dica: Vá para 'Gerenciador de Pacientes' e adicione um novo paciente.")

# Página de Gerenciador de Pacientes
elif page == "Gerenciador de Pacientes":
    st.header("👥 Gerenciador de Pacientes")
    
    # Abas para diferentes funcionalidades
    tab1, tab2, tab3 = st.tabs(["➕ Adicionar Paciente", "📋 Lista de Pacientes", "📊 Histórico de Sessões"])
    
    with tab1:
        st.subheader("Adicionar Novo Paciente")
        
        with st.form("form_paciente"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo *", placeholder="Digite o nome completo")
                idade = st.number_input("Idade *", min_value=0, max_value=120)
                telefone = st.text_input("Telefone *", placeholder="(11) 99999-9999")
                email = st.text_input("E-mail", placeholder="paciente@email.com")
            
            with col2:
                # Data de nascimento com formato brasileiro e limites de ano
                data_nascimento = st.date_input(
                    "Data de Nascimento",
                    format="DD/MM/YYYY",
                    min_value=date(1900, 1, 1),
                    max_value=date(2100, 12, 31),
                    help="Selecione a data de nascimento do paciente. Para ver os meses em português, configure o idioma do navegador para pt-BR."
                )
                genero = st.selectbox("Gênero", ["", "Masculino", "Feminino", "Não binário", "Prefere não informar"])
                endereco = st.text_input("Endereço", placeholder="Rua, número, bairro, cidade")
            
            descricao = st.text_area(
                "Descrição/Histórico do Paciente",
                placeholder="Descreva o histórico, queixas principais, objetivos da terapia..."
            )
            
            # Informações adicionais
            col1, col2 = st.columns(2)
            with col1:
                responsavel = st.text_input("Responsável (se menor de idade)", placeholder="Nome do responsável")
                telefone_responsavel = st.text_input("Telefone do Responsável", placeholder="(11) 99999-9999")
            
            with col2:
                plano_saude = st.text_input("Plano de Saúde", placeholder="Nome do plano")
                numero_plano = st.text_input("Número do Plano", placeholder="Número da carteirinha")
            
            submitted = st.form_submit_button("💾 Salvar Paciente")
            
            if submitted:
                if nome and telefone:
                    # Converter data para formato brasileiro
                    data_nascimento_br = ""
                    if data_nascimento:
                        data_nascimento_br = data_nascimento.strftime("%d/%m/%Y")
                    
                    novo_paciente = {
                        'id': len(pacientes) + 1,
                        'nome': nome,
                        'idade': idade,
                        'telefone': telefone,
                        'email': email,
                        'data_nascimento': data_nascimento_br,
                        'genero': genero,
                        'endereco': endereco,
                        'descricao': descricao,
                        'responsavel': responsavel,
                        'telefone_responsavel': telefone_responsavel,
                        'plano_saude': plano_saude,
                        'numero_plano': numero_plano,
                        'data_cadastro': datetime.now().strftime("%d/%m/%Y %H:%M")
                    }
                    
                    pacientes.append(novo_paciente)
                    salvar_pacientes(pacientes)
                    st.success(f"✅ Paciente {nome} cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Nome e telefone são obrigatórios!")
    
    with tab2:
        st.subheader("Lista de Pacientes")
        
        if pacientes:
            # Filtro de busca
            busca = st.text_input("🔍 Buscar paciente:", placeholder="Digite o nome do paciente")
            
            if busca:
                pacientes_filtrados = [p for p in pacientes if busca.lower() in p['nome'].lower()]
            else:
                pacientes_filtrados = pacientes
            
            if pacientes_filtrados:
                for paciente in pacientes_filtrados:
                    with st.expander(f"👤 {paciente['nome']} - {paciente['idade']} anos"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Telefone:** {paciente.get('telefone', 'Não informado')}")
                            st.write(f"**E-mail:** {paciente.get('email', 'Não informado')}")
                            st.write(f"**Data de Nascimento:** {paciente.get('data_nascimento', 'Não informado')}")
                            st.write(f"**Gênero:** {paciente.get('genero', 'Não informado')}")
                            st.write(f"**Data de Cadastro:** {paciente.get('data_cadastro', 'Não informado')}")
                            if paciente.get('data_atualizacao'):
                                st.write(f"**Última Atualização:** {paciente.get('data_atualizacao', 'Não informado')}")
                        
                        with col2:
                            st.write(f"**Endereço:** {paciente.get('endereco', 'Não informado')}")
                            st.write(f"**Responsável:** {paciente.get('responsavel', 'Não informado')}")
                            st.write(f"**Plano de Saúde:** {paciente.get('plano_saude', 'Não informado')}")
                        
                        st.write(f"**Descrição:** {paciente.get('descricao', 'Sem descrição')}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"✏️ Editar", key=f"edit_{paciente['id']}"):
                                st.session_state.editando_paciente = paciente['id']
                                st.rerun()
                        
                        with col2:
                            if st.button(f"🗑️ Excluir", key=f"del_{paciente['id']}"):
                                pacientes.remove(paciente)
                                salvar_pacientes(pacientes)
                                st.success("Paciente removido com sucesso!")
                                st.rerun()
                        
                        with col3:
                            if st.button(f"📞 Atender", key=f"atend_{paciente['id']}"):
                                st.session_state.paciente_selecionado = paciente['nome']
                                st.rerun()
                
                # Seção de edição de paciente
                if 'editando_paciente' in st.session_state:
                    paciente_editando = next((p for p in pacientes if p['id'] == st.session_state.editando_paciente), None)
                    
                    if paciente_editando:
                        st.divider()
                        st.subheader(f"✏️ Editando Paciente: {paciente_editando['nome']}")
                        
                        # Converter data de nascimento para objeto date se existir
                        data_nascimento_atual = converter_data_br_para_date(paciente_editando.get('data_nascimento', ''))
                        
                        with st.form(f"form_editar_paciente_{paciente_editando['id']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                nome_edit = st.text_input(
                                    "Nome Completo *", 
                                    value=paciente_editando.get('nome', ''),
                                    key=f"nome_edit_{paciente_editando['id']}"
                                )
                                idade_edit = st.number_input(
                                    "Idade *", 
                                    min_value=0, 
                                    max_value=120,
                                    value=paciente_editando.get('idade', 0),
                                    key=f"idade_edit_{paciente_editando['id']}"
                                )
                                telefone_edit = st.text_input(
                                    "Telefone *", 
                                    value=paciente_editando.get('telefone', ''),
                                    key=f"telefone_edit_{paciente_editando['id']}"
                                )
                                email_edit = st.text_input(
                                    "E-mail", 
                                    value=paciente_editando.get('email', ''),
                                    key=f"email_edit_{paciente_editando['id']}"
                                )
                            
                            with col2:
                                data_nascimento_edit = st.date_input(
                                    "Data de Nascimento",
                                    value=data_nascimento_atual,
                                    format="DD/MM/YYYY",
                                    min_value=date(1900, 1, 1),
                                    max_value=date(2100, 12, 31),
                                    help="Selecione a data de nascimento do paciente. Para ver os meses em português, configure o idioma do navegador para pt-BR.",
                                    key=f"data_edit_{paciente_editando['id']}"
                                )
                                genero_edit = st.selectbox(
                                    "Gênero", 
                                    ["", "Masculino", "Feminino", "Não binário", "Prefere não informar"],
                                    index=["", "Masculino", "Feminino", "Não binário", "Prefere não informar"].index(paciente_editando.get('genero', '')),
                                    key=f"genero_edit_{paciente_editando['id']}"
                                )
                                endereco_edit = st.text_input(
                                    "Endereço", 
                                    value=paciente_editando.get('endereco', ''),
                                    key=f"endereco_edit_{paciente_editando['id']}"
                                )
                            
                            descricao_edit = st.text_area(
                                "Descrição/Histórico do Paciente",
                                value=paciente_editando.get('descricao', ''),
                                key=f"descricao_edit_{paciente_editando['id']}"
                            )
                            
                            # Informações adicionais
                            col1, col2 = st.columns(2)
                            with col1:
                                responsavel_edit = st.text_input(
                                    "Responsável (se menor de idade)", 
                                    value=paciente_editando.get('responsavel', ''),
                                    key=f"responsavel_edit_{paciente_editando['id']}"
                                )
                                telefone_responsavel_edit = st.text_input(
                                    "Telefone do Responsável", 
                                    value=paciente_editando.get('telefone_responsavel', ''),
                                    key=f"telefone_responsavel_edit_{paciente_editando['id']}"
                                )
                            
                            with col2:
                                plano_saude_edit = st.text_input(
                                    "Plano de Saúde", 
                                    value=paciente_editando.get('plano_saude', ''),
                                    key=f"plano_saude_edit_{paciente_editando['id']}"
                                )
                                numero_plano_edit = st.text_input(
                                    "Número do Plano", 
                                    value=paciente_editando.get('numero_plano', ''),
                                    key=f"numero_plano_edit_{paciente_editando['id']}"
                                )
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.form_submit_button("💾 Salvar Alterações"):
                                    if nome_edit and telefone_edit:
                                        # Converter data para formato brasileiro
                                        data_nascimento_br = converter_date_para_br(data_nascimento_edit)
                                        
                                        # Atualizar dados do paciente
                                        paciente_editando.update({
                                            'nome': nome_edit,
                                            'idade': idade_edit,
                                            'telefone': telefone_edit,
                                            'email': email_edit,
                                            'data_nascimento': data_nascimento_br,
                                            'genero': genero_edit,
                                            'endereco': endereco_edit,
                                            'descricao': descricao_edit,
                                            'responsavel': responsavel_edit,
                                            'telefone_responsavel': telefone_responsavel_edit,
                                            'plano_saude': plano_saude_edit,
                                            'numero_plano': numero_plano_edit,
                                            'data_atualizacao': datetime.now().strftime("%d/%m/%Y %H:%M")
                                        })
                                        
                                        salvar_pacientes(pacientes)
                                        st.success(f"✅ Paciente {nome_edit} atualizado com sucesso!")
                                        del st.session_state.editando_paciente
                                        st.rerun()
                                    else:
                                        st.error("❌ Nome e telefone são obrigatórios!")
                            
                            with col2:
                                if st.form_submit_button("❌ Cancelar"):
                                    del st.session_state.editando_paciente
                                    st.rerun()
                            
                            with col3:
                                if st.form_submit_button("🔄 Reverter Alterações"):
                                    st.rerun()
            else:
                st.info("Nenhum paciente encontrado com essa busca.")
        else:
            st.info("📝 Nenhum paciente cadastrado ainda.")
    
    with tab3:
        st.subheader("Histórico de Sessões")
        
        if sessoes:
            for sessao in reversed(sessoes):
                with st.expander(f"📅 {sessao['data']} - {sessao['paciente']}"):
                    st.write(f"**Paciente:** {sessao['paciente']}")
                    st.write(f"**Data:** {sessao['data']}")
                    st.write(f"**Tipo:** {sessao['tipo_atendimento']}")
                    st.write(f"**Observações:** {sessao.get('observacoes', 'Sem observações')}")
                    
                    if st.button(f"🗑️ Excluir Sessão", key=f"del_sessao_{sessao['id']}"):
                        sessoes.remove(sessao)
                        salvar_sessoes(sessoes)
                        st.success("Sessão removida com sucesso!")
                        st.rerun()
        else:
            st.info("📝 Nenhuma sessão registrada ainda.")

# Rodapé
st.divider()
st.write("💻 Desenvolvido por Luan Gama")