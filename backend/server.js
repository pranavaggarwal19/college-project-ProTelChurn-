const express = require("express");
const bodyParser = require("body-parser");
const predictionsRoute = require("C:\\Users\\user\\Desktop\\ProTelChurn\\backend\\routes\\prediction.js");
const offersRoute = require("C:\\Users\\user\\Desktop\\ProTelChurn\\backend\\routes\\prediction.js");

const app = express();

// Body parser middleware to parse incoming JSON data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Define routes for handling predictions and offer recommendations
app.use("/api/predictions", predictionsRoute);
app.use("/api/offers", offersRoute);

// Example root endpoint to verify server running
app.get("/", (req, res) => {
  res.send("Churn Prediction System Backend is running");
});

// Define the port for the server to listen on
const PORT = process.env.PORT || 5000;

// Start the server and listen on the defined port
app.listen(PORT, () => {
  console.log(`Server started on port 5000`);
});
