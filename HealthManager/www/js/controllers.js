angular.module('starter.controllers', ['ngCookies'])

.controller('LoginCtrl', function($scope, $http, $ionicLoading, $cookieStore, $location, $window, User) {
	$scope.formData = {};
	$scope.login = function() {
		$http({
			method: "POST",
			url: "http://127.0.0.1:5000/user/login",
			data: $.param($scope.formData),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).success(function(data) {
				if (data["status"] == "success") {
					$cookieStore.put("logged-in", true);
					$cookieStore.put("uid", $scope.formData.uid);
					$cookieStore.put("token", data["token"], {'expires': 7200});
					$cookieStore.put("tokenState", true, {'expires': 7000});
					$location.path("#/tab/home");
					$window.location.reload(true);
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
			url: "http://127.0.0.1:5000/user/register",
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
				$cookieStore.put("logged-in", true);
				$cookieStore.put("token", data["user"]["token"], {'expires': 7200});
				$cookieStore.put("tokenState", true, {'expires': 7000});
				$cookieStore.put("uid", data["user"]["username"]);
				$cookieStore.put("user", data["user"]);
				$location.path("#/tab/home");
				$window.location.reload(true);
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

.controller('SideBarCtrl', function($scope, $cookieStore, $http, User) {
	// $scope.$on('$stateChangeSuccess', $scope.doRefresh());
	$('.sidebar').css("display", "block");
	$scope.logged_in = $cookieStore.get("logged-in");
	var uid = $cookieStore.get("uid");
	var token = $cookieStore.get("token");
	$http({
		"method": "GET",
		"url": "http://127.0.0.1:5000/user/self" + "?uid=" + uid + "&token=" + token
	}).success(function(data) {
		$scope.user = data.user;
	});
	// console.log($scope.user.head_image);
})

.controller('HomeTabCtrl', function($scope, $http) {
	$http({
		method: "GET",
		url: "http://127.0.0.1:5000/news/index",
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
		url: "http://127.0.0.1:5000/news/"+classf+"/"+id,
	}).success(function(data) {
		$scope.news = data.news;
		$scope.news.body = $sce.trustAsHtml($scope.news.body);
	});
})

.controller('UserCtrl', function($scope, $cookieStore, $window, $location, $state, $http) {
	$scope.logged_in = $cookieStore.get("logged-in");
	var status = $scope.logged_in;
	var uid = $cookieStore.get("uid");
	var token = $cookieStore.get("token");
	$http({
		"method": "GET",
		"url": "http://127.0.0.1:5000/user/self" + "?uid=" + uid + "&token=" + token
	}).success(function(data) {
		$scope.user = data.user;
	});

	$('.logout').click(function() {
		$cookieStore.remove("logged-in");
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

.controller('RemindCtrl', function($scope, $ionicPopup, $timeout) {
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
});


// 注意事项: 最上面的最后不能有分号,控制器只有一个分号,就是在最后的那个控制器后