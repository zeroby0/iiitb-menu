module.exports = {
    isDev: process.env.ELEVENTY_ENV == 'development',
    isProd: process.env.ELEVENTY_ENV == 'production',
}