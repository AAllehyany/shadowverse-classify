from glob import glob
import json
import os
import random
import sys
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


def start_cluster(format_name=""):

    if not os.path.exists('samples'):
        print('Unable to locate samples folder')
        sys.exit(2)
    output = {}

    decks_csv = glob("samples/*.csv")

    cards_db = {}
    with open('db/cards.json') as f_cards:
        cards_db = json.load(f_cards)
    
    decks_vectorizer = Vectorizer(cards_db)
    decks_vectorizer.initialize()
    decks_vectorizer.vectorize_from_sample(decks_csv)
    vectorizers = decks_vectorizer.vectorizers

    if(os.path.exists(format_name)):
        f_format = open(format_name)
        output = json.load(f_format)

    for (craft, vectorizer) in vectorizers.items():

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
    with open(format_name, 'w') as out:
        json.dump(output, out, indent=4)

if __name__ =="__main__":
    format_name = sys.argv[1] if sys.argv[1] is not None else 'unknown-meta.json'
    start_cluster(format_name)