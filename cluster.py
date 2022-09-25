from glob import glob
import json
import os
import random
from traceback import print_tb
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from vectorizer import ClassVectorizer

NUM_CLUSTERS = 4
NUM_TOP_VERS = 30


def card_names(_deck):
    return [card[0] for card in _deck]


def most_common_cards(_deck, k):
    _deck.sort(key=lambda _deck: _deck[1], reverse=True)
    return [card[0] for card in _deck[:k]]


def decks_by_label(a_label, _labeled):
    return [(deck, label) for (deck, label) in _labeled if label == a_label]



crafts = ['forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']

decks_csv = glob("jcg-decks/*.csv")

vectorizers = dict((craft, ClassVectorizer(craft)) for craft in crafts)


for n in decks_csv:
    craft = n.split(os.sep)[1]
    craft = craft.split('-')[0]
    df = pd.read_csv(n, header=None)
    df_list = df.values.tolist()
    df_list = df_list[1:]
    vectorizers[craft].vectorize(df_list)

output = {}
for (craft, vectorizer) in vectorizers.items():
    all_cards = []
    class_json = {
        'archetypes': {},
    }

    archetypes = {}


    km = KMeans(n_clusters=NUM_CLUSTERS)
    km.fit(vectorizer.vectorized)
    km_labels = km.labels_
    labeled_decks = list(zip(vectorizer.decks, km_labels))
    
    for cluster_id in range(NUM_CLUSTERS):
        cluster_decks = decks_by_label(cluster_id, labeled_decks)
        print('\n--- Detected new group')
        print(f'There are {len(cluster_decks)} decks in this group. And here is one sample deck.')
        print(*random.choice(cluster_decks)[0], sep='\n')
        name = input(f'What would you like to name this cluster?')
        print(f'--- successfully labeled the group as {name}\n')

        # Get feature cards for this group
        first_deck = decks_by_label(cluster_id, labeled_decks)[0][0] 
        feature_cards = set(most_common_cards(first_deck, 30))

        for deck, _ in decks_by_label(cluster_id, labeled_decks):
            feature_cards.intersection(
                set(most_common_cards(deck, 30))
            )

        
        a_id = name.lower().replace(' ', '_')
        archetype = {
            "name": name,
            "craft": craft,
            "feature_cards": list(feature_cards)
        }

        if a_id in archetypes:
            cards1 = set(archetypes[a_id]["feature_cards"])
            cards2 = feature_cards.intersection(cards1)
            archetypes[a_id]["feature_cards"] = list(cards2)
        else:
            archetypes[a_id] = archetype

    output[craft] = archetypes


#out put details into a file
with open('roar-of-godwyrm.json', 'w') as out:
    json.dump(output, out, indent=4)