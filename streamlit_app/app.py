import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
from datetime import datetime

# --- 1. CONFIGURAÇÕES TÉCNICAS E DE SEGURANÇA ---
st.set_page_config(
    page_title="Lugar | Plataforma de Inteligência Imobiliária",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GESTÃO DE ESTADO (LOGIN E SUBSCRITORES) ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'tipo_plano' not in st.session_state:
    st.session_state.tipo_plano = "Visitante" # Visitante, Pro, Enterprise

# --- 3. ESTILIZAÇÃO CSS AVANÇADA (VISUAL CLARO E "VIVO") ---
st.markdown("""
    <style>
    /* Reset e Fundo Profissional */
    .stApp { background-color: #FFFFFF; color: #1E293B; }
    header {visibility: hidden;}
    
    /* Cabeçalho Lugar */
    .header-lugar {
        background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%);
        padding: 40px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        margin-top: -60px;
        margin-bottom: 40px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .header-lugar h1 { color: white !important; font-size: 3.5rem !important; margin: 0; }
    .header-lugar p { color: #DBEAFE; font-size: 1.2rem; }

    /* Cards de Imóvel Estilo Portal */
    .imovel-card {
        background: #F8FAFC;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    .imovel-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #3B82F6;
    }
    .price-tag { color: #2563EB; font-size: 24px; font-weight: 800; }
    .badge-pro { 
        background-color: #FACC15; color: #713F12; padding: 4px 8px; 
        border-radius: 6px; font-size: 10px; font-weight: bold; 
    }

    /* Barra de Busca Flutuante */
    .search-dock {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #F1F5F9;
        margin-top: -60px;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR - CONTROLE DE ACESSO E ASSINATURAS ---
with st.sidebar:
    st.image("Gemini_Generated_Image_su6quisu6quisu6q.jpg", width=120)
    st.title("Acesso ao Lugar")
    
    if not st.session_state.autenticado:
        with st.expander("🔑 Login de Assinante", expanded=True):
            user = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar"):
                st.session_state.autenticado = True
                st.session_state.tipo_plano = "Pro" # Simulação de sucesso
                st.rerun()
        st.info("Subscreva para ver detalhes exclusivos dos imóveis.")
    else:
        st.success(f"Bem-vindo, {st.session_state.tipo_plano}!")
        if st.button("Sair"):
            st.session_state.autenticado = False
            st.session_state.tipo_plano = "Visitante"
            st.rerun()

    st.divider()
    st.markdown("### 📊 Estatísticas da Receita Consensual")
    st.caption("Imóveis minerados hoje: 142")
    st.caption("Regiões ativas: 12 (Portugal)")

# --- 5. CABEÇALHO PRINCIPAL ---
st.markdown("""
    <div class="header-lugar">
        <h1>Lugar</h1>
        <p>Inteligência de Dados Imobiliários • Gestão de Receita Consensual</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. BARRA DE BUSCA AVANÇADA ---
with st.container():
    st.markdown('<div class="search-dock">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    with c1:
        local = st.text_input("📍 Localização", placeholder="Ex: Aveiro, Glória...")
    with c2:
        range_preco = st.selectbox("Preço Max", ["Qualquer", "€500", "€1000", "€1500", "€2000+"])
    with c3:
        quartos = st.selectbox("Tipologia", ["T0", "T1", "T2", "T3+"])
    with c4:
        st.write("")
        st.button("🔍 Filtrar no Mapa")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. DASHBOARD CENTRAL (MAPA + LISTA) ---
col_mapa, col_lista = st.columns([2, 1])

with col_mapa:
    st.subheader("🗺️ Exploração Visual")
    # Configuração de Mapa Claro (Style: Google Maps / Idealista)
    m = folium.Map(location=[40.6405, -8.6538], zoom_start=13, tiles='CartoDB positron')
    
    # Pontos Simulados (Amanhã conectamos com o seu Scraper/Supabase)
    pontos = [
        {"lat": 40.6445, "lon": -8.6588, "nome": "T2 Renovado", "preco": "€850"},
        {"lat": 40.6380, "lon": -8.6520, "nome": "T1 Próximo à UA", "preco": "€650"}
    ]
    
    for p in pontos:
        folium.Marker(
            [p['lat'], p['lon']],
            popup=f"<b>{p['nome']}</b><br>{p['preco']}",
            icon=folium.Icon(color='blue', icon='home')
        ).add_to(m)
        
    st_folium(m, width="100%", height=600, returned_objects=[])

with col_lista:
    st.subheader("✨ Recomendações")
    
    # Exemplo de lógica de subscrição
    for i in range(3):
        st.markdown(f"""
            <div class="imovel-card">
                <span class="badge-pro">PRO</span>
                <div class="price-tag">€ {700 + (i*200)}/mês</div>
                <h4>Apartamento em Aveiro T{i+1}</h4>
                <p>📍 Vera Cruz, Aveiro</p>
                <hr>
                <div style="font-size: 12px; color: #64748B;">
                    Detectado há 12 min • Fonte: OLX/Idealista
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Funcionalidade bloqueada para visitantes
        if st.session_state.tipo_plano == "Visitante":
            st.warning("🔒 Sublinhe para ver o contato")
        else:
            st.success("📞 Contato: +351 9XX XXX XXX")

# --- 8. RODAPÉ TÉCNICO ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: #94A3B8; padding-bottom: 20px;">
        © 2026 Lugar by Nicolas Martins Silva • Powered by Receita Consensual <br>
        Ambiente de Dados: Aveiro, Portugal
    </div>
""", unsafe_allow_html=True)