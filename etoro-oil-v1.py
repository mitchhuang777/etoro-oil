from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import random
import datetime

PATH = "./chromedriver"
url = "https://www.etoro.com/zh-tw/login"
# Avoid to be the robot.
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=PATH)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
driver.get(url)
# Login.
usr = driver.find_element_by_id("username")
pswd = driver.find_element_by_id("password")
fileobj = open('secret')
username = fileobj.readline()
password = fileobj.readline()
usr.send_keys(username)
time.sleep(1)
pswd.send_keys(password)
time.sleep(10)
# Get into the virtual investment.
driver.find_element_by_xpath("/html/body/ui-layout/div/div/div[1]/et-layout-menu/div/div[2]/div[1]/div[2]/et-select").click()
time.sleep(2)
driver.find_element_by_xpath("/html/body/ui-layout/div/div/div[1]/et-layout-menu/div/div[2]/div[1]/div[2]/et-select/div[2]/div/div[2]/et-select-body/et-select-body-option[2]").click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="cdk-overlay-0"]/et-dialog-container/et-portfolio-toggle-account/div/div[3]/a').click()
time.sleep(5)

# Buy path, now is the Oil.
buy_path = "/html/body/ui-layout/div/div/div[2]/et-watchlist/div[2]/div/et-watchlist-list/section/section[1]/section[13]/et-instrument-row/et-instrument-trading-row/div/et-buy-sell-buttons/et-buy-sell-button[2]/div/div[2]"

counter = 0
# Get the first time price.
def first_price():
    while True:
        x = datetime.datetime.now()
        # 59
        if x.second == 0:
            price = float(driver.find_element_by_xpath(buy_path).text)
            return price
            break
# Calculate the slowEMA, fastEMA, MACD, MACD_Signal.
def macd():
    for i in range(-9, 0, 1):
        slowEMA[i] = (close_price_data[i] - slowEMA[i-1])*slow_weight + slowEMA[i-1]
    for i in range(-23-counter, 0, 1):
        fastEMA[i] = (close_price_data[i] - fastEMA[i-1])*fast_weight + fastEMA[i-1]

    for i in range(-10, 0, 1):
        MACD[i] = fastEMA[i] - slowEMA[i]

    if macd_first_time == 0:
        MACD_Signal[-2] = sum(MACD[-10:-1])/len(MACD[-10:-1])
    MACD_Signal[-1] = (MACD[-1] - MACD_Signal[-2])*MACD_signal_weight + MACD_Signal[-2]


buy_price_before = first_price()
time.sleep(2)
buy_price = first_price()

close_price_data = []
fastEMA = [[]]*35
slowEMA = [[]]*35
MACD = [[]]*35
MACD_Signal = [[]]*35

fast_weight = 2.0/(12+1)
slow_weight = 2.0/(26+1)
MACD_signal_weight = 2.0/(9+1)
macd_first_time = 0
count = 0
x = datetime.datetime.now()
print(x)
# Add the close price to the list.
while len(close_price_data) < 35:
    x = datetime.datetime.now()
    buy_price_real = float(driver.find_element_by_xpath(buy_path).text)

    # x.second == 59
    if x.second == 0:
        close_price_data.append(buy_price_real)
    time.sleep(1)
# Calculate the first time slowEMA and fastEMA
slowEMA[25] = sum(close_price_data[0:26])/len(close_price_data[0:26])
fastEMA[11]  = sum(close_price_data[0:12])/len(close_price_data[0:12])

macd()
# macd_first_time is to determine whether the program calculate the macd.
macd_first_time = 1
    
