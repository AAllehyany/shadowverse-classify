
import pandas as pd

df = pd.read_csv("./jcg-data/1005-classified-decks.csv")


summed1 = df.groupby('archetype').sum('score')
summed1['percentage'] = (summed1['score']/df['score'].sum())*100
summed1['total'] = df['score'].sum()


print(summed1.sort_values(by='score', ascending=False))
