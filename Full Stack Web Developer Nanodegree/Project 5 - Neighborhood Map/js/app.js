// defining global variables for the Google Maps API
var map;
var info;

// defining constants
const foursquare_client_id = "LAKUHJO15R53N4IW2WV2VVFMFGKCNIZRVFHXPQO4O2P2SVL0";
const foursquare_client_secret = "TRA53RKV5EVZBHELQHT3AAFUYR4A2YCSMYZ5KLZCCXZAVFLN";
const center = [40.675606, -73.948640];

function Place(dict) {

    var self = this;

    this.name = dict.name;
    this.lat = dict.lat;
    this.lng = dict.lng;
    this.address = dict.address;
    this.phone = dict.phone;
    this.desc = ["<b>" + this.name + "</b>", this.address, this.phone].join("<br>");

    // creating a marker
    this.marker = new google.maps.Marker({
        position: new google.maps.LatLng(dict.lat, dict.lng),
        title: this.name,
        map: map
    });

    // when the user clicks on the marker, set the InfoWindow content to the Place description and open it.
    this.marker.addListener("click", function() {
        this.setAnimation(google.maps.Animation.DROP);
        info.setContent(self.desc);
        info.open(map, this);
    }, self);

    // when the user clicks on the Place name in the list, animate stuff
    this.click = function() {
        map.panTo(self.marker.getPosition());
        map.setZoom(14);
        self.marker.setAnimation(google.maps.Animation.DROP);
        info.setContent(self.desc);
        info.open(map, self.marker);
    }, self;
}

function AppViewModel() {

    var self = this;
    try {
        map = new google.maps.Map(document.getElementById("map"), {
            center: {lat: center[0], lng: center[1]},
            zoom: 12
        });
    }
    catch(err) {
        alert("Could not load the Google Maps API");
    }
    // creating the map

    // only creating one InfoWindow because I don't want more than one of them at a time on screen.
    info = new google.maps.InfoWindow({
        content: null
    });

    // creating an observable for the search box
    this.search = ko.observable();

    // creating an empty observableArray to push Place objects into
    this.places = ko.observableArray([]);

    // making a call to the Foursquare API to get the location data
    $.ajax({
        dataType: "json",
        type: "GET",
        url: "https://api.foursquare.com/v2/venues/search",
        data: {
            client_id: foursquare_client_id,
            client_secret: foursquare_client_secret,
            v: "20170624",
            ll: center[0].toString() + "," + center[1].toString(),
            query: "pizza",
            limit: 10
        },
        success: function(data) {
            var places = data.response.venues;

            // creating Place objects from the data and pushing it into the observableArray
            for (i = 0; i < places.length; i++) {
                self.places.push(new Place({
                    name: places[i].name,
                    lat: places[i].location.lat,
                    lng: places[i].location.lng,
          address: places[i].location.formattedAddress.join(", "),
          phone: places[i].contact.formattedPhone

                }));
            }
        },
        error: function(data) {
            alert("Could not get data from the Foursquare API");
        }
    });

    // filter the places observable array
    this.searchResults = ko.computed(function() {
        var search = self.search();
        if (!search) {
            // make all markers visible
            self.places().forEach(function(place){
                place.marker.setVisible(true);
            });
            return self.places();
        }
        else {
            return ko.utils.arrayFilter(self.places(), function(place) {
                if (place.name.toLowerCase().search(search.replace(/[\/]/g,"").toLowerCase()) != -1) {
                    place.marker.setVisible(true);
                    //place.marker.setAnimation(google.maps.Animation.DROP);
                    return true;
                }
                else {
                    // if marker isn't in the filtered list, hide it
                    place.marker.setVisible(false);
                    return false;
                }
            }, self);
        }
    });
}

function initMap() {
    ko.applyBindings(new AppViewModel());
}

function googleMapsError() {
    alert("Google Maps could not load correctly");
}
