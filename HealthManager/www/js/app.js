// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var LoginStatus = false;

angular.module('starter', ['ionic', 'starter.controllers', 'starter.directives', 'starter.services', 'ngCookies', 'ngRoute','ngCordova'])

.run(function($ionicPlatform, $rootScope, $cookieStore, $location, $http, $state, $window) {
  $rootScope.$on('$stateChangeStart', function(event, toState) {
      if (toState.name == "login" || toState.name == "register") {
          return;
      }
      if ($window.localStorage.getItem("logged-in")) {
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

 //启动极光推送服务

//    window.plugins.jPushPlugin.init();

 //调试模式

//    window.plugins.jPushPlugin.setDebugMode(true);


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

  .state('tabs.addMedicine',{
    url:'/addMedicine',
    views:{
      'medicine-tab':{
        templateUrl:'templates/add_medicine.html',
        controller:'ExampleController'
      }
    }
  })

  .state('tabs.medicineInfo',{
    url:'/medicineInfo',
    views:{
      'medicine-tab':{
        templateUrl:'templates/medicine_info.html'
      }
    }
  })

  .state('tabs.medicine',{
  	url:'/mymedicine',
    views:{
      'medicine-tab':{
              templateUrl:'templates/my_medicine.html'
            }
      }
  })

  .state('tabs.map', {
    url:'/map',
    views: {
        'home-tab':{
            templateUrl:'templates/map.html',
            controller:'MapCtrl'
        }
    }
  });

  $urlRouterProvider.otherwise('/tab/home');


});
