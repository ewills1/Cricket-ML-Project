import React from "react";

const PlotTab = () => {
  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h3>Predictions vs. Actual Scores</h3>
      <img src="http://127.0.0.1:5000/api/plot" alt="Prediction Plot" width="80%" />
    </div>
  );
};

export default PlotTab;
