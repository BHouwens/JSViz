import {drawChart} from './chart';
require('../styles/index.css');

$.ajax({
    method: 'GET',
    dataType: 'json',
    url: "http://localhost:5000/network"
}).success(d => {
    drawChart(d.files, d.links);
});