import pickle
import random
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

###

driver_path = "C:/Driver/chromedriver.exe" # location of your chromedriver
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe" # location of your Brave browser

d = DesiredCapabilities.CHROME
d['goog:loggingPrefs'] = { 'browser':'ALL' }

option = webdriver.ChromeOptions()
option.add_argument('log-level=3')
option.add_argument('window-size=929, 1012')
option.binary_location = brave_path

driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option, desired_capabilities=d)
main_page = driver.current_window_handle

###
reddit_username = ""
reddit_password = ""
sleeptimeMin = 30 # Minimum time the bot will sleep between actions to look more human
sleeptimeMax = 90 # Maximum time the bot will sleep between actions to look more human
###
debugResolution = True
debugBarsAdd = 0
debugLogfile = "debug.log"
###
version = "1.1.4"
###

driver.get("https://wallet.wax.io/")

def debugger(t = "init"):
    nl = "\n"
    if t == "init":
        f = open(debugLogfile, "w+")
        f.write(f"AWA {version} | {datetime.now().strftime('%c')}{nl}")
        f.close()
    else:
        f = open(debugLogfile, "a")
        print(t)
        f.write(f"{datetime.now().strftime('%X')} | {t}{nl}")
        f.close()


def sleeptime():
    x = random.randint(sleeptimeMin, sleeptimeMax)
    print(f"Going sleep: {x}s")
    return x

size = 0,0

def preload(): # logs into wax.io
    debugger("Preloading...")
    while True:
        debugger("Clicking Reddit loggin")
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[4]/div/div[9]/button').click()
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div/div[3]/div[1]/div[9]/button').click()
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[4]/div[1]/div[9]/button').click()
        except:
            if driver.current_url.startswith("https://www.reddit.com/"):
                debugger("Website is reddit, breaking")
                break
            else:
                time.sleep(0.5)
        else:
            break
    while True:
        debugger("Logging in")
        try:
            driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input').send_keys(reddit_username)
            driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[2]/input').send_keys(reddit_password)
            driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button').click()
        except:
            time.sleep(0.1)
        else:
            break
    time.sleep(2)
    while True:
        debugger("Allowing")
        try:
            driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/form/div/input[1]').click()
        except:
            time.sleep(0.5)
        else:
            break
    time.sleep(3)
    while True:
        if driver.current_url != "https://wallet.wax.io/dashboard":
            debugger("Waiting for dashboard")
            time.sleep(0.6)
        else:
            break
    debugger("Switching to AW")
    driver.get("https://play.alienworlds.io/")
    global size
    debugger(f"DebugRes = {debugResolution}")
    debugger(f"Size = {size}")
    if debugResolution == False:
        size = driver.get_window_size()["width"]/0.5625, driver.get_window_size()["height"]
    if debugResolution == True:
        size = 500, 500
    debugger(f"Size = {size}")
    print(size)
    debugger(f"Set window to size")
    driver.set_window_size(size[0], size[1])


def login(): # login into alienworlds
    found = False
    time.sleep(5)
    while not found:
        debugger(f"Waiting for login")
        for e in driver.get_log('browser'):
            if "Input Manager initialize...\\n" in e["message"]:
                found = True
                break
        time.sleep(0.5)
    global size
    while True:
        _debugLog = driver.get_log('browser')
        driver.set_window_size(size[0], size[1])
        x = driver.get_window_size()["width"]/2
        y = driver.get_window_size()["height"]*0.621761
        if debugResolution == True:
            x, y = 250, 233
        debugger(f"X, Y = {x}, {y}")
        debugger(f"Clicking")
        ActionChains(driver).move_by_offset(x, y).click().perform()
        time.sleep(0.2)
        debugger(f"Backing")
        ActionChains(driver).move_by_offset(-x, -y).click().perform()
        time.sleep(5)
        global debugBarsAdd
        if driver.get_log('browser') == _debugLog:
            if debugBarsAdd > 2:
                debugger(f"Reverse scaling window to {size}, {debugBarsAdd}")
                size = size[0], size[1]-25
                debugBarsAdd = 0
            else:
                debugger(f"Scaling window to {size}, {debugBarsAdd}")
                size = size[0], size[1]+25
                debugBarsAdd += 1
        else:
            break


