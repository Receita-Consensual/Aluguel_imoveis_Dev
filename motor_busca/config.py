import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
GOOGLE_GEOCODING_KEY = os.getenv("GOOGLE_GEOCODING_KEY") or os.getenv("VITE_GOOGLE_MAPS_API_KEY", "")

CIDADES_PORTUGAL = [
    "Lisboa", "Porto", "Aveiro", "Braga", "Coimbra", "Faro", "Leiria",
    "Setubal", "Viseu", "Viana do Castelo", "Evora", "Guarda",
    "Castelo Branco", "Santarem", "Beja", "Braganca", "Vila Real",
    "Funchal", "Ponta Delgada", "Guimaraes", "Almada", "Amadora",
    "Cascais", "Sintra", "Oeiras", "Matosinhos", "Gondomar",
    "Vila Nova de Gaia", "Loures", "Odivelas",
]

TIPOLOGIAS_MAP = {
    "t0": "T0", "t1": "T1", "t2": "T2", "t3": "T3",
    "t4": "T4", "t5": "T5+", "t6": "T5+",
    "moradia": "Moradia", "vivenda": "Moradia",
    "quarto": "Quarto", "room": "Quarto",
    "apartamento": "Apartamento", "flat": "Apartamento",
    "studio": "T0", "estudio": "T0",
}

INTERVALO_ENTRE_CIDADES_SEG = 5
INTERVALO_ENTRE_CICLOS_MIN = 10
MAX_PAGINAS_POR_CIDADE = 5
