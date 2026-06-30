import { useState } from "react";
import UploadBox from "./components/UploadBox";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app">
      <div className="layout">

        {/* LEFT MAIN AREA */}
        <div className="workspace">

          <h1>Crater Detection System</h1>

          <UploadBox setResult={setResult} />

          {/* CENTER RESULTS (IMAGES ONLY) */}
          {result && (
            <div className="results-center">

              <div className="image-grid">

                <div className="image-card">
                  <h3>Annotated Image</h3>
                  <img
                    src={`data:image/jpeg;base64,${result.annotated_image}`}
                  />
                </div>

                <div className="image-card">
                  <h3>Histogram</h3>
                  <img
                    src={`data:image/png;base64,${result.histogram}`}
                  />
                </div>

              </div>

            </div>
          )}

        </div>

        {/* RIGHT INSPECTOR (ONLY STATS) */}
        <div className="inspector">

          <h3>Analysis Panel</h3>

          {!result ? (
            <p className="muted">Upload image to begin analysis</p>
          ) : (
            <>
              <div className="stat-box">Crater Count: {result.crater_count}</div>
              <div className="stat-box">Largest: {result.largest_crater_diameter}</div>
              <div className="stat-box">Average: {result.average_crater_diameter}</div>
              <div className="stat-box">Smallest: {result.smallest_crater_diameter}</div>
            </>
          )}

        </div>

      </div>
    </div>
  );
}

export default App;