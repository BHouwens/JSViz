import {drawChart} from './chart';
require('../styles/index.scss');

$.ajax({
    method: 'GET',
    dataType: 'json',
    url: "http://localhost:5000/network"
}).success(d => {
    console.log(d);
    
    drawChart(d.files, d.links);
});