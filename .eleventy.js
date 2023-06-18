const registerShortcodes = require('./src/shortcodes.js')
const registerTransforms = require('./src/transforms.js')

module.exports = config => {
    registerShortcodes(config);
    registerTransforms(config);

    config.addPassthroughCopy({ 'public': '.' });
    
    return {
        dataTemplateEngine: 'njk',
        htmlTemplateEngine: 'njk',

        dir: {
            input: 'src',
            // These are relative to the input folder.
            includes: 'includes',
            data: '../data'
        }
    }
}