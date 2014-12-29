angular.module('FlightRailsPlan')
  .controller('HomeController', ['$scope','$http', function ($scope, $http) {
    $scope.flights = [];
    $scope.airports = [];
    $scope.selectedAirport = '';

    $http.get('/airports').
    success(function(data, status, headers, config) {
        //console.log(data);
        $scope.airports = data.airports;

    });

    $scope.onAdd = function () {

        //console.log($scope.selectedAirport);
        $http.get('/flight',{params: {
            hour: $scope.newFlight.hour,
            minute: $scope.newFlight.minute,
            port: $scope.newFlight.port,
            airport: $scope.selectedAirport
        }}).
        success(function(data, status, headers, config) {
            // console.log(data)
            $scope.flights.push({
                row  : $scope.flights.length+1,
                time : data.time,
                port : data.port,
                type : 'A320',
                action : data.action,
                cost : data.cost + ' s'
            });
            // this callback will be called asynchronously
            // when the response is available
          }).
        error(function(data, status, headers, config) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });



        //console.log($scope.flights);
    };

  }]);
