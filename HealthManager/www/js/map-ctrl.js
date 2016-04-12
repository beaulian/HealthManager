angular.module('starter.controllers', [])

.controller("MapCtrl", function($scope, $window) {

})

.directive('appMap', function() {
    return {
        restrict: "E",
        replace: true,
        template: "<div id='initMap'></div>",
        scope: {
            center: "=",
            
        }
    }
})