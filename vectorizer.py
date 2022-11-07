import numpy as np
import pandas as pd
import os

class Vectorizer:

    """
    A class that holds the vectorizers for all crafts

    Attributes
    ----------

    all_cards : List
        a list that holds all the cards in the game
    
    vectorizers: Dict of ClassVectorizers
        a dictionary that maps each craft to its vectorizer
    """

    def __init__(self, all_cards):
        self.all_cards = all_cards
        self.vectorizers = {}
        self.crafts = ['forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']

    def initialize(self):
        
        """Initializes all class vectorizers with teh appropriate card pool
        """
        
        for craft in self.crafts:
            craft_name = craft + 'craft'
            scope = (craft_name, 'netural')
            filtered = [card["card_name"] for card in self.all_cards if card["craft"].lower() in scope]

            unique = set(filtered)
            sorted = np.sort(list(unique))
            self.vectorizers[craft] = ClassVectorizer(craft, sorted)

    def initialize_by_ids(self):
        """Initializes all class vectorizers with teh appropriate card pool
        """
        
        for craft in self.crafts:
            craft_name = craft + 'craft'
            target = (craft_name, 'netural')
            filtered = [card["base_id"] for card in self.db if card["craft"].lower() in target]

            ## filter out duplicate IDs because of promo cards
            unique = set(filtered)
            sorted = np.sort(list(unique))
            self.vectorizers[craft] = ClassVectorizer(craft, sorted)

    def vectorize(self, deck, craft):

        """Vectorizes the provided deck using its ClassVectorizer
        
        Parameters
        -----------

        deck: List
            a list of cards and their copies
        
        craft: str
            the deck craft
        """
        if craft not in self.crafts:
            return
        
        self.vectorizers[craft].vectorize(deck)

    def vectorize_from_sample(self, sample_folder):
        for n in sample_folder:
            craft = n.split(os.sep)[1]
            craft = craft.split('-')[2]
            df = pd.read_csv(n, header=None)
            df_list = df.values.tolist()
            df_list = df_list[1:]
            self.vectorizers[craft].vectorize(df_list)

    def vectorize_from_json(self, decks):

        for deck in decks:
            self.vectorizers[deck["craft"]].vectorize_json_deck(deck["deck_list"])

class ClassVectorizer:

    def __init__(self, craft, card_pool):
        self.craft = craft
        self.card_pool = card_pool
        self.vectorized = []
        self.decks = []

    def vectorize(self, deck):
        vector = [0]*len(self.card_pool)

        for (idx, name) in enumerate(self.card_pool):
            for [card, copies, _base_id, _hash] in deck:
                if card == name:
                    vector[idx] += int(copies)

        self.vectorized.append(vector)
        self.decks.append(deck)

    def vectorize_json_deck(self, deck):

        vector = [0]*len(self.card_pool)

        for (idx, card) in enumerate(self.card_pool):

            for deck_card in deck:

                if deck_card["card_name"] == card:
                    vector[idx] += deck_card["copies"]
        
        self.vectorized.append(vector)
        self.decks.append(deck)

