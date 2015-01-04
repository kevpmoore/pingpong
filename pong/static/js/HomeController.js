//app.controller('GreetingController', ['$scope', 'RestAngular', '$log', function($scope, RestAngular, $log) {

//    $scope.createNewUser = function() {
//        $log("called");
//        var user = {
//            'username' : $scope.username,
//            'pass' : $scope.pass,
//            'email' : $scope.email
//        };
//
//        RestAngular.post('api/new-player/', user).then(function(resp) {
//            //deal with response and errors here
//        });
//    }
//}]);

//app.controller('GreetingController', ['$scope', function($scope) {
//  $scope.greeting = 'Hola!';
//}]);