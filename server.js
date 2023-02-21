const puppeteer = require('puppeteer');

const WebSocket = require('ws')

const wss = new WebSocket.Server({ port: 8081 })

wss.on('connection', async function connection(ws) {
    console.log('Client connected')
    // const interval = setInterval(() => {
    //     ws.send('hello world')
    // }, 1000)

    async function lb() {
        const browser = await puppeteer.launch({
            // headless: false,
            defaultViewport: false,
            userDataDir: './tmp'
        });
        const page = await browser.newPage();
        await page.goto('https://theluckyblue.com/');
        await page.waitForSelector('#content > span > span > div > div.col-md-9 > div > div:nth-child(1) > div.col-md-7 > div.mb-2.mt-2.ml-0.mr-0 > div > ul > li > a');
        
        const tenth = '#content > span > span > div > div.col-md-9 > div > div:nth-child(1) > div.col-md-7 > div.mb-2.mt-2.ml-0.mr-0 > div > ul > li:nth-child(10) > a';
        let lastGameCode = 0;
    
        async function getData(page) {
            let newOdd = await page.$eval(tenth, (li) => {
                let code = li.getAttribute('href').split('/').pop();
                let odd = li.textContent
                return [code, odd.slice(0, odd.length-1)]
            });
            if (newOdd[0] == lastGameCode) {
                // do nothing
            } else {
                lastGameCode = newOdd[0];
                // player bets data
                await page.click(tenth);
                listSel = 'body > div.fade.animated.pulse.modal.show > div > div > div.modal-body > div.table-responsive.game-stats > table > tbody > tr > td.num-style'
                await page.waitForSelector(listSel);
                const profits = await page.$$eval(listSel, (ls)=> {
                    even = true;
                    bls = ls.map(x => parseFloat(x.textContent));
                    prof = [];
                    for(const p of bls){
                        if (even) {
                            even = !even;
                        }
                        else {
                            prof.push(p);
                            even = !even;
                        }
                    }
                    return prof;
                });
                total = profits.reduce((a,b) => {
                    return a+b;
                });
                console.log(total)
                total = total > 0 ? -Math.abs(total) : Math.abs(total) ;
                msg = '-> total: ' + total + '|| odd: ' + newOdd[1] + '';
                ws.send(msg)
                // close
                await page.click('body > div.fade.animated.pulse.modal.show > div > div > div.Header.modal-header > button');
            }
            
        }
        setInterval(getData, 5000, page);
        // browser.close();
    }
    await lb();

    ws.on("close", () => {
        console.log("Client disconnected");
    });
    ws.onerror = function () {
        console.log("Some Error occurred");
    }
});