var app = angular.module('MarvelPong', ['ngRoute','ui.bootstrap']);

app.config(function($interpolateProvider, $routeProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'

    $routeProvider
        .when('/', {controller: 'RegisterController', templateUrl: 'static/partials/register.html'})
        .when('/leagues/', {controller: 'LeaguesController', templateUrl: 'static/partials/leagues_list.html'})
        .when('/league/:league_name/', {controller: 'RankingsController', templateUrl: 'static/partials/rankings.html'})
        .when('/login/', {controller: 'LoginController', templateUrl: 'static/partials/login.html'})
        .when('/join-league/', {controller: 'JoinLeagueController', templateUrl: 'static/partials/join_league.html'})
        .when('/create-league/', {controller: 'CreateLeagueController', templateUrl: 'static/partials/create_league.html'})
        .when('/faq/', {controller: '', templateUrl: 'static/partials/faq.html'})
        .when('/league/:league_name/:username/', {controller: 'StatsController', templateUrl: 'static/partials/player-stats.html'})
        .otherwise({redirectTo: '/'});
});

app.controller('RegisterController', ['$scope', '$http', '$location',
    function($scope, $http, $location) {
        $scope.alerts = [];

        $scope.player = {
            email: "",
            password: "",
            username: ""
        };

        initialize = function() {
            $http.get('api/login/').success(
                function(resp) {
                    if(resp['state']) {
                        $location.url('/leagues/');
                    }
                }
            )
        };

        $scope.login = function() {
            $http.post('api/new-player/', $scope.player).success(
                function(resp) {
                    $scope.$parent.currentUser = resp;
                    $location.url('/leagues/');
                }
            ).error(
                function(resp) {
                    $scope.alerts = resp;
                }
            );
        };

        $scope.closeAlert = function(index) {
            $scope.alerts.splice(index, 1);
        };

        initialize();
    }
]);

app.controller('LoginController', ['$scope', '$http', '$location',
    function($scope, $http, $location) {
        $scope.username = "";
        $scope.password = "";
        $scope.alerts = [];

        initialize = function() {
            $http.get('api/login/').success(
                function(resp) {
                    if(resp['state']) {
                        $location.url('/leagues/');
                    }
                }
            )
        };

        $scope.login = function() {
            var data = {
                'username': $scope.username,
                'password': $scope.password
            };

            $http.post('api/login/', data).success(
                function(resp) {
                    $scope.$parent.currentUser = resp;
                    $location.url('/leagues/');
                }
            ).error(
                function(resp) {
                    $scope.alerts = resp;
                }
            );
        };

        $scope.closeAlert = function(index) {
            $scope.alerts.splice(index, 1);
        };

        initialize();
    }
]);

app.controller('LeaguesController', ['$scope', '$http', '$location',
    function($scope, $http, $location) {
        $scope.leagues = [];
        $scope.invites = [];


        $scope.alerts = [];

        initialize = function() {
            $http.get('api/leagues/').success(
                function (resp) {
                    $scope.leagues = resp;
                }
            );

            $http.get('api/invite/action/').success(
                function (resp) {
                    $scope.invites = resp
                }
            );

        };

        $scope.actionInvite = function(invite, action) {
            var data = {
                invite_id: invite.id,
                action: action,
                league_name: invite.league_name
            };

            $http.post('api/invite/action/', data)
            .success(
                function(resp) {
                    for(var i = 0; i < $scope.invites.length; i++) {
                        if (invite.id === $scope.invites[i].id) {
                            $scope.invites.splice(i, 1);
                        }
                    }
                    initialize();
                }
            ).error(
                function(resp) {
                    $scope.alerts = resp;
                    initialize();
                }
            );
        };

        $scope.goToJoin = function() {
            $location.url('/join-league/');
        };

        $scope.goToCreate = function() {
            $location.url('/create-league/');
        };

        $scope.goToLeague = function(league_name) {
            $location.url('/league/' + league_name + '/');
        };

        initialize();
    }
]);

app.controller('CreateLeagueController', ['$scope', '$http', '$location',
    function($scope, $http, $location) {
        $scope.league_name = '';
        $scope.league_pass = '';
        $scope.league_alert = [];


        $scope.createNewLeague = function() {
            var data = {
                'league_name': $scope.league_name,
                'league_pass': $scope.league_pass
            };

            $http.post('api/leagues/', data).success(
                function(resp) {
                    //forward on to league
                    $location.url('/league/' + $scope.league_name + '/')
                }
            ).error(
                function(resp) {
                    $scope.league_alert = resp;
                }
            )
        };

        $scope.closeAlert = function(index) {
            $scope.alerts.splice(index, 1);
        };
    }
]);

