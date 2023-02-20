const puppeteer = require('puppeteer');
const fs = require('fs/promises');

async function start() {
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: false,
        userDataDir: './tmp'
    });
    const page = await browser.newPage();
    await page.goto('https://learnwebcode.github.io/practice-requests/');
    
    const names = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('.info strong')).map(x => x.textContent)
    });
    await fs.writeFile("names.txt", names.join('\r\n'));
    
    await page.click('#clickme');
    const clickedData = await page.$eval('#data', el => el.textContent)
    console.log(clickedData);

    const photos = await page.$$eval('img', (imgs) => {
        return imgs.map(x=>x.src)
    });

    for (const image of photos) {
        const imgpg = await page.goto(image);
        await fs.writeFile(image.split('/').pop(), await imgpg.buffer())
    }
    await browser.close();
}

start();