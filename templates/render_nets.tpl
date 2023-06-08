{% args content %}
        {% if len(content) %}
          {% for net in content %}
            <input class="list-group-item-check" type="radio" name="bssid" id="{{net['bssid']}}" value="{{net['bssid']}}" 
              onclick="remember_selected_element(this)" {{net['state']}}>
            <label class="list-group-item py-3" for="{{net['bssid']}}">
              {{net['ssid']}}
              <span class="d-block small opacity-50">
                Signal quality {{net['quality']}}&#37;, BSSID {{net['bssid']}}
              </span>
            </label>
          {% endfor %}
        {% else %}
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        {% endif %}