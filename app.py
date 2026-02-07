import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, Fullscreen, LocateControl
from streamlit_folium import st_folium
import requests
import numpy as np

try:
    from supabase import create_client, Client
except ImportError:
    from supabase import create_client

st.set_page_config(
    page_title="Lugar | Imóveis no Mapa 🇵🇹",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS Ultra Moderno
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], .stDeployButton,
    footer, #MainMenu {display: none !important;}
    .block-container {padding: 1.5rem !important; max-width: 100% !important;}

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    h1, h2, h3, p, span, label, div {
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .hero-title {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        color: white;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        text-align: center;
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        font-weight: 400;
        margin-bottom: 2rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .stats-card {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem auto;
        border: 2px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        max-width: 400px;
    }

    .stats-number {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        color: white;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .stats-label {
        font-size: 1.1rem;
        margin: 0;
        opacity: 0.95;
    }

    .stTextInput input {
        background: rgba(255,255,255,0.95) !important;
        color: #1a1a1a !important;
        border: 3px solid rgba(255,255,255,0.4) !important;
        border-radius: 15px !important;
        font-size: 1.2rem !important;
        padding: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus {
        border-color: #f093fb !important;
        box-shadow: 0 0 0 3px rgba(240,147,251,0.3) !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        box-shadow: 0 8px 20px rgba(245,87,108,0.4);
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(245,87,108,0.6);
    }

    .founder-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid rgba(255,255,255,0.25);
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }

    .founder-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }

    .stForm {
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
    }

    .stSuccess {
        background-color: rgba(34, 197, 94, 0.2) !important;
        color: white !important;
        border-radius: 10px !important;
    }

    .footer {
        text-align: center;
        color: rgba(255,255,255,0.85);
        padding: 2rem 0;
        margin-top: 3rem;
        font-size: 1rem;
    }

    iframe {
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# CREDENCIAIS DO .env OU st.secrets
import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar .env do diretório raiz
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") if hasattr(st, 'secrets') and 'GOOGLE_API_KEY' in st.secrets else (os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GEOCODING_KEY", ""))
SUPABASE_URL = st.secrets.get("SUPABASE_URL") if hasattr(st, 'secrets') and 'SUPABASE_URL' in st.secrets else os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY") if hasattr(st, 'secrets') and 'SUPABASE_ANON_KEY' in st.secrets else (os.getenv("SUPABASE_ANON_KEY") or os.getenv("VITE_SUPABASE_ANON_KEY", ""))

# Debug - verificar se as variáveis foram carregadas
if not SUPABASE_URL:
    st.error("⚠️ SUPABASE_URL não encontrada. Verifique o arquivo .env")
    st.stop()
if not SUPABASE_KEY:
    st.error("⚠️ SUPABASE_ANON_KEY não encontrada. Verifique o arquivo .env")
    st.stop()

@st.cache_resource
def init_connection():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Erro ao conectar ao Supabase: {str(e)}")
        return None

supabase = init_connection()

if not supabase:
    st.stop()

@st.cache_data(ttl=30)
def carregar_dados():
    try:
        res = supabase.table("imoveis").select("*").neq("lat", 0).limit(2000).execute()
        if res and res.data:
            df = pd.DataFrame(res.data)
            if not df.empty and 'lat' in df.columns and 'lon' in df.columns:
                df['lat'] = df['lat'].astype(float) + np.random.uniform(-0.0005, 0.0005, size=len(df))
                df['lon'] = df['lon'].astype(float) + np.random.uniform(-0.0005, 0.0005, size=len(df))
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

# HERO SECTION
st.markdown('<h1 class="hero-title">🏠 Lugar</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Encontre seu próximo lar em Portugal com inteligência artificial</p>', unsafe_allow_html=True)

# CARREGAR DADOS
df_total = carregar_dados()

# STATS
if not df_total.empty:
    st.markdown(f'''
        <div class="stats-card">
            <div class="stats-number">📍 {len(df_total):,}</div>
            <div class="stats-label">imóveis disponíveis agora</div>
        </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('''
        <div class="stats-card">
            <div class="stats-number">🤖</div>
            <div class="stats-label">O robô está trabalhando...</div>
        </div>
    ''', unsafe_allow_html=True)

# BUSCA
col_search, col_btn = st.columns([7, 3])

with col_search:
    local_input = st.text_input(
        "",
        placeholder="🔍 Digite a cidade (Ex: Porto, Lisboa, Aveiro...)",
        label_visibility="collapsed"
    )

with col_btn:
    buscar = st.button("BUSCAR", use_container_width=True)

# LÓGICA DE BUSCA
map_center = [39.55, -7.85]
zoom_start = 7

if buscar and local_input:
    try:
        supabase.table("logs_pesquisas").insert({"termo_buscado": local_input}).execute()
    except:
        pass

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={local_input},Portugal&key={GOOGLE_API_KEY}"
    r = requests.get(url).json()

    if r['status'] == 'OK':
        loc = r['results'][0]['geometry']['location']
        map_center = [loc['lat'], loc['lng']]
        zoom_start = 13

        cidade = local_input.split(",")[0].strip()
        try:
            supabase.table("demandas").insert({
                "termo_busca": cidade,
                "lat": loc['lat'],
                "lng": loc['lng'],
                "raio_metros": 10000,
                "status": "pendente"
            }).execute()
        except:
            pass

        st.success(f"✅ Mostrando imóveis próximos a {local_input}")
    else:
        st.warning("⚠️ Localização não encontrada. Tente outra cidade.")

# MAPA
m = folium.Map(
    location=map_center,
    zoom_start=zoom_start,
    tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
    attr="Google",
    zoom_control=True,
    scrollWheelZoom=True,
    dragging=True,
)

Fullscreen(position='topright').add_to(m)
LocateControl(
    auto_start=False,
    strings={"title": "Ver minha localização"}
).add_to(m)

# MARCADORES
if not df_total.empty:
    cluster = MarkerCluster(
        options={
            'maxClusterRadius': 50,
            'disableClusteringAtZoom': 15,
            'spiderfyOnMaxZoom': True,
        }
    ).add_to(m)

    for _, row in df_total.iterrows():
        try:
            preco = f"€ {float(row['preco']):,.0f}/mês" if row.get('preco') and row['preco'] > 0 else "Consultar preço"
            titulo = row.get('titulo', 'Imóvel')[:60]
            tipologia = row.get('tipologia', 'Apartamento')
            area = f"{row.get('area_m2', '')}m²" if row.get('area_m2') else ''
            cidade = row.get('cidade', '')

            popup_html = f"""
            <div style="font-family: 'Inter', sans-serif; min-width: 220px; max-width: 280px;">
                <h3 style="margin: 0 0 10px 0; color: #667eea; font-size: 1.3rem; font-weight: 800;">
                    {preco}
                </h3>
                <p style="margin: 0 0 8px 0; font-size: 14px; font-weight: 600; color: #1a1a1a;">
                    {titulo}
                </p>
                <p style="margin: 0 0 5px 0; font-size: 12px; color: #666;">
                    📍 {cidade}
                </p>
                <p style="margin: 0 0 12px 0; font-size: 12px; color: #666;">
                    {tipologia} • {area}
                </p>
                <a href="{row['link']}" target="_blank"
                   style="display: inline-block;
                          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white;
                          padding: 8px 16px;
                          text-decoration: none;
                          border-radius: 8px;
                          font-size: 13px;
                          font-weight: 700;
                          box-shadow: 0 4px 10px rgba(102,126,234,0.3);
                          transition: all 0.3s;">
                    Ver Anúncio Completo →
                </a>
            </div>
            """

            if "moradia" in str(tipologia).lower() or "vivenda" in str(tipologia).lower():
                cor = "purple"
            elif "apartamento" in str(tipologia).lower():
                cor = "blue"
            else:
                cor = "green"

            folium.Marker(
                [row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=cor, icon="home", prefix='fa')
            ).add_to(cluster)

        except Exception as e:
            continue

mapa_data = st_folium(m, width="100%", height=600, returned_objects=["last_object_clicked"])

# LOG CLIQUES
if mapa_data.get("last_object_clicked"):
    click_lat = mapa_data["last_object_clicked"]["lat"]
    click_lon = mapa_data["last_object_clicked"]["lng"]
    match = df_total[
        (np.isclose(df_total['lat'], click_lat, atol=0.001)) &
        (np.isclose(df_total['lon'], click_lon, atol=0.001))
    ]
    if not match.empty:
        try:
            supabase.table("logs_cliques").insert({
                "imovel_id": int(match.iloc[0]['id']),
                "titulo_imovel": match.iloc[0]['titulo']
            }).execute()
        except:
            pass

# SEÇÃO FUNDADOR
st.markdown("---")

st.markdown("""
    <div class="founder-card">
        <div class="founder-title">🎟️ Seja Membro Fundador</div>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem; line-height: 1.6;">
            Cadastre-se agora e garanta <strong>20% de desconto vitalício</strong>
            quando o Lugar for lançado oficialmente. Vagas limitadas!
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
        **Benefícios exclusivos:**
        - ✨ 20% OFF para sempre
        - 🔔 Alertas de novos imóveis
        - 🎯 Busca personalizada
        - 🚀 Acesso antecipado
    """)

with col2:
    with st.form("form_fundador"):
        email_fundador = st.text_input("📧 Seu melhor e-mail", placeholder="seuemail@exemplo.com")
        submit = st.form_submit_button("GARANTIR MEU DESCONTO", use_container_width=True)

        if submit and email_fundador:
            try:
                supabase.table("alertas_clientes").insert({
                    "user_id": email_fundador,
                    "termo_busca": "FOUNDER",
                    "ativo": True
                }).execute()
                st.balloons()
                st.success("🎉 Parabéns! Você é oficialmente um Membro Fundador!")
            except:
                st.info("Você já está cadastrado!")

# FOOTER
st.markdown("""
    <div class="footer">
        <p style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">
            💜 Feito com amor para ajudar você a encontrar seu lar
        </p>
        <p style="font-size: 0.95rem; opacity: 0.9;">
            Dados atualizados automaticamente • Powered by Supabase + Python + AI
        </p>
    </div>
""", unsafe_allow_html=True)