def miner(force = False): # activates miner menu button
    found = False
    while not found:
        debugger(f"Waiting for miner")
        if force == True:
            debugger(f"Force miner")
            break
        for e in driver.get_log('browser'):
            if "successfully downloaded and stored in the indexedDB cache" in e["message"]:
                found = True
                break
        time.sleep(0.6)
    driver.set_window_size(size[0], size[1])
    x = driver.get_window_size()["width"]/1.32714285714
    y = driver.get_window_size()["height"]/3.4
    if debugResolution == True:
        x, y = 405, 105
    debugger(f"X, Y = {x}, {y}")
    debugger(f"Clicking")
    ActionChains(driver).move_by_offset(x, y).click().perform()
    time.sleep(0.2)
    debugger(f"Backing")
    ActionChains(driver).move_by_offset(-x, -y).click().perform()

def mine(force = False): # starts mining
    found = False
    while not found:
        debugger(f"Waiting for mine")
        if force == True:
            debugger(f"Force mine")
            break
        for e in driver.get_log('browser'):
            if "successfully downloaded and stored in the indexedDB cache" in e["message"]:
                found = True
                break
        time.sleep(0.6)
    driver.set_window_size(size[0], size[1])
    x = driver.get_window_size()["width"]/2
    y = driver.get_window_size()["height"]/1.35
    if debugResolution == True:
        x, y = 250, 275
    debugger(f"X, Y = {x}, {y}")
    debugger(f"Clicking")
    ActionChains(driver).move_by_offset(x, y).click().perform()
    time.sleep(0.2)
    debugger(f"Backing")
    ActionChains(driver).move_by_offset(-x, -y).click().perform()
    
def get(force = False): # claims reward
    found = False
    while not found:
        for e in driver.get_log('browser'):
            if "end doWork" in e["message"]:
                found = True
                break
        time.sleep(0.6)
    driver.set_window_size(size[0], size[1])
    x = driver.get_window_size()["width"]/2
    y = driver.get_window_size()["height"]/1.9
    if debugResolution == True:
        x, y = 245, 185
    debugger(f"X, Y = {x}, {y}")
    debugger(f"Clicking")
    ActionChains(driver).move_by_offset(x, y).click().perform()
    time.sleep(0.2)
    debugger(f"Backing")
    ActionChains(driver).move_by_offset(-x, -y).click().perform()
    
def end(force = False): # resets
    found = False
    while not found:
        debugger(f"Waiting for end")
        if force == True:
            debugger(f"Force end")
            break
        for e in driver.get_log('browser'):
            if "Loaded Mining" in e["message"]:
                found = True
                print(found)
                break
        time.sleep(0.6)
    time.sleep(10)
    driver.set_window_size(size[0], size[1])
    x = driver.get_window_size()["width"]/4.05
    y = driver.get_window_size()["height"]/1.52025316456
    if debugResolution == True:
        x, y = 140, 250
    debugger(f"X, Y = {x}, {y}")
    debugger(f"Clicking")
    ActionChains(driver).move_by_offset(x, y).click().perform()
    time.sleep(0.2)
    debugger(f"Backing")
    ActionChains(driver).move_by_offset(-x, -y).click().perform()
    
def wait(): # finds sleep time and waits
    s = ""
    found = False
    while not found:
        for e in driver.get_log('browser'):
            if "until next mine" in e["message"]:
                found = True
                s = e["message"]
                break
        time.sleep(0.6)
    debugger("Sleeping")
    time.sleep(int(s[s.find("mine ")+5:s.find("\"'")])/1000)
    debugger("SleepStop")

debugger("init")

preload()
login()
miner()
mine()
get()
end()
wait()

while True:
    time.sleep(sleeptime())
    mine(True)
    time.sleep(sleeptime()/4)
    get(True)
    end(True)
    wait()
