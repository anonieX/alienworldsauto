import pickle
import random
import time

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
option.binary_location = brave_path

driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option, desired_capabilities=d)
main_page = driver.current_window_handle

###
reddit_username = ""
reddit_password = ""
###

driver.get("https://wallet.wax.io/")

def preload(): # logs into wax.io
    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[4]/div/div[9]/button').click()
        except:
            time.sleep(0.5)
        else:
            break

    while True:
        try:
            driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[1]/input').send_keys(reddit_username)
            driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[2]/input').send_keys(reddit_password)
            driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button').click()
        except:
            time.sleep(0.5)
        else:
            break

    while True:
        try:
            driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/form/div/input[1]').click()
        except:
            time.sleep(0.5)
        else:
            break
    while True:
        if driver.current_url != "https://wallet.wax.io/dashboard":
            time.sleep(0.1)
        else:
            break
    driver.get("https://play.alienworlds.io/")
    
def login(): # login into alienworlds
    found = False
    while not found:
        for e in driver.get_log('browser'):
            print(e, found)
            if "Input Manager initialize...\\n" in e["message"]:
                found = True
                break
           
    ActionChains(driver).move_by_offset(500, 600).click().perform()
    time.sleep(0.2)
    ActionChains(driver).move_by_offset(-500, -600).click().perform()
    
    
def miner(force = False): # activates miner menu button
    found = False
    while not found:
        if force == True:
            break
        for e in driver.get_log('browser'):
            print(e, found)
            if "successfully downloaded and stored in the indexedDB cache" in e["message"]:
                found = True
                break
            
    ActionChains(driver).move_by_offset(700, 400).click().perform()
    time.sleep(0.2)
    ActionChains(driver).move_by_offset(-700, -400).click().perform()

def mine(force = False): # starts mining
    found = False
    while not found:
        if force == True:
            break
        for e in driver.get_log('browser'):
            print(e, found)
            if "successfully downloaded and stored in the indexedDB cache" in e["message"]:
                found = True
                break

    ActionChains(driver).move_by_offset(460, 690).click().perform()
    time.sleep(0.2)
    ActionChains(driver).move_by_offset(-460, -690).click().perform()
    
def get(force = False): # claims reward
    found = False
    while not found:
        for e in driver.get_log('browser'):
            print(e, found)
            if "end doWork" in e["message"]:
                found = True
                break

    ActionChains(driver).move_by_offset(460, 530).click().perform()
    time.sleep(0.2)
    ActionChains(driver).move_by_offset(-460, -530).click().perform()
    
def end(force = False): # resets
    found = False
    while not found:
        if force == True:
            break
        for e in driver.get_log('browser'):
            print(e, found)
            if "Loaded Mining" in e["message"]:
                found = True
                print(found)
                break

    time.sleep(10)
    ActionChains(driver).move_by_offset(250, 650).click().perform()
    time.sleep(0.2)
    ActionChains(driver).move_by_offset(-250, -650).click().perform()
    
def wait(): # finds sleep time and waits
    s = ""
    found = False
    while not found:
        for e in driver.get_log('browser'):
            if "until next mine" in e["message"]:
                found = True
                s = e["message"]
                break

    print("Sleeping")
    time.sleep(int(s[s.find("mine ")+5:s.find("\"'")])/1000)
    print("SleepStop")
    

preload()
login()
miner()
mine()
get()
end()
wait()

while True:
    mine(True)
    get(True)
    end(True)
    wait()
