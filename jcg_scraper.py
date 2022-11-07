
import json
from operator import itemgetter
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sv_portal_reader import SVPortalParser


class JCGScraper:

    def __init__(self, jcg_code, parser: SVPortalParser):
        self.entries_link = f'https://sv.j-cg.com/competition/{jcg_code}/entries'
        self.results_link = f'https://sv.j-cg.com/competition/{jcg_code}/results'
        self.entry_decks = {}
        self.jcg_code = jcg_code
        self.sv_portal_praser = parser
        self.jcg_date = ""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


    
    def scrape_entries(self):

        # Web scrapper for infinite scrolling page 
        self.driver.get(self.entries_link)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 0.2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = self.driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1

        while True:
            # scroll one screen height each time
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

        entries = self.driver.find_elements(By.CSS_SELECTOR, '.entry.winner')
        date = self.driver.find_element(By.CLASS_NAME, 'competition-date')
        self.jcg_date = (date.text.split('\n')[0].replace('.', ''))
        for entry in entries:
            decks = entry.find_element(By.CLASS_NAME, 'entry-deck')
            decks = [link.get_attribute('href') for link in decks.find_elements(By.TAG_NAME, 'a')]
            user = entry.find_element(By.CLASS_NAME, 'name-main')
            id = user.get_attribute('href').split('/')[-1]
            name = user.text.strip()

            parsed_decks = []
            for deck in decks:
                parsed = self.sv_portal_praser.parse_deck(deck)
                parsed_decks.append(parsed)
            
            player_dict = {
                "name": name,
                "decks": parsed_decks,
                "top": 0,
                "id": id
            }

            self.entry_decks[id] = player_dict

    def scrape_entries_json(self):

        # Web scrapper for infinite scrolling page 
        self.driver.get(self.entries_link)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 0.2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = self.driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1

        while True:
            # scroll one screen height each time
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

        entries = self.driver.find_elements(By.CSS_SELECTOR, '.entry.winner')
        date = self.driver.find_element(By.CLASS_NAME, 'competition-date')
        self.jcg_date = (date.text.split('\n')[0].replace('.', ''))
        for entry in entries:
            decks = entry.find_element(By.CLASS_NAME, 'entry-deck')
            decks = [link.get_attribute('href') for link in decks.find_elements(By.TAG_NAME, 'a')]
            user = entry.find_element(By.CLASS_NAME, 'name-main')
            id = user.get_attribute('href').split('/')[-1]
            name = user.text.strip()

            parsed_decks = []
            for deck in decks:
                parsed = self.sv_portal_praser.parse_deck_json(deck, id)

                deck_data = {
                    "link": parsed["link"],
                    "archetype": parsed["archetype"],
                    "craft": parsed["craft"],
                }
                parsed_decks.append(deck_data)
            
            player_dict = {
                "name": name,
                "decks": parsed_decks,
                "top": 0,
                "id": id
            }

            self.entry_decks[id] = player_dict
    
    def get_links(self):

        # Web scrapper for infinite scrolling page 
        self.driver.get(self.entries_link)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 0.2 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = self.driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1
        links = []

        while True:
            # scroll one screen height each time
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

        entries = self.driver.find_elements(By.CSS_SELECTOR, '.entry.winner')

        for entry in entries:
            decks = entry.find_element(By.CLASS_NAME, 'entry-deck')
            decks = [link.get_attribute('href') for link in decks.find_elements(By.TAG_NAME, 'a')]
            links.extend(decks)

        return links


        
        

    def scrape_results(self, rest=False):
        self.driver.get(self.results_link)
        time.sleep(2)  # Allow 2 seconds for the web page to open
        entries = self.driver.find_elements(By.CSS_SELECTOR, '.result-1')
        second_places = self.driver.find_elements(By.CSS_SELECTOR, '.result-2')
        third_fourth = self.driver.find_elements(By.CSS_SELECTOR, '.result-3')

        for entry in entries:
            user = entry.find_element(By.CLASS_NAME, 'result-name')
            id = user.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')[-1]
            if id in self.entry_decks:
                self.entry_decks[id]["top"] += 2

        if rest:
            for entry in second_places:
                user = entry.find_element(By.CLASS_NAME, 'result-name')
                id = user.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')[-1]
                if id in self.entry_decks:
                    self.entry_decks[id]["top"] += 1

            for entry in third_fourth:
                user = entry.find_element(By.CLASS_NAME, 'result-name')
                id = user.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')[-1]
                if id in self.entry_decks:
                    self.entry_decks[id]["top"] += 0.5
        
            
        
        self.driver.close()