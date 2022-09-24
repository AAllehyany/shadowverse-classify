
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sv_portal_reader import SVPortalParser


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
class JCGScraper:

    def __init__(self, jcg_code):
        self.entries_link = f'https://sv.j-cg.com/competition/{jcg_code}/entries'
        self.results_link = f'https://sv.j-cg.com/competition/{jcg_code}/results'
        self.entry_decks = {}

    
    def scrape_entries(self):

        # Web scrapper for infinite scrolling page 
        driver.get("https://sv.j-cg.com/competition/J1kNoaYPvxQx/entries")
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 0.2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1

        while True:
            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

        entries = driver.find_elements(By.CSS_SELECTOR, '.entry.winner')

        for entry in entries:
            decks = entry.find_element(By.CLASS_NAME, 'entry-deck')
            decks = [link.get_attribute('href') for link in decks.find_elements(By.TAG_NAME, 'a')]
            name = entry.find_element(By.CLASS_NAME, 'name-main').text.strip()
            player_dict = {
                "name": name,
                "decks": decks,
                "top": 0
            }

            self.entry_decks[name] = player_dict
        

    def scrape_results(self):
        driver.get(self.results_link)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        entries = driver.find_elements(By.CSS_SELECTOR, '.result-1')

        for entry in entries:
            decks = entry.find_element(By.CLASS_NAME, 'result-deck')
            decks = [link.get_attribute('href') for link in decks.find_elements(By.TAG_NAME, 'a')]
            name = entry.find_element(By.CLASS_NAME, 'result-name').text.strip()
            player_dict = {
                "name": name,
                "decks": decks,
                "top": 0
            }

            self.entry_decks[name] = player_dict
        
        driver.close()



jcg_code = "J1kNoaYPvxQx"
scraper = JCGScraper(jcg_code)
scraper.scrape_results()

for (player, data) in scraper.entry_decks.items():

    for deck in data["decks"]:
        
        parsed_deck = SVPortalParser(deck)
        parsed_deck.parse_deck()
        parsed_deck.find_archetype()

# df = pd.DataFrame.from_dict(scraper.entry_decks, orient='index', columns=['name', 'deck1', 'deck2', 'top'])
# df.to_csv(f'{jcg_code}-decks.csv', index=False)