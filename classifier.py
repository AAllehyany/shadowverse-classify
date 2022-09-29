
import json
import os

from vectorizer import Vectorizer
from sklearn.cluster import KMeans, DBSCAN

d = open('db/cards_data.json')
db = json.load(d)

def detect_feature_cards(_deck, k):
    _deck.sort(key=lambda _deck: _deck[1], reverse=True)
    return [f'{card[0]}' for card in _deck[:k]]

def decks_by_cluster(a_label, _labeled):
    return [(deck, label) for (deck, label) in _labeled if label == a_label]


def classify(format_file="", n_clusters=4, craft="all"):


    samples = []
    sample_file = 'json_sample.json'
    with open(sample_file) as s:
        samples = json.load(s)

    format_meta = {}
    if(os.path.exists(format_file)):
        f_format = open(format_file)
        format_meta = json.load(f_format)

    # Initialize the vectorizers
    base_vectorizer = Vectorizer(db)
    base_vectorizer.initialize_by_ids()
    base_vectorizer.vectorize_from_json(samples)

    if craft == "all":

        for (craft, vectorizer) in base_vectorizer.vectorizers.items():

            # Keep track of detected archetypes
            archetypes = {}

            # If the format file already contains data for this craft
            # we merge it 
            if( craft in format_meta):
                archetypes = format_meta[craft]
            
            km = KMeans(n_clusters=n_clusters)
            km.fit(vectorizer.vectorized)
            km_labels = km.labels_
            labeled_decks = list(zip(vectorizer.decks, km_labels))

            for cluster in range(n_clusters):

                decks = decks_by_cluster(cluster, labeled_decks)

        


