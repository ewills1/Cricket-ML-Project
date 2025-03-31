import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      // Send the file to the Flask API for prediction
      const response = await fetch('http://127.0.0.1:5000/predict-file', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setLoading(false);

      // If prediction exists, display it, otherwise show error
      if (data.predicted_final_score) {
        setPrediction(data.predicted_final_score);
      } else {
        alert("Error: " + data.error);
      }
    } catch (error) {
      setLoading(false);
      alert("An error occurred while sending the request: " + error);
    }
  };

  return (
    <div className="App">
      <h1>Cricket Score Predictor</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Submit File"}
        </button>
      </form>
      
      {prediction !== null && (
        <div>
          <h2>Predicted Final Score: {prediction}</h2>
        </div>
      )}
    </div>
  );
}

export default App;
