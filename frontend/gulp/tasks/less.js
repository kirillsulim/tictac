var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    less = require('gulp-less'),
    rename = require('gulp-rename'),
    mincss = require('gulp-minify-css');

module.exports = function() {
  return gulp.src('source/style/style.less')
    .pipe(less())
    .on('error', function(e){
      console.log(e);
    })
    .pipe(autoprefixer('last 2 versions'))
    .on('error', function(e){
      console.log(e);
    })
    .pipe(rename({suffix: '.min'}))
    .pipe(mincss({keepBreaks: true}))
    .pipe(gulp.dest('build/css'));
};
