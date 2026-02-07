import time
import httpx

_cache: dict[str, tuple[float, float]] = {}
_last_request_time = 0.0


def geocode_address(address: str) -> tuple[float, float] | None:
    global _last_request_time

    key = address.strip().lower()
    if key in _cache:
        return _cache[key]

    elapsed = time.time() - _last_request_time
    if elapsed < 1.1:
        time.sleep(1.1 - elapsed)

    try:
        params = {
            "q": f"{address}, Portugal",
            "format": "json",
            "limit": 1,
            "countrycodes": "pt",
            "accept-language": "pt",
        }
        headers = {
            "User-Agent": "LugarPortugal/1.0 (property-search-engine)",
        }
        r = httpx.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers=headers,
            timeout=10,
        )
        _last_request_time = time.time()
        data = r.json()
        if data and len(data) > 0:
            coords = (float(data[0]["lat"]), float(data[0]["lon"]))
            _cache[key] = coords
            return coords
    except Exception as e:
        print(f"  [geocoder] Erro ao geocodificar '{address}': {e}")

    return None
