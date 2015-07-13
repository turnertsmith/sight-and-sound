from bs4 import BeautifulSoup
import pandas as pd
import urllib2
import re

def scrapeURLs(url):
	'''
	Get a list of the urls where each of the polls 
	are located for either directors or critics
	'''
	critic_urls = []
	soup = BeautifulSoup(urllib2.urlopen(url))
	critic_table = soup.find_all("ul", "noblt")[0].find_all("li")
	for critic in critic_table:
		link = critic.find_all("a")[0]['href']
		critic_urls.append(link)
	return critic_urls

def scrapePoll(url):
	'''
	Scrapes a single voters ballot and return a list with 
	Voter Name, Voter Country and then all of the films 
	voted on by this Critic/Director
	'''
	soup = BeautifulSoup(urllib2.urlopen(url))
	name = soup.find_all("dt")[0].text
	country = soup.find_all("dd")[-1].text
	table = soup.find_all("ol")[0].find_all("li")
	voter_ballot = [name, country]
	for vote in table:
		film = vote.find_all("a")[0].text
		voter_ballot.append(film)
	print voter_ballot
	return voter_ballot


def scrapePolls(urls):
	'''
	Takes a list of urls where polls are located and 
	returns a list of lists containing the votes 
	for each critic as well as the critics location
	'''
	votes = []
	front = "http://old.bfi.org.uk/sightandsound/polls/topten/poll/"
	for url in urls:
		votes.append(scrapePoll(front + url))
	return votes

def scrape2002():
	'''
	Calls 
	'''
	cols = ["Voter_Name", "Voter_Country", "Film_1", "Film_2", "Film_3", "Film_4", "Film_5", "Film_6", "Film_7", "Film_8", "Film_9", "Film_10", "Film_11", "Film_12", "Film_13"]
	critics_url = "http://old.bfi.org.uk/sightandsound/polls/topten/poll/list.php?list=voters&votertype=critic"
	directors_url = "http://old.bfi.org.uk/sightandsound/polls/topten/poll/list.php?list=voters&votertype=director"
	polls = scrapePolls(scrapeURLs(critics_url)) + scrapePolls(scrapeURLs(directors_url))
	df = pd.DataFrame(polls, columns=cols)
	df.to_csv("ballot_table_2002.csv", sep = "|", encoding = "utf-8")

def scrapeFilms(url):
	'''
	Scrape the info concerning the films on a given url
	'''
	soup = BeautifulSoup(urllib2.urlopen(url))
	table = [["Title", "Director"]]
	for i in soup.find_all("tr")[1:]:
		listy = i.find_all("td")
		table.append([listy[0].text, listy[1].text])
	headers = table.pop(0)
	df = pd.DataFrame(table, columns = headers)
	df.to_csv("films_2002.csv", sep = "|", encoding = "utf-8")

def do_all():
	films_url = "http://old.bfi.org.uk/sightandsound/polls/topten/poll/list.php?list=films"
	scrapeFilms(films_url)
	'''
	scrape2002()
	'''

do_all()