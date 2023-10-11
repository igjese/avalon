function initDataTables() {
    $('#suppliesTable').DataTable({
         "pageLength": 100,  // Show 100 rows per page
         "lengthChange": false  // Remove the dropdown menu
     });
     $('#systemsTable').DataTable({
         "pageLength": 100,  // Show 100 rows per page
         "lengthChange": false  // Remove the dropdown menu
     });
     $('#referenceTable').DataTable({  // Assuming you also have a table with this ID for recipes
         "pageLength": 100,  // Show 100 rows per page
         "lengthChange": false  // Remove the dropdown menu
     });
     $('#storageTypeTable').DataTable({  // Assuming you also have a table with this ID for recipes
         "pageLength": 100,  // Show 100 rows per page
         "lengthChange": false  // Remove the dropdown menu
     });
 }


 // Update resource table
 function updateResourceTable(resources) {
    console.log(resources)
     for (const [resourceName, resourceData] of Object.entries(resources)) {
         $(`#${resourceName}_quantity`).text(resourceData['available']);
         $(`#${resourceName}_capacity`).text(resourceData['capacity']);
     }
 }

 // Update alerts
 function updateAlerts(alerts) {
     for (const [resourceName, alertData] of Object.entries(alerts)) {
         $(`#${resourceName}_alert`).removeClass('bg-success bg-warning bg-danger').addClass(alertData['level']);
     }
 }

 function drawHighcharts(historyData) {
     // Prepare data for Highcharts
     //const ticks = historyData.map(item => item.tick);
     const gameTimes = historyData.map(item => item.game_time);  // Use game_time instead of tick

     // Check if historyData has data and if it's not empty
     if (historyData && historyData.length > 0) {
         // Collect all unique resource names from the first 'quantity_data' object
         const resourceNames = Object.keys(historyData[0].quantity_data);

         // Function to create series
         const createSeries = (dataKey, titlePrefix) => {
             return resourceNames.map(resourceName => {
                 return {
                     name: `${resourceName}`,
                     data: historyData.map(item => item[dataKey] ? item[dataKey][resourceName] : null)
                 };
             });
         };

         // Create series dynamically for quantities, production, and consumption
         const quantitySeries = createSeries('quantity_data', 'Quantity');
         const productionSeries = createSeries('production_data', 'Production');
         const consumptionSeries = createSeries('consumption_data', 'Consumption');

         // Check if charts are already initialized
         if (typeof Highcharts.charts[0] !== 'undefined') {
             // Update existing charts
             Highcharts.charts[0].update({ series: quantitySeries, xAxis: { categories: gameTimes } });
             Highcharts.charts[1].update({ series: productionSeries, xAxis: { categories: gameTimes } });
             Highcharts.charts[2].update({ series: consumptionSeries, xAxis: { categories: gameTimes } });
         } else {
             // Initialize new charts
             Highcharts.chart('quantityHistory', {
                 title: { text: 'Resource Quantities Over Time' },
                 xAxis: { categories: gameTimes },
                 yAxis: { title: { text: 'Quantity' } },
                 series: quantitySeries
             });

             Highcharts.chart('productionHistory', {
                 title: { text: 'Resource Production Over Time' },
                 xAxis: { categories: gameTimes },
                 yAxis: { title: { text: 'Production' } },
                 series: productionSeries
             });

             Highcharts.chart('consumptionHistory', {
                 title: { text: 'Resource Consumption Over Time' },
                 xAxis: { categories: gameTimes },
                 yAxis: { title: { text: 'Consumption' } },
                 series: consumptionSeries
             });
         }
     }
 }
