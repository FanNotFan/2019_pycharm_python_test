const gulp = require('gulp')

const rollupEach = require('gulp-rollup-each')
const rollupBabel = require('rollup-plugin-babel')
const rollupResolve = require('rollup-plugin-node-resolve')
const rollupCommon = require('rollup-plugin-commonjs')

const del = require('del')
const gulpIf = require('gulp-if')
const runSequence = require('run-sequence')

const eslint = require('gulp-eslint')
const stylelint = require('gulp-stylelint')

const postcss = require('gulp-postcss')
const sass = require('gulp-sass')
const autoprefixer = require('autoprefixer')
const concat = require('gulp-concat')
const cleanCSS = require('gulp-clean-css')

const imagemin = require('gulp-imagemin')
const mozjpeg = require('imagemin-mozjpeg')
const pngquant = require('imagemin-pngquant')

const plumber = require('gulp-plumber')
const sourcemaps = require('gulp-sourcemaps')
const uglify = require('gulp-uglify')
const jsTargets = ['./src/js/**/*.js']
const jsEntries = ['./src/js/*.js']
const cssTargets = ['./src/css/**/*.scss']
const imageTargets = ['./src/img/**/*']
const copyTarget = ['./_locales/**/*', 'background.js', 'manifest.json']
const config = {
  plumberConfig: {
    errorHandler: function (err) {
      console.log(err.toString())
      this.emit('end')
    }
  },
  env: {
    dev: process.env.NODE_ENV === 'development',
    prod: process.env.NODE_ENV === 'production'
  }
}

gulp.task('lint:js', function () {
  return gulp.src(jsTargets)
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError())
})

gulp.task('lint:css', function () {
  return gulp.src(cssTargets)
    .pipe(stylelint({
      reporters: [
        { formatter: 'string', console: true }
      ]
    }))
})

gulp.task('js', function () {
  return gulp.src(jsEntries)
    .pipe(plumber(config.plumberConfig))
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(gulpIf(config.env.dev, sourcemaps.init({ loadMaps: true })))
    .pipe(rollupEach({
      isCache: true,
      plugins: [
        rollupBabel({
          presets: ['@babel/preset-env']
        }),
        rollupResolve({
          browser: true
        }),
        rollupCommon()
      ]},
      {
        format: 'iife'
      }
      ))
    // write sourcemaps
    .pipe(gulpIf(config.env.dev, sourcemaps.write()))
    .pipe(gulpIf(config.env.prod, uglify()))

    .pipe(gulp.dest('dist/js/'))
})

gulp.task('css', function () {
  return gulp.src(cssTargets)
    .pipe(plumber(config.plumberConfig))
    .pipe(stylelint({
      reporters: [
        { formatter: 'string', console: true }
      ]
    }))
    .pipe(gulpIf(config.env.dev, sourcemaps.init()))
    .pipe(sass({
      outputStyle: 'nested',
      precision: 3,
      includePaths: ['.']
    }))
    .pipe(postcss([
      autoprefixer({
        browsers: ['last 1 versions']
      })
    ]))
    .pipe(concat('style.css'))
    .pipe(gulpIf(config.env.dev, sourcemaps.write()))
    .pipe(gulpIf(config.env.prod, cleanCSS()))
    .pipe(gulp.dest('dist/css/'))
})

gulp.task('img', function () {
  return gulp.src(imageTargets)
    .pipe(plumber(config.plumberConfig))
    .pipe(imagemin([
      pngquant(),
      mozjpeg(),
      imagemin.svgo()], {
      verbose: true
    }))
    .pipe(gulp.dest('dist/img/'))
})
gulp.task('copy', function () {
  return gulp.src(copyTarget, { base: '.' })
    .pipe(gulp.dest('dist/'))
})
gulp.task('build', ['js', 'css', 'img', 'copy'])

gulp.task('clean', function () {
  return del([
    'dist/**/*'
  ])
})
gulp.task('serve', ['clean'], function () {
  runSequence(['build'], function () {
    gulp.watch(copyTarget, ['copy'])
    gulp.watch(jsTargets, ['js'])
    gulp.watch(cssTargets, ['css'])
  })
})

gulp.task('public', ['clean'], function () {
  runSequence(['build'])
})

gulp.task('default', function () {
  console.info('You should use npm run dev to start development mode.')
})
