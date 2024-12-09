const express = require("express");
const mysql = require("mysql2");
const moment = require("moment-timezone");

const app = express();
const port = 5000;

// Middleware to parse JSON body
app.use(express.json());

// MySQL Database Configuration
const dbConfig = {
  'host': 'MYSQL5048.site4now.net',
             'user': 'a50d85_payroll',
             'password': 'p3r3nnial',
             'database': 'db_a50d85_payroll' 
};

// Function to insert webhook payload into the database
async function insertWebhookPayload(payload) {
  // Get current IST time
  const currentTime = moment().tz("Asia/Kolkata").format("YYYY-MM-DD HH:mm:ss");

  // Extract common values from the payload
  const orderId = payload.order_id;
  const status = payload.status;
  const orderDetails = payload.order_details;
  const eventTs = orderDetails?.event_ts || null;

  // Extract fields based on type
  let lat = null,
    long = null,
    driverName = null,
    vehicleNumber = null,
    mobile = null;
  let estimatedTripFare = null,
    actualTripFare = null;

  if (orderDetails?.partner_location) {
    lat = orderDetails.partner_location.lat || null;
    long = orderDetails.partner_location.long || null;
  }

  if (orderDetails?.driver_details) {
    driverName = orderDetails.driver_details.driver_name || null;
    vehicleNumber = orderDetails.driver_details.vehicle_number || null;
    mobile = orderDetails.driver_details.mobile || null;
  }

  if (orderDetails?.estimated_trip_fare) {
    estimatedTripFare = orderDetails.estimated_trip_fare;
  }

  if (orderDetails?.actual_trip_fare) {
    actualTripFare = orderDetails.actual_trip_fare;
  }

  // Prepare SQL queries
  const queryOrderUpdate = `
    INSERT INTO Porter_order_updates 
    (order_id, status, event_ts, lat, \`long\`, driver_name, vehicle_number, mobile, estimated_trip_fare, actual_trip_fare, reopen_event_ts)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
  `;

  const queryOrderLog = `
    INSERT INTO Porter_OrderLog (order_id, order_type, created_on)
    VALUES (?, ?, ?);
  `;

  // Values for queries
  const orderUpdateValues = [
    orderId,
    status,
    eventTs,
    lat,
    long,
    driverName,
    vehicleNumber,
    mobile,
    estimatedTripFare,
    actualTripFare,
    eventTs,
  ];

  const orderLogValues = [orderId, status, currentTime];

  // Create a connection pool
  const pool = mysql.createPool(dbConfig).promise();

  try {
    // Insert into `Porter_order_updates`
    await pool.query(queryOrderUpdate, orderUpdateValues);

    // Insert into `Porter_OrderLog`
    await pool.query(queryOrderLog, orderLogValues);

    console.log("Webhook payload inserted successfully.");
  } catch (error) {
    console.error("Error inserting webhook payload:", error);
    throw error;
  } finally {
    pool.end();
  }
}

// API Endpoint
app.post("/porter/order_update", async (req, res) => {
  try {
    const webhookData = req.body;

    // Insert payload into the database
    await insertWebhookPayload(webhookData);

    // Respond with success message
    res.status(200).send("Webhook received and saved to database");
  } catch (error) {
    console.error("Error:", error);
    res.status(500).send("Failed to process webhook");
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://127.0.0.1:${port}`);
});
