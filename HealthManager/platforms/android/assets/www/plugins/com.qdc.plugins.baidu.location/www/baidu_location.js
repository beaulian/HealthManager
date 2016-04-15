cordova.define("com.qdc.plugins.baidu.location.baidu_location", function(require, exports, module) {
var exec = require('cordova/exec');

var baidu_location = {
  getCurrentPosition: function(successFn, failureFn) {
    exec(successFn, failureFn, 'BaiduLocation', 'getCurrentPosition', []);
  }
};

module.exports = baidu_location
});
