const AnimeCard = ({ anime, index }) => {
  return (
    <div className="anime-card glass-panel">
      <div className="rank-badge gradient-bg text-dark">#{index + 1}</div>
      <div className="anime-poster-placeholder">
        <div className="poster-gradient" />
      </div>
      <div className="anime-details">
        <h3 className="anime-title text-light">{anime.name}</h3>
        <p className="anime-genre text-muted">Thể loại: {anime.genre}</p>
        <div className="score-badge gradient-bg-subtle text-light">
          Độ phù hợp: {(anime.hybrid_score).toFixed(2)}
        </div>
      </div>
    </div>
  );
};

export default AnimeCard;