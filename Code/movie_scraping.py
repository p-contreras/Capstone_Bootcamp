import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as BS
from bs4.element import ResultSet
import re

def get_IMDbInfo(url):
	info = []
	page = requests.get(url)
	# if page not found, return NA
	if page.status_code != 200:
		return np.nan
	soup = BS(page.content, "html.parser")

	prod_company = get_IMDbProdCompany(soup)
	info.append(prod_company)

	cert = get_IMDbCert(soup)
	info.append(cert)

	return info

def get_IMDbProdCompany(soup):
	try:
		data = soup.find_all("a", attrs = {"href": re.compile("/company/.+")})
	except:
		return np.nan
	if isinstance(data, ResultSet):
		try:
			prod_company = str(data[0].string).strip()
		except:
			return np.nan
	else:
		return np.nan

	return prod_company


def get_IMDbCert(soup):
	try:
		data = soup.find_all("div", class_ = "subtext")
	except:
		return np.nan

	if isinstance(data, ResultSet):
		try:
			cert = str(data[0].text).strip()[:5]
		except:
			return np.nan
	else:
		return np.nan

	for rating in ["R", "PG-13", "PG", "G"]:
		if rating in cert:
			return rating
	return np.nan

def get_TMDbFranchise(url):
	page = requests.get(url)
	# if page not found, return NA
	if page.status_code != 200:
		return np.nan
	soup = BS(page.content, "html.parser")

	try:
		data = soup.find_all("div", attrs = {"id": "collection_waypoint"})
	except:
		return 0
	try:
		franchise = data[0]
	except:
		return 0

	return 1

def saveData(i, df, f, p, c):
	# create DataFrames
	df_franchise = pd.DataFrame({"id": df["id"][:i], "belongs_to_franchise": f})
	df_companies = pd.DataFrame({"imdb_id": df["imdb_id"][:i], "production_company": p})
	df_cert = pd.DataFrame({"imdb_id": df["imdb_id"][:i], "cert": c})

	# store results
	df_franchise.to_csv("../data/web_scrape/franchise.csv")
	df_companies.to_csv("../data/web_scrape/prod_companies.csv")
	df_cert.to_csv("../data/web_scrape/cert.csv")

	return None



def main():
	# read in data
	df = pd.read_csv("../data/df.csv")
	# initialize empty lists
	franchise = []
	prod_companies = []
	certs = []
	# check if web-scraping is working
	fail = False
	for i in range(len(df)):
		IMDb_ID = df["imdb_id"][i]
		TMDb_ID = df["id"][i]
		print(i, df["title"][i])
		url_IMDb = "https://www.imdb.com/title/" + IMDb_ID
		url_TMDb = "https://www.themoviedb.org/movie/" + str(TMDb_ID)

		try:
			IMDb_data = get_IMDbInfo(url_IMDb)
		except:
			# save the data we have up to i
			saveData(i, df, franchise, prod_companies, certs)
			fail = True
			break
		try:
			TMDb_data = get_TMDbFranchise(url_TMDb)
		except:
			saveData(i, df, franchise, prod_companies, certs)
			fail = True
			break

		print(IMDb_data, TMDb_data)

		if isinstance(IMDb_data, list):
			prod_companies.append(IMDb_data[0])
			certs.append(IMDb_data[1])
		else:
			prod_companies.append(IMDb_data)
			certs.append(IMDb_data)
		franchise.append(TMDb_data)
		
	# if web scraping hasn't failed, save all the data
	if not fail:
		saveData(len(df), df, franchise, prod_companies, certs)

	return None

if __name__ == '__main__':
	main()