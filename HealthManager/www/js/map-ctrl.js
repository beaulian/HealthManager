<<<<<<< HEAD
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
=======
var map = new BMap.Map("initMap");
map.centerAndZoom(new BMap.Point(116.404, 39.915), 14);
>>>>>>> origin/front_one
