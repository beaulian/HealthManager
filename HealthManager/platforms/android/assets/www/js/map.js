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


.controller("MapCtrl", function($scope, $window, $ionicLoading, Pharmacy, Hospital, $ionicActionSheet, Preferences, $timeout) {
  $scope.Style = "width:100%;height:100%;";

  var chooseType = function(type) {

    if (!type && Preferences.get('type')) {
      type = Preferences.get('type');
    }
    Preferences.set('type', type);

    switch(type) {
      case 1:
        $scope.service = Pharmacy;
        $scope.describe = "药店";
        break;
      case 2:
        $scope.service = Hospital;
        $scope.describe = "医院";
        break;
      default:
        $scope.service = Pharmacy;
        $scope.describe = "药店";
        break;
    }
  }
   chooseType(1);

  $scope.chooseTypeButtonClick = function() {
      var hideSheet = $ionicActionSheet.show({
        buttons: [
            { text: '医院' },
            { text: '药店' },
        ],
        titleText: '选择您的想查询的类型',
        cancelText: '取消',
        cancel: function () {
            // Nothing to do
        },
        buttonClicked: function (index) {
            chooseType(index + 1);
            return true;
        }
      });

      $timeout(function() {
          hideSheet();
      }, 2000);
  }

})

.controller("MapListCtrl", function($scope, Pharmacy) {
  $scope.results = Pharmacy.get();
  alert($scope.results);
})

.directive('appMap', function() {
    return {
        restrict: "AE",
        replace: true,
        template: "<div id='initMap'></div>",
        scope: {
          service: "@",
          describe: "@"
        },
        link: function(scope, element, attrs) {
            var map;
            baidu_location.getCurrentPosition(function(position) {
              console.log(scope.service);

              var position = eval("(" + position + ")");
              var longitude = position.lontitude;
              var latitude = position.latitude;

              var point = new BMap.Point(longitude, latitude);
              map = new BMap.Map("initMap");
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
                    console.log(results);
                    var s = [];
                    for (var i = 0; i < results.getCurrentNumPois(); i ++){
                      s.push(results.getPoi(i).title + "&" + results.getPoi(i).address);
                    }
                    scope.service.set(s);
                  }
                }
              };

              var local = new BMap.LocalSearch(map, options);
              local.searchInBounds(scope.describe, map.getBounds());

            }, function(error) {
              alert(error);
            });

        }
    };
})

.directive('hideTabs', function($rootScope) {
    return {
        restrict: 'A',
        link: function(scope, element, attributes) {
            scope.$on('$ionicView.beforeEnter', function() {
                scope.$watch(attributes.hideTabs, function(value){
                    $rootScope.hideTabs = value;
                });
            });

            scope.$on('$ionicView.beforeLeave', function() {
                $rootScope.hideTabs = false;
            });
        }
    };
});

