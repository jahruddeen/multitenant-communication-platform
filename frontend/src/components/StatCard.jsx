
const StatCard = ({ title, value, icon: Icon, color }) => {
  return (
    <div className="stat-card">
      <div>
        <p>{title}</p>
        <h2>{value ?? 0}</h2>
      </div>

      {Icon && (
        <div className="stat-icon" style={{ color }}>
          <Icon size={28} />
        </div>
      )}
    </div>
  );
};

export default StatCard;
