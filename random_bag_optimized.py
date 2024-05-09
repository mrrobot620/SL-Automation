from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time
import logging


op = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory': r"/home/administrator/cbs_bag_hold/data",
    'directory_upgrade': True
}
op.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=op)
session = requests.Session()


def login_flo(user: str, pasw: str):
    driver.get("http://10.24.1.71/mh-ops")
    time.sleep(5)
    username = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[1]")
    username.send_keys(user)
    password = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[2]")
    password.send_keys(pasw)
    time.sleep(2)
    try:
        cross = driver.find_element(By.XPATH, "/html/body/div[4]/div/button")
        cross.click()
    except NoSuchElementException:
        print("Cross Button Not Found")
    time.sleep(1)
    submit = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/form/div/div[4]/div[4]/button/span")
    submit.click()
    time.sleep(3)

    csrf_token = driver.execute_script(
        "return document.querySelector('meta[name=csrf-token]').getAttribute('content');")
    if csrf_token:
        session.headers.update({"csrf-token": csrf_token})
        print(csrf_token)
    else:
        print("CSRF Token not found in page")
    selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    session.headers.update({"user-agent": selenium_user_agent})
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    return None


def session_checker() -> bool:
    try:
        response = session.get("http://10.24.1.71/mh-ops-routes-api/mh-ops-proxy/v1/track-and-trace-proxy/container/bag1/track" , timeout=1)
        response.raise_for_status()  # Raise exception for 4xx or 5xx status codes
        logging.info("API endpoint is reachable. Status code: %d", response.status_code)
        return True
    except requests.exceptions.RequestException as e:
        logging.error("Failed to reach API endpoint: %s", e)
        return False


def bag_retriever() -> list[str]:
    with open('a.txt', 'r') as f:
        bags = f.readlines()
    return bags


def sealID_finder(bags: list[str]):
    seals: list[str] = []
    for bag in bags:
        api = f"http://10.24.1.71/mh-ops-routes-api/mh-ops-proxy/v1/track-and-trace-proxy/container/{bag}/track"
        response = session.get(api)
        data = response.json()
        seal_id = data['data']['seal_id']
        seals.append(seal_id)
    return seals

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    if session_checker():


