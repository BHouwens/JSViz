/*-------- PostCSS imports ----------*/

var autoprefixer = require('autoprefixer'),
    rucksack = require('rucksack-css'),
    mqPacker = require('css-mqpacker'); 

/*----------- Server modules --------------*/

var webpack = require("webpack"),
    path = require("path");

/* ------- Directories --------*/

var rootDir = path.join(__dirname, "static");

/*-----------------------------------*/

var config = {
    context: rootDir,
    entry: './src/index.js',
    output: {
        path: rootDir,
        filename: 'bundle.js'
    },
    devtool: 'source-map',
    module: {
        loaders: [
            { test: /\.scss$/, loaders: ["style", "css", "postcss-loader", "sass"], include: path.resolve(rootDir, "styles") },
            { test: /\.js$/, loader: "babel-loader", include: path.resolve(rootDir, "src"), 
              query: {
                   presets: ['es2015']
            }}
        ]
    },
    resolve: {
        extensions: ['', '.js', '.scss']
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            d3: "d3"
        })
    ],
    postcss: function () {
        return [autoprefixer({ browsers: ['last 2 versions']}),
                rucksack({ fallbacks: true }),
                mqPacker];
    }
};

module.exports = config;