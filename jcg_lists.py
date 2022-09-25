
from getopt import GetoptError, getopt
import json
import os
import sys

from jcg_scraper import JCGScraper
from sv_portal_reader import SVPortalParser

def write_list(parsed_deck, i):
    outdir = './samples'
    file = f'{parsed_deck["craft"]}-{i}.csv'
    parsed_deck["cards_df"].to_csv(os.path.join(outdir, file),index=False)


def main(argv):

    jcg_code = ''

    try:
        opts, args = getopt(argv, 'c:')

        if not os.path.exists('samples'):
            os.makedirs('samples')

        for opt, arg in opts:
            if opt == "-c":
                jcg_code = arg

        sv_portal = SVPortalParser(format_data={})
        scraper = JCGScraper(jcg_code, parser=sv_portal)
        scraper.scrape_entries()

        for idx, deck in enumerate(scraper.deck_cards):
            write_list(deck, idx)

    except GetoptError:
        print('jcg_lists.py -c <jcg-code>')
        sys.exit(2)

    

if __name__ == "__main__":
    main(sys.argv[1:])