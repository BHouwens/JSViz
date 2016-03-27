export function drawChart(data) {
    let width = 500,
        height = 500;

    let force = d3.layout.force()
        .size([width, height]);

    let svg = d3.select('body').append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g');

    let nodes = data.files,
        links = data.links;

    force.nodes(nodes).links(links);
    force.start();

    let node = svg.selectAll('circle')
        .data(nodes).enter().append('circle')
        .attr('r', 5);

    let link = svg.selectAll('line')
        .data(links).enter().append('line');


    force.on('tick', () =>{
        node.attr('cx', d => { return d.x })
            .attr('title', d => { return d.name })
            .attr('class', () => { return 'node' })
            .attr('cy', d => { return d.y });

        link.attr('x1', d => { return d.source.x })
            .attr('y1', d => { return d.source.y })
            .attr('x2', d => { return d.target.x })
            .attr('y2', d => { return d.target.y })
    });

}