import streamlit as st
import requests

# --- CONFIGURAÇÃO DA PÁGINA (Limpa o topo roxo padrão) ---
st.set_page_config(
    page_title="Receita Consensual | Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS PROFISSIONAL (AZUL CLARO E CINZA) ---
st.markdown("""
    <style>
    /* Remove a linha colorida do topo do Streamlit */
    header {visibility: hidden;}
    
    /* Fundo Principal (Cinza muito claro/Slate) */
    .main { 
        background-color: #F8FAFC; 
    }
    
    /* Sidebar Neutra */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9 !important;
        border-right: 1px solid #E2E8F0;
    }

    /* Títulos em Azul Escuro Profissional */
    h1, h2, h3 {
        color: #1E293B !important;
        font-family: 'Inter', sans-serif;
    }

    /* CARD DO IMÓVEL (O coração do visual) */
    .prop-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .prop-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #BAE6FD; /* Azul clarinho no hover */
    }

    /* Preço em destaque (Azul) */
    .price-tag {
        color: #0284C7;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    /* Localização e detalhes em Cinza */
    .loc-tag {
        color: #64748B;
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 15px;
    }

    /* Botão Estilo "SaaS" (Azul Slate) */
    .btn-details {
        display: block;
        background-color: #475569;
        color: #FFFFFF !important;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        transition: background-color 0.2s;
    }
    .btn-details:hover {
        background-color: #1E293B;
    }

    /* Badge Discreta */
    .badge {
        background-color: #F1F5F9;
        color: #475569;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (FILTROS) ---
with st.sidebar:
    st.markdown("### 🏢 Receita Consensual")
    st.write("Filtros de busca ativa")
    st.divider()
    
    # Campo de busca (Substituirá o autocomplete por agora para ser rápido)
    busca = st.text_input("📍 Localização", placeholder="Ex: Aveiro, Portugal")
    
    preco_max = st.slider("Preço Máximo", 400, 2500, 1000, step=50)
    
    st.divider()
    st.caption("Motor Infinito: Ativo ✅")

# --- ÁREA PRINCIPAL ---
st.title("🔭 Radar de Oportunidades")
st.write(f"Resultados recentes em **{busca if busca else 'Aveiro e região'}**")

# Grid de 3 colunas
col1, col2, col3 = st.columns(3)

# DADOS PARA TESTE VISUAL (Amanhã você conecta o Supabase aqui)
imoveis = [
    {"titulo": "T2 Moderno - Glória", "preco": "850", "local": "Aveiro, Centro", "tipo": "Apartamento"},
    {"titulo": "Moradia Isolada T3", "preco": "1.200", "local": "Ílhavo, Aveiro", "tipo": "Moradia"},
    {"titulo": "T1 Vista Ria - Vera Cruz", "preco": "750", "local": "Aveiro, Beira-Mar", "tipo": "Apartamento"}
]

for i, imovel in enumerate(imoveis):
    target_col = [col1, col2, col3][i % 3]
    with target_col:
        st.markdown(f"""
            <div class="prop-card">
                <span class="badge">{imovel['tipo']}</span>
                <div style="height: 12px;"></div>
                <div class="price-tag">€ {imovel['preco']}</div>
                <div style="font-weight: 700; font-size: 19px; color: #1E293B;">{imovel['titulo']}</div>
                <div class="loc-tag">📍 {imovel['local']}</div>
                <a href="#" class="btn-details">Ver Anúncio Completo</a>
            </div>
        """, unsafe_allow_html=True)

st.divider()
st.info("💡 Dica: O motor captura anúncios do OLX e Idealista a cada 10 minutos.")