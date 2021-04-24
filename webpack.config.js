const HtmlWebpackPlugin = require('html-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const path = require('path');

module.exports = {
  entry: './pastecan-ui/src/index.tsx',
  output: {
    publicPath: '/',
    filename: 'main.bundle.js',
    path: path.resolve(__dirname, 'pastecan-ui/dist'),
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx'],
    alias: {
      react: 'preact/compat',
      'react-dom': 'preact/compat',
    },
  },
  plugins: [new HtmlWebpackPlugin({
    template: './pastecan-ui/src/static/index.html',
  })],
  optimization: {
    minimizer: [new TerserPlugin({ extractComments: false })],
  },
};
