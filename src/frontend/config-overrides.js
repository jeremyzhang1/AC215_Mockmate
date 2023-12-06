const rewireBabelLoader = require("react-app-rewire-babel-loader");
const path = require("path");
const fs = require("fs");

const appDirectory = fs.realpathSync(process.cwd());
const resolveApp = relativePath => path.resolve(appDirectory, relativePath);

module.exports = function override(config, env) {
  config = rewireBabelLoader.include(
    config,
    resolveApp("node_modules/@monaco-editor/react")
  );

  // disable chunks so the index.html won't change during development 
  config.optimization.splitChunks = {
    cacheGroups: {
      default: false,
    },
  };
  config.optimization.runtimeChunk = false;

  config.module.rules = [
    {
      test: /node_modules\/monaco-editor/,
      use: {
        loader: 'babel-loader',
        // if you include your babel config here,
        // you don’t need the `babel.config.json` file
        options: { presets: ['@babel/preset-env'] }
      }
    },
    ...config.module.rules
  ]

  config.module.rules.push({
    test: /\.mjs$/,
    include: /node_modules/,
    type: "javascript/auto"
  });

  return config;
}
