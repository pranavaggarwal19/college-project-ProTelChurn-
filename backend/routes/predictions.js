const express = require("express");
const router = express.Router();
const { spawn } = require("child_process");

// Route for handling churn predictions
router.post("/predictChurn", (req, res) => {
  // Receive user input data from req.body (assuming it contains necessary data for prediction)
  const userData = req.body;

  // Execute Python script (churn_model.py) using child_process.spawn
  const pythonProcess = spawn("python", [
    "C:\\Users\\user\\Desktop\\ProTelChurn\\backend\\models\\churn_model.py",
    JSON.stringify(userData),
  ]);

  // Collect data from the Python script
  let result = "";
  pythonProcess.stdout.on("data", (data) => {
    result += data.toString();
  });

  // Handle completion of Python script execution
  pythonProcess.on("close", (code) => {
    // Parse the result (assuming it's JSON data)
    const predictionResult = JSON.parse(result);

    // Send predictions as response to the frontend
    res.json(predictionResult);
  });
});

module.exports = router;
