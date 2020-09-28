function colorBgCheckbox(){
  chart.destroy();
  console.log('Bg color changed.');
  bg_color_html = document.getElementById('bgColors').value;
  if (type == 'doughnut' || type == 'polarArea' || type == 'pie') { bg_color = ['#ff3300', '#0033cc', '#ffff66', '#00ff00', '#660066', '#ff00ff', '#800000', '#00ffff', '#996633', '#009999', '#cc6699', '#cccc00']; }
  else { bg_color = bg_color_html; }
  make_chart();
}

function colorBorderCheckbox() {
  chart.destroy();
  bord_color = document.getElementById('borderColors').value;
  make_chart();
}

function typeCheckbox() {
  chart.destroy();
  type = document.getElementById('type').value;
  if ((type == 'doughnut' || type == 'polarArea' || type == 'pie')) {bg_color = ['#ff3300', '#0033cc', '#ffff66', '#00ff00', '#660066', '#ff00ff', '#800000', '#00ffff', '#996633', '#009999', '#cc6699', '#cccc00', '#ff1a1a', '#b32d00', '#1affff']; }
  else { bg_color = '#b3b3ff'; }
  make_chart();
}
