import streamlit as st

st.set_page_config(
    page_title="Lugar | Debug",
    page_icon="🏠",
    layout="wide",
)

st.title("Debug - Testando imports")

try:
    st.write("1. Testando Supabase...")
    from supabase import create_client
    st.success("✅ Supabase OK")
except Exception as e:
    st.error(f"❌ Supabase ERRO: {e}")

try:
    st.write("2. Testando Pandas...")
    import pandas as pd
    st.success("✅ Pandas OK")
except Exception as e:
    st.error(f"❌ Pandas ERRO: {e}")

try:
    st.write("3. Testando Folium...")
    import folium
    st.success("✅ Folium OK")
except Exception as e:
    st.error(f"❌ Folium ERRO: {e}")

try:
    st.write("4. Testando Streamlit-Folium...")
    from streamlit_folium import st_folium
    st.success("✅ Streamlit-Folium OK")
except Exception as e:
    st.error(f"❌ Streamlit-Folium ERRO: {e}")

try:
    st.write("5. Testando conexão Supabase...")
    from supabase import create_client

    SUPABASE_URL = "https://zprocqmlefzjrepxtxko.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpwcm9jcW1sZWZ6anJlcHh0eGtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgyMjgyODIsImV4cCI6MjA1MzgwNDI4Mn0.wg6f1uejAzG-Ss1e6hFCaDpoBPrP4xDIgAiNf0pFjMw"

    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.success("✅ Conexão Supabase OK")

    # Testar query
    result = client.table("imoveis").select("*").limit(1).execute()
    st.write(f"Total de registros na tabela: {len(result.data) if result.data else 0}")

    if result.data:
        st.write("Exemplo de registro:")
        st.json(result.data[0])

except Exception as e:
    st.error(f"❌ Conexão Supabase ERRO: {e}")
    import traceback
    st.code(traceback.format_exc())

st.write("---")
st.write("Se todos os testes passaram, o app.py deveria funcionar!")
