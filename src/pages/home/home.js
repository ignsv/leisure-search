import app from 'index';

class HomePage {
    static factory(...injections) {
        return new HomePage(...injections);
    }

    constructor($http) {
        this.$http = $http;
        this.categories = []
        this.near = {
            minRank: 1
        };
        this.map = {
            center: {
              latitude: 45,
              longitude: -73
            },
            zoom: 14
        };
        this.userMarker = {
          id: 0,
          options: {
              visible: false,
              draggable: false
          },
          label: 'Y'
        };
        this.nearPlace = {
          id: 100000000000,
          options: {
            visible: false,
            draggable: true
          },
          label: 'N'
        };
        this.inRadius = [];
        this.circle = {
          stroke: {
              color: '#08B21F',
              weight: 2,
              opacity: 1
          },
          fill: {
              color: '#08B21F',
              opacity: 0.3
          },
        };

        this.getCategories(this.$http);
        this.getUserLocation();
    }

    getCategories($http) {
        $http({
            method: 'GET',
            url: 'http://localhost:8000/api/leisure/category/',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage.getItem('token')
            }
        }).then(response => {
            this.categories = response.data.results;
        });
    }

    getUserLocation() {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
                this.map.center = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                this.userMarker.coords = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                }
                this.userMarker.options.visible = true;
                this.map.zoom = 17;
            }, this.handleLocationError(false, this.infoWindow, this.map.center));
        } else {
            // Browser doesn't support Geolocation
            this.handleLocationError(false, this.infoWindow, this.map.center);
        }
    }

    handleLocationError(browserHasGeolocation, infoWindow, pos) {
        console.log('Error');
    }

    findNearestPlace($http, coords, query) {
        $http({
            method: 'POST',
            url: 'http://localhost:8000/api/leisure/search/closer',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage.getItem('token')
            },
            data: {
                category: query.category,
                rank_for_search: query.minRank,
                latitude_start_search: coords.latitude.toFixed(10),
                longitude_start_search: coords.longitude.toFixed(10)
            }
        }).then(response => {
            this.nearPlace = {
                id: response.data.id,
                coords: {
                    latitude: response.data.latitude,
                    longitude: response.data.longitude
                },
                options: {
                    visible: true,
                    draggable: false
                },
                label: 'N',
                data: {
                  id: response.data.id,
                  address: response.data.address,
                  categories: response.data.categories,
                  city: response.data.city,
                  name: response.data.name,
                  photo: response.data.photo
                }
            };
        });
    }

    findInRadius($http, coords, query) {
        $http({
            method: 'POST',
            url: 'http://localhost:8000/api/leisure/search/radius',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage.getItem('token')
            },
            data: {
                radius: query.radius,
                category: query.category,
                rank_for_search: query.minRank,
                latitude_start_search: coords.latitude.toFixed(10),
                longitude_start_search: coords.longitude.toFixed(10)
            }
        }).then(response => {
            this.inRadius = [];
            for (let i = 0; i < response.data.results.length; i++) {
                $http({
                    method: 'GET',
                    url: 'http://localhost:8000/api/leisure/institution/' + response.data.results[i] + '/',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Token ' + localStorage.getItem('token')
                    }
                }).then(res => {
                    this.inRadius.push({
                        id: res.data.id,
                        coords: {
                            latitude: res.data.latitude,
                            longitude: res.data.longitude
                        },
                        options: {
                            visible: true,
                            draggable: false
                        },
                        name: res.data.name,
                        photo: res.data.photo,
                        city: res.data.city.name,
                        address: res.data.address,
                        categories: res.data.categories
                    });
                });
            }
        });
    }

    getInfo(place) {
        this.id = place.id;
        var categories = '';
        for (let i = 0; i < place.categories.length; i++) {
            if (i > 0) {
                categories += ', '
            }
            categories += place.categories[i].name;
        }
        $('#placeModal').modal('show');
        $('#modalId').text(place.id).hide();
        $('#modalName').text(place.name);
        $('#modalCity').text(place.city.name);
        $('#modalAddress').text(place.address);
        $('#modalCategory').text(categories);
        document.getElementById('modalPhoto').src = 'http://localhost:8000' + place.photo;
    }

    setRank($http, rank) {
        $http({
            method: 'POST',
            url: 'http://localhost:8000/api/leisure/create/like',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage.getItem('token')
            },
            data: {
                institution: document.getElementById('modalId').innerText,
                rank: rank
            }
        })
    }
}

HomePage.factory.$inject = [
    '$http'
];

export default app.component('homePage', {
    templateUrl: 'pages/home/home.html',
    controller: HomePage.factory
});
