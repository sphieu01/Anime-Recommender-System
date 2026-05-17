import { useState } from 'react';
import axios from 'axios';
import AnimeCard from '../components/AnimeCard';

const MALSearch = () => {
  const [username, setUsername] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userInfo, setUserInfo] = useState(null);

  const handleRecommend = async (e) => {
    e.preventDefault();
    if (!username.trim()) return;
    setLoading(true); setError(null); setRecommendations([]); setUserInfo(null);

    try {
      const response = await axios.post('http://localhost:5000/api/recommend', { username });
      setRecommendations(response.data.recommendations);
      setUserInfo({ name: response.data.username, totalWatched: response.data.total_watched });
    } catch (err) {
      setError(err.response?.data?.error || "Lỗi kết nối Server!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-wrapper">
      <form className="search-box glass-panel" onSubmit={handleRecommend}>
        <label className="input-label text-muted">Nhập Username MyAnimeList</label>
        <div className="input-row">
          <input 
            type="text" 
            placeholder="Ví dụ: sphieu47, Xinil..." 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            disabled={loading}
            className="text-input glass-input text-light"
          />
          <button type="submit" disabled={loading || !username.trim()} className="submit-btn gradient-bg text-dark">
            {loading ? 'Đang phân tích...' : 'Gợi ý ngay!'}
          </button>
        </div>
      </form>

      {/* Khu vực thông báo (Loading/Error/Success) */}
      {loading && <div className="loader glass-panel gradient-text-accent">Đang tính toán ma trận...</div>}
      {error && <div className="error-message glass-panel-red text-red">⚠️ {error}</div>}
      {userInfo && (
        <div className="success-message glass-panel-green text-green">
          Đã đồng bộ <strong>{userInfo.totalWatched}</strong> phim từ tài khoản <strong>{userInfo.name}</strong>.
        </div>
      )}

      {/* Khu vực kết quả */}
      {!loading && recommendations.length > 0 && (
        <section className="recommendation-grid-wrapper glass-panel">
          <h2 className="section-title text-light">Top 10 Gợi ý</h2>
          <div className="anime-grid">
            {recommendations.map((anime, index) => (
              <AnimeCard anime={anime} index={index} key={anime.anime_id} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default MALSearch;