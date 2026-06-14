import pickle
import pandas as pd
import concurrent.futures
from core.scraper import get_anime_poster

print("[CORE] Đang nạp SVD và Cosine Matrix lên bộ nhớ...")

# Sử dụng đường dẫn trỏ vào thư mục models/
with open('models/svd_model.pkl', 'rb') as f:
    svd_model = pickle.load(f) 
    
with open('models/tfidf_cosine_sim.pkl', 'rb') as f:
    tfidf_cosine_sim = pickle.load(f)
with open('models/bert_cosine_sim.pkl', 'rb') as f:
    bert_cosine_sim = pickle.load(f)
    
with open('models/anime_artifacts.pkl', 'rb') as f:
    artifacts = pickle.load(f)

anime_df = artifacts['dataframe']
id_to_index = artifacts['id_to_index']
print("[CORE] Tải model thành công!")

# THÊM THAM SỐ `engine` VÀO HÀM (Mặc định là deep_learning)
def recommend_animes(user_ratings_dict, username, engine="deep_learning"):
    clean_ratings = {int(k): float(v) for k, v in user_ratings_dict.items()}
    user_ratings_dict = clean_ratings
    candidate_scores = {}
    watched_anime_ids = list(user_ratings_dict.keys())


    # CẤU HÌNH CÔNG TẮC: CHỌN MA TRẬN & TRỌNG SỐ

    if engine == "deep_learning":
        cosine_sim = bert_cosine_sim # Dùng AI đọc hiểu ngữ nghĩa
        cb_weight = 0.2              # Trọng số CB thấp vì BERT tìm ra rất nhiều phim giống nhau
        svd_weight = 0.8             # Tin tưởng SVD 80% để đoán điểm chính xác
        print(f"[AI ENGINE] Đang chạy bằng Deep Learning (BERT) cho user: {username}")
    else:
        cosine_sim = tfidf_cosine_sim # Dùng thuật toán đếm từ khóa cũ
        cb_weight = 0.5               
        svd_weight = 0.5
        print(f"[AI ENGINE] Đang chạy bằng Classic (TF-IDF) cho user: {username}")


    # BƯỚC 1: Lọc thô bằng Content-Based (Cosine) + Trọng số Chất lượng

    for anime_id, rating in user_ratings_dict.items():
        if anime_id in id_to_index:
            idx = id_to_index[anime_id]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]

            for i, sim in sim_scores:
                # Lấy toàn bộ thông tin của dòng anime đó ra
                row = anime_df.iloc[i] 
                candidate_id = row['anime_id']
                
                if candidate_id in watched_anime_ids:
                    continue
                    
                # 🚀 LẤY TRỌNG SỐ CHẤT LƯỢNG (Nếu file .pkl không có thì mặc định là 1.0)
                quality_multiplier = row.get('quality_weight', 1.0)
                
                # 🚀 TÍNH ĐIỂM: Độ tương đồng * Điểm user chấm * Trọng số chất lượng phim
                score = sim * rating * quality_multiplier 
                
                if candidate_id in candidate_scores:
                    candidate_scores[candidate_id] += score
                else:
                    candidate_scores[candidate_id] = score
    
    # Lấy ra Top 50 ứng viên sáng giá nhất
    top_50_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:50]


    # BƯỚC 2: Tinh chỉnh bằng Collaborative (SVD)

    final_recommendations = []
    for candidate_id, cb_score in top_50_candidates:
        svd_prediction = svd_model.predict(username, candidate_id)
        predicted_rating = svd_prediction.est 

        # Áp dụng tỷ lệ trọng số 80-20 hoặc 50-50 tùy theo engine
        hybrid_score = (cb_score * cb_weight) + (predicted_rating * svd_weight) # hybrid_score = (cb_score * 0.5) + (predicted_rating * 0.5)
        final_recommendations.append((candidate_id, hybrid_score))

    top_10_final = sorted(final_recommendations, key=lambda x: x[1], reverse=True)[:10]

    result_indices = [id_to_index[cid] for cid, score in top_10_final]
    result_df = anime_df.iloc[result_indices][['anime_id', 'name', 'genre']].copy()
    result_df['hybrid_score'] = [score for cid, score in top_10_final]
    
    recommendations_list = result_df.to_dict(orient='records')

    # BƯỚC 3: Cào ảnh đa luồng

    print(f"\n[DEBUG] Cào ảnh bìa cho 10 phim gợi ý của {username}...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_anime = {executor.submit(get_anime_poster, anime['anime_id']): anime for anime in recommendations_list}
        for future in concurrent.futures.as_completed(future_to_anime):
            anime = future_to_anime[future]
            try:
                anime['image_url'] = future.result()
            except Exception:
                anime['image_url'] = "https://via.placeholder.com/225x318/1e293b/94a3b8?text=No+Poster"

    return recommendations_list