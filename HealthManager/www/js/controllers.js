angular.module('starter.controllers', ['ngCookies'])

.controller('LoginCtrl', function($scope, $http, $ionicLoading, $cookieStore, $location, $state, $window, User) {
	$scope.formData = {};
	$scope.login = function() {
		$ionicLoading.show({
			content: 'Loading',
		    animation: 'fade-in',
		    maxWidth: 200,
		    showDelay: 0,
		    noBackdrop: true
		});

		$http({
			method: "POST",
			url: "http://222.198.155.138:5000/user/login",
			data: $.param($scope.formData),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(data) {
				$ionicLoading.hide();
				if (data["status"] == "success") {
					// $cookieStore.put("logged-in", true);
					// $cookieStore.put("uid", $scope.formData.uid);
					// $cookieStore.put("token", data["token"], {'expires': 7200});
					// $cookieStore.put("tokenState", true, {'expires': 7000});
					// $location.path("#/tab/home");
					$window.localStorage.setItem("logged-in", true);
					$window.localStorage.setItem("uid", $scope.formData.uid);
					$window.localStorage.setItem("token", data["token"], {'expires': 7200});
					$window.localStorage.setItem("tokenState", true, {'expires': 7000});
					// $location.path("#/tab/home");
					// event.preventDefault();// 取消默认跳转行为
					User.set("logged-in", true);
					User.set("uid", $scope.formData.uid);
					User.set("token", data["token"]);
					$state.go("tabs.home");
					// $window.location.reload(true);
					// $route.reload();
				}
		})
		.error(function(data) {
				if (data["error_code"] == "2000") {
					$ionicLoading.show({
						template: '邮箱未认证',
						noBackdrop: true,
						duration: 2000
					});
				} else if (data["error_code"] == "2004") {
					$ionicLoading.show({
						template: '用户名或密码错误',
						noBackdrop: true,
						duration: 2000
					});
				}
		});
	};
})

.controller('RegisterCtrl', function($scope, $http, $ionicLoading, $cookieStore, $window, $location, User) {
	$scope.formData = {};
	$scope.register = function() {
		$ionicLoading.show({
			content: 'Loading',
		    animation: 'fade-in',
		    maxWidth: 200,
		    showDelay: 0,
		    noBackdrop: true
		});

		$http({
			method: "POST",
			url: "http://222.198.155.138:5000/user/register",
			data: $.param($scope.formData),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(data) {
			$ionicLoading.hide();
			if (data["status"] == "success") {
				$ionicLoading.show({
					template: '请打开邮箱进行验证',
					showBackdrop: true,
					duration: 2000
				});
				$window.localStorage.setItem("logged-in", true);
				$window.localStorage.setItem("token", data["user"]["token"], {'expires': 7200});
				$window.localStorage.setItem("tokenState", true, {'expires': 7000});
				$window.localStorage.setItem("uid", data["user"]["username"]);
				$window.localStorage.setItem("user", data["user"]);
				// $window.location.reload(true);
			}
		})
		.error(function(data){
			if (data["error_code"] == "2009") {
				$ionicLoading.show({
					template: '请填写完整信息',
					noBackdrop: true,
					duration: 2000
				});
			} else if (data["error_code"] == "2002") {
				$ionicLoading.show({
					template: '用户名已存在',
					noBackdrop: true,
					duration: 2000
				});
			} else if (data["error_code"] == "2001") {
				$ionicLoading.show({
					template: '邮箱已存在',
					noBackdrop: true,
					duration: 2000
				});
			}
		});
	};
})

.controller('SideBarCtrl', function($scope, $cookieStore, $rootScope, $http, $window, User) {
	// $scope.$on('$stateChangeSuccess', $scope.doRefresh());
	// $('.sidebar').css("display", "block");
	// $scope.logged_in = $cookieStore.get("logged-in");
	// var uid = $cookieStore.get("uid");
	// var token = $cookieStore.get("token");
	$rootScope.$on('$stateChangeSuccess',
	    function(event, toState, toParams, fromState, fromParams) {
	      if ((fromState.name == "login" && toState.name == "tabs.home") || (fromState.name == "register" && toState.name == "tabs.home")) {

        	// console.log(User.get("uid"));
         	$scope.logged_in = User.get("logged-in");
			var uid = User.get("uid");
			var token = User.get("token");
			$http({
				"method": "GET",
				"url": "http://222.198.155.138:5000/user/self" + "?uid=" + uid + "&token=" + token
			}).success(function(data) {
				$scope.user = data.user;
			});

	      }
	      else {
	      	$scope.logged_in = $window.localStorage.getItem("logged-in");
			var uid = $window.localStorage.getItem("uid");
			var token = $window.localStorage.getItem("token");
		  	$http({
				"method": "GET",
				"url": "http://222.198.155.138:5000/user/self" + "?uid=" + uid + "&token=" + token
			}).success(function(data) {
				$scope.user = data.user;
			});
	      }
  	});

	// console.log($scope.user.head_image);
})

.controller('HomeTabCtrl', function($scope, $http, $state, $window) {
	// $scope.$on("$ionicView.Enter", function() {
	// 	$window.location.reload(true);
	// })
	$http({
		method: "GET",
		url: "http://222.198.155.138:5000/news/index",
	}).success(function(data) {
		$scope.mutinews = data.mutinews;
		// console.log($scope.mutinews);
	});
})

.controller('NewsCtrl', function($scope, $http, $stateParams, $sce) {
	var classf = $stateParams.classf;
	var id = $stateParams.id;
	$http({
		method: "GET",
		url: "http://222.198.155.138:5000/news/"+classf+"/"+id,
	}).success(function(data) {
		$scope.news = data.news;
		$scope.news.body = $sce.trustAsHtml($scope.news.body);
	});
})

.controller('UserCtrl', function($scope, $cookieStore, $window, $location, $state, $http, $ionicLoading) {
	$scope.logged_in = $window.localStorage.getItem("logged-in");
	var status = $scope.logged_in;
	var uid = $window.localStorage.getItem("uid");
	var token = $window.localStorage.getItem("token");
	$http({
		"method": "GET",
		"url": "http://222.198.155.138:5000/user/self" + "?uid=" + uid + "&token=" + token
	}).success(function(data) {
		$scope.user = data.user;
	});

	$('.logout').click(function() {
		$ionicLoading.show({
			content: 'Loading',
		    animation: 'fade-in',
		    maxWidth: 200,
		    showDelay: 0,
		    noBackdrop: true
		});

		$window.localStorage.removeItem("logged-in");
		$state.go('tabs.home');
		$window.location.reload(true);
	});
})

.controller('FamilyCtrl', function($scope, $ionicPopup, $timeout) {
	 $scope.showPopup = function() {
       $scope.data = {}

       // 自定义弹窗
       var myPopup = $ionicPopup.show({
         template: "<div class='polist'><a class='popup' href='#'>添加家庭成员</a><a class='popup' href='#'>添加平时购药记录</a><a class='popup' href='#'>添加门诊/住院记录</a></div>",
         title: '选择操作',
         scope: $scope,
       });
       myPopup.then(function(res) {
         console.log('Tapped!', res);
       });
       $timeout(function() {
          myPopup.close(); // 3秒后关闭弹窗
       }, 2500);
      };
})

.controller('FamilyMemberCtrl', function($scope, $window, $location, $state, $http, $ionicLoading) {
	// $scope.logged_in = $window.localStorage.getItem("logged-in");
	// var status = $scope.logged_in;
	// var uid = $window.localStorage.getItem("uid");
	// var token = $window.localStorage.getItem("token");
	// $http({
	// 	"method": "GET",
	// 	"url": "http://222.198.155.138:5000/user/" + uid + "?uid=" + uid + "&token=" + token
	// }).success(function(data) {
	// 	$scope.user = data.user;
	// });
})

.controller('RemindCtrl', function($scope, $ionicPopup, $timeout,$window) {

	$scope.test_notification = function(){
		var now             = new Date().getTime(),
    _5_sec_from_now = new Date(now + 5*1000);

		cordova.plugins.notification.local.schedule({
		    text: "Delayed Notification",
		    at: _5_sec_from_now,
		    led: "FF0000",
		    sound: null
		});
	};


	 $scope.showPopup = function() {
       $scope.data = {}

       // 自定义弹窗
       var myPopup = $ionicPopup.show({
         template: "<div class='polist'><a class='popup' href='#'>喝水</a><a class='popup' href='#'>吃药</a><a class='popup' href='#'>自定义</a></div>",
         title: '选择提醒类型',
         scope: $scope,
       });
       myPopup.then(function(res) {
         console.log('Tapped!', res);
       });
       $timeout(function() {
          myPopup.close(); // 3秒后关闭弹窗
       }, 2500);
      };

      //开关
       $scope.RemindsList = [
	    { text: "喝水", time: "07:00", period: "每两天", checked: false },
	    { text: "吃药", time: "18:00", period: "每天", checked: false },
	    { text: "买药", time: "13:00", period: "每天", checked: false }
	  ];



	  $scope.pushNotificationChange = function() {
	    console.log('Push Notification Change', $scope.pushNotification.checked);
	  };

	  $scope.pushNotification = { checked: true };
	  $scope.emailNotification = 'Subscribed';
})


.controller('InfoCtrl', function($scope, $http, $stateParams,$cordovaSQLite,$rootScope,dbMed) {

//testSqlite
	$scope.insert = function() {
		var data=[$scope.medicine["name"],"", $scope.medicine["feature"],$scope.medicine["company"],$scope.medicine["usage"],$scope.medicine["taboo"],"","","","",0,"",""]
		if(dbMed.insert(data)!=false){
			alert('yes');
		}else{
			alert('no');
		}
	}

	$scope.select = function() {
		if(dbMed.select()){
			alert('yes');
		}else{
			alert('no');
		}
	}

	$scope.medicineList =new Array();
	var id = $stateParams.id;
	$http({
		method: "GET",
		url: "http://222.198.155.138:5000/medicine/lilac/"+id,
	}).success(function(data) {
		if(data.status=="success"){
			$scope.medicine=data.medicine;
		}
		else{
			alert('获取药品信息失败！');
		}
	});
})

.controller('myMedCtrl',function($scope, $http, $stateParams,$scope,$cordovaSQLite,$rootScope,$timeout,dbMed){
	alert('1');
	dbMed.select();
	alert($rootScope.selectResult.length);
	$scope.select = function() {
		if(dbMed.select()!=false){
			if($rootScope.selectResult.length==0){
				$scope.status="暂未添加药品";
			}else{
				$scope.status="";
				$scope.medicines=$rootScope.selectResult;
				$scope.$broadcast('scroll.refreshComplete');
			}
		}else{
			alert('no');
		}
	}
})

.controller('addMedCtrl',function($rootScope,$http,$scope,$stateParams){
	var id=$stateParams.id;
	$http({
		method: "GET",
		url: "http://222.198.155.138:5000/medicine/lilac/"+id,
	}).success(function(data) {
		if(data.status=="success"){
			$scope.medicine=data.medicine;
		}
		else{
			alert('获取药品信息失败！');
		}
	});

	$scope.addSubmit=function(){

	}

})

.controller("ExampleController", function($scope, $cordovaBarcodeScanner, $ionicPopup,$http,$rootScope,$cordovaNetwork,$ionicLoading) {

		// $scope.medicines=[];

		$scope.mSearch = function(){
			$ionicLoading.show({
				content: 'Loading',
			    animation: 'fade-in',
			    maxWidth: 200,
			    showDelay: 0,
			    noBackdrop: true
			});
			$http({
				method: "GET",
				url: "http://222.198.155.138:5000/medicine/lilac?type=medicine&keyword="+$('#msea').val()
			}).success(function(data) {
				$ionicLoading.hide();
				if(!data.medicines){
					alert('药品未收录！');}
				else {
					$scope.medicines=data.medicines;
				}
			}).error(function(data){
				alert('查询失败！');
			});
	}

	$scope.scanBarcode = function(){
		$cordovaBarcodeScanner.scan()
		.then(function(imageData)
		{
			$ionicLoading.show({
				content: 'Loading',
			    animation: 'fade-in',
			    maxWidth: 200,
			    showDelay: 0,
			    noBackdrop: true
			});
		$.ajax({
			 url: 'http://www.tngou.net/api/drug/code?',
			 type: "GET",
			 data: {'code':imageData.text},
			 dataType: 'jsonp',
			 jsonp:'callback',
			 success: function(data){
				 if(!data.status){
					 $ionicLoading.hide();
					 alert('药品信息未收录！');
				 }
				 else {
				 	$http({
						method:"GET",
						url:"http://222.198.155.138:5000/medicine/lilac?type=medicine&keyword="+data.name
					}).success(function(){
						if(!data.medicines){
		 				 $ionicLoading.hide();
							alert('药品未收录！');}
						else {
		 				 $ionicLoading.hide();
						 $scope.medicines=data.medicines;
						}
					}).error(function(){
						alert('查询失败！');
					})
				 }
			 },
			 error:function(data){
			 	alert('查询失败！');
			 }
	 	});
	});

}



});




// 注意事项: 最上面的最后不能有分号,控制器只有一个分号,就是在最后的那个控制器后
