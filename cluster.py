from glob import glob
import json
import os
import random
import sys
from traceback import print_tb
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from vectorizer import Vectorizer

NUM_CLUSTERS = 4
NUM_TOP_VERS = 30


def most_common_cards(_deck, k):
    _deck.sort(key=lambda _deck: _deck[1], reverse=True)
    return [card[0] for card in _deck[:k]]


def decks_by_label(a_label, _labeled):
    return [(deck, label) for (deck, label) in _labeled if label == a_label]



decks_csv = glob("samples/*.csv")

f = open('db/cards.json')
cards_db = json.load(f)
decks_vectorizer = Vectorizer(cards_db)
decks_vectorizer.initialize()
vectorizers = decks_vectorizer.vectorizers


for n in decks_csv:
    craft = n.split(os.sep)[1]
    craft = craft.split('-')[0]
    df = pd.read_csv(n, header=None)
    df_list = df.values.tolist()
    df_list = df_list[1:]
    vectorizers[craft].vectorize(df_list)


name_out = sys.argv[1] if sys.argv[1] is not None else 'unknown-meta.json'
output = {}

if(os.path.exists(name_out)):
    f = open(name_out)
    output = json.load(f)

for (craft, vectorizer) in vectorizers.items():
    all_cards = []
    class_json = {
        'archetypes': {},
    }

    archetypes = {}

    if(craft in output):
        archetypes = output[craft]


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
with open(name_out, 'w') as out:
    json.dump(output, out, indent=4)


    




