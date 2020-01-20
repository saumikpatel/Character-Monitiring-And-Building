
// var ctx = document.getElementById('myChart').getContext('2d');
// var chart = new Chart(ctx, {
//     // The type of chart we want to create
//     type: 'line',

//     // The data for our dataset
//     data: {
//         labels: ["January", "February", "March", "April", "May", "June", "July"],
//         datasets: [{
//             label: "My First dataset",
//             backgroundColor: 'rgb(255, 99, 132)',
//             borderColor: 'rgb(255, 99, 132)',
//             data: [0, 10, 5, 2, 20, 30, 45],
//         }]
//     },

//     // Configuration options go here
//     options: {}
// });



// var myDoughnutChart = new Chart(ctx, {
//     type: 'doughnut',
//     data : {
//     datasets: [{
//         data: [85, 03, 03,03,03,03],
//         backgroundColor:['#ff0000','#FFFF33','#039be5','#FF1493','#999933','#663366'
//         ]
//     }],

//     // These labels appear in the legend and in the tooltips when hovering different arcs
//     labels: [
//         'Anger',
//         'Fear',
//         'Happiness',
//         'Love',
//         'Sad',
//         'Surprise'
//     ]
// },
//     options: {}
// });
/**
 * Plugin: Manipulate z-index of the chart
 */
AmCharts.addInitHandler(function(chart) {
  
  // init holder for nested charts
  if (AmCharts.nestedChartHolder === undefined)
    AmCharts.nestedChartHolder = {};

  if (chart.bringToFront === true) {
    chart.addListener("init", function(event) {
      // chart inited
      var chart = event.chart;
      var div = chart.div;
      var parent = div.parentNode;
      
      // add to holder
      if (AmCharts.nestedChartHolder[parent] === undefined)
        AmCharts.nestedChartHolder[parent] = [];
      AmCharts.nestedChartHolder[parent].push(chart);
      
      // add mouse mouve event
      chart.div.addEventListener('mousemove', function() {
        
        // calculate current radius
        var x = Math.abs(chart.mouseX - (chart.realWidth / 2));
        var y = Math.abs(chart.mouseY - (chart.realHeight / 2));
        var r = Math.sqrt(x*x + y*y);
        
        // check which chart smallest chart still matches this radius
        var smallChart;
        var smallRadius;
        for(var i = 0; i < AmCharts.nestedChartHolder[parent].length; i++) {
          var checkChart = AmCharts.nestedChartHolder[parent][i];
          
          if((checkChart.radiusReal < r) || (smallRadius < checkChart.radiusReal)) {
            checkChart.div.style.zIndex = 1;
          }
          else {
            if (smallChart !== undefined)
              smallChart.div.style.zIndex = 1;
            checkChart.div.style.zIndex = 2;
            smallChart = checkChart;
            smallRadius = checkChart.radiusReal;
          }
          
        }
      }, false);
    });
  }

}, ["pie"]);

/**
 * Create the charts
 */
AmCharts.makeChart("chart1", {
  "type": "pie",
  "bringToFront": true,
  "dataProvider": [{
    "title": "$",
    "value": 100,
    "color": "#090E0F"
  }],
  "startDuration": 0,
  "pullOutRadius": 0,
  "color": "#fff",
  "fontSize": 14,
  "titleField": "title",
  "valueField": "value",
  "colorField": "color",
  "labelRadius": 20,
  "labelColor": "#fff",
  "radius": 25,
  "innerRadius": 0,
  "labelText": "[[title]]",
  "balloonText": "[[title]]: [[value]]"
});

AmCharts.makeChart("chart2", {
  "type": "pie",
  "bringToFront": true,
  "dataProvider": [{
    "title": "Surprise",
    "value": 12,
    "color": "#BA3233"
  }, {
    "title": "Enthusiasm",
    "value": 18,
    "color": "#6179C0"
  }, {
    "title": "Happiness",
    "value": 25,
    "color": "#624B6A"
  },  {
    "title": "Love",
    "value": 13,
    "color": "orange"
  },
   {
    "title": "Sad",
    "value": 14,
    "color": "green"
  }, 
  {
    "title": "Worry",
    "value": 04,
    "color": "#3d3d3d"
  },
  {
    "title": "Hate",
    "value": 06,
    "color": "#ddd"
  },
  {
    "title": "Fear",
    "value": 15,
    "color": "#039be5"
  },
  {
    "title": "Fun",
    "value": 10,
    "color": "#669966"
  },
  {
    "title": "Anger",
    "value": 18,
    "color": "#333"
  }],
  "startDuration": 1,
  "pullOutRadius": 0,
  "color": "#fff",
  "fontSize": 12,
  "titleField": "title",
  "valueField": "value",
  "colorField": "color",
  "labelRadius": -40,
  "labelColor": "#fff",
  "radius": 148,
  "innerRadius": 27,
  "outlineAlpha": 1,
  "outlineThickness": 4,
  "labelText": "[[title]]",
  "balloonText": "[[title]]: [[value]]"
});

