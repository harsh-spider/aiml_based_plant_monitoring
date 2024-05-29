<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" rel="stylesheet">
    <script src="https://kit.fontawesome.com/2f19bcb8c6.js" crossorigin="anonymous"></script>
    <style>
      html {
      font-family: Arial;
      display: inline-block;
      margin: 0px auto;
      text-align: center;
      height: 100%;
    }
    .background {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-image: url('./images/1.png'); /* Replace 'background.jpg' with the path to your background image */
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      opacity: 0.5; /* Adjust the opacity as needed */
      z-index: -1; /* Ensure the background is behind the content */
    }
    .content {
      position: relative;
      z-index: 1;
    }
      h1 { font-size: 2.0rem; }
      p { font-size: 2.0rem; }
      .units { font-size: 1.2rem; }
      .dht-labels{
        font-size: 1.5rem;
        vertical-align:middle;
        padding-bottom: 15px;
      }
    </style>
  </head>
  <body>
      <div class="background"></div>
  <div class="content">
    <h1>AIML Based Plant Monitoring</h1>

<?php
$servername = "localhost";
$dbname = "devil";
$username = "root";
$password = "";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch data from database
$sql = "SELECT humidity, temperature, soil_moisture, motion_status, rain_status, reading_time FROM ESPData ORDER BY id DESC";
$result = $conn->query($sql);



// Check if query was successful
if ($result) {
    // Fetch data and assign to variables
    $row = $result->fetch_assoc();
    $row_humidity = $row["humidity"];
    $row_temperature = $row["temperature"];
    $row_soil_moisture = $row["soil_moisture"];
    $row_motion_status = ($row["motion_status"] == "1") ? "Alert! Motion Detected" : "No Motion"; 
    $row_rain_status =($row["rain_status"] == "1") ? "Alert! Raining" : "No Rain"; 
    
    
    
    // Output data
    echo "
        <p>
            <i class='fa fa-thermometer-half' style='font-size:3.0rem;color:#62a1d3;'></i> 
            <span class='dht-labels'>Temperature : </span> 
            <span id='TemperatureValue'>$row_temperature</span>
            <sup class='units'>&deg;C</sup>
        </p>
        <p>
            <i class='fa fa-tint' style='font-size:3.0rem;color:#75e095;'></i>
            <span class='dht-labels'>Humidity : </span>
            <span id='HumidityValue'>$row_humidity</span>
            <sup class='units'>%</sup>
        </p>
        <p>
            <i class='fa-solid fa-cloud-rain' style='font-size:3.0rem;color:#2CA58D5;'></i>
            <span class='dht-labels'>Rain Status : </span>
            <span id='RainStatusValue'>$row_rain_status</span>
        </p>
        <p>
            <i class='fa-solid fa-hat-cowboy' style='font-size:3.0rem;color:#bc6c25;'></i>
            <span class='dht-labels'>Motion Detector : </span>
            <span id='MotionStatusValue'>$row_motion_status</span>
        </p>
        <p>
            <i class='fa-solid fa-droplet' style='font-size:3.0rem;color:#03045e;'></i>
            <span class='dht-labels'>Soil Moistures : </span>
            <span id='SoilMoistureValue'>$row_soil_moisture</span>
        </p>
    ";

    // Free result set
    $result->free();
} else {
    echo "Error: " . $conn->error;
}

// Close connection
$conn->close();
?>
  </div>
  </body>
</html>
