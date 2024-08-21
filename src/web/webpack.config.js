const path = require('path');
const webpack = require('webpack');
require('dotenv').config();

module.exports = {
    entry: ['./src/index.ts', './src/welcome.ts'],
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist'),
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ],
    },
    plugins: [
        new webpack.DefinePlugin({
            'process.env': {
                'WEB_APP_PORT': JSON.stringify(process.env.WEB_APP_PORT),
                'API_URL': JSON.stringify(process.env.API_URL)
            }
        })
    ],
    resolve: {
        extensions: ['.ts', '.js'],
    },
    mode: 'development',
};
