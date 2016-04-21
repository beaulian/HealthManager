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

  var AMapArea=document.getElementById('amap');
  AMapArea.parentNode.style.height="100%";
  $scope.AMapId='container';
  $scope.mapObj;//存放初始化的地图对象
  $scope.lng;
  $scope.lat;

  $scope.getCurrentPosition = function() {
    $scope.mapObj.plugin('AMap.Geolocation', function() {
      geolocation = new AMap.Geolocation({
              enableHighAccuracy: true,//是否使用高精度定位，默认:true
              timeout: 10000,          //超过10秒后停止定位，默认：无穷大
              buttonPosition: 'RB',    //定位按钮停靠位置，默认：'LB'，左下角
              buttonOffset: new AMap.Pixel(10, 20),//定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
              zoomToAccuracy:true      //定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
      });
      $scope.mapObj.addControl(geolocation);
      geolocation.getCurrentPosition();
      AMap.event.addListener(geolocation, 'complete', onComplete);//返回定位信息
      AMap.event.addListener(geolocation, 'error', onError);      //返回定位出错信息
    });

    var onComplete = function(data) {
      console.log(data.position.getLng());
    }

    var onError = function() {
      alert("定位失败");
    }
  }

  $scope.initAMap=function(){
    var position=new AMap.LngLat(116.397428,39.90923);
    $scope.mapObj=new AMap.Map($scope.AMapId,{
      resizeEnable: true,
      view: new AMap.View2D({
              center:position,
              zoom:14,
              rotation:0
      }),
      lang: 'zh_cn'
    });
  }

})

.controller("MapListCtrl", function($scope, Pharmacy, Hospital) {
  $scope.results = Pharmacy.get();
  alert($scope.results);
})

//.directive('appMapPharmacy', function(Pharmacy) {
//    return {
//        restrict: "AE",
//        replace: true,
//        template: "<div id='initMapPharmacy'></div>",
//        scope: {
//
//        },
//        link: function(scope, element, attrs) {
//
//
//        }
//    };
//})

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

