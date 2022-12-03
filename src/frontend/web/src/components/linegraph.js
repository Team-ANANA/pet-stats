import * as d3 from 'd3';
import {nest} from 'd3-collection';

import {useEffect, useState} from 'react';

const LineGraph = (props) => {    
	const [data, setData] = useState([]);

  useEffect(()=>{
    if (data.length > 0) {
      drawChart();
    } else {
       let tempData = [];
       for(let i=0; i < props.data.length; i++){
            tempData.push({date: d3.timeParse("%Y-%m-%d")(props.data[i].date), value: parseFloat(props.data[i].value), sort: props.data[i].sort});
       }
       setData(tempData);
    }
  },[data])

const drawChart = () => {

	// establish margins
	const margin = { top: 10, right: 50, bottom: 50, left: 50 };
    const width = 1000;
    const height = 600;

	// create the chart area
    d3.select('#timeseries-graphs')
      .select('svg')
      .remove();
      
	const svg = d3
	    .select('#timeseries-graphs')
	    .append('svg')
	    .attr('width', width + margin.left + margin.right)
	    .attr('height', height + margin.top + margin.bottom)
	    .append('g')
	    .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add X axis
    var x = d3.scaleTime()
      .domain(d3.extent(data, function(d) { return d.date; }))
      .range([ 0, width ]);
      
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(2));


    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) { return +d.value; })])
      .range([ height, 0 ]);

    svg.append("g")
      .call(d3.axisLeft(y));

    const nested_data = nest()
        .key(function(d) {return d.sort;})
        .entries(data);

    console.log(nested_data);

    // color palette
    var res = nested_data.map(function(d){ return d.key }) // list of group names
    var color = d3.scaleOrdinal()
        .domain(res)
        .range(['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999'])
 
    // Draw the lines
    svg.selectAll(".line")
    .data(nested_data)
    .enter()
    .append("path")
        .attr("fill", "none")
        .attr("stroke", function(d){ return color(d.key) })
        .attr("stroke-width", 1.5)
        .attr("d", function(d){
            return d3.line()
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(+d.value); })
            (d.values)
        })
 }

return (
	<div id='timeseries-graphs'/>
	)

}

export default LineGraph;