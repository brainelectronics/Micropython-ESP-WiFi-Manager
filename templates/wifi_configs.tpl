{% args req, wifi_nets %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <title>Remove WiFi Network</title>
  <link href="style.css" rel="stylesheet">
</head>
<body style="margin:0;">
  <div id="overlay" class="overlay">
    <div id="loader" class="loader"></div>
  </div>

  <div class="center" style="width:400px;">
    <div style="display:none;" id="myDiv" class="animate-bottom">
      <h4>Remove a configured WiFi network</h4>
      <table name="wifi_network" id="wifi_network">
        <tr>
          <th>Network</th>
          <th></th>
        </tr>
        {% for ele in wifi_nets %}
          <tr>
            <td>{{ele}}</td>
            <td>
              <button class="btnDelete">Remove</button>
            </td>
          </tr>
        {% endfor %}
      </table>
    </div>
  </div>
  <script>
    window.onload = function(e) {
      setTimeout(showPage, 1000);
    };
    function showPage() {
      document.getElementById("loader").style.display = "none";
      document.getElementById("myDiv").style.display = "block";
      //document.getElementById("rcorners3").style.display = "block";
      document.getElementById("overlay").style.display = "none";
    };
    document.getElementById("wifi_network").addEventListener("click", e => {
      console.log('Button hit');
      var xhttp = new XMLHttpRequest();
      var url = 'remove_wifi_config';
      xhttp.open("POST", url, true);
      xhttp.setRequestHeader("Content-Type", "application/json;charset=utf-8")
      xhttp.send(JSON.stringify({"name": "all", "index": 0}));
    })

    /*
    document.getElementById("wifi_network").addEventListener("click", e => {
      console.log('Button hit');

      var closest_match = e.target.closest('tr');
      // console.log('closest_match: ' + closest_match);
      // console.log('closest_match rowIndex: ' + closest_match.rowIndex);
      // console.log('Available cells: ' + closest_match.cells);
      // console.log('Available cells length: ' + closest_match.cells.length);

      network_to_remove = closest_match.cells[0].innerText;
      row_index = closest_match.rowIndex;
      console.log('Remove row with name: ' + network_to_remove + ' at index ' + row_index);
      if (row_index) {
        var confirm_text = network_to_remove + ' will be deleted from configured networks';
        if (confirm(confirm_text)) {
          // OK clicked
          report_delete_network(network_to_remove, row_index);
          // remove this row from the table
          closest_match.remove();
        }
        // else {
        //   // cancel clicked
        // }
      }
    })

    function report_delete_network(name, index) {
      console.log('Report removal of ' + name);

      var xhttp = new XMLHttpRequest();
      var url = 'remove_wifi_config';
      var params = 'name=' + name + '&index=' + index;

      console.log('POST data: ' + params)
      xhttp.open("POST", url, true);
      xhttp.send(params);
    };
    */
  </script>
</body>
</html>
