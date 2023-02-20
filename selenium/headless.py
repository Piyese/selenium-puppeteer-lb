import csv
import time
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# options.headless = True


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.maximize_window()

def profits(source_code):
    soup = BeautifulSoup(source_code, 'html.parser')
    try:
        betlist = soup.find('div', class_='game-stats')
    except:
        time.sleep(5)
        betlist = soup.find('div', class_='game-stats')
        print('exception thrown')

    tbody = betlist.find('tbody')
    rows = tbody.find_all('tr')

    res = []
    for row in rows:
        det = row.find_all('td')
        det = det[-2:]
        stake = float(det[0].text[:-4])
        win = float(det[1].text[:-4])
        if win == 0.0:
            res.append(stake)
        else:
            res.append(-abs(win))
    
    return round(sum(res), 2)

       
with open('odds_file2.csv', mode= 'r') as odd_file:
    with open('output3.csv', mode = 'a', newline='') as output:
        odd_reader = csv.reader(odd_file)

        for row in odd_reader:
            code = row[1]
            url = "https://theluckyblue.com/game/{gamecode}".format(gamecode=code)
            
            driver.get(url)
            time.sleep(4)
            
            source = driver.page_source
            final_kut = profits(source)
            row.append(final_kut)

            odd_writer = csv.writer(output, delimiter=',')
            odd_writer.writerow(row)
            
            # print(final_kut)
    driver.quit()

