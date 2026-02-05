/**
 * Story Tree Visualization using D3.js
 * Renders a force-directed graph of story pages and choices
 */

async function renderStoryTree(storyId) {
    const container = document.getElementById('story-tree');
    if (!container) return;
    
    // Clear existing content
    container.innerHTML = '';
    
    // Fetch tree data
    let data;
    try {
        const response = await fetch(`/play/${storyId}/tree/`);
        data = await response.json();
    } catch (error) {
        container.innerHTML = '<p class="text-muted text-center p-3">Could not load story map</p>';
        return;
    }
    
    if (!data.nodes || data.nodes.length === 0) {
        container.innerHTML = '<p class="text-muted text-center p-3">No pages yet</p>';
        return;
    }
    
    // Set up SVG
    const width = container.clientWidth;
    const height = container.clientHeight || 300;
    
    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height]);
    
    // Create arrow marker for directed edges
    svg.append('defs').append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 20)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .append('path')
        .attr('d', 'M 0,-5 L 10,0 L 0,5')
        .attr('fill', '#999');
    
    // Create force simulation
    const simulation = d3.forceSimulation(data.nodes)
        .force('link', d3.forceLink(data.edges)
            .id(d => d.id)
            .distance(80))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(30));
    
    // Create links
    const link = svg.append('g')
        .selectAll('line')
        .data(data.edges)
        .join('line')
        .attr('class', 'link')
        .attr('stroke', '#999')
        .attr('stroke-width', 1.5)
        .attr('marker-end', 'url(#arrowhead)');
    
    // Create nodes
    const node = svg.append('g')
        .selectAll('g')
        .data(data.nodes)
        .join('g')
        .attr('class', d => {
            if (d.is_start) return 'node start';
            if (d.is_ending) return 'node ending';
            return 'node normal';
        })
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));
    
    // Add circles to nodes
    node.append('circle')
        .attr('r', d => d.is_start ? 12 : (d.is_ending ? 10 : 8))
        .attr('fill', d => {
            if (d.is_start) return '#28a745';
            if (d.is_ending) return '#dc3545';
            return '#007bff';
        });
    
    // Add labels
    node.append('text')
        .text(d => d.is_start ? 'Start' : (d.is_ending ? 'End' : d.id))
        .attr('x', 15)
        .attr('y', 4)
        .attr('font-size', '10px')
        .attr('fill', '#333');
    
    // Add tooltips
    node.append('title')
        .text(d => {
            let text = `Page ${d.id}`;
            if (d.is_start) text += ' (Start)';
            if (d.is_ending) text += ` - ${d.ending_label || 'Ending'}`;
            return text;
        });
    
    // Update positions on tick
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        node.attr('transform', d => `translate(${d.x},${d.y})`);
    });
    
    // Drag functions
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }
    
    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }
    
    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

// Export
window.renderStoryTree = renderStoryTree;
