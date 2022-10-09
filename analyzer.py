import getopt
import json
import os
import sys
import pandas as pd
from operator import itemgetter
from sv_portal_reader import SVPortalParser
from jcg_scraper import JCGScraper

def analyzer(argv):


    try:
        if not os.path.exists('jcg-data'):
            os.makedirs('jcg-data')
        
        format = ""
        jcg_code = ""
        opts, args = getopt.getopt(argv, 'c:f:')

        for opt, arg in opts:
            if opt == "-c":
                jcg_code = arg
            
            if opt == "-f":
                format = arg

        f = open(format)
        data = json.load(f)
        sv_portal = SVPortalParser(format_data=data)
        scraper = JCGScraper(jcg_code, parser=sv_portal)
        scraper.scrape_entries()
        scraper.scrape_results()

        jcg_data = scraper.entry_decks.values()
        sorted_data = sorted(jcg_data, key=itemgetter("top"), reverse=True)
        

        jcg_decks_data = []
        players_data = []

        for data in jcg_data:
            player = {
                "id": data["id"],
                "name": data["name"],
                "top": data["top"]
            }

            for (idx, deck) in enumerate(data["decks"]):
                result = (deck["craft"], deck["archetype"], deck["link"], data["top"], data["name"], data["id"])
                player[f'deck_{idx+1}'] = deck["archetype"]
                player[f'link_{idx+1}'] = deck["link"]
                jcg_decks_data.append(result)
            
            players_data.append(player)

        players_data_df = pd.DataFrame(players_data)
        decks_data_df = pd.DataFrame(jcg_decks_data,
            columns=[
                "craft",
                "archetype",
                "deck_link",
                "score",
                "player_name",
                "player_id"
            ]
        )
        outdir = './jcg-data'


        archetype_df = decks_data_df['archetype'].value_counts()
        craft_df = decks_data_df['craft'].value_counts()

        players_data_df.to_csv(os.path.join(outdir, f'{scraper.jcg_date}-lineups.csv'), index=False)
        decks_data_df.to_csv(os.path.join(outdir, f"{scraper.jcg_date}-classified-decks.csv"), index=False)
        archetype_df.to_csv(os.path.join(outdir, f"{scraper.jcg_date}-archetypes-data.csv"))
        craft_df.to_csv(os.path.join(outdir, f"{scraper.jcg_date}-crafts-data.csv"))
    except getopt.GetoptError:
        print('analyzer.py -c <jcg-code> -f <format-file>')
        sys.exit(2)
    
    

if __name__ == "__main__":
    analyzer(sys.argv[1:])
