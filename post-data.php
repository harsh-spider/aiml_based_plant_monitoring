
<html>
<body>

<?php

$dbname = 'devil';
$dbuser = 'root';  
$dbpass = ''; 
$dbhost = 'localhost'; 

$connect = @mysqli_connect($dbhost,$dbuser,$dbpass,$dbname);

if(!$connect){
	echo "Error: " . mysqli_connect_error();
	exit();
}

echo "Connection Success!<br><br>";

$temperature = $_GET["temperature"];
$humidity = $_GET["humidity"]; 

$humidity = $_GET["humidity"];
$temperature = $_GET["temperature"];
$soil_moisture = $_GET["soil_moisture"];
$motion_status = $_GET["motion_status"];
$rain_status = $_GET["rain_status"];



$query = "INSERT INTO espdata (temperature, humidity,soil_moisture,motion_status,rain_status) VALUES ('$temperature', '$humidity','$soil_moisture','$motion_status','$rain_status')";
$result = mysqli_query($connect,$query);

echo "Insertion Success!<br>";


function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

?>
</body>
</html>