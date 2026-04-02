const RecommenderForm = ({ username, setUsername, handleRecommend, loading }) => {
  return (
    <form className="search-box glass-panel" onSubmit={handleRecommend}>
      <label className="input-label text-muted">Nhập Username MyAnimeList</label>
      <div className="input-row">
        <input 
          type="text" 
          placeholder="Ví dụ: coolname, trunghieu1504..." 
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={loading}
          className="text-input glass-input text-light"
        />
        <button type="submit" disabled={loading || !username.trim()} className="submit-btn gradient-bg text-dark">
          {loading ? 'Đang phân tích...' : 'Gợi ý ngay!'}
        </button>
      </div>
      {/* <p className="api-info text-muted">Kết nối trực tiếp tới Flask Server.</p> */}
    </form>
  );
};

export default RecommenderForm;