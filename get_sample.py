
import argparse
from getopt import GetoptError, getopt
import json
import os
import pandas as pd
import sys

from jcg_scraper import JCGScraper
from sv_portal_reader import SVPortalParser


def main(jcg_code):

    if not os.path.exists('deck-samples'):
        os.makedirs('deck-samples')

    sv_portal = SVPortalParser(format_data={})
    scraper = JCGScraper(jcg_code, parser=sv_portal)
    scraper.scrape_entries_json()

    with open (os.path.join('deck-samples', f'jcg-{jcg_code}-decks.json'), 'w') as out:
        json.dump(sv_portal.decks, out, indent=4)

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, help="JCG Tournamet Code or ID")
    args = parser.parse_args() 
    main(args.c)