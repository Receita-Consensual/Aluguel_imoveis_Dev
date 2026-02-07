import httpx
from config import GOOGLE_GEOCODING_KEY

_cache: dict[str, tuple[float, float]] = {}


def geocode_address(address: str) -> tuple[float, float] | None:
    key = address.strip().lower()
    if key in _cache:
        return _cache[key]

    try:
        params = {
            "address": f"{address}, Portugal",
            "key": GOOGLE_GEOCODING_KEY,
            "region": "pt",
            "language": "pt",
        }
        r = httpx.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params=params,
            timeout=10,
        )
        data = r.json()
        if data.get("status") == "OK" and data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            coords = (loc["lat"], loc["lng"])
            _cache[key] = coords
            return coords
    except Exception as e:
        print(f"  [geocoder] Erro ao geocodificar '{address}': {e}")

    return None
