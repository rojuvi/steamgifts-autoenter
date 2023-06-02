from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from enum import Enum
import pickle
import os
import time
import sys

username = os.environ.get("STEAM_USERNAME")
password = os.environ.get("STEAM_PASSWORD")
cookies_file = os.environ.get("COOKIES_FILE")
if cookies_file is None or cookies_file == None:
    cookies_file = "cookies.pkl"

base_url = "https://www.steamgifts.com"
user_settings_route = "/account/settings/profile"
login_route = "/?login"
giveaways_search_route = "/giveaways/search"

class Filter(Enum):
    WISHLIST = "type=wishlist"
    RECOMMENDED = "type=recommended"
    DLC = "dlc=true"
    

def store_cookies(driver):
    print(f"Storing cookies to {cookies_file}")
    os.makedirs(os.path.dirname(cookies_file), exist_ok=True)
    pickle.dump(driver.get_cookies(), open(cookies_file, "wb"))

def load_cookies(driver):
    if os.path.isfile(cookies_file):
        print(f"Cookies available at {cookies_file}")
        cookies = pickle.load(open(cookies_file, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)


def login(driver, username:str, password: str):
    if username is None or username == "":
        sys.exit("Missing username")
    if password is None or password == "":
        sys.exit("Missing password")
    driver.get(f"{base_url}{login_route}")
    pass_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    )
    user_elem = driver.find_element(By.XPATH, "//input[@type='text']")
    user_elem.clear()
    user_elem.send_keys(username)
    pass_elem.clear()
    pass_elem.send_keys(password)
    submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_btn.click()
    
    print("Waiting for user to allow the login...")
    signin_followup = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, "imageLogin"))
    )
    
    signin_followup.click()
    store_cookies(driver)
    
def sync_steam(driver):
    print("Sync with steam...")
    driver.get(f"{base_url}{user_settings_route}")
    driver.find_element(By.CLASS_NAME, "form__sync-default").click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='notification notification--success']"))
    )
    
    
def wait_for_load(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "nav__right-container"))
    )
    
def get_available_points(driver):
    return int(driver.find_element(By.CLASS_NAME, "nav__points").text)
    
def navigate_and_enter_giveaways(driver, filter: Filter = None):
    driver.get(f"{base_url}{giveaways_search_route}{f'?{filter.value}' if filter is not None else ''}")
    enter_giveaways(driver)
        
def enter_giveaways(driver):
    wait_for_load(driver)
    not_entered = driver.find_elements(By.XPATH, "//div[@class='giveaway__row-inner-wrap']")
    giveaways_hrefs = []
    for giveaway in not_entered:
        anchor = giveaway.find_element(By.XPATH, "a[@class='giveaway_image_thumbnail']")
        points_text = giveaway.find_element(By.CLASS_NAME, "giveaway__heading__thin").text
        cost = int(points_text[1:points_text.index('P')])
        giveaways_hrefs.append((anchor.get_attribute("href"), cost))
    for (giveaway_page, cost) in giveaways_hrefs:
        driver.get(giveaway_page)
        enter_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-do='entry_insert']"))
        )
        if get_available_points(driver) > cost:
            enter_btn.click()
            print(f"Giveaway entered: {giveaway_page}")
            time.sleep(1)
    pagination_elements = driver.find_elements(By.XPATH, "//a[./span[contains(., 'Next')]]")
    if len(pagination_elements) > 0:
        pagination_elements[0].click()
        enter_giveaways(driver)
        
def __main__():
    print("Start steamgifts auto enter")
    if len(sys.argv) > 0 and "headless" in sys.argv:
        print("Going headless")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Firefox()
    try:
        driver.get(base_url)
        load_cookies(driver)
        driver.get(base_url)
        wait_for_load(driver)
        is_not_signed_in = len(driver.find_elements(By.XPATH, "//a[@href='/?login']")) > 0
        if is_not_signed_in:
            login(driver, username, password)
        sync_steam(driver)
        print(f"Available points: {get_available_points(driver)}")
            
        if get_available_points(driver) > 0:
            navigate_and_enter_giveaways(driver, Filter.WISHLIST)
            print(f"Available points after wishlist giveaways: {get_available_points(driver)}")
        if get_available_points(driver) > 0:
            navigate_and_enter_giveaways(driver, Filter.DLC)
            print(f"Available points after dlc giveaways: {get_available_points(driver)}")
        if get_available_points(driver) > 0:
            navigate_and_enter_giveaways(driver, Filter.RECOMMENDED)
            print(f"Available points after recommended giveaways: {get_available_points(driver)}")
    finally:
        driver.close()
    print("Steamgifts auto enter done")
    
__main__()