import json
import pandas as pd

hashes = pd.read_csv("db/codes.csv")

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

        d = pd.DataFrame(hash_list)
        d = d[0].value_counts().reset_index().rename(columns={'index': 'code', 0: 'count'})
        deck_df = pd.merge(d, hashes)[['count', 'card_name']]
        deck_df = deck_df.groupby('card_name', as_index = False).agg('sum')

        cards = deck_df.values.tolist()
        cards_df = deck_df
        archetype = self.find_archetype(cards, craft)

        deck_data = {
            "link": deck_link,
            "archetype": archetype,
            "craft": craft,
            "cards_df": cards_df
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
                for (card_n, copies) in cards:
                    if card_n == card:
                        archetype_score += copies

            if archetype_score > current_score:
                current_score = archetype_score
                current_archetype = name  

        
        return current_archetype

            





    
