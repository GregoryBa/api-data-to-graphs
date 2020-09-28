var data = [];
var chart_data_values = [];
var bg_color = '#b3b3ff';
var bord_color = '#8080ff';
var type = 'bar';
var chart;

function get_data_wins() {
  fetch('/request_value_per_customer')
      .then(function (response) {
          return response.json();
      })
      .then(function (json) {
        data = Object.keys(json).map(function (key){ return [String(key)]; });
        chart_data_values = Object.keys(json).map(function (key){ return [json[key]]; });
        make_chart();
      })
}

function make_chart() {
  var ctx = document.getElementById('chart_deals_won').getContext('2d');

  chart = new Chart(ctx, {
      type: type,
      data: {
          labels: data,
          datasets: [{
              label: 'Value',
              backgroundColor: bg_color,
              borderColor: bord_color,
              data: chart_data_values
          }]
      },
      options: {}
  });
}

function showData() {
  var div_raw_data = document.getElementById('raw-data-div');
  div_raw_data.innerHTML = '';
  for (var i = 0; i < data.length; i++) {
    div_raw_data.innerHTML += data[i] + " : ";
    div_raw_data.innerHTML += chart_data_values[i] + '<br>';
  }
}

get_data_wins();
