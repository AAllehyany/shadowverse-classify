from getopt import GetoptError, getopt
import json
import os
import re
import sys
import pandas as pd

from sv_portal_reader import SVPortalParser

def write_list(parsed_deck: SVPortalParser, i):
    outdir = './training'
    file = f'{parsed_deck.craft}-{i}.csv'
    parsed_deck.cards_df.to_csv(os.path.join(outdir, file),index=False)


def main(argv):

    data_file = ''
    outdir = './training'

    try:
        opts, args = getopt(argv, "i:o:")
    except GetoptError:
        print("train.py -i <inputfile> -o <outputfile>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-i":
            data_file = arg
        elif opt == "-o":
            outdir = arg

    tourney_decks = pd.read_csv(data_file)
    tourney_list = tourney_decks.values.tolist()

    for idx, deck in enumerate(tourney_list):
        parsed1= SVPortalParser(deck[1])
        parsed2= SVPortalParser(deck[2])

        parsed1.parse_deck()
        parsed2.parse_deck()

        write_list(parsed1, idx)
        write_list(parsed2, idx)
    

if __name__=="__main__":
    main(sys.argv[1:])
