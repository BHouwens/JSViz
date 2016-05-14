/*-------- PostCSS imports ----------*/

var autoprefixer = require('autoprefixer'),
    rucksack = require('rucksack-css'),
    nesting = require('postcss-nested'),
    colourFunctions = require('postcss-colour-functions'),
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
            { test: /\.css$/, loaders: ["style", "css", "postcss-loader"], include: path.resolve(rootDir, "styles") },
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
                nesting({ bubble: ['phone'] }),
                colourFunctions,
                mqPacker];
    }
};

module.exports = config;