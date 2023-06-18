const fs = require('fs');
const { chromium } = require('playwright');

const url_login = 'https://iiitbac-my.sharepoint.com/:x:/r/personal/foodcommittee_iiitb_ac_in/Documents/IIITB-Menu.xlsx?d=w9345dc2a600f4e5a824d9510f774cddf&csf=1&web=1&e=cMYLbj';
const url_download = 'https://iiitbac-my.sharepoint.com/:x:/r/personal/foodcommittee_iiitb_ac_in/Documents/IIITB-Menu.xlsx';

const username = process.env.MS_USERNAME;
const password = process.env.MS_PASSWORD;

const selector_username = 'input[name="loginfmt"]';

console.log("Username: ", username);
// console.log("Password: ", password);

(async () => {
  const browser = await chromium.launch();

  const context = await browser.newContext();
  const page = await context.newPage();

  console.log("Started");

  // This page will ask for login
  await page.goto(url_login);
  console.log("Opened Login Page");

  // Wait for the sign-in form to appear and fill in the credentials
  await page.waitForSelector(selector_username);
  await page.fill(selector_username, username);
  await page.click('#idSIButton9');
  console.log("Entered Username");

  await page.waitForSelector('#i0118');
  await page.fill('#i0118', password);
  await page.click('#idSIButton9');
  console.log("Entered Password");


  // Keep Signed in?
  await page.waitForSelector('input[name="DontShowAgain"]')
  await page.click('input[type="button"]');
  console.log("Selected Don't remember");


  // Start waiting for download before clicking. Note no await.
  console.log("Starting Download");
  const downloadPromise = page.waitForEvent('download');

  // This will fail or timeout, but that's okay.
  page.goto(url_download);

  const download = await downloadPromise;

  const download_path = await download.path();

  fs.copyFileSync(download_path, './data/IIITB-Menu.xlsx');
  console.log("XLSX file downloaded and copied.");

  await browser.close();
})();
