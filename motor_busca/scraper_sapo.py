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
            items = soup.select(".property-list .searchResultProperty")

            if not items:
                items = soup.select(".property-list .property-info-content, .searchResults .property")

            if not items:
                break

            for item in items:
                try:
                    link_el = item.select_one("a[href]")
                    if not link_el:
                        continue

                    href = link_el.get("href", "")
                    if not href.startswith("http"):
                        href = BASE_URL + href

                    title_el = item.select_one(".property-type, .property-info h2, a span")
                    title = title_el.get_text(strip=True) if title_el else ""

                    price_el = item.select_one(".property-price, .priceFirst")
                    price_text = price_el.get_text(strip=True) if price_el else "0"
                    preco = parse_price(price_text)

                    area_el = item.select_one(".property-features, .property-features-text")
                    area_text = area_el.get_text(strip=True) if area_el else ""
                    area = parse_area(area_text)

                    img_el = item.select_one("img")
                    img_url = ""
                    if img_el:
                        img_url = img_el.get("src", "") or img_el.get("data-original", "")

                    loc_el = item.select_one(".property-location, .property-info-address")
                    endereco = loc_el.get_text(strip=True) if loc_el else ""

                    desc_el = item.select_one(".property-description")
                    descricao = desc_el.get_text(strip=True) if desc_el else ""

                    tipologia = detect_tipologia(f"{title} {area_text}")
                    mobiliado = any(
                        kw in descricao.lower()
                        for kw in ["mobilado", "mobiliado", "equipado"]
                    )

                    address_for_geo = endereco or f"{title}, {cidade}"
                    coords = geocode_address(address_for_geo)
                    lat, lon = coords if coords else (0, 0)

                    resultados.append({
                        "titulo": title[:500],
                        "link": href,
                        "endereco": endereco[:500],
                        "cidade": cidade,
                        "freguesia": "",
                        "tipologia": tipologia,
                        "preco": preco,
                        "area_m2": area,
                        "imagem_url": img_url,
                        "lat": lat,
                        "lon": lon,
                        "mobiliado": mobiliado,
                        "fonte": "sapo",
                        "descricao": descricao[:2000],
                    })
                except Exception as e:
                    print(f"  [sapo] Erro ao parsear item: {e}")
                    continue

            print(f"  [sapo] {cidade} pagina {pagina}: {len(items)} anuncios")
            time.sleep(3)

        except Exception as e:
            print(f"  [sapo] Erro em {cidade} pagina {pagina}: {e}")
            break

    client.close()
    return resultados
