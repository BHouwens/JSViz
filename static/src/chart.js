export function drawChart(nodeData, linkData) {
    let width = 900,
        height = 700;

    let force = d3.layout.force()
        .size([width, height])
        .charge(-250)
        .linkDistance(50);

    let svg = d3.select('body').append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g');

    let nodes = nodeData,
        links = linkData;

    force
        .nodes(nodes)
        .links(links)
        .start();

    let link = svg.selectAll('.link')
                  .data(links)
                  .enter()
                  .insert('line')
                  .attr('class','link');

    let node = svg.selectAll('.node')
                    .data(nodes)
                    .enter()
                    .append('g')
                    .attr('class', 'node')
                    .call(force.drag);
        
    node.append('circle')
        .attr('class', 'node')
        .attr('r', 5);
        
    node
        .append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name})
        
    force.on('tick', () =>{
        node.attr('cx', d => { return d.x })
            .attr('title', d => { return d.name })
            .attr('class', () => { return 'node' })
            .attr('cy', d => { return d.y });

        link.attr('x1', d => { return d.source.x })
            .attr('y1', d => { return d.source.y })
            .attr('x2', d => { return d.target.x })
            .attr('y2', d => { return d.target.y });
            
        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    });

}