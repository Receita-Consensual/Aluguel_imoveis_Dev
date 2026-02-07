import re
import time
import httpx
from bs4 import BeautifulSoup
from geocoder import geocode_address
from config import TIPOLOGIAS_MAP, MAX_PAGINAS_POR_CIDADE

BASE_URL = "https://casa.sapo.pt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

SLUG_DISTRITOS = {
    "Lisboa": "Lisboa",
    "Porto": "Porto",
    "Aveiro": "Aveiro",
    "Braga": "Braga",
    "Coimbra": "Coimbra",
    "Faro": "Faro",
    "Leiria": "Leiria",
    "Setubal": "Setubal",
    "Viseu": "Viseu",
    "Viana do Castelo": "Viana+do+Castelo",
    "Evora": "Evora",
    "Guarda": "Guarda",
    "Castelo Branco": "Castelo+Branco",
    "Santarem": "Santarem",
    "Beja": "Beja",
    "Braganca": "Braganca",
    "Vila Real": "Vila+Real",
    "Funchal": "Funchal",
    "Ponta Delgada": "Ponta+Delgada",
    "Guimaraes": "Braga",
    "Almada": "Setubal",
    "Amadora": "Lisboa",
    "Cascais": "Lisboa",
    "Sintra": "Lisboa",
    "Oeiras": "Lisboa",
    "Matosinhos": "Porto",
    "Gondomar": "Porto",
    "Vila Nova de Gaia": "Porto",
    "Loures": "Lisboa",
    "Odivelas": "Lisboa",
}


def detect_tipologia(text: str) -> str:
    text_lower = text.lower()
    for key, value in TIPOLOGIAS_MAP.items():
        if key in text_lower:
            return value
    return ""


def parse_price(text: str) -> float:
    nums = re.findall(r"[\d.,]+", text.replace(".", "").replace(",", "."))
    for n in nums:
        try:
            val = float(n)
            if 50 < val < 50000:
                return val
        except ValueError:
            pass
    return 0


def parse_area(text: str) -> float:
    match = re.search(r"(\d+)\s*m", text)
    if match:
        return float(match.group(1))
    return 0


def extract_real_link(href: str) -> str:
    match = re.search(r"l=(https://casa\.sapo\.pt/[^&?]+)", href)
    if match:
        return match.group(1)
    if href.startswith("http"):
        return href
    return BASE_URL + href


def scrape_cidade(cidade: str) -> list[dict]:
    distrito = SLUG_DISTRITOS.get(cidade)
    if not distrito:
        return []

    resultados = []
    client = httpx.Client(headers=HEADERS, follow_redirects=True, timeout=20)

    for pagina in range(1, MAX_PAGINAS_POR_CIDADE + 1):
        url = f"{BASE_URL}/Arrendar/Apartamentos/?sa=11&lc={distrito}"
        if pagina > 1:
            url += f"&pn={pagina}"

        try:
            resp = client.get(url)
            if resp.status_code != 200:
                print(f"  [sapo] Status {resp.status_code} em {cidade} pagina {pagina}")
                break

            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("div.property")

            if not items:
                break

            parsed_count = 0
            for item in items:
                try:
                    info = item.select_one("a.property-info")
                    if not info:
                        continue

                    price_type_el = info.select_one(".property-price-type")
                    price_type = price_type_el.get_text(strip=True).lower() if price_type_el else ""
                    if "alugar" not in price_type and "arrendar" not in price_type:
                        continue

                    href = info.get("href", "")
                    link = extract_real_link(href)

                    type_el = info.select_one(".property-type")
                    title = type_el.get_text(strip=True) if type_el else ""

                    price_val_el = info.select_one(".property-price-value")
                    price_text = price_val_el.get_text(strip=True) if price_val_el else "0"
                    preco = parse_price(price_text)

                    features_el = info.select_one(".property-features-text")
                    features_text = features_el.get_text(strip=True) if features_el else ""
                    area = parse_area(features_text)

                    loc_el = info.select_one(".property-location")
                    endereco = loc_el.get_text(strip=True) if loc_el else ""

                    img_el = item.select_one("img")
                    img_url = ""
                    if img_el:
                        src = img_el.get("src", "")
                        if src and not src.startswith("data:"):
                            img_url = src

                    tags_el = info.select(".property-features-tag span")
                    tags_text = " ".join(t.get_text(strip=True) for t in tags_el)

                    tipologia = detect_tipologia(f"{title} {features_text}")
                    mobiliado = any(
                        kw in f"{features_text} {tags_text}".lower()
                        for kw in ["mobilado", "mobiliado", "equipado"]
                    )

                    freguesia = ""
                    if "," in endereco:
                        parts = [p.strip() for p in endereco.split(",")]
                        if len(parts) >= 2:
                            freguesia = parts[0]

                    address_for_geo = endereco or f"{title}, {cidade}"
                    coords = geocode_address(address_for_geo)
                    lat, lon = coords if coords else (0, 0)

                    resultados.append({
                        "titulo": title[:500],
                        "link": link,
                        "endereco": endereco[:500],
                        "cidade": cidade,
                        "freguesia": freguesia[:200],
                        "tipologia": tipologia,
                        "preco": preco,
                        "area_m2": area,
                        "imagem_url": img_url,
                        "lat": lat,
                        "lon": lon,
                        "mobiliado": mobiliado,
                        "fonte": "sapo",
                        "descricao": "",
                    })
                    parsed_count += 1
                except Exception as e:
                    print(f"  [sapo] Erro ao parsear item: {e}")
                    continue

            print(f"  [sapo] {cidade} pagina {pagina}: {parsed_count} arrendamentos de {len(items)} anuncios")
            time.sleep(3)

        except Exception as e:
            print(f"  [sapo] Erro em {cidade} pagina {pagina}: {e}")
            break

    client.close()
    return resultados
