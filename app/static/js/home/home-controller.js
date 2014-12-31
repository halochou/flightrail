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

        $scope.newFlight.airport = $scope.selectedAirport;
        // console.log($scope.newFlight);

        $http.get('/flight',{params: $scope.newFlight}).
        success(function(data, status, headers, config) {
            // console.log(data)
            $scope.flights.push({
                row  : $scope.flights.length+1,
                time : data.time,
                port : data.port,
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
