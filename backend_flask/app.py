from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import requests

app = Flask(__name__)
CORS(app) # Cho phép Frontend (React) kết nối với Backend (Flask)

# 1. TẢI CÁC FILE MODEL (.pkl) LÊN BỘ NHỚ
print("Đang tải model...")
with open('svd_model.pkl', 'rb') as f: #  Collaborative Filtering
    svd_model = pickle.load(f) 
with open('cosine_sim.pkl', 'rb') as f: # Content-Based
    cosine_sim = pickle.load(f)
with open('anime_artifacts.pkl', 'rb') as f: #  {tên phim, ID, thể loại} , id_to_index
    artifacts = pickle.load(f)

anime_df = artifacts['dataframe']
id_to_index = artifacts['id_to_index']
indices = artifacts['indices']
print("Tải model thành công!")


def get_mal_user_animelist(username):
    print(f"\n[DEBUG API] Đang cào dữ liệu từ hệ thống gốc MyAnimeList cho: {username}")
    user_ratings = {}
    offset = 0
    
    # Giả dạng trình duyệt người dùng để MyAnimeList không chặn
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    while True:
        # Đường dẫn nội bộ của MAL. status=7 nghĩa là lấy toàn bộ phim, offset là trang
        url = f"https://myanimelist.net/animelist/{username}/load.json?offset={offset}&status=7"
        # https://myanimelist.net/animelist/sphieu47/load.json?offset=0&status=7
        
        try:
            response = requests.get(url, headers=headers, timeout=10) # timeout=10s
            
            # Bắt lỗi nếu gõ sai tên hoặc danh sách bị khóa Private
            if response.status_code != 200:
                print(f"[DEBUG API] LỖI: MAL từ chối (Mã {response.status_code}). User không tồn tại hoặc list bị Private!")
                if offset == 0: return None
                break
                
            data = response.json()
            
            # Kiểm tra cấu trúc dữ liệu
            if not isinstance(data, list):
                print(f"[DEBUG API] LỖI: Dữ liệu bị sai cấu trúc.")
                if offset == 0: return None
                break
                
            # Nếu mảng rỗng (Hết phim) thì thoát vòng lặp
            if len(data) == 0:
                break
                
            # Lôi điểm số và ID ra khỏi mảng
            for item in data:
                score = item.get('score', 0)
                if score > 0:
                    anime_id = item.get('anime_id')
                    user_ratings[anime_id] = float(score)
                    
            print(f"[DEBUG API] Đã quét từ vị trí {offset} đến {offset + len(data)}...")
            offset += 300 # Đẩy offset lên 300 vì mỗi lần gọi MAL chỉ nhả tối đa 300 phim
            
        except Exception as e:
            print(f"[DEBUG API] LỖI HỆ THỐNG: {str(e)}")
            if offset == 0: return None
            break

    print(f"[DEBUG API] TỔNG KẾT: Lọc được {len(user_ratings)} bộ phim đã chấm điểm!")
    return user_ratings

# # 3. HÀM GỢI Ý (Bê y nguyên từ Colab của bạn sang)
# def recommend_animes(user_ratings_dict):
#     candidate_scores = {}
#     watched_anime_ids = list(user_ratings_dict.keys())

#     for anime_id, rating in user_ratings_dict.items():
#         if anime_id in id_to_index:
#             idx = id_to_index[anime_id]
#             sim_scores = list(enumerate(cosine_sim[idx]))
#             sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]

#             for i, sim in sim_scores:
#                 candidate_id = anime_df.iloc[i]['anime_id']
#                 if candidate_id in watched_anime_ids:
#                     continue

#                 score = sim * rating
#                 if candidate_id in candidate_scores:
#                     candidate_scores[candidate_id] += score
#                 else:
#                     candidate_scores[candidate_id] = score

