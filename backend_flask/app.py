from flask import Flask, request, jsonify
from flask_cors import CORS
from core.scraper import get_mal_user_animelist
from core.recommender import recommend_animes, anime_df

app = Flask(__name__)
CORS(app) 

# ==========================================
# API 1: GỢI Ý TỪ MYANIMELIST USERNAME
# ==========================================
@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({'error': 'Vui lòng nhập Username'}), 400
        
    user_ratings = get_mal_user_animelist(username)
    if user_ratings is None:
        return jsonify({'error': 'Không tìm thấy user hoặc danh sách Private'}), 404
    if len(user_ratings) == 0:
        return jsonify({'error': 'User này chưa chấm điểm bộ anime nào!'}), 400
         
    recommendations = recommend_animes(user_ratings, username)
    return jsonify({
        'message': 'Thành công',
        'username': username,
        'total_watched': len(user_ratings),
        'recommendations': recommendations
    })

# ==========================================
# API 2: TÌM KIẾM ANIME (AUTOCOMPLETE 24.000 PHIM)
# ==========================================
@app.route('/api/search-anime', methods=['GET'])
def search_anime():
    query = request.args.get('q', '').lower()
    if len(query) < 2:
        return jsonify([])
    
    # Tìm tất cả phim có chứa chuỗi query trong tên, lấy 15 kết quả đầu tiên
    matches = anime_df[anime_df['name'].str.lower().str.contains(query, na=False)].head(15)
    results = matches[['anime_id', 'name', 'genre']].to_dict(orient='records')
    return jsonify(results)

# ==========================================
# API 3: GỢI Ý TỪ DANH SÁCH NHẬP THỦ CÔNG
# ==========================================
@app.route('/api/recommend-manual', methods=['POST'])
def recommend_manual():
    data = request.get_json()
    manual_ratings = data.get('ratings') # Nhận một dictionary {anime_id: score}
    
    if not manual_ratings or len(manual_ratings) == 0:
        return jsonify({'error': 'Danh sách trống'}), 400
        
    # Gọi AI với một username ảo (Cold Start)
    recommendations = recommend_animes(manual_ratings, "manual_guest_user")
    
    return jsonify({
        'message': 'Thành công',
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)