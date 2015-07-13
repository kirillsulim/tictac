var gulp = require('gulp'),
    bowerFiles = require('gulp-bower-files');
 
module.exports = function(){
    return bowerFiles()
      .pipe(gulp.dest("./build/vendor/"));
};
