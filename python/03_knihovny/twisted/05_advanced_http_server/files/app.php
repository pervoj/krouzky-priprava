<?php

header("HTTP/1.1 404 Not Found");
header("X-Test-Header: Test Header");

?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Simple App</title>
</head>
<body>
  <h1>Simple App</h1>
  <p>3 * 4 = <?= 3 * 4 ?></p>
</body>
</html>
