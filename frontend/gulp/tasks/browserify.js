var gulp = require('gulp'),
    glob = require('glob'),
    browserify = require('browserify'),
    source = require('vinyl-source-stream');

module.exports = function() {
  glob('./source/**/*.js', {}, function(er, files){    
    var b = browserify();
    files.forEach(function(file){
      b.add(file);
    });
    b.bundle()
      .pipe(source('bundle.js'))
      .pipe(gulp.dest('./build/'));
  });
};
