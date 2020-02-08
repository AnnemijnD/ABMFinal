var HistogramModule = function(bins, canvas_width, canvas_height, data) {

    // Create the tag:
    var canvas_tag = "<canvas id='canvas' width='" + canvas_width + "' height='" + canvas_height + "' ";
    canvas_tag += "></canvas>";
    // Append it to body:
    var canvas = $(canvas_tag)[0];
    $("body").append(canvas);

    // Create the context and the drawing controller:
    var context = canvas.getContext("2d");
    canvas.width = canvas_width

    // Prep the chart properties and series:
    var datasets = [{
        label: "Number of customers in an attraction",
        fillColor: "rgba(151,187,205,0.5)",
        strokeColor: "rgba(151,187,205,0.8)",
        highlightFill: "rgba(151,187,205,0.75)",
        highlightStroke: "rgba(151,187,205,1)",
        data: data
    }];

    // Add a zero value for each bin
    for (var i in data) {
      console.log(datasets[0].data);
      datasets[0].data.push(data[i]);
    }


    var data = {
        labels: bins,
        datasets: datasets
    };

    var options = {
      scales: {
    yAxes: [{
      id: 'y-axis-0',
      gridLines: {
        display: true,
        lineWidth: 1,
        color: "rgba(0,0,0,0.30)"
      },
      ticks: {
        beginAtZero:true,
        mirror:false,
        suggestedMin: 0,
        suggestedMax: 10,
      },
      afterBuildTicks: function(chart) {

      }
    }],
    xAxes: [{
      id: 'x-axis-0',
      gridLines: {
        display: false
      },
      ticks: {
        beginAtZero: true
      }
    }]
}

    };

    // Create the chart object
    var chart = new Chart(context, {
        type: "bar",
        data: data,
        options: options
      },
      options);

    this.render = function(data) {
        for (var i in data)
            chart.data.datasets[0].data[i] = data[i];
            console.log(chart.data, "CHARTDATA");
        chart.update();
    };

    this.reset = function() {
        chart.destroy();
        // Create the chart object
        var chart = new Chart(context, {
            type: "bar",
            data: data,
            options: options
          },
          options);
    };
};
