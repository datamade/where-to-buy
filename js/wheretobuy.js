var geocoder = new google.maps.Geocoder();

var WhereToBuy = WhereToBuy || {};
var WhereToBuy = {

    // Map config
    map: null,
    mapCentroid: [41.790, -87.636],
    googleStyles: [{
                        stylers: [
                            { saturation: -100 },
                            { lightness: 40 }
                        ]
                      }],
    defaultZoom: 8,
    lastClickedLayer: null,
    legend: null,
    locationScope: 'Chicago',

    // Carto databases
    chicagoBoundaries: 'chicago_community_areas',
    suburbBoundaries: 'suburb_boundaries',

    // Layer styles
    boundaries: {
        cartocss: $('#boundary-styles').html().trim(),
        color: '#ffffcc',
        opacity: 0.75
    },

    initialize: function() {

        if (!WhereToBuy.map) {
            // Initialize a Leaflet map
            WhereToBuy.map = L.map('map', {
                center: WhereToBuy.mapCentroid,
                zoom: WhereToBuy.defaultZoom,
                dragging: true,
                touchZoom: true,
                zoomControl: true,
                tap: true,
                scrollWheelZoom: false
            });
        }

        // Add streets to the map
        WhereToBuy.streets = new L.Google('ROADMAP', {mapOptions: {styles: WhereToBuy.googleStyles}});
        WhereToBuy.map.addLayer(WhereToBuy.streets);

        // Query carto for boundaries
        var fields = "";
        var layerOpts = {
            user_name: 'datamade',
            type: 'cartodb',
            sublayers: [{
                sql: "SELECT * FROM" + WhereToBuy.chicagoBoundaries,
                cartocss: WhereToBuy.boundaries.cartocss,
                interactivity: fields
            }, {
                sql: "SELECT * FROM" + WhereToBuy.suburbBoundaries,
                cartocss: WhereToBuy.boundaries.cartocss,
                interactivity: fields
            }]
        };

        var boundaries = cartodb.createLayer(WhereToBuy.map, layerOpts, { https: true },
            function(layer) {

                var sublayers = [];
                var sub1 = layer.getSubLayer(0);
                var sub2 = layer.getSublayer(1);
                sublayers.push(sub1, sub2);

                sublayers.forEach(function(sublayer) {
                    sublayer.setInteraction(true);
                    // Set more interactions here
                });
            }).on('done', function(layer) {
                layer.addTo(WhereToBuy.map);
            });

    }

};