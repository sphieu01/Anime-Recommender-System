import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import AnimeCard from '../components/AnimeCard';

const ManualImport = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [selectedAnimes, setSelectedAnimes] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const dropdownRef = useRef(null);

  // 1. Lọc gợi ý từ API
  useEffect(() => {
    const delayDebounceFn = setTimeout(async () => {
      if (searchQuery.length < 2) {
        setSuggestions([]); 
        return;
      }
      try {
        const response = await axios.get(`http://localhost:5000/api/search-anime?q=${searchQuery}`);
        setSuggestions(response.data);
      } catch (err) {
        console.error("Lỗi khi tìm kiếm:", err);
      }
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery]);

  // 2. Xử lý thao tác User
  const handleSelectAnime = (anime) => {
    setSelectedAnimes(prev => {
      if (!prev.find(a => a.anime_id === anime.anime_id)) {
        return [...prev, { ...anime, score: 7 }];
      }
      return prev;
    });
    setSearchQuery('');
    setSuggestions([]);
  };

  const handleScoreChange = (id, newScore) => {
    setSelectedAnimes(prev => prev.map(a => a.anime_id === id ? { ...a, score: newScore } : a));
  };

  const handleRemove = (id) => {
    setSelectedAnimes(prev => prev.filter(a => a.anime_id !== id));
  };

  // 3. Xử lý gửi danh sách đi tính toán AI
  const handleCalculateAI = async () => {
    if (selectedAnimes.length === 0) return;
    
    setLoading(true);
    setError(null);
    setRecommendations([]);

    const ratingsDict = {};
    selectedAnimes.forEach(anime => {
      ratingsDict[anime.anime_id] = anime.score;
    });

    try {
      const response = await axios.post('http://localhost:5000/api/recommend-manual', {
        ratings: ratingsDict
      });

      if (response.data.recommendations && response.data.recommendations.length > 0) {
        setRecommendations(response.data.recommendations);
      } else {
        setError("AI không tìm thấy gợi ý nào phù hợp.");
      }
    } catch (err) {
      setError(err.response?.data?.error || "Không thể kết nối đến AI Server!");
    } finally {
      setLoading(false);
    }
  };

  // 4. GIAO DIỆN (RETURN)
  return (
    <div className="page-wrapper manual-import">
      {/* Box Tìm kiếm */}
      <div className="search-box glass-panel position-relative" style={{ zIndex: 100 }}>
        <label className="input-label text-muted">Tìm kiếm Anime để thêm vào danh sách</label>
        <input 
          type="text" 
          placeholder="Nhập tên phim (VD: Naruto, Bleach...)" 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="text-input glass-input text-light w-100"
        />
        
        {/* Hộp Dropdown Gợi ý */}
        {suggestions.length > 0 && (
          <div className="autocomplete-dropdown glass-panel">
            {suggestions.map(anime => (
              <div 
                key={anime.anime_id} 
                className="dropdown-item" 
                onClick={() => handleSelectAnime(anime)}
              >
                {anime.name}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Danh sách phim đã chọn & Chấm điểm */}
      {selectedAnimes.length > 0 && (
        <div className="selected-list glass-panel" style={{ zIndex: 1 }}>
          <h3 className="section-title text-light mb-4">Danh sách chấm điểm ({selectedAnimes.length})</h3>
          
          {selectedAnimes.map(anime => (
            <div key={anime.anime_id} className="selected-item glass-input">
              <div className="item-info">
                <span className="item-name text-light">{anime.name}</span>
                <span className="item-score gradient-text-accent">{anime.score} / 10</span>
              </div>
              <div className="item-controls">
                <input 
                  type="range" min="1" max="10" step="1" 
                  value={anime.score} 
                  onChange={(e) => handleScoreChange(anime.anime_id, parseInt(e.target.value))}
                  className="score-slider"
                />
                <button className="remove-btn text-red" onClick={() => handleRemove(anime.anime_id)}>Xóa</button>
              </div>
            </div>
          ))}

          <button 
            className="submit-btn gradient-bg text-dark mt-4 w-100" 
            onClick={handleCalculateAI}
            disabled={loading}
          >
            {loading ? 'Hệ thống AI đang tính toán...' : 'Tính toán AI với Danh sách này!'}
          </button>
        </div>
      )}

      {/* Trạng thái Loading / Error */}
      {loading && <div className="loader glass-panel gradient-text-accent mt-4">Đang chạy thuật toán lai ghép SVD...</div>}
      {error && <div className="error-message glass-panel-red text-red mt-4">⚠️ {error}</div>}
      
      {/* Lưới hiển thị kết quả Top 10 Anime */}
      {recommendations.length > 0 && (
        <section className="recommendation-grid-wrapper glass-panel mt-4 fade-in">
          <h2 className="section-title text-light">Top 10 Gợi ý dành riêng cho bạn</h2>
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

export default ManualImport;