{% args req, wifi_nets %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <title>Select WiFi</title>
  <link href="style.css" rel="stylesheet">
</head>
<body style="margin:0;">
  <div id="overlay" class="overlay">
    <div id="loader" class="loader"></div>
  </div>

  <div class="center">
    <div style="display:none;" id="myDiv" class="animate-bottom">
      <h4>Select a WiFi network</h4>
      <form action="save_wifi_config" method="post" id="save_wifi_config_form">
        <select name="wifi_network" id="wifi_network" size="5">
          {% for ele in wifi_nets %}
            <option value="{{ele['bssid']}}">{{ele['ssid'].decode('ascii')}} - {{ele['quality']}}&#37;</option>
          {% endfor %}
        </select>
        <input type="text" name="ssid" id="ssid" placeholder="Custom Network Name">
        <input type="password" name="password" id="password" placeholder="Password" onkeydown="if(event.keyCode==13)document.getElementById('save').click()"/>
        <input type="submit" class="button" id="save" value="Save">
      </form>
      <form>
        <input type="button" onclick="window.location.href = '/';" value="Go Back"/>
      </form>
    </div>
  </div>

  <script>
    window.onload = function(e) {
      setTimeout(showPage, 1000);
      setTimeout(get_new_networks, 100);
      var myInterval = setInterval(get_new_networks, 10000);
    };
    /*
    window.onunload = function(e) {
      var xhttp = new XMLHttpRequest();
      // open(method, url, async)
      xhttp.open("POST", "unload_data", false);
      var data = 'name=wifi_select_loader';
      xhttp.send(data);
      // console.log('Data sent to unload_data');
      return undefined; // show NO warning for user
      // return true; // show warning for user, requires user confirmation
    };
    */
    function showPage() {
      document.getElementById("loader").style.display = "none";
      document.getElementById("myDiv").style.display = "block";
      //document.getElementById("rcorners3").style.display = "block";
      document.getElementById("overlay").style.display = "none";
    };
    document.getElementById("save_wifi_config_form").onsubmit = function(e) {
      window.onbeforeunload = null;
      return true;
    };
    function get_new_networks() {
      // console.log('Getting new networks');
      var xmlhttp = new XMLHttpRequest();
      var url = "scan_result";
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          var myArr = JSON.parse(this.responseText);
          console.log(myArr);
          update_wifi_nets_selection(myArr);
        }
      };
      xmlhttp.open("GET", url);
      xmlhttp.send();
    }
    function update_wifi_nets_selection(arr) {
      // console.log('Updating options list function');
      var oldSel = document.getElementById("wifi_network");
      // backup current selection
      var selected_index = oldSel.selectedIndex;
      // console.log('Add options to cleared element' + oldSel.options);
      for (var i = 0; i < arr.length; i++) {
        var opt = document.createElement('option');
        var new_option_text = arr[i].ssid + ' - ' + arr[i].quality + '%';
        // 'NET-WORK_A - 42%'
        opt.text = new_option_text;
        opt.value = arr[i].bssid;
        console.log('checking: ' + new_option_text + ', value: ' + opt.value);
        is_unique = true;
        for (var j = 0; j < oldSel.options.length; j++) {
          let old_text = oldSel.options[j].text;
          const old_text_array = old_text.split("-");
          // ['NET', 'WORK_A ', ' 42%']
          const old_ssid = old_text_array.slice(0, old_text_array.length - 1).join("-");
          // 'NET-WORK_A '
          const old_quality = old_text_array[old_text_array.length - 1];
          // ' 42%'
          // console.log('checking oldSel thing' + oldSel.options[j]);
          if (old_ssid.trim() == arr[i].ssid) {
            // this option already exists in oldSel
            // console.log(arr[i].ssid + ' exists already, updating text');
            // update text of option
            oldSel.options[j].text = new_option_text;
            is_unique = false;
            break;
          }
        }
        if (is_unique) {
          // console.log(opt.text + ' is unique/new');
          oldSel.add(opt, null);
        }
      }
      // re apply selected index
      oldSel.selectedIndex = selected_index;
    }
  </script>
</body>
</html>
