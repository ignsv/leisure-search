import app from 'index';

class HomePage {
    static factory(...injections) {
        return new HomePage(...injections);
    }

    constructor($scope) {
        this.$scope = $scope;



        this.init();
    }

    init() {
        this.map = {
          center: {
            latitude: 49.2265996,
            longitude: 28.4545255
          },
          zoom: 14,
          styles: {
            featureType: "poi",
            elementType: "labels",
            stylers: [
              { visibility: "off" }
            ]
          }
        };

        const infoWindow = new google.maps.InfoWindow;

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
              this.map.center = {
                  latitude: position.coords.latitude,
                  longitude: position.coords.longitude
              };

              this.currentCoords = {
                  latitude: position.coords.latitude,
                  longitude: position.coords.longitude
              };

              infoWindow.setPosition(pos);
              infoWindow.setContent('Location found.');
              infoWindow.open(this.map);
              this.map.setCenter(pos);
            }, () => {
              handleLocationError(true, infoWindow, this.map.getCenter());
            });
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, this.map.getCenter());
        }

    }
}

HomePage.factory.$inject = [
    '$scope'
];

export default app.component('homePage', {
    templateUrl: 'pages/home/home.html',
    controller: HomePage.factory
});
