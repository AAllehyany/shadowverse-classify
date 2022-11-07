
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
    scraper.scrape_entries()
    scraper.scrape_results()

    jcg_data = scraper.entry_decks.values()


    for data in jcg_data:
        
        for deck in data["decks"]:
            name = f'{jcg_code}-{data["top"]}-{deck["craft"]}-{data["id"]}.csv'
            deck_df = pd.DataFrame(deck["deck_list"], columns=[
                "card_name", "copies", "base_id", "hash"
            ])

            deck_df.to_csv(os.path.join('deck-samples', name), index=False)

    # samples = []
    # if os.path.exists(os.path.join('deck-samples', 'samples.json')):
    #     with open(os.path.join('deck-samples', 'samples.json')) as ff:
    #         samples = json.load(ff)
    
    # samples.extend(sv_portal.decks)

    # with open (os.path.join('deck-samples', f'samples.json'), 'w') as out:
    #     json.dump(samples, out, indent=4)

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, help="JCG Tournamet Code or ID")
    args = parser.parse_args() 
    main(args.c)