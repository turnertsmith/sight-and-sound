from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import re

def scrapeFilms(url):
	soup = BeautifulSoup(urllib2.urlopen(url))
	film_blocks = soup.find_all("div", "sas-all-films-group")
	film_list = []
	for film_block in film_blocks:
		film_list += scrapeFilmBlock(film_block)
	return film_list

def scrapeFilmBlock(film_block):
	film_list = []
	film_entries = film_block.find_all("tr")
	for film_entry in film_entries:
		film_list.append(scrapeFilmEntry(film_entry))
	return film_list

def scrapeFilmEntry(film_entry):
	film_attributes = film_entry.find_all("td")
	film_name, year = fix_film_name_year(film_entry)
	director = fix_director(film_attributes[1])
	country = fix_country(film_attributes[2])
	return [film_name, year, director, country]

def fix_director(director_td):
	director = director_td.text
	director = re.sub("\s", " ", director)
	director = re.sub(r"\/", r", ", director)
	director = re.sub(r"&", r", ", director)
	director = re.sub(r"\s+,", r",", director)
	director = re.sub(r"  +", " ", director)
	if director == "Joel, Ethan Coen":
		director = "Joel Coen, Ethan Coen"
	elif director == "Jim Abrahams, David, Jerry Zucker":
		director = "Jim Abrahams, David Zucker, Jerry Zucker"
	return director

def fix_country(country_td):
	country = country_td.text
	country = re.sub(r",\s+", ", ", country)
	return country

def fix_film_name_year(film_entry):
	title = film_entry.find('td').string.strip()
	year = film_entry['data-year'].strip()
	if re.search(r"\(" + year + r"\)$", title):
		title = re.sub(r"\s*\(" + year + r"\)$", "", title)
	return title, year

def scrape_films_csv():
	table = scrapeFilms("http://explore.bfi.org.uk/sightandsoundpolls/2012/film")
	headers = ["Title", "Year", "Director", "Country"]
	df = pd.DataFrame(table, columns = headers)
	df.to_csv("films_2012.csv", sep = "|", encoding = "utf-8")

def scrape_voters(url):
	soup = BeautifulSoup(urllib2.urlopen(url))
	voter_blocks = soup.find_all("div", "sas-all-films-group")
	voter_list = []
	for voter_block in voter_blocks:
		voter_list += scrapeVoterBlock(voter_block)
	return voter_list

def scrapeVoterBlock(voter_block):
	voter_list = []
	voters = voter_block.find_all("tr")
	for voter in voters:
		voter_list.append(scrapeVoterEntry(voter))
	return voter_list

def scrapeVoterEntry(voter):
	name = voter.find("td").string.strip()
	voter_url = voter.find("td").find("a")["href"].strip()
	poll = voter["data-poll"].strip()
	occupation = voter["data-category"].strip()
	sex = voter["data-gender"].strip()
	if sex == "Male": 
		sex = "M"
	elif sex == "Female": 
		sex = "F"
	else: 
		sex = ""
	country = voter["data-country"].strip()
	voter_ballot = [name, poll, occupation, sex, country] + strip_ballot(voter_url)
	return voter_ballot

def strip_ballot(url):
	choices = []
	soup = BeautifulSoup(urllib2.urlopen(url))
	ballot = soup.find_all('div', class_="sas-voter-details-votes")[0]
	for vote in ballot.find_all('tr'):
		title = vote.find_all('td')[0].text
		choices.append(title)
	return choices

def scrape_films_csv():
	table = scrape_voters("http://explore.bfi.org.uk/sightandsoundpolls/2012/voter")
	headers = ["Name", "Poll", "Occupation", "Sex", "Country", "Film_1", "Film_2", "Film_3", "Film_4", "Film_5", "Film_6", "Film_7", "Film_8", "Film_9", "Film_10", "Film_11", "Film_12"]
	df = pd.DataFrame(table, columns = headers)
	df.to_csv("ballots_2012.csv", sep = "|", encoding = "utf-8")

df1 = pd.read_csv("ballots_2012AQ.csv", sep = "|", encoding = "utf-8")
df2 = pd.read_csv("ballots_2012QZ.csv", sep = "|", encoding = "utf-8")
df = df1.append(df2)
print df.head()
df = df.drop("Unnamed: 0", 1)
df = df.reset_index()
df = df.drop("index", 1)
df.to_csv("ballots_2012.csv", sep = "|", encoding = "utf-8")