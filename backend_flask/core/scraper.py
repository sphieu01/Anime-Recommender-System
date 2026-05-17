import requests
from bs4 import BeautifulSoup

def get_mal_user_animelist(username):
    print(f"\n[DEBUG API] Đang cào dữ liệu từ hệ thống gốc MyAnimeList cho: {username}")
    user_ratings = {}
    offset = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    while True:
        url = f"https://myanimelist.net/animelist/{username}/load.json?offset={offset}&status=7"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                if offset == 0: return None
                break
                
            data = response.json()
            if not isinstance(data, list) or len(data) == 0:
                break
                
            for item in data:
                score = item.get('score', 0)
                if score > 0:
                    anime_id = item.get('anime_id')
                    user_ratings[anime_id] = float(score)
                    
            offset += 300
        except Exception as e:
            print(f"[DEBUG API] LỖI HỆ THỐNG: {str(e)}")
            if offset == 0: return None
            break

    return user_ratings

def get_anime_poster(anime_id):
    url = f"https://myanimelist.net/anime/{anime_id}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        img_tag = soup.find('img', itemprop='image')
        if img_tag:
            return img_tag.get('data-src') or img_tag.get('src')
    except Exception as e:
        pass
    return "https://via.placeholder.com/225x318/1e293b/94a3b8?text=No+Poster"