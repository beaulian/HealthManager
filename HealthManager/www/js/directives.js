angular.module('starter.directives', [])

.directive('appMap', function() {
    return {
        restrict: "E",
        replace: true,
        template: "<div id='initMap'></div>",
        scope: {},
        link: function(scope, element, attrs) {
            var map;
            var point = new BMap.Point(116.404, 39.915);
            map = new BMap.Map("initMap");
            map.centerAndZoom(point, 14);
            map.enableScrollWheelZoom();
            var marker = new BMap.Marker(point);        // 创建标注
            map.addOverlay(marker);

            marker.addEventListener("click", function(){
             alert("您点击了标注");
            });

        }
    };
});
