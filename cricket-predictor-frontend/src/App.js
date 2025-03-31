import React, { useState, useEffect } from "react";
import axios from "axios";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";

const App = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/predictions")
      .then(res => {
        setData(res.data);
        console.log("Data fetched successfully:", res.data);
      })
      .catch(err => console.error("Error fetching data:", err));
  }, []);

  return (
    <TableContainer component={Paper} sx={{ maxWidth: 800, margin: "auto", mt: 4 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell><strong>Team</strong></TableCell>
            <TableCell><strong>Opponent</strong></TableCell>
            <TableCell><strong>Over</strong></TableCell>
            <TableCell><strong>Actual Final Score</strong></TableCell>
            <TableCell><strong>Predicted Final Score</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((item, index) => (
            <TableRow key={index}>
              <TableCell>{item.Team}</TableCell>
              <TableCell>{item.Opponent}</TableCell>
              <TableCell>{item.Over}</TableCell>
              <TableCell>{item["Actual Final Score"]}</TableCell>
              <TableCell>{item["Predicted Final Score"].toFixed(2)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default App;
