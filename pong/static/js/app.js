var app = angular.module('Pong', ['ngRoute','ui.bootstrap']);

app.config(function($interpolateProvider, $routeProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';


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
            if ($scope.player.username.indexOf('_') > -1) {
                $scope.alerts.push({
                    'type': 'warning',
                    'msg': 'Underscores in usernames and league names are currently blowing some things up. Be cool about it'
                });
                return;
            }
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
            if ($scope.league_name.indexOf('_') > -1) {
                $scope.league_alert.push({
                    'type': 'warning',
                    'msg': 'Underscores in usernames and league names are currently blowing some things up. Be cool about it'
                });
                return;
            }
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
        var old_ranks = [];
        var new_ranks = [];

        initialize = function() {
            $scope.league_name = $routeParams.league_name;

            $http.get('api/leagues/' + $scope.league_name).success(
                function (resp) {
                    $scope.players = resp;
                }
            );

            $http.get('api/leagues/games/' + $scope.league_name + '/')
            .success(
                function(resp) {
                    $scope.games = resp;
                }
            );
        };

        makeNewRanks = function() {
            new_ranks = angular.copy($scope.players);

            new_ranks.sort(function(a,b) {
                return b['rating']-a['rating']
            });
        };

        makeOldRanks = function() {
            old_ranks = angular.copy($scope.players);
            old_ranks.sort(function(a,b) {
                return b['rating']-a['rating'];
            });
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

        slackIt = function(winner, loser) {
            //determine a message by getting relative positions
            var old_win_pos, win_pos, old_lose_pos, lose_pos;

            //I should really do sorting or the b/e but whatever..
//            var new_ranks = $scope.players;
//            new_ranks.sort(function(a,b) {
//                return b['rating']-a['rating']
//            });

            for(var i = 0; i < old_ranks.length; i++) {
                if(old_ranks[i].username === winner) {
                    old_win_pos = i+1;
                    continue;
                }

                if(old_ranks[i].username === loser) {
                    old_lose_pos = i+1;
                }
            }

            for(var j = 0; j < new_ranks.length; j++) {
                if(new_ranks[j].username === winner) {
                    win_pos = j+1;
                    continue;
                }
                if(new_ranks[j].username === loser) {
                    lose_pos = j+1;
                }
            }

            var data =  {
                'old_winner_pos': old_win_pos,
                'old_loser_pos': old_lose_pos,
                'winner_pos': win_pos,
                'loser_pos': lose_pos,
                'win_user': winner,
                'lose_user': loser
            };

            var message = determineAwesomeMessage(data, new_ranks);

            message = message + ' -> <http://pong-app.io/#/league/marvel-pong/|Rankings!>';
            var hook = 'https://hooks.slack.com/services/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';

            $http.post('api/slack-it/', { "hook": hook, "msg": message});
        };

        determineAwesomeMessage = function(data, new_ranks) {
            var msg = '';
            var p = old_ranks.length - 1;
            var x = Math.floor((Math.random() * 2) + 1);

            //if 1st place now different
            if(old_ranks[0].username !== new_ranks[0].username) {
                //if 1st place lost
                if(data['lose_user'] === old_ranks[0].username) {
                    msg = data['lose_user']
                        + ' crumbles under pressure from '
                        + data['win_user']
                        + ' to give '
                        + new_ranks[0].username
                        + ' the top spot';
                }
                else {
                    //if other place overtook 1st
                    msg = data['win_user']
                        + ' sweeps '
                        + data['lose_user']
                        + ' aside to take the top spot from '
                        + old_ranks[0].username
                        + '. The rankings are heating up.';
                }
            }
            //if last place is now different
            else if (old_ranks[p].username !== new_ranks[p].username) {
                //did lower move themselves up ?
                if (old_ranks[p].username === data['win_user']) {
                     msg = data['win_user']
                        + ' with an unanticipated win over '
                        + data['lose_user']
                        + '. Sending '
                        + new_ranks[p].username
                        + 'to the bottom. Its a dogfight down there!';
                }
                //did lower lose and move to the bottom
                else {
                    msg = data['win_user']
                        + ' held no prisoners against'
                        + data['lose_user']
                        + ' and sends him right into the gutter of the league';
                }

            //lower beat upper
            } else if(data['old_winner_pos'] > data['old_loser_pos']) {
                if (x === 1) {
                    msg = data['win_user']
                        + ' pulls off a magnificent victory against '
                        + data['lose_user']
                        + '. The bookies had him at 60/1 to win today.';
                } else {
                    msg = data['win_user']
                        + ' rope-a-dopes '
                        + data['lose_user']
                        + ' to a magnificent victory.'
                }
            //upper beat lower
            } else {
                if (data['old_winner_pos'] > data['winner_pos']) {
                    if (x === 1) {
                        msg = 'Routine victory from '
                            + data['win_user']
                            + ' against '
                            + data['lose_user']
                            + '. '
                            + new_ranks[data['win'] - 1].username
                            + ' will nervous after that result.'
                    } else {
                        msg = 'Its all change in the rankings after '
                            + data['win_user']
                            + ' claims victory over '
                            + data['loser_user']
                    }
                } else {
                    if (x === 1) {
                        msg = data['win_user']
                            + ' solidifies the number '
                            + data['winner_pos']
                            + ' spot by beating '
                            + data['lose_user']
                            + ' who is now in spot '
                            + data['loser_pos'];
                    } else if (data['old_winner_pos'] === 1 && data['winner_pos'] === 1) {
                        msg = data['win_user']
                            + ' defends the top spot against '
                            + data['lose_user']
                            + ', to become undisputed. Who can stop the lad ?!'
                    } else {
                        msg = 'Im not sure the fans expected anything else as '
                            + data['win_user']
                            + ' beats '
                            + data['lose_user']
                            + '. ' + new_ranks[data['loser_pos']-1].username
                            + ' will be happy with that result.'
                    }
                }
            }

            return msg;
        };

        $scope.addNewGame = function() {
            var data = {
                'loser' : $scope.loser.username,
                'league_name': $scope.league_name
            };

            $http.post('api/leagues/games/', data)
            .success(
                function(resp) {
                    makeOldRanks();
                    $http.get('api/leagues/' + $scope.league_name).success(
                        function (resp) {
                            $scope.players = resp;
                            makeNewRanks();
                            slackIt($scope.$parent.currentUser.username, data['loser'])
                        }
                    );

                    $http.get('api/leagues/games/' + $scope.league_name + '/')
                    .success(
                        function(resp) {
                            $scope.games = resp;
                        }
            );
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