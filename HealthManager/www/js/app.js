// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('ionicApp', ['ionic'])

  .config(function($stateProvider, $urlRouterProvider,$ionicConfigProvider) {

  	$ionicConfigProvider.platform.ios.tabs.style('standard');
  	$ionicConfigProvider.platform.ios.tabs.position('bottom');
  	$ionicConfigProvider.platform.android.tabs.style('standard');
  	$ionicConfigProvider.platform.android.tabs.position('standard');

  	$ionicConfigProvider.platform.ios.navBar.alignTitle('center');
  	$ionicConfigProvider.platform.android.navBar.alignTitle('left');

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
      .state('tabs.facts', {
        url: "/facts",
        views: {
          'home-tab': {
            templateUrl: "templates/facts.html"
          }
        }
      })
      .state('tabs.facts2', {
        url: "/facts2",
        views: {
          'home-tab': {
            templateUrl: "templates/facts2.html"
          }
        }
      })
      .state('tabs.about', {
        url: "/about",
        views: {
          'about-tab': {
            templateUrl: "templates/about.html"
          }
        }
      })
      .state('tabs.navstack', {
        url: "/navstack",
        views: {
          'about-tab': {
            templateUrl: "templates/nav-stack.html"
          }
        }
      })
      .state('tabs.contact', {
        url: "/contact",
        views: {
          'contact-tab': {
            templateUrl: "templates/contact.html"
          }
        }
      });


     $urlRouterProvider.otherwise("/tab/home");

  })

  .controller('HomeTabCtrl', function($scope) {
    console.log('HomeTabCtrl');
      $scope.data = {
        showDelete: false
      };

      $scope.edit = function(item) {
        alert('Edit Item: ' + item.id);
      };
      $scope.share = function(item) {
        alert('Share Item: ' + item.id);
      };

      $scope.moveItem = function(item, fromIndex, toIndex) {
        $scope.items.splice(fromIndex, 1);
        $scope.items.splice(toIndex, 0, item);
      };

      $scope.onItemDelete = function(item) {
        $scope.items.splice($scope.items.indexOf(item), 1);
      };

      $scope.items = [
        { id: 0 ,imgPath:'img/adam.jpg'},
        { id: 1 ,imgPath:'img/ben.png'},
        { id: 2 ,imgPath:'img/ionic.png'},
        { id: 3 ,imgPath:'img/max.png'},
        { id: 4 ,imgPath:'img/mike.png'},
        { id: 5 ,imgPath:'img/perry.png'}
      ];
  });
