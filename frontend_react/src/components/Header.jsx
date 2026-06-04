const Header = ({ importMode, setImportMode, aiEngine, setAiEngine }) => {
  return (
    <header className="header glass-panel">
      {/* Sử dụng Flexbox để chia 2 cột: 
        - justifyContent: 'space-between' đẩy 2 thành phần ra 2 mép
        - alignItems: 'flex-start' giúp chúng bám lên lề trên cùng
      */}
      <div className="header-top" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '20px' }}>
        
        {/* --- CỘT TRÁI: TIÊU ĐỀ --- */}
        <div className="logo-section">
          <h1 className="header-title text-light" style={{ margin: 0 }}> 
            <span className="gradient-text-accent">Anime Recommender System</span>
          </h1>
        </div>

        {/* --- CỘT PHẢI: KHU VỰC NÚT GẠT (XẾP DỌC) --- */}
        <div className="controls-section" style={{ display: 'flex', flexDirection: 'column', gap: '12px', alignItems: 'flex-end' }}>
          
          {/* CÔNG TẮC 1: CHẾ ĐỘ NHẬP */}
          <div className="toggle-switch glass-input" style={{ width: '340px' }}>
            <div 
              className={`toggle-slider ${importMode === 'manual' ? 'right' : 'left'}`}
            ></div>
            <button 
              className={`toggle-btn ${importMode === 'mal' ? 'active' : ''}`}
              onClick={() => setImportMode('mal')}
            >
              MyAnimeList Sync
            </button>
            <button 
              className={`toggle-btn ${importMode === 'manual' ? 'active' : ''}`}
              onClick={() => setImportMode('manual')}
            >
              Manual Import
            </button>
          </div>

          {/* CÔNG TẮC 2: CHỌN LÕI AI */}
          <div className="toggle-switch glass-input" style={{ width: '340px' }}>
            <div 
              className={`toggle-slider ${aiEngine === 'deep_learning' ? 'right' : 'left'}`}
            ></div>
            <button 
              className={`toggle-btn ${aiEngine === 'classic' ? 'active' : ''}`}
              onClick={() => setAiEngine('classic')}
            >
              TF-IDF 
            </button>
            <button 
              className={`toggle-btn ${aiEngine === 'deep_learning' ? 'active' : ''}`}
              onClick={() => setAiEngine('deep_learning')}
            >
              BERT (Deep Learning)
            </button>
          </div>

        </div>
        {/* ----------------------------------------- */}
      </div>
      
      {/* --- KHU VỰC MÔ TẢ PHÍA DƯỚI --- */}
      <div className="header-bottom" style={{ marginTop: '20px', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '16px' }}>
        <p className="header-desc text-muted">
          {importMode === 'mal' 
            ? "Nhập Username MyAnimeList để hệ thống tự động đồng bộ lịch sử xem phim và tính toán gợi ý." 
            : "Tự tìm kiếm phim, chấm điểm thủ công (1-10) để huấn luyện AI gợi ý theo sở thích cá nhân."}
          <br/>
          <span style={{ fontSize: '0.95rem', color: '#10b981', marginTop: '8px', display: 'inline-block' }}>
            Trạng thái AI: Đang sử dụng thuật toán <strong>{aiEngine === 'deep_learning' ? 'Học sâu (Sentence-BERT + SVD)' : 'Cổ điển (TF-IDF + SVD)'}</strong>.
          </span>
        </p>
      </div>
    </header>
  );
};

export default Header;