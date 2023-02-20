import csv
import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import NoSuchAttributeException
from bs4 import BeautifulSoup

def game_code(url):
    # https://theluckyblue.com/game/1675497321
    code = url[-10:]
    return code

def profits(source_code):
    soup = BeautifulSoup(source_code, 'html.parser')
    betlist = soup.find('div', class_='game-stats')
    tbody = betlist.find('tbody')
    rows = tbody.find_all('tr')

    res = []
    for row in rows:
        det = row.find_all('td', class_='num-style')
        detail = float(det[1].text)
        res.append(detail)

    total = sum(res)

    if total == 0:
        total = total
    elif total < 0: #negative
        total = abs(total)
    else: #positive 
        total = -abs(total)
    
    return round(total, 2)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.headless = True

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.maximize_window()
url = "https://theluckyblue.com/"

driver.get(url)

#wait out the js to load
time.sleep(15)

# to avoid repetition
last_gamecode = 0

# count = 0
while True:
    
    data = driver.find_element(By.XPATH, '/html/body/div/div[2]/span/span/div/div[1]/div/div[1]/div[1]/div[1]/div/ul/li[10]/a')
    gamecode = game_code(data.get_attribute('href'))
    
    # to avoid repetition
    if last_gamecode == gamecode:
        continue

    odd = data.get_attribute('innerHTML')[:-1]
    timestamp = time.asctime(time.localtime())

    try:
        data.click()
        time.sleep(5)
        source = driver.page_source
        final_kut = profits(source)
        close = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/button')
        close.click()

        # set new game code as last
        last_gamecode = gamecode

        # add to a csv file
        with open('odds_file4.csv', mode= 'a', newline='' ) as odd_file:
            odd_writer = csv.writer(odd_file, delimiter=',')
            odd_writer.writerow([timestamp, gamecode, odd, final_kut])


        time.sleep(4)
    except ElementNotSelectableException:
        final_kut = 0.00
        # set new game code as last
        last_gamecode = gamecode

        # add to a csv file
        with open('odds_file4.csv', mode= 'a', newline='' ) as odd_file:
            odd_writer = csv.writer(odd_file, delimiter=',')
            odd_writer.writerow([timestamp, gamecode, odd, final_kut])
    except AttributeError:
        time.sleep(4)
        source = driver.page_source
        final_kut = profits(source)
        close = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/button')
        close.click()

        # set new game code as last
        last_gamecode = gamecode

        # add to a csv file
        with open('odds_file4.csv', mode= 'a', newline='' ) as odd_file:
            odd_writer = csv.writer(odd_file, delimiter=',')
            odd_writer.writerow([timestamp, gamecode, odd, final_kut])
