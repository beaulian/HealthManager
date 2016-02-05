// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var LoginStatus = false;

angular.module('starter', ['ionic', 'starter.controllers', 'starter.services', 'ngCookies'])

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
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
  });

  $urlRouterProvider.otherwise('/tab/home');


});