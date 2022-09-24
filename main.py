import json
import os
import re
import pandas as pd

df = pd.read_csv("codes.csv")

def hash_list(deck_link):
    card_hashes = deck_link.split('.',3)[3:]
    card_hashes = ".".join(card_hashes)
    card_hashes = card_hashes.split('?')[0]
    card_hashes = card_hashes.split('.')
    
    return card_hashes


def detect_class(deck_link):
    classes = ['forest', 'sword', 'rune', 'dragon', 'shadow', 'blood', 'haven', 'portal']
    class_code = int(deck_link.split('.')[2]) - 1

    return classes[class_code]

def write_list(deck_link, i):
    card_hashes = hash_list(deck_link)
    deck_class = detect_class(deck_link)
    d = pd.DataFrame(card_hashes)
    d = d[0].value_counts().reset_index().rename(columns={'index': 'code', 0: 'count'})
    deck_df = pd.merge(d, df)[['count', 'card_name']]
    deck_df = deck_df.groupby('card_name', as_index = False).agg('sum')

    outdir = './jcg-decks'
    file = f'{deck_class}-{i}.csv'
    deck_df.to_csv(os.path.join(outdir, file),index=False)


tourney_decks = pd.read_csv("J1kNoaYPvxQx-decks.csv")
tourney_list = tourney_decks.values.tolist()

for idx, deck in enumerate(tourney_list):
    write_list(deck[1], idx)
    write_list(deck[2], idx)