import pandas as pd
import numpy as np
from pandasql import sqldf
import re

pysqldf = lambda q: sqldf(q, globals())

films = pd.read_csv("tables/films_2002.csv", delimiter = "|", encoding = "utf-8")
films = films[films.columns.values[1:]]
ballots = pd.read_csv("tables/ballot_table_2002.csv", delimiter = "|", encoding = "utf-8")
ballots = ballots[ballots.columns.values[1:]]
print films.head()
print ballots.head()
ballot_cols = ballots.columns.values
filmframes = []

def return_ballots(ballots, cols, i):
	frame = ballots[np.append(cols[0:2], cols[i])]
	string = "Film_" + str(i-2)
	frame.columns = np.append(cols[0:2],"Film")
	return frame

for i in range(2, 15):
	filmframes.append(return_ballots(ballots, ballot_cols, i))

df = filmframes[0].append(filmframes[1])
for i in filmframes[2:]:
	df = df.append(i)

df = df[pd.notnull(df['Film'])]
df["Director"] = df["Film"].apply(lambda x: x[x.rfind('('):][1:-1])
df["Film"] = df["Film"].apply(lambda x: x[:x.rfind('(') - 1])
print df

q = """SELECT distinct Voter_Country FROM df"""
voter_country_list = pysqldf(q)["Voter_Country"].tolist()
countries = set()
for i in voter_country_list:
	add = i.split("/")
	countries.update(add)
print countries