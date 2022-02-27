{% args req, content %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <meta name="description" content="WiFi Manager Index page">
  <meta name="author" content="Jonas Scharpf aka brainelectronics">
  <title>Setup</title>
  <link href="bootstrap.min.css" rel="stylesheet">
  <!-- <link rel="icon" href="/docs/4.0/assets/img/favicons/favicon.ico"> -->
</head>
<body>
  <div class="d-flex flex-column min-vh-100 justify-content-center align-items-center">
    <div class="list-group text-center">
      <a href="/" class="list-group-item list-group-item-action active">This page</a>
      {{content}}
    </div>
  </div>
</body>
</html>
