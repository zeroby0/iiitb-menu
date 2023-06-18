const postcss = require('../postcss.config.js')

const cssconcat = async function () {
    const css = await postcss.process('assets/tailwind.css') + ''

    return css
}

module.exports = config => {
    config.addNunjucksAsyncShortcode('cssconcat', cssconcat)
}