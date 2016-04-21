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
    };
})

.service('Pharmacy', function($window) {
    var Pharmacy = {};

    Pharmacy.set = function(s) {
       var results = [];
       for (var i=0; i<s.length; i++) {
         var temp = {
           "title": s[i].split("&")[0],
           "address": s[i].split("&")[1]
         }
         results.push(temp);
       }
       $window.localStorage.setItem('results', JSON.stringify(results));
    };
    Pharmacy.get = function() {
      return $window.localStorage.getItem('results');
    };

    return Pharmacy;
})

.service('Hospital', function($window) {
    var Hospital = {};

    Hospital.set = function(s) {
       var results = [];
       for (var i=0; i<s.length; i++) {
         var temp = {
           "title": s[i].split("&")[0],
           "address": s[i].split("&")[1]
         }
         results.push(temp);
       }
       $window.localStorage.setItem('results', JSON.stringify(results));
    };
    Hospital.get = function() {
      return $window.localStorage.getItem('results');
    };

    return Hospital;
})

.service('Preferences', function ($window) {
        var Preferences = {};

        /**
         * 获取配置
         * @param key {String}
         * @returns {*}
         */
        Preferences.get = function (key) {
            return $window.localStorage.getItem(key);
        };


        /**
         * 设定配置
         * @param key {String}
         * @param value {String}
         * @returns {*}
         */
        Preferences.set = function (key, value) {
            return $window.localStorage.setItem(key, value);
        };


        return Preferences;
})

.service('dbMed',function($cordovaSQLite,$rootScope){
  this.select = function(limit,key,value){
    if(limit){
      var query = "SELECT * FROM medicine WHERE "+key+"='"+value+"'";
    }
  else {
      var query = "SELECT * FROM medicine";
  }
  console.log('query',query);
    $cordovaSQLite.execute($rootScope.db,query).then(function(res){
      for(var i=0;i<res.rows.length;i++){
        $rootScope.selectResult[i]=res.rows.item(i);
      }
      return true;
    },function(err){
      return false;
  });};

  this.delete = function(condition){
    var query="DELETE FROM medicine WHERE "+condition;
    console.log('query',query);
    $cordovaSQLite.execute($rootScope.db,query).then(function(res){
      console.log('success',res);
      return true;
    },function(err){
      console.log('error',err);
      return false;
    })
  }

  this.insert = function(data){
    var name=["id","name","thumbnail", "feature", "company" ,"usage" ,"taboo" ,"reaction" ,"place" ,"buy_time" ,"overdue_time" ,"long_term_use" ,"purchase_quantity" ,"residue_quantity"]
    var values=new Array;
    var j=0;
    for (i in name){
      values[j]=data[name[j]];
      j++;
    }
    var query = "INSERT INTO medicine (id,name, thumbnail, feature, company ,usage ,taboo ,reaction ,place ,buy_time ,overdue_time ,long_term_use ,purchase_quantity ,residue_quantity) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)";
  	$cordovaSQLite.execute($rootScope.db,query,values).then(function(res) {
      console.log('res',res);
  			return true;
  	}, function (err) {
  			return false;
  	});
  }
});
