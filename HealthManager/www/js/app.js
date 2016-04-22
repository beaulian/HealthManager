// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var LoginStatus = false;
var db = null;
angular.module('starter', ['ionic', 'starter.controllers', 'starter.services', 'ngCookies', 'ngRoute','ngCordova'])

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
})

.run(function($ionicPlatform, $rootScope, $cookieStore, $location, $http, $state, $window,$cordovaSQLite) {
  $rootScope.$on('$stateChangeStart', function(event, toState) {
      if (toState.name == "login" || toState.name == "register") {
          return;
      }
      if (!$window.localStorage.getItem("logged-in")) {
        event.preventDefault();// 取消默认跳转行为
        $state.go("login");
      }

      // if (!$cookieStore.get("tokenState") && $cookieStore.get("token")) {
      //   $http.put("http://10.251.102.89:5000/user/login?uid="+$cookieStore.get("uid")+"&token="+$cookieStore.get("token")).success(function(data){
      //     $cookieStore.remove("token");
      //     $cookieStore.put("token", data["token"], {'expires': 7200});
      //     $cookieStore.put("tokenState", true, {'expires': 7000});
      //   });
      // }
      // console.log($cookieStore.get("token"));



  });

  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard

    // for form inputs)

    if(window.cordova && window.cordova.plugins.Keyboard) {

      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

    }

    if(window.StatusBar) {

      StatusBar.styleDefault();

    }

    //sqlite测试
    $rootScope.selectResult = new Array();
    $rootScope.db = $cordovaSQLite.openDB({name: 'my.db', location: 'default'});
    $cordovaSQLite.execute($rootScope.db, "CREATE TABLE IF NOT EXISTS medicine (id text,name text, thumbnail text, feature text,company text,usage text,taboo text,reaction text,place text,buy_time text,overdue_time text,long_term_use INTEGER,purchase_quantity text,residue_quantity text)");
 //启动极光推送服务

    window.plugins.jPushPlugin.init();

 //调试模式

    window.plugins.jPushPlugin.setDebugMode(true);


    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }

  });
})

.config(function($stateProvider, $urlRouterProvider, $ionicConfigProvider) {

  $ionicConfigProvider.platform.ios.tabs.style('standard');
  $ionicConfigProvider.platform.ios.tabs.position('bottom');
  $ionicConfigProvider.platform.android.tabs.style('standard');
  $ionicConfigProvider.platform.android.tabs.position('bottom');

  $ionicConfigProvider.platform.ios.navBar.alignTitle('center');
  $ionicConfigProvider.platform.android.navBar.alignTitle('center');

  $ionicConfigProvider.platform.ios.backButton.previousTitleText('').icon('ion-ios-arrow-thin-left');
  $ionicConfigProvider.platform.android.backButton.previousTitleText('').icon('ion-android-arrow-back');

  $ionicConfigProvider.platform.ios.views.transition('ios');
  $ionicConfigProvider.platform.android.views.transition('android');


  $stateProvider

  .state('tabs', {
        url: "/tab",
        abstract: true,
        templateUrl: "templates/tabs.html"
  })

  .state('tabs.home', {
    url: "/home",
    views: {
      'home-tab': {
        templateUrl: "templates/home.html",
        controller: 'HomeTabCtrl'
      }
    }
  })

  .state('tabs.remind', {
    url: "/remind",
    views: {
      'remind-tab': {
        templateUrl: "templates/remind.html",
        controller: "RemindCtrl"
      }
    }
  })

  .state('tabs.family', {
    url: "/family",
    views: {
      'family-tab': {
        templateUrl: "templates/family.html",
        controller: "FamilyCtrl"
      }
    }
  })

  .state('tabs.family-member', {
    url:"/member",
    views:{
      'family-tab':{
        templateUrl:'templates/family_member.html',
        controller: "FamilyMemberCtrl"
      }
    }
  })

  // set up abstract state for user
  .state('login', {
    url: '/user/login',
    templateUrl: 'templates/login.html',
    controller: 'LoginCtrl'
  })

  .state('register', {
    url: '/user/register',
    templateUrl: 'templates/register.html',
    controller: 'RegisterCtrl'
  })

  .state('tabs.indexnews', {
    url: "/news/:classf/:id",
    views:{
      'home-tab':{
      templateUrl: 'templates/news.html',
      controller: 'NewsCtrl'
    }
  }
  })

  .state('user', {
    url: '/user/detail',
    templateUrl: 'templates/user.html',
    controller: 'UserCtrl'
  })

  .state('tabs.searchMedicine',{
    url:'/searchMedicine',
    views:{
      'medicine-tab':{
        templateUrl:'templates/search_medicine.html',
        controller:'ExampleController'
      }
    }
  })

  .state('tabs.medicineInfo',{
    url:'/medicineInfo/:id',
    cache:true,
    views:{
      'medicine-tab':{
        templateUrl:'templates/medicine_info.html',
        controller:'InfoCtrl'
      }
    }
  })

  .state('tabs.addMedicine',{
    url:'/addMedicine/:id',
    views:{
      'medicine-tab':{
        templateUrl:'templates/add_medicine.html',
        controller:'addMedCtrl'
      }
    }
  })

  .state('tabs.medicine',{
  	url:'/mymedicine',
    views:{
      'medicine-tab':{
        templateUrl:'templates/my_medicine.html',
        controller:'myMedCtrl'
        }
      }
  })

  .state('tabs.map', {
    url:'/map',
    views: {
        'home-tab':{
<<<<<<< HEAD
            templateUrl:'templates/map.html',
=======
            templateUrl:'templates/map/map.html',
>>>>>>> origin/front_one
            controller:'MapCtrl'
        }
    }
  });

  $urlRouterProvider.otherwise('/tab/home');


});
