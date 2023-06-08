from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from enum import Enum
from typing import List
import pickle
import os
import time
import sys

base_url = "https://www.steamgifts.com"
user_settings_route = "/account/settings/profile"
login_route = "/?login"
giveaways_search_route = "/giveaways/search"

class Filter(Enum):
    WISHLIST = "type=wishlist"
    RECOMMENDED = "type=recommended"
    DLC = "dlc=true"

class SteamgiftsAutoenter():
    
    def __init__(self, username:str, password: str, cookies_file:str, blacklist: List[str], log = print):
        if username is None or username == "":
            sys.exit("Missing username")
        if password is None or password == "":
            sys.exit("Missing password")
        self.username = username
        self.password = password
        self.cookies_file = cookies_file
        self.blacklist = blacklist
        self.log = log
        if self.cookies_file is None or self.cookies_file == None:
            self.cookies_file = "cookies.pkl"
    
    def store_cookies(self):
        self.log(f"Storing cookies to {self.cookies_file}")
        parent_dir = os.path.dirname(self.cookies_file)
        if parent_dir is not None and parent_dir != "":
            os.makedirs(parent_dir, exist_ok=True)
        pickle.dump(self.driver.get_cookies(), open(self.cookies_file, "wb"))
    
    def load_cookies(self):
        if os.path.isfile(self.cookies_file):
            self.log(f"Cookies available at {self.cookies_file}")
            cookies = pickle.load(open(self.cookies_file, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
    
    def login(self):
        self.driver.get(f"{base_url}{login_route}")
        pass_elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        user_elem = self.driver.find_element(By.XPATH, "//input[@type='text']")
        user_elem.clear()
        user_elem.send_keys(self.username)
        pass_elem.clear()
        pass_elem.send_keys(self.password)
        submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_btn.click()
        
        self.log("Waiting for user to allow the login...")
        signin_followup = WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.ID, "imageLogin"))
        )
        
        signin_followup.click()
        self.store_cookies()
        
    def sync_steam(self):
        self.log("Sync with steam...")
        self.driver.get(f"{base_url}{user_settings_route}")
        self.driver.find_element(By.CLASS_NAME, "form__sync-default").click()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='notification notification--success']"))
        )
        
        
    def wait_for_load(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav__right-container"))
        )
        
    def get_available_points(self):
        return int(self.driver.find_element(By.CLASS_NAME, "nav__points").text)
        
    def navigate_and_enter_giveaways(self, filter: Filter = None):
        self.driver.get(f"{base_url}{giveaways_search_route}{f'?{filter.value}' if filter is not None else ''}")
        self.enter_giveaways()
        
    def get_game_name_from_url(self, url):
        split = url.split("/")
        return split[len(split)-1]
    
    def enter_giveaways(self):
        self.wait_for_load()
        not_entered = self.driver.find_elements(By.XPATH, "//div[@class='giveaway__row-inner-wrap']")
        giveaways_hrefs = []
        for giveaway in not_entered:
            anchor_candidates = giveaway.find_elements(By.XPATH, "a[@class='giveaway_image_thumbnail']")
            if len(anchor_candidates) < 1:
                anchor_candidates = giveaway.find_elements(By.XPATH, "a[@class='giveaway_image_thumbnail_missing']")
            if len(anchor_candidates) < 1:
                self.log("Error getting the giveaway link. Skipping...")
                continue
            anchor = anchor_candidates[0]
            headings = giveaway.find_elements(By.CLASS_NAME, "giveaway__heading__thin")
            if len(headings) > 1:
                points_text = headings[1].text
            else:
                points_text = headings[0].text
            cost = int(points_text[1:points_text.index('P')])
            giveaways_hrefs.append((anchor.get_attribute("href"), cost))
        for (giveaway_page, cost) in giveaways_hrefs:
            if self.get_game_name_from_url(giveaway_page) not in self.blacklist and self.get_available_points() > cost:
                self.enter_giveaway(giveaway_page)
        pagination_elements = self.driver.find_elements(By.XPATH, "//a[./span[contains(., 'Next')]]")
        if len(pagination_elements) > 0:
            pagination_elements[0].click()
            self.enter_giveaways()
            
    def enter_giveaway(self, giveaway_page):
        try:
            self.driver.get(giveaway_page)
            enter_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-do='entry_insert']"))
            )
            enter_btn.click()
            self.log(f"Giveaway entered: {giveaway_page}")
            time.sleep(1)
        except TimeoutException as e:
            self.log(f"WARNING! Could not find the enter button for giveaway {giveaway_page}. Skipping...")
            
    def run(self, headless = True):
        self.log("Start steamgifts auto enter")
        if headless:
            self.log("Going headless")
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Firefox()
            
        try:
            self.driver.get(base_url)
            self.load_cookies()
            self.driver.get(base_url)
            self.wait_for_load()
            is_not_signed_in = len(self.driver.find_elements(By.XPATH, "//a[@href='/?login']")) > 0
            if is_not_signed_in:
                self.login()
            self.sync_steam()
            self.log(f"Available points: {self.get_available_points()}")
                
            if self.get_available_points() > 0:
                self.navigate_and_enter_giveaways(Filter.WISHLIST)
                self.log(f"Available points after wishlist giveaways: {self.get_available_points()}")
            if self.get_available_points() > 0:
                self.navigate_and_enter_giveaways(Filter.DLC)
                self.log(f"Available points after dlc giveaways: {self.get_available_points()}")
            if self.get_available_points() > 0:
                self.navigate_and_enter_giveaways(Filter.RECOMMENDED)
                self.log(f"Available points after recommended giveaways: {self.get_available_points()}")
        finally:
            self.driver.close()
        self.log("Steamgifts auto enter done")