import json
import pandas as pd

hashes = pd.read_csv("codes.csv")

class SVPortalParser:


    def __init__(self, deck_link):
        self.deck_link = deck_link
        self.deck = {}
        self.hash_list = []
        self.craft = ""

    def parse_craft(self):
        classes = ['forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']
        class_code = int(self.deck_link.split('.')[2]) - 1

        self.craft = classes[class_code]
    
    def prase_hashes(self):
        card_hashes = self.deck_link.split('.',3)[3:]
        card_hashes = ".".join(card_hashes)
        card_hashes = card_hashes.split('?')[0]
        card_hashes = card_hashes.split('.')
        
        self.hash_list = card_hashes
    
    def parse_deck(self):
        self.parse_craft()
        self.prase_hashes()

        d = pd.DataFrame(self.hash_list)
        d = d[0].value_counts().reset_index().rename(columns={'index': 'code', 0: 'count'})
        deck_df = pd.merge(d, hashes)[['count', 'card_name']]
        deck_df = deck_df.groupby('card_name', as_index = False).agg('sum')

        self.deck["cards"] = deck_df.values.tolist()
    
    def find_archetype(self):
        f = open('./roar-of-godwyrm.json')
        archetypes = json.load(f)

        craft_archetypes = archetypes[self.craft]
        current_score = 0
        current_archetype = ""

        # for each archetype => check score.
        # if current score is max => make it archetype

        for (name, details) in craft_archetypes.items():
            archetype_score = 0
            for card in details["feature_cards"]:
                for (card_n, copies) in self.deck["cards"]:
                    if card_n == card:
                        archetype_score += copies

            if archetype_score > current_score:
                current_score = archetype_score
                current_archetype = name  
        
        print('\n--------')
        print(f'this deck belongs to {current_archetype}.')
        print(*self.deck["cards"])
        print('--------\n')

            





    
