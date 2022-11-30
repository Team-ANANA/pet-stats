import React, { useEffect } from 'react';
import * as d3 from 'd3';
import Datamap from 'datamaps/dist/datamaps.world.min.js';
import CanadaJson from './Canada.topo.json';

// class ChoroplethMap extends Component {
//     componentDidMount() {
function ChoroplethMap(props){
    useEffect(() => {
        document.getElementById('map').innerHTML = '';
        //console.log(props.data)
        let dataset = {};

        //let onlyValues = this.props.data.map(function (obj) { return obj[1]; });
        let onlyValues = props.data.map(function (obj) { return obj[1]; });
        let minValue = Math.min.apply(null, onlyValues),
            maxValue = Math.max.apply(null, onlyValues);

        // create color palette function
        // color can be whatever you wish
        let paletteScale = d3.scaleLinear()
            .domain([minValue, maxValue])
            .range(["#EFEFFF", "#02386F"]); // blue color

        // fill dataset in appropriate format
        props.data.forEach(function (item) { //
            // item example value ["USA", 70]
            let iso = item[0],
                value = item[1];
            dataset[iso] = { numberOfThings: value, fillColor: paletteScale(value) }; //{ numberOfThings: value,fillKey: 'MEDIUM' }//
        });

        console.log(dataset)

        let map = new Datamap({
            element: document.getElementById('map'),
            scope: 'canada',
            geographyConfig: {
                popupOnHover: true,
                highlightOnHover: true,
                borderColor: '#444',
                highlightBorderWidth: 1,
                borderWidth: 0.5,
                dataJson: CanadaJson,
                popupTemplate: function (geo, data) {
                    // don't show tooltip if country don't present in dataset
                    if (!data) { return; }
                    // tooltip content
                    return ['<div class="hoverinfo">',
                        '<strong>', geo.properties.name, '</strong>',
                        '<br>Count: <strong>', data.numberOfThings, '</strong>',
                        '</div>'].join('');
                }
            },
            fills: {
                HIGH: '#afafaf',
                LOW: '#123456',
                MEDIUM: 'blue',
                UNKNOWN: 'rgb(0,0,0)',
                defaultFill: '#eee'
            },
            data: dataset,
            setProjection: function (element) {
                var projection = d3.geoMercator()
                .center([-106.3468, 68.1304]) // always in [East Latitude, North Longitude]
                .scale(250)
                .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
                    // .center([-106.3468, 68.1304]) // always in [East Latitude, North Longitude]
                    // .scale(20)
                    // .translate([element.offsetWidth / 2, element.offsetHeight / 2]);

                var path = d3.geoPath().projection(projection);
                return { path: path, projection: projection };
            }
        });
    }, [props.data]);
        return (
            <div id="map" style={{
                height: "600px",
                width: "600px",
                position: "relative",
            }}></div>
        );
}

export default ChoroplethMap;