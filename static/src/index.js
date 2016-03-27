import {drawChart} from './chart';

$.ajax({
    url: "http://localhost:5000/network"
}).done(d => {
    console.log(d);
    drawChart(d);
});