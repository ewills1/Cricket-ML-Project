import React, { useState, useEffect } from "react";
import axios from "axios";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Paper } from "@mui/material";

const PredictionsTable = () => {
  const [data, setData] = useState([]);
  const [searchTeam, setSearchTeam] = useState("");  // Filter for Team Name
  const [searchOver, setSearchOver] = useState("");  // Filter for Over Numbe

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/predictions")
      .then(response => setData(response.data))
      .catch(error => console.error("Error fetching predictions:", error));
  }, []);

  // Filter Data Based on Search Inputs
  const filteredData = data.filter(row =>
    row.Team.toLowerCase().includes(searchTeam.toLowerCase()) &&
    (searchOver === "" || row.Over === Number(searchOver)) // Convert Over to number
  );

  return (
    <div style={{ padding: "20px" }}>

      {/*Search Fields */}
      <TextField
        label="Search by Team"
        variant="outlined"
        value={searchTeam}
        onChange={(e) => setSearchTeam(e.target.value)}
        style={{ marginBottom: "10px", marginRight: "10px" }}
      />
      <TextField
        label="Search by Over"
        variant="outlined"
        type="number"
        value={searchOver}
        onChange={(e) => setSearchOver(e.target.value)}
        style={{ marginBottom: "10px" }}
      />

      {/* Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Team</TableCell>
              <TableCell>Opponent</TableCell>
              <TableCell>Over</TableCell>
              <TableCell>Actual Final Score</TableCell>
              <TableCell>Predicted Final Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredData.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row.Team}</TableCell>
                <TableCell>{row.Opponent}</TableCell>
                <TableCell>{row.Over}</TableCell>
                <TableCell>{row["Actual Final Score"]}</TableCell>
                <TableCell>{row["Predicted Final Score"].toFixed(2)}</TableCell> 
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default PredictionsTable;
