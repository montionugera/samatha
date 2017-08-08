var gulp = require('gulp');
var livereload = require('gulp-livereload');

gulp.task('watch-html', function () {
    return gulp.src('**/*.html')
        .pipe(livereload())
});

gulp.task('default', function(){
    livereload.listen();
    gulp.watch('**/*.html',['watch-html']);
});