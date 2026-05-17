const Header = ({ importMode, setImportMode }) => {
  return (
    <header className="header glass-panel">
      <div className="header-top">
        <div className="logo-section">
          <p className="project-sub gradient-text-accent">GRADUATION PROJECT</p>
          <h1 className="header-title text-light">Anime <span className="gradient-text-accent">AI Engine</span></h1>
        </div>

        {/* --- NÚT CÔNG TẮC (TOGGLE SWITCH) --- */}
        <div className="toggle-switch glass-input">
          <div 
            className={`toggle-slider ${importMode === 'manual' ? 'right' : 'left'}`}
          ></div>
          <button 
            className={`toggle-btn ${importMode === 'mal' ? 'active' : ''}`}
            onClick={() => setImportMode('mal')}
          >
            🌐 MyAnimeList Sync
          </button>
          <button 
            className={`toggle-btn ${importMode === 'manual' ? 'active' : ''}`}
            onClick={() => setImportMode('manual')}
          >
            ✍️ Manual Import
          </button>
        </div>
        {/* ---------------------------------- */}
      </div>
      
      <div className="header-bottom">
        <p className="header-desc text-muted">
          {importMode === 'mal' 
            ? "Nhập Username MyAnimeList để hệ thống tự động đồng bộ lịch sử xem phim và tính toán gợi ý." 
            : "Tự tìm kiếm phim, chấm điểm thủ công (1-10) để huấn luyện AI gợi ý theo sở thích cá nhân."}
        </p>
      </div>
    </header>
  );
};

export default Header;