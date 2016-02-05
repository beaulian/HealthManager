angular.module('starter.services', [])

.factory('User', function() {
	var user = {};

	return {
		set: function(temp_user) {
			user = temp_user;
		},
		get: function() {
			return user;
		}
	};
});