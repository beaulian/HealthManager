angular.module('starter.services', [])

.factory('AuthenticationService', function() {
    var auth = {
        isLogged: false
    }
 
    return auth;
})


.factory('User', function($http) {
    var user = {
        "logged-in": undefined,
        "uid": "",
        "token": ""
    };

    return {
        set: function(key, value) {
            user[key] = value;
        },
        get: function(key) {
            return user[key];
        }
   //      Register: function(postdata) {
   //          return $http({
   //              method: "POST",
   //              url: "http://127.0.0.1:5000/user/register",
   //              data: $.param(postdata),
   //              headers: {'Content-Type': 'application/x-www-form-urlencoded'}
   //          });
   //      },

   //      logIn: function(postdata) {
   //          return $http({
			// 	method: "POST",
			// 	url: "http://127.0.0.1:5000/user/login",
			// 	data: $.param(postdata),
   //              headers: {'Content-Type': 'application/x-www-form-urlencoded'}
			// });
   //      },
 
   //      logOut: function() {
 
   //      }

    };
});