import re
import time
import httpx
from bs4 import BeautifulSoup
from geocoder import geocode_address
from config import TIPOLOGIAS_MAP, MAX_PAGINAS_POR_CIDADE

BASE_URL = "https://www.idealista.pt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.idealista.pt/",
}

SLUG_CIDADES = {
    "Lisboa": "lisboa",
    "Porto": "porto",
    "Aveiro": "aveiro",
    "Braga": "braga",
    "Coimbra": "coimbra",
    "Faro": "faro",
    "Leiria": "leiria",
    "Setubal": "setubal",
    "Viseu": "viseu",
    "Viana do Castelo": "viana-do-castelo",
    "Evora": "evora",
    "Guarda": "guarda",
    "Castelo Branco": "castelo-branco",
    "Santarem": "santarem",
    "Beja": "beja",
    "Braganca": "braganca",
    "Vila Real": "vila-real",
    "Funchal": "funchal",
    "Ponta Delgada": "ponta-delgada",
    "Guimaraes": "guimaraes",
    "Almada": "almada",
    "Amadora": "amadora",
    "Cascais": "cascais",
    "Sintra": "sintra",
    "Oeiras": "oeiras",
    "Matosinhos": "matosinhos",
    "Gondomar": "gondomar",
    "Vila Nova de Gaia": "vila-nova-de-gaia",
    "Loures": "loures",
    "Odivelas": "odivelas",
}


def detect_tipologia(title: str, area_text: str = "") -> str:
    combined = f"{title} {area_text}".lower()
    for key, value in TIPOLOGIAS_MAP.items():
        if key in combined:
            return value
    return ""


def parse_price(text: str) -> float:
    nums = re.findall(r"[\d.,]+", text.replace(".", "").replace(",", "."))
    if nums:
        try:
            return float(nums[0])
        except ValueError:
            pass
    return 0


def parse_area(text: str) -> float:
    match = re.search(r"(\d+)\s*m", text)
    if match:
        return float(match.group(1))
    return 0


def scrape_cidade(cidade: str) -> list[dict]:
    slug = SLUG_CIDADES.get(cidade)
    if not slug:
        print(f"  [idealista] Slug nao encontrado para {cidade}")
        return []

    resultados = []
    client = httpx.Client(headers=HEADERS, follow_redirects=True, timeout=20)

    for pagina in range(1, MAX_PAGINAS_POR_CIDADE + 1):
        url = f"{BASE_URL}/arrendar-casas/{slug}/"
        if pagina > 1:
            url += f"pagina-{pagina}.htm"

        try:
            resp = client.get(url)
            if resp.status_code == 403:
                print(f"  [idealista] 403 em {cidade} pagina {pagina} - pausando")
                time.sleep(60)
                break
            if resp.status_code != 200:
                print(f"  [idealista] Status {resp.status_code} em {cidade} pagina {pagina}")
                break

            soup = BeautifulSoup(resp.text, "html.parser")
            items = soup.select("article.item")

            if not items:
                break

            for item in items:
                try:
                    link_el = item.select_one("a.item-link")
                    if not link_el:
                        continue

                    href = link_el.get("href", "")
                    if not href.startswith("http"):
                        href = BASE_URL + href

                    title = link_el.get_text(strip=True)

                    price_el = item.select_one(".item-price")
                    price_text = price_el.get_text(strip=True) if price_el else "0"
                    preco = parse_price(price_text)

                    detail_els = item.select(".item-detail span")
                    details_text = " ".join(el.get_text(strip=True) for el in detail_els)
                    area = parse_area(details_text)

                    img_el = item.select_one("img")
                    img_url = ""
                    if img_el:
                        img_url = img_el.get("src", "") or img_el.get("data-src", "")

                    desc_el = item.select_one(".item-description")
                    descricao = desc_el.get_text(strip=True) if desc_el else ""

                    tipologia = detect_tipologia(title, details_text)
                    mobiliado = any(
                        kw in descricao.lower()
                        for kw in ["mobilado", "mobiliado", "equipado", "furnished"]
                    )

                    endereco_parts = []
                    addr_el = item.select_one(".item-detail-char .item-parking")
                    if addr_el:
                        endereco_parts.append(addr_el.get_text(strip=True))

                    endereco = ", ".join(endereco_parts) if endereco_parts else ""

                    coords = geocode_address(f"{title}, {cidade}")
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
                        "fonte": "idealista",
                        "descricao": descricao[:2000],
                    })
                except Exception as e:
                    print(f"  [idealista] Erro ao parsear item: {e}")
                    continue

            print(f"  [idealista] {cidade} pagina {pagina}: {len(items)} anuncios")
            time.sleep(3)

        except Exception as e:
            print(f"  [idealista] Erro em {cidade} pagina {pagina}: {e}")
            break

    client.close()
    return resultados