hold = 0
while True:
    x = datetime.datetime.now()
    buy_price_real = float(driver.find_element_by_xpath(buy_path).text)
    # x.second == 59
    if x.second == 0:
        close_price_data.append(buy_price_real)
        # Gold Cross
        if (MACD[-1] - MACD_Signal[-1] > 0) and (MACD[-2] - MACD_Signal[-2] < 0 and hold == 0):
            print str(x) + "\tbuy"
            driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[2]/et-watchlist/div[2]/div/et-watchlist-list/section/section[1]/section[13]/et-instrument-row/et-instrument-trading-row/div/et-buy-sell-buttons/et-buy-sell-button[2]/div/div[2]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/input').send_keys(Keys.CONTROL+'a')
            driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/input').send_keys(Keys.DELETE)
            driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/input').send_keys('1000')
            driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[3]/tabs/div[1]/div[2]/tabstitles/tabtitle[2]/a/span/div[1]').click()
            driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[3]/tabs/div[3]/tabscontent/tab[2]/div/div[1]/a[1]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[4]/div/button').click()
            time.sleep(2)
            hold = 1
        # Death Cross
        if (MACD[-1] - MACD_Signal[-1] < 0) and (MACD[-2] - MACD_Signal[-2] > 0 and hold == 1):
            print str(x) + "\tsell"
            driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[1]/et-layout-menu/div/div[2]/div[1]/a[2]').click()
            driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[2]/div/div[2]/portfolio-list-view/div/ui-table/ui-table-body/div/a/ui-table-button-cell/div/span').click()
            driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[2]/div/div[2]/portfolio-list-view/div/ui-table/ui-table-body/div/a/ui-table-button-cell/div/div/div/div[1]').click()
            time.sleep(0.5)
            driver.find_element_by_xpath('//div[2]/close-all-positions/div/div[3]/div[3]/div/div/label').click()
            driver.find_element_by_xpath('//div[2]/close-all-positions/div/div[3]/div[4]/button').click()
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[1]/et-layout-menu/div/div[2]/div[1]/a[1]').click()
            hold = 0
            time.sleep(2)

        fastEMA.append('')
        slowEMA.append('')
        MACD.append('')
        MACD_Signal.append('')
        macd()
        time.sleep(1)

        # buy 
           # driver.find_element_by_xpath("/html/body/ui-layout/div/div/div[2]/et-watchlist/div[2]/div/et-watchlist-list/section/section[1]/section[9]/et-instrument-row/et-instrument-trading-row/div/et-buy-sell-buttons/et-buy-sell-button[2]/div/div[1]").click()
           # time.sleep(2)
           # driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[3]/tabs/div[1]/div[2]/tabstitles/tabtitle[2]/a/span/div[2]').click()
           # time.sleep(1)
           # driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[3]/tabs/div[3]/tabscontent/tab[2]/div/div[1]/a[1]').click()
           # time.sleep(1)
           # driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/input').send_keys(Keys.CONTROL+'a')
           # driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/input').send_keys(Keys.DELETE)
           # time.sleep(2)
           # driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/input').send_keys('1000')
           # time.sleep(2)


           # driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[4]/div/button').click()
           # time.sleep(1)
           # driver.find_element_by_xpath('//*[@id="open-position-view"]/div[2]/div/div[4]/div/button').click()
           # time.sleep(1)

           # 
           # driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[1]/et-layout-menu/div/div[2]/div[1]/a[2]').click()
           # time.sleep(0.5)
           # driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[2]/div/div[2]/portfolio-list-view/div/ui-table/ui-table-body/div[6]/a/ui-table-button-cell/div/span').click()
           # time.sleep(0.5)
           # driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[2]/div/div[2]/portfolio-list-view/div/ui-table/ui-table-body/div[6]/a/ui-table-button-cell/div/div/div/div[1]').click()
           # time.sleep(3)
           # driver.find_element_by_xpath('//*[@id="CB"]').click()
           # time.sleep(0.5)
           # driver.find_element_by_xpath('//*[@id="CB"]').click()
           # time.sleep(0.5)
           # driver.find_element_by_xpath('//*[@id="uidialog3"]/div[2]/close-all-positions/div/div[3]/div[4]/button').click()




   # btc_buy_before = btc_buy_now
   # btc_buy = driver.find_element_by_xpath('/html/body/ui-layout/div/div/div[2]/et-watchlist/div[2]/div/et-watchlist-list/section/section[1]/section[11]/et-instrument-row/et-instrument-trading-row/div/et-buy-sell-buttons/et-buy-sell-button[2]/div/div[2]').text

   # btc_buy_now = float(btc_buy)

   # up_rate = (btc_buy_now - btc_buy_before)/btc_buy_before

   # btc_sell = driver.find_element_by_xpath("/html/body/ui-layout/div/div/div[2]/et-watchlist/div[2]/div/et-watchlist-list/section/section[1]/section[11]/et-instrument-row/et-instrument-trading-row/div/et-buy-sell-buttons/et-buy-sell-button[1]/div/div[2]").text

   # x = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
   # print x, "btc", btc_sell, btc_buy, "{:.5f}".format(up_rate)
   # time.sleep(1)

#while True:
#    time.sleep(0.1)
#    x = datetime.datetime.now()
#    if x.second%10 == 0:
#        print("haha")
#        break
