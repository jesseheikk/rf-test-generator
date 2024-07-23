from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def initialize_driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver

def read_js_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def inject_js_click_listener(driver, script):
    driver.execute_script(script)

def log_element_info(log_path, action_info):
    with open(log_path, "a") as log_file:
        log_file.write(action_info + "\n")

def wait_for_page_load_and_inject_js(driver, script):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    inject_js_click_listener(driver, script)

def get_logged_actions(driver):
    return driver.execute_script("return window.loggedElementInfo")

def clear_logged_actions(driver):
    driver.execute_script("window.loggedElementInfo = []")
