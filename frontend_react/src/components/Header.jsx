const Header = () => {
  return (
    <header className="header glass-panel">
      <div className="header-top">
        <p className="project-sub gradient-text-accent">AI PROJECT</p>
        {/* <svg className="header-icon" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="iconGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#06b6d4" />
            </linearGradient>
          </defs>
          <rect fill="url(#iconGrad)" rx="40" height="384" width="384" y="64" x="64"/>
          <circle fill="#0a0e17" r="28" cy="192" cx="192"/>
          <circle fill="#0a0e17" r="28" cy="192" cx="320"/>
          <circle fill="#0a0e17" r="28" cy="256" cx="256"/>
          <circle fill="#0a0e17" r="28" cy="320" cx="192"/>
          <circle fill="#0a0e17" r="28" cy="320" cx="320"/>
        </svg> */}
        <h1 className="header-title text-light">Anime <span className="gradient-text-accent">Recommender System</span></h1>
      </div>
      <div className="header-bottom">
        <p className="header-desc text-muted">Hệ thống gợi ý Anime Hybrid (Collaborative + Content-based)</p>
      </div>
    </header>
  );
};

export default Header;