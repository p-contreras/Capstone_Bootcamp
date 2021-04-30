import pandas as pd
import numpy as np
import ast

def IMDb_update(df, imdb_df, left, right):
	updated_df = df.merge(imdb_df, left_on = left, right_on = right, how = "left")
	updated_df.drop(right, axis = 1, inplace = True)
	bools = updated_df.isna().any()
	if any(bools):
		print("There are NAs present.  Please fix these columns\n")
		print(updated_df.isna().sum() / len(updated_df))
	return updated_df

def convert_stringList(string):
	if pd.isnull(string):
		return np.nan
	x = ast.literal_eval(string)
	if isinstance(x, list):
		if len(x) > 0:
			d = x[0]
			return d["name"]
		else:
			return np.nan
	elif isinstance(x, dict):
		return x["name"]
	else:
		return np.nan

def genre_separator(string):
    if pd.isnull(string):
        return np.nan
    else:
    	genre = string.split(",")[0]
    	return genre

def create_dummies(x, base):

	dummies = pd.DataFrame()

	for level in x.unique():
		if level == base:
			continue
		dummy = x.apply(lambda l: 1 if l == level else 0)

		if level == "Walt Disney Studios":
			dummy.name = "Disney"
		elif level == "Sony Pictures":
			dummy.name = "Sony"
		elif level == "PG-13":
			dummy.name = "PGThirteen"
		else:
			dummy.name = level

		dummies[dummy.name] = dummy

	return dummies

def prod_company_bin(df, pc, film_studio):
	bools = df["production_company"].str.contains(pc)
	if bools.sum() > 0:
		df.loc[bools, "production_company"] = film_studio
	return df

