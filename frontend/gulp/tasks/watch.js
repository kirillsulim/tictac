var gulp = require('gulp');


module.exports = function() {
  gulp.watch('source/style/**/*', ['less']);
  gulp.watch('source/templates/**/*', ['templates']);
  gulp.watch('source/js/**/*', ['browserify']);
};
