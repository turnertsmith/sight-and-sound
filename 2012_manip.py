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

q = """SELECT df.country as voter_country, df.sex, films.title, films.year, films.director, films.country as film_country FROM df LEFT JOIN films on df.Film = films.title"""
table = pysqldf(q).copy()
print table.head()


q = """SELECT distinct country FROM df"""
voter_country_list = pysqldf(q)
print voter_country_list
voter_country_list = voter_country_list["Country"].tolist()#["voter_country"].tolist()
editted_list = set([])
for country in voter_country_list:
	listy = []
	if country:
		listy = [x.strip() for x in country.split(",")]
	editted_list.update(listy)

voter_countries = list(editted_list)
voter_countries.sort()
print voter_countries

q = """SELECT distinct country from films"""
film_country_list = pysqldf(q)["Country"].tolist()#["film_country"].tolist()
editted_list = set([])
for country in film_country_list:
	listy = []
	if country:
		listy = [x.strip() for x in country.split(",")]
	editted_list.update(listy)

film_countries = list(editted_list)
film_countries.sort()
print film_countries

