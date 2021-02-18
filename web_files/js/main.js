// Global variables
var wordCloudChart;
var ourData = {};

var margin = { top: 10, right: 10, bottom: 10, left: 10 },
    width = 1000 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

var fill = d3.scaleOrdinal(d3.schemeSet1);
// append the svg object to the body of the page
var svg = d3.select("#my_dataviz").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");
var layout = d3.layout.cloud()
    .size([width, height]);
var text = svg.append('g')
    .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
    .attr('class', 'text-words')


var btn = document.getElementById("btn");
var e = document.getElementById("var-select");

btn.addEventListener("click", function () {
    var strCategory = e.options[e.selectedIndex].value;
    var request = new XMLHttpRequest();

    request.open('POST', 'http://127.0.0.1:5000/'+strCategory);
    request.onload = function () {
        ourData = JSON.parse(request.responseText)
        renderHTML(ourData)
    }
    request.send()
})



function renderHTML(data) {

    layout
        .words(data.map(function (d) { return { text: d.word, size: d.size }; }))
        .padding(5)        //space between words
        .rotate(function () { return ~~(Math.random() * 2) * 90; })
        .fontSize(function (d) { return d.size; })      // font size of words
        .on("end", draw);
    layout.start();

}

function draw(words) {
    text
        .selectAll(".text")
        .data(words)
        .join(
            enter => enter
                .append("text")
                .attr('class', 'text')
                .style("font-size", function (d) { return d.size; })
                .attr("text-anchor", "middle")
                .style("font-family", "Impact")
                .style("fill", function (d, i) { return fill(i); })
                .attr("transform", function (d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function (d) { return d.text; }),
            update => update
                .transition()
                .duration(700)
                .style("font-size", function (d) { return d.size; })
                .style("fill", function (d, i) { return fill(i); })
                .attr("text-anchor", "middle")
                .style("font-family", "Impact")
                .attr("transform", function (d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function (d) { return d.text; }),
            exit => exit
                .transition()
                .duration(500)
                .style('opacity', 1e-6)
                .remove()

        )

}



