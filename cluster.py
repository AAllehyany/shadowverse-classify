from ast import arg
import collections
from glob import glob
import json
import os
import random
import sys
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, OPTICS
import matplotlib.pyplot as plt
import argparse

from vectorizer import Vectorizer

NUM_TOP_VERS = 40

f = open('db/cards_data.json')
cards_data = json.load(f)

def most_common_cards(_deck, k):
    _deck.sort(key=lambda _deck: _deck["copies"], reverse=True)
    return [f'{card["card_name"]}' for card in _deck[:NUM_TOP_VERS]]


def decks_by_label(a_label, _labeled):
    return [(deck, label) for (deck, label) in _labeled if label == a_label]

def process_samples(sample_file):

    s = open(sample_file)
    return json.load(s)


def start_cluster(format_name="", num_clusters=4, target_craft="all"):
    """Clusters each craft into 4 different decks to identify archetypes.

    This method separates all decks into their proper craft vectorizer,
    and then iterates over the vectorizers to detect different archetypes.

    If a cluster is named the same as another cluster, they will be merged 
    together and their cards will form a set. However, you can still end up
    with four different clusters for each craft, and you can 
    change n_clusters to how many clusters you want.
    """
    # if not os.path.exists('samples'):
    #     print('Unable to locate samples folder')
    #     sys.exit(2)
    output = {}

    decks_csv = glob("samples/*.csv")
    
    decks_vectorizer = Vectorizer(cards_data)
    decks_vectorizer.initialize()
    # decks_vectorizer.vectorize_from_sample(decks_csv)
    decks_vectorizer.vectorize_from_json(process_samples('./deck-samples/samples.json'))
    vectorizers = decks_vectorizer.vectorizers

    
    if(os.path.exists(format_name)):
        f_format = open(format_name)
        output = json.load(f_format)

    for (craft, vectorizer) in vectorizers.items():

        if target_craft != "all" and craft != target_craft:
            continue
        
        archetypes = {}
        generics = set()

        if(craft in output):
            archetypes = output[craft]


        km = KMeans(n_clusters=num_clusters)
        km.fit(vectorizer.vectorized)
        km_labels = km.labels_
        labeled_decks = list(zip(vectorizer.decks, km_labels))

        # km = OPTICS(min_samples=12)
        # km.fit(vectorizer.vectorized)
        # km_labels = km.labels_
        # labeled_decks = list(zip(vectorizer.decks, km_labels))
        # num_clusters = len(set(km_labels)) - (1 if -1 in km_labels else 0)
        # noise = list(km_labels).count(-1)

        # print(f'We got {num_clusters} clusters. And {noise} noisy samples')

        for cluster_id in range(num_clusters):
            cluster_decks = decks_by_label(cluster_id, labeled_decks)
            
            # Get feature cards for this group
            first_deck = cluster_decks[0][0] 
            feature_cards = set(most_common_cards(first_deck, 15))

            for deck, _ in decks_by_label(cluster_id, labeled_decks):
                new_features = set(most_common_cards(deck, 15))
                feature_cards = feature_cards.intersection(new_features)

            print('\n--- Up to three (3) sample decks from group.')
            three = random.choices(cluster_decks, k=4)

            for d in three:
                sorted_deck = sorted(d[0], key=lambda i: i["card_name"])
                [print(f'{card["copies"]}x {card["card_name"]}') for card in sorted_deck]
                print('---')
            
            print(f'Most common cards: {feature_cards}')
            name = input(f'[{len(cluster_decks)}] Similar decks. Archetype name: ')


            a_id = name.lower().replace(' ', '_')
            # Grab all different hashes for each card
            featured_list = list(feature_cards)
            
            archetype = {
                "name": name,
                "craft": craft,
                "feature_cards": featured_list
            }

            if a_id in archetypes:
                cards1 = archetypes[a_id]["feature_cards"]
                featured_list.extend(cards1)
                cards2 = set(featured_list)
                archetypes[a_id]["feature_cards"] = list(cards2)
            else:
                archetypes[a_id] = archetype

        output[craft] = archetypes


    #out put details into a file
    with open(format_name, 'w') as out:
        json.dump(output, out, indent=4)


def get_list_with_hashes(common_cards):
    result = []

    for card in common_cards:
        cards_with_hash = [f'{c["card_name"]}---{c["card_hash"]}' for c in cards_data if c["card_name"].lower() == card.lower()]
        result.extend(cards_with_hash)
    
    return result

    
    

    
if __name__ =="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help="The format file you want to save to.", default="celestial-dragonblade.json")
    parser.add_argument('-n', type=int, help="How many clusters do you want to separate decks to", default=4)

    parser.add_argument('-c', type=str, help="If you want to work on one class only", default="all")
    args = parser.parse_args()
    start_cluster(args.f, args.n, args.c)