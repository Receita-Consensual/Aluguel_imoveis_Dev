import streamlit as st
from supabase import create_client
import pandas as pd
import folium
from folium.plugins import MarkerCluster, Fullscreen, LocateControl
from streamlit_folium import st_folium
import requests
import numpy as np

# Configuração SEO
st.set_page_config(
    page_title="Lugar | Imóveis no Mapa 🇵🇹",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS Moderno
st.markdown("""
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], .stDeployButton, footer, #MainMenu {display: none !important;}
    .block-container {padding: 1rem !important;}
    .stApp {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;}

    h1, h2, h3, p, span, label {
        color: #ffffff !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .brand-text {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .stTextInput input {
        background-color: rgba(255,255,255,0.95) !important;
        color: #1a1a1a !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .stats-box {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Conexão Supabase
SUPABASE_URL = "https://zprocqmlefzjrepxtxko.supabase.co"
SUPABASE_KEY = "sb_publishable_wPBDEtqfKPrYMD6m6IJzWw_VWL9sVlM"
GOOGLE_API_KEY = "AIzaSyCws8dm1mPhPKdu4VUk7BTBEe25qGZDrb4"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

@st.cache_data(ttl=30)
def carregar_dados():
    try:
        res = supabase.table("imoveis").select("*").neq("lat", 0).limit(2000).execute()
        df = pd.DataFrame(res.data)
        if not df.empty:
            df['lat'] += np.random.uniform(-0.0005, 0.0005, size=len(df))
            df['lon'] += np.random.uniform(-0.0005, 0.0005, size=len(df))
        return df
    except:
        return pd.DataFrame()

# Interface
st.markdown('<div class="brand-text">🏠 Lugar</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Encontre seu próximo lar em Portugal</div>', unsafe_allow_html=True)

df_total = carregar_dados()

# Stats Box
if not df_total.empty:
    st.markdown(f'''
        <div class="stats-box">
            <h2 style="margin:0; font-size: 2rem;">📍 {len(df_total):,}</h2>
            <p style="margin:0;">imóveis disponíveis</p>
        </div>
    ''', unsafe_allow_html=True)

# Barra de Busca
col_search, col_btn = st.columns([8, 2])
with col_search:
    local_input = st.text_input("", placeholder="🔍 Digite a cidade (ex: Porto, Lisboa, Aveiro...)", label_visibility="collapsed")
with col_btn:
    buscar = st.button("BUSCAR")

# Lógica de Busca
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
            supabase.table("demandas").insert({"termo": cidade, "status": "pendente"}).execute()
        except:
            pass

        st.success(f"✅ Mostrando imóveis próximos a {local_input}")

# Mapa
m = folium.Map(
    location=map_center,
    zoom_start=zoom_start,
    tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
    attr="Google"
)

Fullscreen().add_to(m)
LocateControl(auto_start=False, strings={"title": "Ver minha localização"}).add_to(m)

if not df_total.empty:
    cluster = MarkerCluster(
        options={
            'maxClusterRadius': 50,
            'disableClusteringAtZoom': 15
        }
    ).add_to(m)

    for _, row in df_total.iterrows():
        try:
            preco = f"€ {float(row['preco']):,.0f}/mês" if row['preco'] and row['preco'] > 0 else "Consultar"
            titulo = row.get('titulo', 'Imóvel')[:50]
            tipologia = row.get('tipologia', '')
            area = f"{row.get('area_m2', '')}m²" if row.get('area_m2') else ''

            popup_html = f"""
            <div style="font-family: sans-serif; min-width: 200px;">
                <h4 style="margin: 0 0 8px 0; color: #667eea;">{preco}</h4>
                <p style="margin: 0 0 5px 0; font-size: 12px;"><b>{titulo}</b></p>
                <p style="margin: 0 0 8px 0; font-size: 11px; color: #666;">{tipologia} {area}</p>
                <a href="{row['link']}" target="_blank"
                   style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; padding: 6px 12px; text-decoration: none;
                          border-radius: 6px; font-size: 12px; font-weight: bold;">
                    Ver Anúncio →
                </a>
            </div>
            """

            cor = "purple" if "moradia" in str(tipologia).lower() else "blue"

            folium.Marker(
                [row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.Icon(color=cor, icon="home", prefix='fa')
            ).add_to(cluster)
        except:
            continue

st_folium(m, width="100%", height=600, returned_objects=[])

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.8); padding: 2rem;">
        <p style="font-size: 1.2rem; margin-bottom: 1rem;">💜 Feito com amor para ajudar você a encontrar seu lar</p>
        <p style="font-size: 0.9rem;">Dados atualizados automaticamente • Supabase + Python + Streamlit</p>
    </div>
""", unsafe_allow_html=True)
