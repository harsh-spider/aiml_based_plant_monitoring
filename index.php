<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plant Monitoring</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
   body {
    z-index: 0;
    position: relative;
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    
 
    
}

body::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url("https://images.pexels.com/photos/55766/pexels-photo-55766.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1") no-repeat center center;
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    opacity: 0.8; /* Adjust the opacity here */
    filter: brightness(0.5); /* Adjust the brightness here */
    z-index: -1;  /* Ensure the pseudo-element is behind the content */
}

        .custom-paragraph {
            margin: 0 auto;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 20px;
            max-width: 100%;
          
               
             
        }
        .custom-paragraph p {
            color: #333;
            font-size: 40px;
            font-weight: bold;
            /* background-color: #f0f0f0; */
            padding: 15px;
            border-radius: 5px;
            font-family: Roboto Slab; 
            margin-bottom: 20px;
        }
        .table-container {
            margin: 0 auto;
            max-width: 800px;
            margin-top: 20px;
        }
        .table-container td {
            color: #000;
            
            font-size: 20px;
            font-weight:bold;
            
        }
        
        /* @media (min-width: 351px) and (max-width: 768px) {
            .custom-paragraph p {
                background-color: #28a745;
                text-align: center;
                width: 100%;
            }
        }
        @media (min-width: 769px) {
            .custom-paragraph p {
                background-color: #007bff;
                text-align: center;
                width: 100%;
            }
        } */
        .btn-primary:hover {
            background-color: #007bff;
            border-color: #007bff;
        }
        .btn-primary:hover:focus {
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.5);
        }
        .table-container th {
            color: #fff;
            background-color: #c1121f;
        }
        .fw-bold {
            color: red;
            margin-left: 20px;
            font-size: 20px;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="row">
        <div class="col">
            <div class="custom-paragraph">
                <p>AIML Based Plant Monitoring</p>
            </div>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col-md-6 text-center mt-3">
            <a href="./gui.php" class="btn btn-primary">Open</a>
            <span class="fw-bold text-danger bg-dark">For GUI</span>
            <div class="mt-3"></div>
            <a href="http://127.0.0.1:5000/" class="btn btn-success ml-4" target="_blank">Prediction</a>
            <span class="fw-bold text-light bg-dark">For prediction</span>
        </div>
    </div>
    <div class="table-container">
        <?php
        $dbname = 'devil';
        $dbuser = 'root';
        $dbpass = '';
        $dbhost = 'localhost';

        $connect = new mysqli($dbhost, $dbuser, $dbpass, $dbname);

        if ($connect->connect_error) {
            die("Connection failed: " . $connect->connect_error);
        }

        

        if (isset($_GET["temperature"]) && isset($_GET["humidity"]) && isset($_GET["soil_moisture"]) && isset($_GET["motion_status"]) && isset($_GET["rain_status"])) {
            $temperature = $connect->real_escape_string($_GET["temperature"]);
            $humidity = $connect->real_escape_string($_GET["humidity"]);
            $soil_moisture = $connect->real_escape_string($_GET["soil_moisture"]);
            $motion_status = $connect->real_escape_string($_GET["motion_status"]);
            $rain_status = $connect->real_escape_string($_GET["rain_status"]);

            $stmt = $connect->prepare("INSERT INTO espdata (temperature, humidity, soil_moisture, motion_status, rain_status) VALUES (?, ?, ?, ?, ?)");
            $stmt->bind_param("sssss", $temperature, $humidity, $soil_moisture, $motion_status, $rain_status);

            if ($stmt->execute()) {
                echo "Insertion Success!<br>";
            } else {
                echo "Error: " . $stmt->error;
            }

            $stmt->close();
        }

        $sql = "SELECT humidity, temperature, soil_moisture, motion_status, rain_status, reading_time FROM ESPData ORDER BY id DESC LIMIT 100";

        echo '<table cellspacing="5" cellpadding="5">
              <tr>
                <td></td>
                <td></td>
                <th>Humidity</th>
                <td></td>
                <td></td>
                <th>Temperature</th>
                <td></td>
                <td></td>
                <th>Soil_Moisture</th>
                <td></td>
                <td></td>
                <th>Motion_Status</th>
                <td></td>
                <td></td>
                <th>Rain_Status</th>
                <td></td>
                <td></td>
                <th>Timestamp</th>
              </tr>';

        if ($result = $connect->query($sql)) {
            while ($row = $result->fetch_assoc()) {
                $row_humidity = $row["humidity"];
                $row_temperature = $row["temperature"];
                $row_soil_moisture = $row["soil_moisture"];
                $row_motion_status = ($row["motion_status"] == "1") ? "Alert! Motion Detected" : "No Motion";
                $row_rain_status = ($row["rain_status"] == "1") ? "Alert! Raining" : "No Rain";
                $row_reading_time = $row["reading_time"];

                echo '<tr>
                        <td></td>
                        <td></td>
                        <td>' . $row_humidity . '</td>
                        <td></td>
                        <td></td>
                        <td>' . $row_temperature . '</td>
                        <td></td>
                        <td></td>
                        <td>' . $row_soil_moisture . '</td>
                        <td></td>
                        <td></td>
                        <td>' . $row_motion_status . '</td>
                        <td></td>
                        <td></td>
                        <td>' . $row_rain_status . '</td>
                        <td></td>
                        <td></td>
                        <td>' . $row_reading_time . '</td>
                        <td></td>
                        <td></td>
                      </tr>';
            }
            $result->free();
        }
        $connect->close();
        ?>
        </table>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
