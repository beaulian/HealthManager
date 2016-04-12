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

            function addMarker(point, index) {
                var myIcon = new BMap.Icon("http://api.map.baidu.com/images/marker_red_sprite.png",
                                        new BMap.Size(23,25), {
                                          offset: new BMap.size(10,25),
                                          imageOffset: new BMap.Size(0, 0-index*25)
                             });
                var marker = new BMap.Marker(point, {icon: myIcon});
                map.addOverlay(marker);
            }

            var bounds = map.getBounds();
            var lngSpan = bounds.maxX - bounds.minX;
            var latSpan = bounds.maxY - bounds.minY;
            for (var i = 0; i < 10; i ++) {
                var point = new BMap.Point(bounds.minX + lngSpan * (Math.random() * 0.7 + 0.15),
                bounds.minY + latSpan * (Math.random() * 0.7 + 0.15));
                addMarker(point, i);
            }
        }
    };
});