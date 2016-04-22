angular.module('starter.services', [])

.factory('AuthenticationService', function() {
    var auth = {
        isLogged: false
    }

    return auth;
})

//
// .factory('dbMed',function($cordovaSQLite,$rootScope,$http){
//   var dbMed = {};
//   dbMed.select = function(limit,key,value){
//     if(limit)
//       var query = "SELECT * FROM medicine where "+key+" = "+value;
//     var query = "SELECT * FROM medicine";
//     ;
//     $cordovaSQLite.execute($rootScope.db,query).then(function(res){
//       var result = new Array();
//       for(var i=0;i<res.rows.length;i++){
//         result[i]=res.rows.item(i);
//       }
//       return result;
//     },function(err){
//       return false;
//   });};
//
//   dbMed.insert = function(data){
//     var query = "INSERT INTO medicine (name, thumbnail, feature, company ,usage ,taboo ,reaction ,place ,buy_time ,overdue_time ,long_term_use ,purchase_quantity ,residue_quantity) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)";
//   	$cordovaSQLite.execute($rootScope.db,query,data).then(function(res) {
//   			return true;
//   	}, function (err) {
//   			return false;
//   	});
//   }
// })

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
