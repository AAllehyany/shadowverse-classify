
from getopt import GetoptError, getopt
import os
import sys

from jcg_scraper import JCGScraper
from sv_portal_reader import SVPortalParser

def write_list(parsed_deck: SVPortalParser, i):
    outdir = './samples'
    file = f'{parsed_deck.craft}-{i}.csv'
    parsed_deck.cards_df.to_csv(os.path.join(outdir, file),index=False)


def main(argv):

    jcg_code = ''
    outdir = './samples'

    try:
        opts, args = getopt(argv, 'c:')

    except GetoptError:
        print('jcg_lists.py -c <jcg-code>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-c":
            jcg_code = arg
    
    scraper = JCGScraper(jcg_code)
    decks = scraper.get_links()

    for idx, deck in enumerate(decks):
        parsed1= SVPortalParser(deck)
        parsed1.parse_deck()
        write_list(parsed1, idx)

if __name__ == "__main__":
    main(sys.argv[1:])