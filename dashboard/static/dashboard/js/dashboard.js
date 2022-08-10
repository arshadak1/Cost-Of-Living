

const chart_doughnut = document.getElementById('doughnutChart');
const chart_line = document.getElementById('savingsMonthChart');

const datas = Object.entries(JSON.parse(document.getElementById('data_list').getAttribute('data-list')));
const bar_datas = Object.entries(JSON.parse(document.getElementById('data_bar_list').getAttribute('data-list')));


const TODAY = new Date()
var doughnut_django_data = []
var bar_django_data = Array(12).fill(0);

var doughnut_label = []
var total_savings = 0

for (var data of datas) {

  if (data[1][1] == 'Income') {
    total_savings += Number(data[1][0])
  }
  else {
    total_savings -= Number(data[1][0])
    doughnut_django_data.push(data[1][0])
    doughnut_label.push(data[0])
  }
}

for (var bar_data of bar_datas){
  bar_django_data[Number(bar_data[0])] = Number(bar_data[1])
}



doughnut_label.push('Balance')
doughnut_django_data.push(total_savings)


const MONTHS = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec'
];

function random_rgba() {
  var o = Math.round, r = Math.random, s = 255;
  return 'rgba(' + o(r()*s) + ',' + o(r()*s) + ',' + o(r()*s) + ',' + r().toFixed(1) + ')';
}


function months(config) {
  var cfg = config || {};
  var count = cfg.count || 12;
  var section = cfg.section;
  var values = [];
  var i, value;

  for (i = 0; i < count; ++i) {
    value = MONTHS[Math.ceil(i) % 12];
    values.push(value.substring(0, section));
  }

  return values;
}

var background_dougnut_color = []

for(var i=0; i < doughnut_django_data.length; i++){
  background_dougnut_color.push(random_rgba())
}

const doughnut_data = {
  labels: doughnut_label,
  datasets: [{
    label: 'Monthly Expense',
    data: doughnut_django_data,
    backgroundColor: background_dougnut_color,
    hoverOffset: 4
  }]
};
const doughnut_config = {
  type: 'doughnut',
  data: doughnut_data,
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: `Annual Data`
      },
    },
  }
};


const doughnutChart = new Chart(chart_doughnut, doughnut_config)

const labels = months({ count: 12 });
const savings_chart_data = {
  labels: labels,
  datasets: [{
    label: 'Expense',
    data: bar_django_data,
    fill: false,
    borderColor: 'rgb(75, 192, 192)',
    cubicInterpolationMode: 'monotone',
    tension: 0.4,
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
    ],
    borderColor: [
      'rgb(255, 99, 132)',
          ],
    borderWidth: 1

  }]
};

const line_chart_config = {
  type: 'bar',
  data: savings_chart_data,
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: `Monthly Expenses of ${TODAY.getFullYear()}`
      },
    },
  }
}

const lineChart = new Chart(chart_line, line_chart_config)

