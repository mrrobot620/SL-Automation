from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC3
from selenium.webdriver.common.action_chains import ActionChains
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests_html import HTMLSession
import time


op = webdriver.ChromeOptions()
# op.add_argument('--headless=new')
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory': r"/home/administrator/cbs_bag_hold/data",
    'directory_upgrade': True
}
op.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=op)

session = HTMLSession()

def login_flo():
    driver.get("http://10.24.1.71/mh-ops")
    time.sleep(5)
    username = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[1]")
    username.send_keys("ca.2670054")
    password = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[2]")
    password.send_keys("Chauhan@8091")
    time.sleep(2)
    try:
        cross = driver.find_element(By.XPATH, "/html/body/div[4]/div/button")
        cross.click()
    except:
        print("Cross Button Failed")
    time.sleep(1)
    submit = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/form/div/div[4]/div[4]/button/span")
    submit.click()
    time.sleep(3)

login_flo()
session_cookie = driver.get_cookies()
csrf_token = driver.execute_script("return document.querySelector('meta[name=csrf-token]').getAttribute('content');")

if csrf_token:
    session.headers.update({"csrf-token": csrf_token})
    print(csrf_token)
else:
    print("CSRF Token not found in page")

selenium_user_agent = driver.execute_script("return navigator.userAgent;")
print(selenium_user_agent)
session.headers.update({"user-agent": selenium_user_agent})
for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])




