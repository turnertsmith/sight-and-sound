
q = """SELECT distinct country FROM df"""
voter_country_list = pysqldf(q)
voter_country_list = voter_country_list["Country"].tolist()#["voter_country"].tolist()
editted_list = set([])
for country in voter_country_list:
	listy = []
	if country:
		listy = [x.strip() for x in country.split(",")]
	editted_list.update(listy)

voter_countries = list(editted_list)
voter_countries.sort()
print len(voter_countries)

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
print len(film_countries)

shared_countries = set(film_countries) & set(voter_countries)
film_only = set(film_countries) - set(voter_countries)
voter_only = set(voter_countries) - set(film_countries)

country_dict = {}

for country in shared_countries:
	country_dict[country] = country

for country in film_only:
	country_dict[country] = raw_input(country + ":")

for country in voter_only:
	country_dict[country] = raw_input(country + ":")

with open('dict.csv', 'wb') as f:
	w = csv.DictWriter(f, country_dict.keys())
	w.writeheader()
	w.writerow(country_dict)
