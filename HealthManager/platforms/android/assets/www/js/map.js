 //创建自定义控件
function GeolocationControl() {
  this.defaultAnchor = BMAP_ANCHOR_BOTTOM_LEFT;
  this.defaultOffset = new BMap.Size(10, 40);
}
GeolocationControl.prototype = new BMap.Control();
GeolocationControl.prototype.initialize = function(map) {
  var div = document.createElement("div");
  var span = document.createElement("span");

  div.style.width = "26px";
  div.style.height = "26px";
  div.style.overflow = "hidden";
  div.style.backgroundColor = "rgba(255,255,255,0.8)";
  div.style.textAlign = "center";
  div.style.lineHeight = "26px";

  span.style.width = "14px";
  span.style.height = "14px";
  span.style.verticalAlign = "middle";
  span.style.display = "inline-block";
  span.style.background = "url(img/map/baiduGeo.png)";
  span.style.backgroundSize = "76px,auto";

  div.appendChild(span);

  span.onclick = function(e) {
    map.panTo(new BMap.Point(longitude, latitude));
  }
  map.getContainer().appendChild(div);
  return div;
}


angular.module("starter.map", ['ionic'])


.controller("MapPharmacyCtrl", function($scope, $window, $state, $ionicActionSheet, $timeout) {

  $scope.chooseTypeButtonClick = function() {
      $state.go('tabs.mapHospital', {reload: true});
  }

})

.controller("MapHospitalCtrl", function($scope, $window, $state, $ionicActionSheet, $timeout) {

  $scope.chooseTypeButtonClick = function() {
    $state.go('tabs.mapPharmacy', {reload: true});
  }

})

.controller("MapListCtrl", function($scope, Pharmacy, Hospital) {
  $scope.results = Pharmacy.get();
  alert($scope.results);
})

.directive('appMapPharmacy', function(Pharmacy) {
    return {
        restrict: "AE",
        replace: true,
        template: "<div id='initMapPharmacy'></div>",
        scope: {

        },
        link: function(scope, element, attrs) {
            var map;
            baidu_location.getCurrentPosition(function(position) {
              var position = eval("(" + position + ")");
              var longitude = position.lontitude;
              var latitude = position.latitude;

              var point = new BMap.Point(longitude, latitude);
              map = new BMap.Map("initMapPharmacy");
              map.centerAndZoom(point, 15);

              map.enableScrollWheelZoom();    //允许鼠标滚动
              map.addControl(new GeolocationControl());
              map.addControl(new BMap.NavigationControl());  //添加默认缩放平移控件
              map.addControl(new BMap.ScaleControl());       // 添加默认比例尺控件
              map.addControl(new BMap.MapTypeControl({mapTypes: [BMAP_NORMAL_MAP,BMAP_HYBRID_MAP]}));     //2D图，卫星图

              //创建标注
              var marker = new BMap.Marker(point);
              map.addOverlay(marker);              // 将标注添加到地图中

            //本地搜索
            var options = {
               renderOptions:{
                 map: map,
                 autoViewport: true,
                 selectFirstResult: false
               },
               onSearchComplete: function(results){
                  if (local.getStatus() == BMAP_STATUS_SUCCESS){
                    // 判断状态是否正确
                    var s = [];
                    for (var i = 0; i < results.getCurrentNumPois(); i ++){
                      s.push(results.getPoi(i).title + "&" + results.getPoi(i).address);
                    }
                    Pharmacy.set(s);
                  }
                }
              };
              var local = new BMap.LocalSearch(map, options);
              local.searchInBounds("药店", map.getBounds());

            }, function(error) {
              alert(error);
            });

        }
    };
})

.directive('appMapHospital', function(Hospital, $rootScope) {
    return {
        restrict: "AE",
        replace: true,
        template: "<div id='initMapHospital'></div>",
        scope: {
        },
        link: function(scope, element, attrs) {
            var map;
            baidu_location.getCurrentPosition(function(position) {
              var position = eval("(" + position + ")");
              var longitude = position.lontitude;
              var latitude = position.latitude;

              var point = new BMap.Point(longitude, latitude);
              map = new BMap.Map("initMapHospital");
              map.centerAndZoom(point, 15);

              map.enableScrollWheelZoom();    //允许鼠标滚动
              map.addControl(new GeolocationControl());
              map.addControl(new BMap.NavigationControl());  //添加默认缩放平移控件
              map.addControl(new BMap.ScaleControl());       // 添加默认比例尺控件
              map.addControl(new BMap.MapTypeControl({mapTypes: [BMAP_NORMAL_MAP,BMAP_HYBRID_MAP]}));     //2D图，卫星图

              //创建标注
              var marker = new BMap.Marker(point);
              map.addOverlay(marker);              // 将标注添加到地图中

            //本地搜索
            var options = {
               renderOptions:{
                 map: map,
                 autoViewport: true,
                 selectFirstResult: false
               },
               onSearchComplete: function(results){
                  if (local.getStatus() == BMAP_STATUS_SUCCESS){
                    // 判断状态是否正确
                    var s = [];
                    for (var i = 0; i < results.getCurrentNumPois(); i ++){
                      s.push(results.getPoi(i).title + "&" + results.getPoi(i).address);
                    }
                    Hospital.set(s);
                  }
                }
              };
              var local = new BMap.LocalSearch(map, options);
              local.searchInBounds("医院", map.getBounds());

            }, function(error) {
              alert(error);
            });

        }
    };
})

.directive('hideTabs', function($rootScope) {
    return {
        restrict: 'A',
        link: function($scope, $el) {
            $rootScope.hideTabs = true;
            $scope.$on('$destroy', function() {
                $rootScope.hideTabs = false;
            });
        }
    };
});

