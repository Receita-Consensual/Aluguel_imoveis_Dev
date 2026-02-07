import streamlit as st

# Configuração da página
st.set_page_config(page_title="Receita Consensual", layout="wide")

# CSS para garantir que nada fique invisível
st.markdown("""
    <style>
    .main { background-color: #F1F5F9; }
    .prop-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .price { color: #1E40AF; font-size: 24px; font-weight: bold; }
    .title { font-size: 18px; font-weight: bold; color: #1E293B; }
    </style>
""", unsafe_allow_html=True)

st.title("🔭 Radar de Imóveis | Receita Consensual")
st.info("Visualizador em Modo Seguro (Sem dependências externas)")

# Criando 3 colunas para os cards
col1, col2, col3 = st.columns(3)

# Dados de teste para você ver o visor funcionando
casas = [
    {"preco": "850", "titulo": "T2 em Aveiro Centro", "local": "Aveiro"},
    {"preco": "1.100", "titulo": "Moradia em Ílhavo", "local": "Ílhavo"},
    {"preco": "700", "titulo": "T1 Vista Ria", "local": "Vera Cruz"}
]

for i, casa in enumerate(casas):
    target = [col1, col2, col3][i % 3]
    with target:
        st.markdown(f"""
            <div class="prop-card">
                <div class="price">€ {casa['preco']}</div>
                <div class="title">{casa['titulo']}</div>
                <p style="color: #64748B;">📍 {casa['local']}</p>
                <div style="background: #2563EB; color: white; text-align: center; padding: 8px; border-radius: 5px;">
                    Ver Anúncio
                </div>
            </div>
        """, unsafe_allow_html=True)