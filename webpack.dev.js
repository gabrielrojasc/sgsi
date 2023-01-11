/* eslint-disable import/no-extraneous-dependencies */
const glob = require('glob');
const path = require('path');

// Packages
const autoprefixer = require('autoprefixer');
const { merge } = require('webpack-merge');

// Plugins
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

// Config files
const common = require('./webpack.common');

// Config
module.exports = merge(common, {
  mode: 'development',

  output: {
    filename: '[name].js',
    publicPath: 'http://localhost:3000/',
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
    }),
  ],

  devtool: 'eval-cheap-source-map',
  // To debug code that looks like original source, but makes compilations slower:
  // devtool: 'eval-source-map',

  devServer: {
    port: 3000,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    watchFiles: ['**/*.pug'],
  },

  module: {
    rules: [
      {
        test: /\.tsx?$/,
        include: path.resolve('./assets/ts'),
        exclude: /node_modules/,
        use: [
          {
            loader: 'ts-loader',
            options: {
              // Allow development with temporary type errors.
              // Check them with lint-staged instead.
              transpileOnly: true,
            },
          },
        ],
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          'css-hot-loader',
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              sourceMap: true,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              sourceMap: true,
              postcssOptions: {
                plugins: () => [autoprefixer()],
              },
            },
          },
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true,
              sassOptions: {
                includePaths: glob.sync('node_modules').map((d) => path.join(__dirname, d)),
              },
            },
          },
        ],
      },
    ],
  },
});
