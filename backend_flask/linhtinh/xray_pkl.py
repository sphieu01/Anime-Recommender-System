import pickle
import pandas as pd

print("Đang mở hộp đen anime_artifacts.pkl...")

# 1. Mở file pkl
with open('anime_artifacts.pkl', 'rb') as f:
    artifacts = pickle.load(f)

# 2. Lấy cái Bảng dữ liệu (Dataframe) ra
anime_df = artifacts['dataframe']

# 3. Xuất bảng này ra thành file CSV để xem trực quan
anime_df.to_csv('xem_thu_data.csv', index=False, encoding='utf-8')

# 4. In thử ra Terminal cho bạn xem
print("\n=== 1. BẢNG DỮ LIỆU PHIM (5 dòng đầu) ===")
print(anime_df.head())

print("\n=== 2. TỪ ĐIỂN ID -> INDEX (5 phần tử đầu) ===")
id_to_index = artifacts['id_to_index']
# Chỉ lấy 5 phần tử đầu ra để in cho đỡ lag
preview_dict = {k: id_to_index[k] for k in list(id_to_index.keys())[:5]}
print(preview_dict)

print("\n✅ THÀNH CÔNG! Hãy nhìn sang thanh bên trái của VSCode, bạn sẽ thấy file 'xem_thu_data.csv' vừa được tạo ra!")