AmCharts.makeChart("chart3", {
  "type": "pie",
  "bringToFront": true,
  "dataProvider": [{
    "title": "Openness",
    "value": 35,
    "color": "orange"
  }, {
    "title": "Conscientiousness",
    "value": 17,
    "color": "#BA3233"
  }, {
    "title": "Extroversion",
    "value": 23,
    "color": "green"
  }, {
    "title": "Agreeableness",
    "value": 14,
    "color": "#333"
  }, {
    "title": "Neuroticism",
    "value": 16,
    "color": "#624B6A"
  }], 
  "startDuration": 1,
  "pullOutRadius": 0,
  "color": "#fff",
  "fontSize": 12,
  "titleField": "title",
  "valueField": "value",
  "colorField": "color",
  "labelRadius": -57,
  "labelColor": "#fff",
  "radius": 250,
  "innerRadius": 150,
  "outlineAlpha": 1,
  "outlineThickness": 4,
  "labelText": "[[title]]",
  "balloonText": "[[title]]: [[value]]"
});

// AmCharts.makeChart("chart4", {
//   "type": "pie",
//   "bringToFront": true,
//   "dataProvider": [{
//     "title": "Design",
//     "value": 5.5,
//     "color": "#BA3233"
//   }, {
//     "title": "P&P",
//     "value": 5.5,
//     "color": "#BA3233"
//   }, {
//     "title": "Magazines",
//     "value": 11,
//     "color": "#BA3233"
//   }, {
//     "title": "Outdoor",
//     "value": 3.66,
//     "color": "#BA3233"
//   }, {
//     "title": "Promo",
//     "value": 3.66,
//     "color": "#BA3233"
//   }, {
//     "title": "Endorsement",
//     "value": 3.66,
//     "color": "#BA3233"
//   }, {
//     "title": "Maintenance",
//     "value": 8.25,
//     "color": "#624B6A"
//   }, {
//     "title": "Acquisition",
//     "value": 8.25,
//     "color": "#624B6A"
//   }, {
//     "title": "Raw",
//     "value": 5.5,
//     "color": "#624B6A"
//   }, {
//     "title": "Recycling",
//     "value": 5.5,
//     "color": "#624B6A"
//   }, {
//     "title": "Logistics",
//     "value": 5.5,
//     "color": "#624B6A"
//   }, {
//     "title": "LAB1",
//     "value": 3.3,
//     "color": "#6179C0"
//   }, {
//     "title": "LAB2",
//     "value": 3.3,
//     "color": "#6179C0"
//   }, {
//     "title": "LAB3",
//     "value": 3.3,
//     "color": "#6179C0"
//   }, {
//     "title": "Supply",
//     "value": 3.3,
//     "color": "#6179C0"
//   }, {
//     "title": "Disposal",
//     "value": 3.3,
//     "color": "#6179C0"
//   }, {
//     "title": "Application",
//     "value": 5.5,
//     "color": "#6179C0"
//   }, {
//     "title": "Acquisition",
//     "value": 5.5,
//     "color": "#6179C0"
//   }, {
//     "title": "Settlement",
//     "value": 5.5,
//     "color": "#6179C0"
//   }],
//   "startDuration": 1,
//   "pullOutRadius": 0,
//   "color": "#fff",
//   "fontSize": 8,
//   "titleField": "title",
//   "valueField": "value",
//   "colorField": "color",
//   "labelRadius": -27,
//   "labelColor": "#fff",
//   "radius": 190,
//   "innerRadius": 137,
//   "outlineAlpha": 1,
//   "outlineThickness": 4,
//   "labelText": "[[title]]",
//   "balloonText": "[[title]]: [[value]]",
//   "allLabels": [{
//     "text": "ACME Inc. Spending Chart",
//     "bold": true,
//     "size": 18,
//     "color": "#404040",
//     "x": 0,
//     "align": "center",
//     "y": 20
//   }]
// });