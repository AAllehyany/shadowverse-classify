import numpy as np


class Vectorizer:

    def __init__(self, all_cards):
        self.all_cards = all_cards
        self.vectorizers = {}
        self.crafts = ['forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']

    def initialize(self):
        
        
        for craft in self.crafts:
            craft_name = craft + 'craft'
            scope = (craft_name, 'netural')
            ignored = ("promo", "token")
            filtered = [card["name_"] for card in self.all_cards.values() if card["craft_"].lower() in scope and card["expansion_"].lower() not in ignored]

            unique = set(filtered)
            sorted = np.sort(list(unique))
            self.vectorizers[craft] = ClassVectorizer(craft, sorted)

    def vectorize(self, deck, craft):
        if craft not in self.crafts:
            return
        
        self.vectorizers[craft].vectorize(deck)

class ClassVectorizer:

    def __init__(self, craft, card_pool):
        self.craft = craft
        self.card_pool = card_pool
        self.vectorized = []
        self.decks = []

    # def initialize(self):
    #     self.card_pool = get_craft_vector(self.craft)

    def vectorize(self, deck):
        vector = [0]*len(self.card_pool)

        for (idx, name) in enumerate(self.card_pool):
            for [card, copies] in deck:
                if card == name:
                    vector[idx] += int(copies)

        self.vectorized.append(vector)
        self.decks.append(deck)
