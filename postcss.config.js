const fs = require('fs').promises
const path = require('path')

const postcss = require('postcss')
// const cssnano = require('cssnano')
const purgecss = require('@fullhuman/postcss-purgecss')
const atImport = require("postcss-import")


const process = async function (cssfilepath) {
    const postcssPlugins = [
        atImport,
        require('tailwindcss')('tailwind.config.js'),
        require('autoprefixer'),
        require('cssnano')
    ]

    const css = await postcss(...postcssPlugins).process(
        await fs.readFile(cssfilepath),
        { from: cssfilepath }
    ) + ''

    // const cssmin = await postcss(cssnano).process(
    //     css
    // ) + ''

    return css
}

module.exports.process = process