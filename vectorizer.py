import numpy as np
import json

f = open('cards.json')
cards_db = json.load(f)
def get_craft_vector(craft):
    crafts = ['forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']
    
    if craft not in crafts:
        return

    craft_name = craft + 'craft'
    scope = (craft_name, 'netural')
    ignored = ("promo", "token")
    filtered = [card["name_"] for card in cards_db.values() if card["craft_"].lower() in scope and card["expansion_"].lower() not in ignored]

    unique = set(filtered)
    sorted = np.sort(list(unique))
    
    return sorted

class ClassVectorizer:

    def __init__(self, craft):
        self.craft = craft
        self.card_pool = []
        self.vectorized = []
        self.decks = []

        self.initialize()

    def initialize(self):
        self.card_pool = get_craft_vector(self.craft)

    def vectorize(self, deck):
        vector = [0]*len(self.card_pool)

        for (idx, name) in enumerate(self.card_pool):
            for [card, copies] in deck:
                if card == name:
                    vector[idx] += int(copies)

        self.vectorized.append(vector)
        self.decks.append(deck)
