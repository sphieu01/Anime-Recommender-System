# KHAI BÁO THƯ VIỆN
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from surprise import Reader, Dataset, SVD, accuracy
from surprise.model_selection import train_test_split
import pickle

# 1: ĐỌC VÀ TIỀN XỬ LÝ DỮ LIỆU

print("1. Đang tải và dọn dẹp dữ liệu...")
# Xử lý Anime
anime_df = pd.read_csv('/content/drive/MyDrive/Hybrid Anime Recommender System/anime-filtered.csv')
anime_df = anime_df.rename(columns={'Name': 'name', 'Genres': 'genre'})
anime_df['genre'] = anime_df['genre'].fillna('')

# Xử lý Rating (Dùng 2 triệu dòng, ép kiểu để tối ưu RAM)
rating_df = pd.read_csv('/content/drive/MyDrive/Hybrid Anime Recommender System/user-filtered.csv',
                        nrows=2000000,
                        dtype={'user_id': 'int32', 'anime_id': 'int32', 'rating': 'int8'})

# Xóa điểm 0 (Người dùng lưu phim nhưng lười chấm điểm)
rating_df = rating_df[rating_df['rating'] > 0]

# Lọc dữ liệu thưa (Chỉ lấy User > 50 phim và Anime > 50 lượt vote)
min_anime_ratings = 50
filter_animes = rating_df['anime_id'].value_counts() > min_anime_ratings
filter_animes = filter_animes[filter_animes].index.tolist() # mang gom nhung id user > 50 phim

min_user_ratings = 50
filter_users = rating_df['user_id'].value_counts() > min_user_ratings
filter_users = filter_users[filter_users].index.tolist()

rating_df_clean = rating_df[(rating_df['anime_id'].isin(filter_animes)) & (rating_df['user_id'].isin(filter_users))]
print(f"-> Tổng số rating tinh khiết để train AI: {len(rating_df_clean)}")

# co the bo sung train theo mo ta, dao dien, ...
#2: HUẤN LUYỆN CONTENT-BASED
print("\n2. Đang xây dựng ma trận nội dung (TF-IDF & Cosine)...")

# ÉP MA TRẬN NHỎ LẠI
valid_anime_ids = rating_df_clean['anime_id'].unique()
anime_df = anime_df[anime_df['anime_id'].isin(valid_anime_ids)]

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=1, stop_words='english')
tfidf_matrix = tf.fit_transform(anime_df['genre'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Tạo từ điển tra cứu nhanh
anime_df = anime_df.reset_index(drop=True)
indices = pd.Series(anime_df.index, index=anime_df['name'])        # Tra theo Tên
id_to_index = pd.Series(anime_df.index, index=anime_df['anime_id']) # Tra theo ID

# 3: HUẤN LUYỆN COLLABORATIVE FILTERING (SVD)
print("\n3. Đang huấn luyện SVD và đo sai số (Có thể mất 1-2 phút)...")
reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(rating_df_clean[['user_id', 'anime_id', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Khởi tạo SVD với các siêu tham số chống học vẹt (Regularization)
svd_model = SVD(n_epochs=30, lr_all=0.005, reg_all=0.1, verbose=False) # Tắt verbose cho gọn màn hình
svd_model.fit(trainset)

# Tính sai số
predictions = svd_model.test(testset)
print(f"-> RMSE CHÍNH THỨC CỦA HỆ THỐNG: {accuracy.rmse(predictions, verbose=False):.4f}")

# 4: HÀM HYBRID GỢI Ý (MULTI-INPUT BY ID)
def multi_input_hybrid_recommendation_by_id(user_ratings_dict):
    candidate_scores = {}
    watched_anime_ids = list(user_ratings_dict.keys())

    for anime_id, rating in user_ratings_dict.items():
        if anime_id in id_to_index:
            idx = id_to_index[anime_id]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:21]

            for i, sim in sim_scores:
                candidate_id = anime_df.iloc[i]['anime_id']
                if candidate_id in watched_anime_ids:
                    continue

                score = sim * rating
                if candidate_id in candidate_scores:
                    candidate_scores[candidate_id] += score
                else:
                    candidate_scores[candidate_id] = score

    top_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    result_indices = [id_to_index[cid] for cid, score in top_candidates]
    result_df = anime_df.iloc[result_indices][['anime_id', 'name', 'genre']].copy()
    result_df['hybrid_score'] = [score for cid, score in top_candidates]

    return result_df

# 5: CHẠY THỬ NGHIỆM (DEMO)

danh_sach_myanimelist_id = {
    19815: 10.0,  # No Game No Life
    30831: 10.0,  # KonoSuba
    1535: 606,    # Death Note
    38691: 9.0    # Dr. Stone: Stone Wars
}

print("\n=> KẾT QUẢ GỢI Ý CHO DANH SÁCH BẰNG ID:")
print(multi_input_hybrid_recommendation_by_id(danh_sach_myanimelist_id))