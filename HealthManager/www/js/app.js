// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var LoginStatus = false;

angular.module('starter', ['ionic', 'starter.controllers', 'starter.services', 'ngCookies', 'ngRoute'])

.run(function($ionicPlatform, $rootScope, $cookieStore, $location, $http, $state) {
  $rootScope.$on('$stateChangeStart', function(event, toState) {
      if (toState.name == "login") {
          return;
      }
      if (!$cookieStore.get("logged-in")) {
        event.preventDefault();// 取消默认跳转行为
        $state.go("login");
      }
    // }else {
    //   if (!$cookieStore.get("tokenState") && $cookieStore.get("token")) {
    //     $http.put("http://127.0.0.1:5000/user/login?uid="+$cookieStore.get("uid")+"&token="+$cookieStore.get("token")).success(function(data){
    //       $cookieStore.remove("token");
    //       $cookieStore.put("token", data["token"], {'expires': 7200});
    //       $cookieStore.put("tokenState", true, {'expires': 7000});
    //     });
    //   }
  });

  $ionicPlatform.ready(function() {
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

.config(function($stateProvider, $urlRouterProvider) {

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
        templateUrl: "templates/remind.html"
      }
    }
  })

  .state('tabs.family', {
    url: "/family",
    views: {
      'family-tab': {
        templateUrl: "templates/family.html"
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

  .state('indexnews', {
    url: "/news/:classf/:id",
    templateUrl: 'templates/news.html',
    controller: 'NewsCtrl' 
  })

  .state('user', {
    url: '/user/detail',
    templateUrl: 'templates/user.html',
    controller: 'UserCtrl'
  });

  $urlRouterProvider.otherwise('/tab/home');


});