app.controller('JoinLeagueController', ['$scope', '$http', '$location',
    function($scope, $http, $location) {
        $scope.join_league_name = '';
        $scope.join_league_pass = '';
        $scope.join_league_alert = [];

        $scope.joinLeague = function() {
            var data = {
                'league_name': $scope.join_league_name,
                'league_pass': $scope.join_league_pass
            };

            $http.post('api/leagues/join/', data)
            .success(
                function(resp) {
                    $scope.join_league_name = '';
                    $scope.join_league_pass = '';
                    $scope.join_league_alert = resp;
                    $location.url('/leagues/')
                }
            ).error(
                function(resp) {
                    $scope.join_league_alert = resp;
                }
            )
        };

        $scope.closeJoinAlert = function(index) {
            $scope.join_league_alert.splice(index, 1);
        };
    }
]);

app.controller('ApplicationController', ['$scope', '$http',
    function($scope, $http) {
        $scope.currentUser = null;

        initialize = function() {
            $http.get('api/login/').success(
                function(resp) {
                    $scope.currentUser = resp;
                }
            );
        };

        initialize();
    }
]);

app.controller('StatsController', ['$scope', '$http', '$location', '$routeParams',
    function($scope, $http, $location, $routeParams) {
        $scope.stats = null;
        $scope.league_name = '';

        initialize = function() {
            $scope.league_name = $routeParams.league_name;
            var username = $routeParams.username;

            $http.get('api/leagues/' + $scope.league_name + '/' + username + '/')
            .success(
                function(resp) {
                    $scope.stats = resp;
                }
            );
        };

        $scope.back = function() {
            $location.url('/league/' + $scope.league_name + '/');
        };
        initialize();
    }
]);

app.controller('NavBarController', ['$scope', '$http', '$location',
    function($scope, $http, $location) {

        $scope.logout = function() {
            $http.post('api/logout/', {})
            .success(
                function(resp) {
                    $scope.$parent.currentUser = null;
                    $location.url('/login/');
                }
            )
        };
    }
]);

app.controller('RankingsController', ['$scope', '$http', '$location', '$routeParams',
    function($scope, $http, $location, $routeParams) {

        $scope.players = [];
        $scope.games = [];
        $scope.loser = "";
        $scope.league_name = "";
        $scope.invited_user = "";
        $scope.game_alerts = [];
        $scope.invite_alerts = [];
//        $scope.loggedInUser = "";

        initialize = function() {
            $scope.league_name = $routeParams.league_name;

            $http.get('api/leagues/' + $scope.league_name).success(
                function (resp) {
                    $scope.players = resp;
                }
            );

//            $http.get('api/login/').success(
//                function(resp) {
//                    $scope.loggedInUser = resp['username'];
//                }
//            );

            $http.get('api/leagues/games/' + $scope.league_name + '/')
            .success(
                function(resp) {
                    $scope.games = resp;
                }
            );
        };

        $scope.sendInvite = function() {
            var data = {
                'league_name': $scope.league_name,
                'invited_user': $scope.invited_user
            };
            $http.post('api/invite/new/', data)
            .success(
                function(resp) {
                    $scope.invite_alerts = resp;
                }
            ).error(
                function(resp) {
                    $scope.invite_alerts = resp;
                }
            );
        };

        $scope.addNewGame = function() {
            var data = {
                'loser' : $scope.loser.username,
                'league_name': $scope.league_name
            };

            $http.post('api/leagues/games/', data)
            .success(
                function(resp) {
                    initialize();
                    $scope.game_alerts = resp;
                }
            )
            .error(
                function(resp) {
                    $scope.game_alerts = resp;
                }
            );
        };

        $scope.goToStats = function(username) {
            $location.url('/league/' + $scope.league_name + '/' + username + '/');
        };

        $scope.closeGameAlert = function(index) {
            $scope.game_alerts.splice(index, 1);
        };

        $scope.closeInviteAlert = function(index) {
            $scope.invite_alerts.splice(index, 1);
        };

        initialize();
    }
]);