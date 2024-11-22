# JavaScript code for custom hover behavior
HOVER_JS = '''
<script>
    document.addEventListener("DOMContentLoaded", function() {
        var myPlot = document.getElementsByClassName('plotly-graph-div')[0];

        if (!myPlot) {
            console.error('Plotly graph not found');
            return;
        }

        console.log('Plotly graph found:', myPlot);

        // Function to handle hover event
        function handleHover(data) {
            console.log('Hover event triggered');
            console.log('Data object:', data);  // Debug: Log the entire data object

            if (!data || !data.points || !data.points[0]) {
                console.error('No data points found on hover');
                return;
            }

            var hoveredGroups = data.points[0].customdata;
            console.log('Hovered groups:', hoveredGroups);  // Debug: Log the groups of the hovered marker

            var defaultUpdate = {
                //'marker.opacity': 0.3,
                'line.width': 1,
                'marker.line.width': 1 // Set default marker line width for all traces
            };
            Plotly.restyle(myPlot, defaultUpdate);

            var indices = [];
            for (var i = 0; i < myPlot.data.length; i++) {
                var traceGroups = myPlot.data[i].customdata;
                var traceMode = myPlot.data[i].mode;
                console.log(`Trace ${i} customdata:`, traceGroups, `Mode: ${traceMode}`);  // Debug: Log the customdata and mode of each trace

                if (traceGroups) {
                    // Flatten customdata if necessary
                    if (Array.isArray(traceGroups[0])) {
                        traceGroups = traceGroups.flat();
                    }
                    if (hoveredGroups.some(group => traceGroups.includes(group))) {
                        console.log('Match found: Trace', i, 'shares a value with hovered customdata');  // Debug: Log when a match is found
                        indices.push(i);
                    }
                }
            }
            console.log('Indices to be updated:', indices);  // Debug: Log the indices to be updated

            // Update only the matched traces with increased marker line width and opacity
            var updateHover = {
                // 'marker.opacity': 1,
                'line.width': 4,
                'marker.line.width': 4 // Increase marker line width for hovered elements
            };
            Plotly.restyle(myPlot, updateHover, indices).then(function() {
                console.log('Restyle complete');  // Debug: Log when restyling is complete
            }).catch(function(error) {
                console.error('Restyle error:', error);  // Debug: Log any restyle errors
            });
        }

        // Function to handle unhover event
        function handleUnhover(data) {
            console.log('Unhover event triggered');
            var resetUpdate = {
                // 'marker.opacity': 1,
                'line.width': 2,
                'marker.line.width': 2 // Reset marker line width for unhovered elements
            };
            Plotly.restyle(myPlot, resetUpdate).then(function() {
                console.log('Restyle complete on unhover');  // Debug: Log when restyling on unhover is complete
            }).catch(function(error) {
                console.error('Restyle error on unhover:', error);  // Debug: Log any restyle errors on unhover
            });
        }

        // Attach hover and unhover event listeners
        myPlot.on('plotly_hover', handleHover);
        myPlot.on('plotly_unhover', handleUnhover);

        console.log('Event listeners attached');
    });
</script>
'''
