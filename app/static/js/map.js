let marker, x, y, oldmap;

const hkCentre = {
    coords: {
        latitude: 22.28056,
        longitude: 114.17222
    }
};


function initMap() {
    let map = document.getElementById('donate_map');
    const strictBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(22.1193278, 114.0028131),
        new google.maps.LatLng(22.4393278, 114.3228131)
    );
    const run = (position) => {
        map.style.display = "block";
        oldmap = new google.maps.Map(
            map, {
                zoom: 13,
                center: { lat: position.coords.latitude, lng: position.coords.longitude },
                restriction: {
                    latLngBounds: strictBounds,
                },
            });
        oldmap.addListener("click", function(e) { // allow user to point the map
            let latLng = e.latLng;

            x = e.latLng.lat();
            y = e.latLng.lng();

            document.getElementById("point_location").value = [x, y];
            document.getElementById("point_location").disabled = false;

            // if marker exists and has a .setMap method, hide it
            if (marker && marker.setMap) {
                marker.setMap(null);
            }
            // the below cannot make as a function, otherwise the marker cannot delete
            marker = new google.maps.Marker({
                position: latLng,
                map: oldmap
            });
        });
    }

    if (navigator.geolocation) {
        map.style.display = "none";
        navigator.geolocation.getCurrentPosition(run, () => { run(hkCentre) });
    }
    else {
        run(hkCentre);
    }
}

function stuRegMap() {
    let map = document.getElementById('stu_reg_map');
    const strictBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(22.1193278, 114.0028131),
        new google.maps.LatLng(22.4393278, 114.3228131)
    );
    const run = (position) => {
        map.style.display = "block";
        oldmap = new google.maps.Map(
            map, {
                zoom: 13,
                center: { lat: position.coords.latitude, lng: position.coords.longitude },
                restriction: {
                    latLngBounds: strictBounds,
                },
            });
        oldmap.addListener("click", function(e) { // allow user to point the map
            let latLng = e.latLng;

            x = e.latLng.lat();
            y = e.latLng.lng();

            document.getElementById("point_location").value = [x, y];
            document.getElementById("point_location").disabled = false;

            // if marker exists and has a .setMap method, hide it
            if (marker && marker.setMap) {
                marker.setMap(null);
            }
            // the below cannot make as a function, otherwise the marker cannot delete
            marker = new google.maps.Marker({
                position: latLng,
                map: oldmap
            });
        });
    }
    if (navigator.geolocation) {
        map.style.display = "none";
        navigator.geolocation.getCurrentPosition(run, () => { run(hkCentre) });
    }
    else {
        run(hkCentre);
    }
}

// Keep references
var storyMap, markers = [];

// Our markers database (for testing)


function initialize() {
    let map = document.getElementById('map-canvas');
    const strictBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(22.1193278, 114.0028131),
        new google.maps.LatLng(22.4393278, 114.3228131)
    );
    const run = (position) => {
        map.style.display = "block";
        storyMap = new google.maps.Map(
            map, {
                zoom: 13,
                center: { lat: position.coords.latitude, lng: position.coords.longitude },
                restriction: {
                    latLngBounds: strictBounds,
                },
            });

        // var storyMapProp = {
        //     zoom: 11,
        //     center: new google.maps.LatLng(22.302711, 114.177216)
        //     // center: {lat: 22.302711, lng: 114.177216},
        // };
        //
        // storyMap = new google.maps.Map(document.getElementById('map-canvas'), storyMapProp)

        // Adding our markers from our "big database"
        // addMarkers();
        // get_stu_locations();

        // Fired when the map becomes idle after panning or zooming.
        google.maps.event.addListener(storyMap, 'idle', function() {
            get_stu_locations();
            showVisibleMarkers();
        });
    }
    if (navigator.geolocation) {
        map.style.display = "none";
        navigator.geolocation.getCurrentPosition(run, () => { run(hkCentre) });
    }
    else {
        run(hkCentre);
    }

}

function get_stu_locations() {
    var bounds = storyMap.getBounds()
    var southWest = bounds.getSouthWest();
    var northEast = bounds.getNorthEast();
    var params = {
        fromLat: southWest.lat(),
        toLat: northEast.lat(),
        fromLng: southWest.lng(),
        toLng: northEast.lng(),
        item_id: document.getElementById('item_id').value,
    };
    $.ajax('/donate/getdata', // request url
        {
            dataType: "json",
            data: params,
            success: function(data, status, xhr) { // success callback function
                addMarkers(data);
            }
        });
}

function addMarkers(locations) {

    // Remove previous markers
    for (let i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
    }

    // Reset markers array
    markers = [];

    for (var i = 0; i < locations.length; i++) {
        const records = locations[i],
            myLatLng = new google.maps.LatLng(records[1], records[2]),
            marker = new google.maps.Marker({
                position: myLatLng,
                title: records[0],
                map: storyMap
            });

        // contentString = records[3],
        this.infoWindow = new google.maps.InfoWindow();

        // set map icon colour with condition
        if (records[0] === "StudentDemoA1") {
            marker.setIcon("http://maps.google.com/mapfiles/ms/icons/red-dot.png")
        }
        else {
            marker.setIcon("http://maps.google.com/mapfiles/ms/icons/yellow-dot.png")
        }

        // marker.setMap(storyMap);
        // markerCluster.setMap(storyMap);

        // Keep marker instances in a global array
        markers.push(marker);

        marker.addListener("click", () => {
            this.infoWindow.setContent(records[3])
            this.infoWindow.open(storyMap, marker)
        })

        // Attach click event to the marker.
        // (function (records, marker, infoWindow) {
        //     // const contentString = records[3];
        //     // const infowindow = new google.maps.InfoWindow({
        //     //     content: contentString,
        //     // });
        //     marker.addListener("click", () => {
        //         infoWindow.close();
        //         infoWindow.setContent(records[3])
        //         infoWindow.open(storyMap, marker);
        //     })
        // })(records, marker, this.infoWindow);
    }
    // Put markers into cluster
    new MarkerClusterer(storyMap, markers, {
        imagePath: "/static/map_icon/m"
    });
    // const markerCluster = new MarkerClusterer(storyMap, markers, {
    //     imagePath: "/static/map_icon/m"
    //     // imagePath: "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m"
    // });
    // markerCluster.addMarker(marker);
}

function showVisibleMarkers() {
    var bounds = storyMap.getBounds(),
        count = 0;

    for (var i = 0; i < markers.length; i++) {
        var marker = markers[i],
            infoPanel = $('.info-' + (i + 1)); // array indexes start at zero, but not our class names :)

        if (bounds.contains(marker.getPosition()) === true) {
            infoPanel.show();
            count++;
        }
        else {
            infoPanel.hide();
        }
    }

    $('#infos h2 span').html(count);
}


// google.maps.event.addDomListener(window, 'load', initialize);
