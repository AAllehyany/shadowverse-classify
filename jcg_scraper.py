
from operator import itemgetter
import pandas as pd
import numpy as np
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
        self.jcg_code = jcg_code

    
    def scrape_entries(self):

        # Web scrapper for infinite scrolling page 
        driver.get(self.entries_link)
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
            user = entry.find_element(By.CLASS_NAME, 'name-main')
            id = user.get_attribute('href').split('/')[-1]
            name = user.text.strip()

            parsed_decks = []

            for deck in decks:
                parsed_deck = SVPortalParser(deck, 'roar-of-godywrm.json')
                parsed_deck.parse_deck()
                parsed_deck.find_archetype()
                parsed_decks.append(parsed_deck.get_deck_data())
            
            player_dict = {
                "name": name,
                "decks": parsed_decks,
                "top": 0,
                "id": id
            }

            self.entry_decks[id] = player_dict
    
    def get_links(self):

        # Web scrapper for infinite scrolling page 
        driver.get(self.entries_link)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 0.2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1
        links = []

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
            links.extend(decks)

        return links
        # links_df = pd.DataFrame(links)
        # links_df.to_csv(f'{self.jcg_code}-decks.csv', index=False)

        
        

    def scrape_results(self):
        driver.get(self.results_link)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        entries = driver.find_elements(By.CSS_SELECTOR, '.result-1')

        for entry in entries:
            user = entry.find_element(By.CLASS_NAME, 'result-name')
            id = user.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')[-1]
            if id in self.entry_decks:
                self.entry_decks[id]["top"] += 4
            
        
        driver.close()



# jcg_code = "7170grvqK2HI"
# scraper = JCGScraper(jcg_code)
# scraper.scrape_entries()
# scraper.scrape_results()

# jcg_data = scraper.entry_decks.values()
# sorted_data = sorted(jcg_data, key=itemgetter("top"), reverse=True)

# jcg_decks_data = []

# for data in jcg_data:
#     for deck in data["decks"]:
#         result = (deck["craft"], deck["archetype"], deck["link"], data["top"])
#         jcg_decks_data.append(result)

# decks_data_df = pd.DataFrame(jcg_decks_data,
#     columns=[
#         "craft",
#         "archetype",
#         "deck_link",
#         "score"
#     ]
# )

# archetype_df = decks_data_df['archetype'].value_counts()
# craft_df = decks_data_df['craft'].value_counts()

# decks_data_df.to_csv(f"classified_decks-{jcg_code}.csv", index=False)
# archetype_df.to_csv(f"archetypes-{jcg_code}.csv")
# craft_df.to_csv(f"crafts-{jcg_code}.csv")