# steam_api.py
import requests

class SteamError(Exception):
    """Base exception for all Steam API related errors"""
    pass

def get_game_name(appid):
    """
    Get the official game name from Steam API.
    """
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data and data.get(str(appid), {}).get('success'):
                return data[str(appid)]['data']['name']
        return f"AppID {appid}"  # Fallback: return AppID if name cannot be found
    except Exception:
        return f"AppID {appid}"

def get_steam_reviews(appid):
    """
    Fetch the latest 100 English reviews for a game.
    """
    url = f"https://store.steampowered.com/appreviews/{appid}"
    params = {
        'json': 1,
        'filter': 'recent',
        'language': 'english',
        'num_per_page': 100
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        raise SteamError(f"Network connection issues: {e}")

    if response.status_code != 200:
        raise SteamError(f"Steam server returned status code {response.status_code}")

    try:
        data = response.json()
    except Exception:
        raise SteamError("Failed to parse JSON response from Steam API")

    if data.get('success') != 1:
        raise SteamError(f"Invalid AppID or Steam API failure for AppID {appid}")

    reviews_list = data.get('reviews', [])
    if not reviews_list:
        raise SteamError(f"No English reviews found for AppID {appid}")

    return [rev['review'] for rev in reviews_list]