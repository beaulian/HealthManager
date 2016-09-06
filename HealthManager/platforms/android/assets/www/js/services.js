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

.factory('Pusher', function ($cordovaDialogs, $window) {
  var pusher = null;

  return {
    onReceiveMessage: function (event) {
      if(pusher){
        $cordovaDialogs.alert(pusher.receiveMessage.message);
      }
    },
    onOpenNotification: function (event) {
      var alert = null;
      if(pusher && pusher.openNotification.alert){
        alert = pusher.openNotification.alert;
      }else{
        alert = event.aps.alert;
      }
      $cordovaDialogs.alert(alert);
    },
    onReceiveNotification: function (event) {
      $cordovaDialogs.alert(event);
    },
    getRegistradionID: function () {
      return $window.localStorage.getItem('jPushID', null);
    },
    init: function () {
      if (window.plugins && window.plugins.jPushPlugin) {
        pusher = window.plugins.jPushPlugin;
        // 初始化
        pusher.init();
        // 获取注册ID
        pusher.getRegistrationID(function (id) {
          $window.localStorage.setItem('jPushID', id);
        });
        // 设置
        plugins.jPushPlugin.setDebugMode(true);
//        plugins.jPushPlugin.openNotificationInAndroidCallback = notificationCallback;
//        plugins.jPushPlugin.receiveNotificationIniOSCallback = notificationCallback;
      }
    }
  };
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
});
