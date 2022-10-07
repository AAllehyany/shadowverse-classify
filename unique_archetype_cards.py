import collections
import json


f = open('./formats/celestial-dragonblade.json')
data = json.load(f)

def filter_repeated_cards(craft):
    cards = []

    for (archetype, data) in craft.items():
        cards.extend(data["feature_cards"])

    repeated = [n for (n, x) in collections.Counter(cards).items() if x > 1]

    for (archetype,data) in craft.items():
        x = set(data["feature_cards"])
        rs = set(repeated)

        data["feature_cards"] = list(x.difference(rs))
    

for (craft, archetypes) in data.items():

    filter_repeated_cards(archetypes)

with open('./formats/unique-celestial-cleared.json', 'w') as u:
    json.dump(data, u, indent=4)
