'use strict';

// Include Gulp & Tools We'll Use
var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var runSequence = require('run-sequence');
var mainBowerFiles = require('main-bower-files');

var browserSync = require('browser-sync');
var reload = browserSync.reload;

var AUTOPREFIXER_BROWSERS = [
  'ie >= 10',
  'ie_mob >= 10',
  'ff >= 30',
  'chrome >= 34',
  'safari >= 7',
  'opera >= 23',
  'ios >= 7',
  'android >= 4.4',
  'bb >= 10'
];

gulp.task('jshint', function () {
  return gulp.src('app/src/**/*.js')
    .pipe($.jshint())
    .pipe($.jshint.reporter('jshint-stylish'))
    .pipe($.if(!browserSync.active, $.jshint.reporter('fail')));
});

gulp.task('coffee', function() {
  return gulp.src('app/src/*.coffee')
    .pipe($.coffee({bare: false}))
    .pipe(gulp.dest('dest'))
});

gulp.task('styles', function () {
  return gulp.src([
    'app/styles/*.scss',
    'app/styles/**/*.css'
  ])
    .pipe($.changed('styles', {extension: '.scss'}))
    .pipe($.sass({
      precision: 10
    }))
    .on('error', console.error.bind(console))
    .pipe($.autoprefixer({browsers: AUTOPREFIXER_BROWSERS}))
    .pipe(gulp.dest('dest'));
});

gulp.task('serve', ['styles'], function () {
  browserSync({
    notify: false,
    // Customize the BrowserSync console logging prefix
    logPrefix: 'WSK',
    // Run as an https by uncommenting 'https: true'
    // Note: this uses an unsigned certificate which on first access
    //       will present a certificate warning in the browser.
    // https: true,
    server: ['./app','app/elements/*.js','app/assets', 'app/dest']
  });

  gulp.watch(['app/*.html','app/elements/*.js','app/src/**/*.js'], reload);
  gulp.watch(['app/src/**/*.coffee'], ['coffee']);
  gulp.watch(['app/styles/**/*.{scss,css}'], ['styles']);
  gulp.watch(['app/src/**/*.js'], ['jshint']);
});

gulp.task('server-static-clean', function () {
  return gulp.src('server/static', {read: false})
    .pipe($.clean());
});

gulp.task('to-server',['server-static-clean'],function(){
  return gulp.src(['./app/**/*','!**/examples/**','!**/example/**',
                  '!**/tutorial/**','!**/tutorials/**',
                  '!**/test/**','!**/tests/**','!**/docs/**'],{base:'./app'})
    .pipe(gulp.dest('server/static'));
});
/*
gulp.task('vulcanize', function () {
    var DEST_DIR = 'dist';

    return gulp.src('app/index.html')
        .pipe($.vulcanize({
            dest: DEST_DIR
        }))
        .pipe(gulp.dest(DEST_DIR));
});*/
/*
gulp.task('bower', function() {
  return gulp.src(mainBowerFiles(), {
      base: 'app/bower_components'
    })
    .pipe(gulp.dest('server/public/bower_components'));
});*/

// Build Production Files, the Default Task
/*gulp.task('default', function (cb) {
  runSequence(['styles','coffee'], ['serve'], cb);
});*/

gulp.task('default', ['to-server'],function(){

});


