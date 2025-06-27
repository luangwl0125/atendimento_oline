import os
# garante que ffmpeg.exe e ffprobe.exe na raiz sejam encontrados
os.environ["PATH"] += os.pathsep + os.getcwd()

import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import pandas as pd
from datetime import datetime, date
import json

# Configuração única da página
st.set_page_config(
    page_title="OriaPsi",
    page_icon="🧠",
    layout="wide"
)

# ==== Parte “somente vídeo” se houver ?room=xxx ====
params = st.experimental_get_query_params()
room = params.get("room", [None])[0]

if room:
    st.title(f"🧠 Videochamada — Sala {room}")
    rtc_config = RTCConfiguration({
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    })
    webrtc_streamer(
        key=f"webrtc_{room}",
        rtc_configuration=rtc_config,
        media_stream_constraints={"video": True, "audio": True}
    )
    st.stop()

# ==== Funções de I/O e utilitárias ====
def carregar_pacientes():
    try:
        if os.path.exists('pacientes.json'):
            return json.load(open('pacientes.json', 'r', encoding='utf-8'))
    except Exception as e:
        st.error(f"Erro ao carregar pacientes: {e}")
    return []

def salvar_pacientes(pacientes):
    try:
        json.dump(pacientes, open('pacientes.json', 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar pacientes: {e}")

def carregar_sessoes():
    try:
        if os.path.exists('sessoes.json'):
            return json.load(open('sessoes.json', 'r', encoding='utf-8'))
    except Exception as e:
        st.error(f"Erro ao carregar sessões: {e}")
    return []

def salvar_sessoes(sessoes):
    try:
        json.dump(sessoes, open('sessoes.json', 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar sessões: {e}")

# ==== Cabeçalho e estado ====
st.title("🧠 Plataforma de Psicologia")
page = st.sidebar.selectbox("Escolha uma opção:", ["Atendimento On-line", "Gerenciador de Pacientes"])
if st.sidebar.button("🔄 Recarregar Dados"):
    st.experimental_rerun()

pacientes = carregar_pacientes()
sessoes = carregar_sessoes()

# ==== Página de Atendimento On-line ====
if page == "Atendimento On-line":
    st.header("📞 Atendimento On-line")
    if not pacientes:
        st.warning("⚠️ Nenhum paciente cadastrado.")
    else:
        st.success(f"✅ {len(pacientes)} paciente(s) cadastrado(s)")
        nomes = [p['nome'] for p in pacientes]
        sel = st.selectbox("Selecione o paciente:", ["..."] + nomes)
        if sel != "...":
            p = next(x for x in pacientes if x['nome'] == sel)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📋 Informações do Paciente")
                st.write(f"**Nome:** {p['nome']}")
                st.write(f"**Idade:** {p['idade']} anos")
                st.write(f"**Nascimento:** {p.get('data_nascimento','–')}")
                st.write(f"**Telefone:** {p.get('telefone','–')}")
            with col2:
                st.subheader("📝 Descrição")
                st.write(p.get('descricao','Sem descrição'))
            st.divider()

            st.subheader("🎥 Opções de Atendimento")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💬 Enviar link por WhatsApp"):
                    tel = ''.join(filter(str.isdigit, p.get('telefone','')))
                    if tel.startswith('55'): tel = tel[2:]
                    room_id = room or datetime.now().strftime("%H%M%S")
                    link = f"{st.runtime.server_url}?room={room_id}"
                    msg = f"Olá, acesse sua videochamada: {link}"
                    wa = f"https://wa.me/55{tel}?text={st.experimental_get_query_params()}"
                    st.markdown(f"[Abrir WhatsApp]({wa})")
            with c2:
                st.markdown("### 🎥 Iniciar WebRTC")
                rtc = RTCConfiguration({"iceServers":[{"urls":["stun:stun.l.google.com:19302"]}]})
                webrtc_streamer(key="video_call", rtc_configuration=rtc,
                               media_stream_constraints={"video":True,"audio":True})
            st.divider()

            st.subheader("📝 Observações")
            obs = st.text_area("", height=150)
            if st.button("💾 Salvar Observações"):
                sessoes.append({
                    'id':len(sessoes)+1,
                    'paciente':p['nome'],
                    'data':datetime.now().strftime("%d/%m/%Y %H:%M"),
                    'observacoes':obs
                })
                salvar_sessoes(sessoes)
                st.success("Observações salvas!")
        else:
            st.info("👆 Selecione um paciente.")

# ==== Gerenciador de Pacientes ====
else:
    st.header("👥 Gerenciador de Pacientes")
    tab1, tab2, tab3 = st.tabs(["➕ Adicionar","📋 Lista","📊 Histórico"])
    with tab1:
        st.subheader("Adicionar Paciente")
        with st.form("form"):
            n = st.text_input("Nome *")
            i = st.number_input("Idade *",0,120)
            t = st.text_input("Telefone *")
            e = st.text_input("E-mail")
            d = st.date_input("Nascimento",format="DD/MM/YYYY")
            g = st.selectbox("Gênero",["","M","F","NB","–"])
            desc = st.text_area("Descrição")
            if st.form_submit_button("💾 Salvar"):
                pacientes.append({
                    'id':len(pacientes)+1,'nome':n,'idade':i,'telefone':t,
                    'email':e,'data_nascimento':d.strftime("%d/%m/%Y"),
                    'genero':g,'descricao':desc,
                    'data_cadastro':datetime.now().strftime("%d/%m/%Y %H:%M")
                })
                salvar_pacientes(pacientes)
                st.experimental_rerun()
    with tab2:
        st.subheader("Lista de Pacientes")
        for p in pacientes:
            with st.expander(f"{p['nome']} ({p['idade']}a)"):
                st.write(p)
    with tab3:
        st.subheader("Histórico de Sessões")
        for s in reversed(sessoes):
            with st.expander(f"{s['data']} – {s['paciente']}"):
                st.write(s['observacoes'])

st.divider()
st.write("💻 Desenvolvido por Luan Gama")
