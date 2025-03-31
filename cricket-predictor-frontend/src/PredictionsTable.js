import React, { useState, useEffect } from "react";
import axios from "axios";
import { Table, TableHead, TableBody, TableRow, TableCell, Paper, TableContainer } from "@mui/material";

const PredictionsTable = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/predictions")
      .then(response => setData(response.data))
      .catch(error => console.error("Error fetching predictions:", error));
  }, []);

  return (
    <TableContainer component={Paper} sx={{ maxWidth: 800, margin: "auto" }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell><b>Team</b></TableCell>
            <TableCell><b>Opponent</b></TableCell>
            <TableCell><b>Actual Score</b></TableCell>
            <TableCell><b>Predicted Score</b></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.Team}</TableCell>
              <TableCell>{row.Opponent}</TableCell>
              <TableCell>{row["Actual Final Score"]}</TableCell>
              <TableCell>{row["Predicted Final Score"].toFixed(2)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default PredictionsTable;