#     top_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:10]
#     result_indices = [id_to_index[cid] for cid, score in top_candidates]
#     result_df = anime_df.iloc[result_indices][['anime_id', 'name', 'genre']].copy()
#     result_df['hybrid_score'] = [score for cid, score in top_candidates]
    
#     # Chuyển Dataframe thành JSON để gửi cho React
#     return result_df.to_dict(orient='records')

# 3. HÀM GỢI Ý LAI GHÉP (HYBRID CASCADE)
def recommend_animes(user_ratings_dict, username):
    candidate_scores = {}
    watched_anime_ids = list(user_ratings_dict.keys())

    # ==========================================
    # BƯỚC 1: CONTENT-BASED / ITEM-BASED (Lọc thô)
    # ==========================================
    for anime_id, rating in user_ratings_dict.items():
        if anime_id in id_to_index:
            idx = id_to_index[anime_id]
            # Lấy top 20 phim giống với phim user đã xem
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]

            for i, sim in sim_scores:
                candidate_id = anime_df.iloc[i]['anime_id']
                if candidate_id in watched_anime_ids:
                    continue

                # Tính điểm sơ bộ dựa trên độ tương đồng
                score = sim * rating #similarity = 0.9, rating = 2 điểm => low => ghet phim nay
                if candidate_id in candidate_scores:
                    candidate_scores[candidate_id] += score
                else:
                    candidate_scores[candidate_id] = score
    
    # Lấy ra Top 50 ứng viên sáng giá nhất để đưa cho AI (SVD) chấm điểm
    top_50_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:50]
    # print(top_50_candidates)
    # ==========================================
    # BƯỚC 2 & 3: COLLABORATIVE SVD & RERANK (Xếp hạng tinh)
    # ==========================================
    final_recommendations = []
    
    for candidate_id, cb_score in top_50_candidates:
        # Gọi "bộ não" SVD ra làm việc. 
        # Nó sẽ dự đoán xem "username" này sẽ chấm "candidate_id" này mấy điểm.
        svd_prediction = svd_model.predict(username, candidate_id)
        predicted_rating = svd_prediction.est #estimated chính là con số điểm dự đoán (VD: 8.5 điểm).
        
        # Công thức lai ghép (Hybrid): 50% trọng số của Cosine + 50% trọng số của SVD
        # Bạn có thể đổi tỷ lệ này (vd 0.3 và 0.7) nếu muốn SVD quyết định nhiều hơn
        hybrid_score = (cb_score * 0.5) + (predicted_rating * 0.5)
        
        final_recommendations.append((candidate_id, hybrid_score))

    # Sắp xếp lại lần cuối để lấy Top 10 gửi cho người dùng
    top_10_final = sorted(final_recommendations, key=lambda x: x[1], reverse=True)[:10]

    # Đóng gói dữ liệu thành JSON để gửi về Frontend
    result_indices = [id_to_index[cid] for cid, score in top_10_final]
    result_df = anime_df.iloc[result_indices][['anime_id', 'name', 'genre']].copy()
    result_df['hybrid_score'] = [score for cid, score in top_10_final]
    
    return result_df.to_dict(orient='records') # dữ liệu Pandas -> định dạng JSON

# 4. TẠO API ENDPOINT GIAO TIẾP VỚI FRONTEND
@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({'error': 'Vui lòng nhập Username'}), 400
        
    # Bước 1: Gọi API lấy lịch sử xem phim
    user_ratings = get_mal_user_animelist(username)
    
    if user_ratings is None:
        return jsonify({'error': 'Không tìm thấy user hoặc API bị lỗi'}), 404
        
    if len(user_ratings) == 0:
         return jsonify({'error': 'User này chưa chấm điểm bộ anime nào!'}), 400
         
    # Bước 2: Chạy hàm AI gợi ý
    # recommendations = recommend_animes(user_ratings)
    recommendations = recommend_animes(user_ratings, username)
    
    return jsonify({
        'message': 'Thành công',
        'username': username,
        'total_watched': len(user_ratings),
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)