import pandas as pd
import numpy as np
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

films = pd.read_csv("tables/films_2012.csv", delimiter = "|", encoding = "utf-8")
films = films[films.columns.values[1:]]
ballots = pd.read_csv("tables/ballots_2012.csv", delimiter = "|", encoding = "utf-8")
ballots = ballots[ballots.columns.values[1:]]
ballot_cols = ballots.columns.values
filmframes = []

def return_ballots(ballots, cols, i):
	frame = ballots[np.append(cols[0:5], cols[i])]
	string = "Film_" + str(i-5)
	frame.columns = np.append(cols[0:5],"Film")
	return frame

for i in range(5, 17):
	filmframes.append(return_ballots(ballots, ballot_cols, i))

df = filmframes[0].append(filmframes[1])
for i in filmframes[2:]:
	df = df.append(i)

df = df[pd.notnull(df['Film'])]
print df.tail()
print films.head()
'''
q = """SELECT df.country, df.sex, films.title, films.year, films.director, films.country FROM df LEFT JOIN films on df.Film = films.title"""
table = pysqldf(q)
'''
q = """select voter_country, film_country, count(sex) from (SELECT df.country as voter_country, df.sex, films.title, films.year, films.director, films.country as film_country FROM df LEFT JOIN films on df.Film = films.title) where voter_country not like '%US%' and film_country LIKE "%USA%" group by voter_country, film_country order by count(sex) DESC"""
print pysqldf(q)