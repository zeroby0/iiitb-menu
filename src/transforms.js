const htmlmin = require('html-minifier')
const env = require("../data/env.js")

const minifyHTML = (content, outputPath) => {
    // Eleventy 1.0+: use this.inputPath and this.outputPath instead
    if (env.isDev) return content
    if (!outputPath || !outputPath.endsWith('.html')) return content

    return htmlmin.minify(content, {
        useShortDoctype: true,
        removeComments: true,
        collapseWhitespace: true,
        minifyJS: true,
        sortAttributes: true,
        sortClassName: true,
    })
}

module.exports = config => {
    config.addTransform('htmlmin', minifyHTML)
}