var gulp = require('./gulp/')([
  'bower-files',
  'browserify',
  'browser-sync',
  'less',
  'templates',
  'watch'
]);

gulp.task('build', ['bower-files', 'browserify', 'less', 'templates']);
gulp.task('default', ['build', 'watch', 'browser-sync'])  
