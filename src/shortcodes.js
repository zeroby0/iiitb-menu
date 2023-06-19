const fs = require('fs').promises
const postcss = require('../postcss.config.js')


const cssconcat = async function () {
    const css = await postcss.process('assets/tailwind.css') + ''

    return css
}

const scriptconcat = async function() {
    const script = await fs.readFile('assets/index.js')

    return script
}

module.exports = config => {
    config.addNunjucksAsyncShortcode('cssconcat', cssconcat)
    config.addNunjucksAsyncShortcode('scriptconcat', scriptconcat)
}