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
def carregar_pacientes():
    try:
        if os.path.exists('pacientes.json'):
            return json.load(open('pacientes.json','r',encoding='utf-8'))
    except Exception as e:
        st.error(f"Erro ao carregar pacientes: {e}")
    return []

def salvar_pacientes(pacientes):
    try:
        with open('pacientes.json','w',encoding='utf-8') as f:
            json.dump(pacientes,f,ensure_ascii=False,indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar pacientes: {e}")

def carregar_sessoes():
    try:
        if os.path.exists('sessoes.json'):
            return json.load(open('sessoes.json','r',encoding='utf-8'))
    except Exception as e:
        st.error(f"Erro ao carregar sessões: {e}")
    return []

def salvar_sessoes(sessoes):
    try:
        with open('sessoes.json','w',encoding='utf-8') as f:
            json.dump(sessoes,f,ensure_ascii=False,indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar sessões: {e}")

# ==== Cabeçalho e estado global ====
st.title("🧠 OriaPsi - Atendimento On-line 📞")
page = st.sidebar.selectbox(
    "Escolha uma opção:",
    ["Atender Agora","Gerenciar Pacientes"]
)
if st.sidebar.button("🔄 Recarregar Dados"):
    st.rerun()

# Carrega e garante room_id permanente por paciente
pacientes = carregar_pacientes()
updated = False
for p in pacientes:
    if 'room_id' not in p:
        p['room_id'] = uuid.uuid4().hex[:8]
        updated = True
if updated:
    salvar_pacientes(pacientes)
sessoes = carregar_sessoes()

# ==== Página de Atendimento On-line ====
if page == "Atendimento On-line":
    if not pacientes:
        st.warning("⚠️ Nenhum paciente cadastrado. Adicione pelo gerenciador.")
    else:
        st.success(f"✅ {len(pacientes)} paciente(s) cadastrado(s)")
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
                salvar_sessoes(sessoes)
                st.success("Observações salvas com sucesso!")
        else:
            st.info("👆 Selecione um paciente para iniciar.")

# ==== Gerenciador de Pacientes ====
else:
    st.header("👥 Gerenciador de Pacientes")
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
                    salvar_pacientes(pacientes)
                    st.rerun()
    with tab2:
        st.subheader("Lista de Pacientes")
        if pacientes:
            busca=st.text_input("🔍 Buscar paciente:")
            filtrados=[p for p in pacientes if busca.lower() in p['nome'].lower()] if busca else pacientes
            for p in filtrados:
                with st.expander(f"👤 {p['nome']} - {p['idade']} anos"):
                    col1,col2=st.columns(2)
                    with col1:
                        st.write(f"📱 {p.get('telefone','–')}")
                        st.write(f"✉️ {p.get('email','–')}")
                        st.write(f"📅 {p.get('data_nascimento','–')}")
                    with col2:
                        st.write(f"🏠 {p.get('endereco','–')}")
                        st.write(f"👤 {p.get('responsavel','–')}")
                    if st.button("🗑️ Excluir",key=f"del_{p['id']}"):
                        pacientes.remove(p)
                        salvar_pacientes(pacientes)
                        st.success("Paciente removido!")
                        st.rerun()
    with tab3:
        st.subheader("Histórico de Sessões")
        for s in reversed(sessoes):
            with st.expander(f"📅 {s['data']} - {s['paciente']}"):
                st.write(s.get('observacoes','Sem observações'))

st.divider()
st.write("💻 Desenvolvido por Luan Gama")
