var map;
var marker;
var org = {
    lat: 14.5579,
    lng: 121.0085
};
var dest = {
    lat: 14.562442311912873,
    lng: 121.0214638710022
};
var directionsService;
var directionsDisplay;

var pusher = new Pusher('e9edd41d83c667edc487', {
    cluster: 'ap1',
    forceTLS: true
});
var channel = pusher.subscribe('autobot');
channel.bind('update-gps', updateMap);
channel.bind('update-location', updateMap);

function initMap() {
    map = new google.maps.Map(
        document.getElementById('map'), {
            zoom: 16,
            center: org 
        });

    google.maps.event.addListener(map, 'click', (event) => {
        dest.lat = event.latLng.lat(),
        dest.lng = event.latLng.lng()
        console.log("dest:", dest);
        updateMap(org);
    });

    origin = new google.maps.LatLng(org.lat, org.lng);
    destination = new google.maps.LatLng(dest.lat, dest.lng);
    getRoute(origin, destination);
}

function getRoute(origin, destination) {

    if (directionsDisplay) {
        directionsDisplay.setMap(null);
        directionsDisplay = null;
    }

    directionsService = new google.maps.DirectionsService;
    directionsDisplay = new google.maps.DirectionsRenderer({
        map: map
    });
    displayRoute(directionsService, directionsDisplay, origin, destination);
}

function displayRoute(directionsService, directionsDisplay, origin, destination) {
    directionsService.route({
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.WALKING
    }, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

function updateMap(payload) {
    console.log('updateMap:', payload);
    org.lat = parseFloat(payload.lat);
    org.lng = parseFloat(payload.lng);

    const origin = new google.maps.LatLng(org.lat, org.lng);
    const destination = new google.maps.LatLng(dest.lat, dest.lng);
    getRoute(origin, destination);
}
