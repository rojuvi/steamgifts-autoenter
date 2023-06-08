from steamgifts_autoenter import SteamgiftsAutoenter
import os
import sys


username = os.environ.get("STEAM_USERNAME")
password = os.environ.get("STEAM_PASSWORD")
blacklist = [game_name.strip().replace("\"", "").replace("'", "") for game_name in os.environ.get("BLACKLIST").split(",")]
print(f"blacklist: {blacklist}")
cookies_file = os.environ.get("COOKIES_FILE")
if cookies_file is None or cookies_file == None:
    cookies_file = "cookies.pkl"
headless = len(sys.argv) > 0 and "--headless" in sys.argv
    
SteamgiftsAutoenter(username, password, cookies_file, blacklist).run(headless=headless)