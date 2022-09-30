from collections import Counter
import json
from typing import Collection
import pandas as pd

f = open('db/cards_data.json')
hashes = json.load(f)

class SVPortalParser:

    """
    A Class to read and parse decks from Shadowverse Portal link


    Attributes:
    ------------
    archetypes: str
        a string with the name of the 
    """

    def __init__(self, format_data={}):
        self.deck = {}

        self.craft = ""
        self.archetypes = format_data
        self.decks = []

    def parse_craft(self, deck_link):
        """Returns the craft the deck belongs to

        Parameters
        -----------
        deeck_link : str
            a https://shadowverse-porta.com link to the deck
        """

        classes = ['forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']
        class_code = int(deck_link.split('.')[2]) - 1

        return classes[class_code]
    
    def prase_hashes(self, deck_link):
        """Separates the different hashes in the deck link

        Parameters
        -----------
        deeck_link : str
            a https://shadowverse-porta.com link to the deck
        """

        card_hashes = deck_link.split('.',3)[3:]
        card_hashes = ".".join(card_hashes)
        card_hashes = card_hashes.split('?')[0]
        card_hashes = card_hashes.split('.')
        return card_hashes
    
    def parse_deck(self, deck_link):
        """Returns info about the parsed deck

        Parameters
        -----------
        deeck_link : str
            a https://shadowverse-porta.com link to the deck
        """
        craft = self.parse_craft(deck_link)
        hash_list = self.prase_hashes(deck_link)
        hash_count = dict(Counter(hash_list))

        deck_list = [(c["card_name"], hash_count[c["card_hash"]], c["card_hash"]) for c in hashes if c["card_hash"] in hash_list]

        archetype = self.find_archetype(hash_list, craft)

        deck_data = {
            "link": deck_link,
            "archetype": archetype,
            "craft": craft,
            "cards_df": deck_list
        }

        return deck_data

    def parse_deck_json(self, deck_link):
        """Returns info about the parsed deck

        Parameters
        -----------
        deeck_link : str
            a https://shadowverse-porta.com link to the deck
        """
        craft = self.parse_craft(deck_link)
        hash_list = self.prase_hashes(deck_link)
        hash_count = dict(Counter(hash_list))
        cards_list = [c["card_name"] for c in hashes if c["card_hash"] in hash_list]
        deck_list = [{
            "card_name": c["card_name"],
            "copies": hash_count[c["card_hash"]],
            "base_id": c["base_id"],
            "hash": c["card_hash"]
        } for c in hashes if c["card_hash"] in hash_list]

        self.decks.append({"craft": craft, "deck_list":deck_list})

        archetype = self.find_archetype(cards_list, craft)

        deck_data = {
            "link": deck_link,
            "archetype": archetype,
            "craft": craft,   
        }

        return deck_data
    
    def find_archetype(self, cards, craft):
        """Returns the craft the deck belongs to

        Parameters
        -----------
        cards : List
            a list of the cards in the deck
        
        craft : str
            the craft the deck belongs to
        """

        if craft not in self.archetypes:
            return ""
        
        craft_archetypes = self.archetypes[craft]
        current_score = 0
        current_archetype = ""

        for (name, details) in craft_archetypes.items():
            archetype_score = 0
            for card in details["feature_cards"]:
                _card = card
                for hash in cards:
                    if hash == _card:
                        archetype_score += 1

            if archetype_score > current_score:
                current_score = archetype_score
                current_archetype = name  

        
        return current_archetype

    def write_lists(self):
        pass
            





    
