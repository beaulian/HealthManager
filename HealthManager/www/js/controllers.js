angular.module('starter.controllers', ['ngCookies'])

.controller('LoginCtrl', function($scope, $http, $ionicLoading, $cookieStore, $location, User) {
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
					$cookieStore.put("token", data["token"], {'expires': 7200});
					$cookieStore.put("tokenState", true, {'expires': 7000});
					$location.path("#/tab/home");
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

.controller('RegisterCtrl', function($scope, $http, $ionicLoading, $cookieStore, $location, User) {
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

.controller('SideBarCtrl', function($scope, $cookieStore, User) {
	$scope.logged_in = $cookieStore.get("logged-in");
	$scope.user = $cookieStore.get("user");
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
	// var top = $('.news_nav').offset().top;
	// var windowTop =  $(window).height();
 //    if (top > windowTop) {
 //    	$("news_nav").offset.top = 603;
 //    	$("news_nav").css("position","fixed");
 //    } else {
 //    	$("news_nav").css("position","static");
 //    }
});


// 注意事项: 最上面的最后不能有分号,控制器只有一个分号,就是在最后的那个控制器后