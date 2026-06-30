export default function Results({ result }) {
  if (!result) return null;

  return (
    <div className="results">
      <h2 style={{ marginBottom: "20px" }}>Results</h2>

      <div className="stats">
        <div className="stat-box">Number of Craters: {result.crater_count}</div>
        <div className="stat-box">Largest Crater: {result.largest_crater_diameter}</div>
        <div className="stat-box">Average Crater Size: {result.average_crater_diameter}</div>
        <div className="stat-box">Smallest Crater: {result.smallest_crater_diameter}</div>
      </div>

      <h3 style={{ marginBottom: "20px", marginTop: "20px" }}>Annotated Image</h3>
      <img src={`data:image/jpeg;base64,${result.annotated_image}`} />

      <h3 style={{ marginBottom: "20px", marginTop: "20px" }}>Histogram</h3>
      <img src={`data:image/png;base64,${result.histogram}`} />
    </div>
  );
}