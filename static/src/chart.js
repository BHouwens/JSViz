export function drawChart(nodeData, linkData) {
    let width = 1200,
        height = 1500;

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
        .attr('class', 'link');

    let node = svg.selectAll('.node')
        .data(nodes)
        .enter()
        .append('g')
        .attr('class', 'node')
        .call(force.drag);

    node.append('circle')
        .attr('class', d => { return d.class })
        .attr('r', 5);

    node
        .append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name });

    node.on('mouseover', n => {
        link
            .style('stroke-width', l => {
                if (n === l.source || n === l.target)
                    return 2;
                else
                    return 1.5;
            })
            .style('stroke', l => {
                if (n === l.source){
                    return '#7ec042';
                }else if (n === l.target){
                    return '#e14a49';
                }
                return '#ccc';
            });
    });

    // Set the stroke width back to normal when mouse leaves the node.
    node.on('mouseout', function() {
        link.style('stroke-width', 1.5).style('stroke', '#ccc');
    });

    force.on('tick', () => {
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