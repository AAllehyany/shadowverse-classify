import json
import math
import requests
import pandas as pd


# Credit to Finalysis for this conversion table
base64 = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J',
 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T',
 30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z', 36: 'a', 37: 'b', 38: 'c', 39: 'd',
 40: 'e', 41: 'f', 42: 'g', 43: 'h', 44: 'i', 45: 'j', 46: 'k', 47: 'l', 48: 'm', 49: 'n',
 50: 'o', 51: 'p', 52: 'q', 53: 'r', 54: 's', 55: 't', 56: 'u', 57: 'v', 58: 'w', 59: 'x',
 60: 'y', 61: 'z', 62: '-', 63: '_'}

crafts = ['neutral', 'forestcraft', 'swordcraft', 'runecraft', 'dragoncraft', 'shadowcraft', 'bloodcraft',
'havencraft', 'portalcraft']
# Credit to Finalysis for this hash conversion method
def id_to_hash(card_id):
    list1 = []
    for n in range(0, 6):
        divide = card_id*((1/64)**n)
        mod = math.floor(divide%64)
        list1.append(math.floor(mod))
        
    list2 = list(reversed(list1[:-1]))
    output = ""
    for m in list2:
        hashvalue = str(m).replace(str(m), base64[m])
        output += (hashvalue)
        
    return output

def map_card_fields(card):
    return {
        "base_id": card["base_card_id"],
        "base_hash": id_to_hash(card['base_card_id']),
        "card_name": card["card_name"],
        "craft": crafts[card["clan"]],
        "card_hash": id_to_hash(card["card_id"]),
        "card_id": card["card_id"]
    }

def map_to_db(card):
    return [card['card_id'], card['cost'], card['card_name'], card['clan'], card['base_card_id']]

api = "https://shadowverse-portal.com/api/v1/cards"

result = requests.get(api, {"format": "json", "lang": "en"})

json_result = result.json()

cards_list = json_result["data"]["cards"]

cards = [map_card_fields(card) for card in cards_list if card["card_set_id"] < 90000]
csv_cards = [map_to_db(card) for card in cards_list if card["card_set_id"] < 90000]



with open('./db/db_data.json', 'w') as f:
    json.dump(cards_list, f, indent=4)

# df = pd.DataFrame(csv_cards, columns=['id', 'cost', 'card_name', 'craft_id'])

# df.to_csv('./db/cards-master.csv', index=False)

