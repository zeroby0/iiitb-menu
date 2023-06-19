const fs = require('fs').promises
const postcss = require('../postcss.config.js')


const cssconcat = async function () {
    const css = await postcss.process('assets/tailwind.css') + '';

    return css;
};


const istDateString = function () {
    // Get current date and time
    const now = new Date();


    // Define options for formatting
    const options = {
        timeZone: 'Asia/Kolkata', // IST timezone
        hour12: false, // 24-hour format
        weekday: 'long', // full weekday name
        year: 'numeric', // 4-digit year
        month: 'long', // full month name
        day: 'numeric', // day of the month
        hour: 'numeric', // hour (0-23)
        minute: 'numeric', // minute
        second: 'numeric' // second
    };

    // Convert to IST string representation
    const istDateString = now.toLocaleString('en-IN', options);

    return istDateString;
};

module.exports = config => {
    config.addNunjucksAsyncShortcode('cssconcat', cssconcat);
    config.addShortcode('istDateString', istDateString);
}