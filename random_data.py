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
import json


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
    username.send_keys("ca.2273429")
    password = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[2]")
    password.send_keys("xMtapye9CUuw")
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
with open('a.txt' , 'r') as f:
    bags = f.readlines()

print(bags)


def sealID_finder(bags):
    seals: list[str] = []
    for bag in bags:
        api = f"http://10.24.1.71/mh-ops-routes-api/mh-ops-proxy/v1/track-and-trace-proxy/container/{bag}/track"
        response = session.get(api)
        data = response.json()
        seal_id  = data['data']['seal_id']
        seals.append(seal_id)
        return seals


def random_data(seal: str):
    api = f"http://10.24.0.157/print/label/{seal}?Entity=BAG"
    response = session.get(api)
    data = response.text
    data1 = data.split("\n")[0]
    values = data1.split(",")
    bag_id = values[4]
    seal_id = values[8]
    shipments = values[5]
    casper = values[10]
    real_casper = casper.split("^")
    return {
        'bag_id': bag_id,
        'seal_id': seal_id,
        'shipments': shipments,
        'casper': real_casper[0]
    }


data_list = []
for seal in sealID_finder(bags):
    data_list.append(random_data(seal))

import pandas as pd

df =pd.DataFrame(data_list)

df.to_csv("random_data.csv" , index=False)

df
