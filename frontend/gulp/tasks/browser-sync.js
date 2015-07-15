var gulp = require('gulp'),
    browserSync = require('browser-sync');


module.exports = function() {
  var files = [
    'build/**/*.html',
    'build/**/*.css',
    'build/**/*.js'
  ];

  return browserSync.init(files, {
    server: {
      baseDir: './build'
    }
  });
};
