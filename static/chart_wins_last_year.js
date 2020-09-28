var data;
var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
var bg_color = '#b3b3ff';
var bord_color = '#8080ff';
var type = 'bar';
var chart;

function get_data_wins() {
  fetch('/request_wins')
      .then(function (response) {
          return response.json();
      })
      .then(function (json) {
        data = json;
        make_chart();
      })
}

function make_chart() {
  var ctx = document.getElementById('chart_deals_won').getContext('2d');
  chart = new Chart(ctx, {
      type: type,
      data: {
          labels: months,
          datasets: [{
              label: 'Wins',
              backgroundColor: bg_color,
              borderColor: bord_color,
              data: data
          }]
      },
      options: {}
  });
}

function showData() {
  var div_raw_data = document.getElementById('raw-data-div');
  div_raw_data.innerHTML = '';
  for (var i = 0; i < data.length; i++) {
    div_raw_data.innerHTML += months[i] + " : ";
    div_raw_data.innerHTML += data[i] + '<br>';
  }
}

get_data_wins();
