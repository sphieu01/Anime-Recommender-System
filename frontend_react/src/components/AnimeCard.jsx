const AnimeCard = ({ anime, index }) => {
  const MAL_url = `https://myanimelist.net/anime/${anime.anime_id}/`;
  return (
    <a href ={MAL_url} target="_blank" rel="noopener noreferrer" className="anime-card glass-panel" >

        <div className="rank-badge gradient-bg text-dark">#{index + 1}</div>
        
        <div className="anime-poster-wrapper">
          <img 
            src={anime.image_url} 
            alt={`Poster of ${anime.name}`} 
            className="anime-poster"
            loading="lazy"
          />
        </div>

        <div className="anime-details">
          <h3 className="anime-title text-light">{anime.name}</h3>
          <p className="anime-genre text-muted">Thể loại: {anime.genre}</p>
          <div className="score-badge gradient-bg-subtle text-light">
            Độ phù hợp: {(anime.hybrid_score).toFixed(2)}
          </div>
        </div>

    </a>
  );
};

export default AnimeCard;