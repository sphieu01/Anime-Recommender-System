import { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import RecommenderForm from './components/RecommenderForm';
import StatusSection from './components/StatusSection';
import AnimeCard from './components/AnimeCard';
import './App.css';

function App() {
  const [username, setUsername] = useState(''); // username: Lưu trữ chuỗi ký tự người dùng đang gõ vào ô Input.
  const [recommendations, setRecommendations] = useState([]); // danh sach cac phim
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userInfo, setUserInfo] = useState(null); // { name: "sphieu47", totalWatched: 150 }

  const handleRecommend = async (e) => {
    e.preventDefault();
    if (!username.trim()) return;

    setLoading(true);
    setError(null);
    setRecommendations([]);
    setUserInfo(null);

    try {
      const response = await axios.post('http://localhost:5000/api/recommend', {
        username: username
      });

      setRecommendations(response.data.recommendations);
      setUserInfo({
        name: response.data.username,
        totalWatched: response.data.total_watched
      });
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.error);
      } else {
        setError("Không thể kết nối đến Server. Vui lòng kiểm tra Backend!");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="layout-container">
      <div className="layout-inner">
        <Header />
        
        <RecommenderForm 
          username={username} 
          setUsername={setUsername} 
          handleRecommend={handleRecommend} 
          loading={loading} 
        />
        
        <StatusSection 
          error={error} 
          userInfo={userInfo} 
          loading={loading} 
        />
        
        {!loading && recommendations.length > 0 && (
          <section className="recommendation-grid-wrapper glass-panel">
            <h2 className="section-title text-light">
              Top 10 Gợi ý <span className="item-count text-muted">({recommendations.length} items)</span>
            </h2>
            <div className="anime-grid">
              {recommendations.map((anime, index) => (
                <AnimeCard anime={anime} index={index} key={anime.anime_id} />
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

export default App;