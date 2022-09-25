import json
import os
import re
import pandas as pd

from sv_portal_reader import SVPortalParser

df = pd.read_csv("codes.csv")
def write_list(parsed_deck: SVPortalParser, i):
    outdir = './training'
    file = f'{parsed_deck.craft}-{i}.csv'
    parsed_deck.cards_df.to_csv(os.path.join(outdir, file),index=False)


tourney_decks = pd.read_csv("J1kNoaYPvxQx-decks.csv")
tourney_list = tourney_decks.values.tolist()

for idx, deck in enumerate(tourney_list):
    parsed1= SVPortalParser(deck[1])
    parsed2= SVPortalParser(deck[2])

    parsed1.parse_deck()
    parsed2.parse_deck()

    write_list(parsed1, idx)
    write_list(parsed2, idx)