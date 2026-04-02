const StatusSection = ({ error, userInfo, loading }) => {
  return (
    <section className="status-messages">
      {loading && (
        <div className="loader glass-panel gradient-text-accent">
          <span className="spinner"></span> Đang tính toán ma trận trọng số...
        </div>
      )}
      
      {error && (
        <div className="error-message glass-panel-red text-red">
          ⚠️ {error}
        </div>
      )}
      
      {userInfo && (
        <div className="success-message glass-panel-green text-green">
          Đã đồng bộ <strong className="gradient-text-accent">{userInfo.totalWatched}</strong> bộ phim từ tài khoản <strong className="gradient-text-accent">{userInfo.name}</strong>. Kết quả đề xuất:
        </div>
      )}
    </section>
  );
};

export default StatusSection;