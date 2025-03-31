import React, { useState, useEffect } from "react";
import axios from "axios";
import { AppBar, Tabs, Tab, Box, Typography } from "@mui/material";
import PredictionsTable from "./PredictionsTable";
import PlotTab from "./PlotTab";

const App = () => {
  const [tabIndex, setTabIndex] = useState(0);

  return (
    <Box sx={{ width: "100%", textAlign: "center", mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        ML Cricket Predictor
      </Typography>

      <AppBar position="static">
        <Tabs value={tabIndex} onChange={(e, newIndex) => setTabIndex(newIndex)}>
          <Tab label="Predictions Table" />
          <Tab label="Prediction Plot" />
        </Tabs>
      </AppBar>

      <Box sx={{ mt: 3 }}>
        {tabIndex === 0 && <PredictionsTable />}
        {tabIndex === 1 && <PlotTab />}
      </Box>
    </Box>
  );
};

export default App;
