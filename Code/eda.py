import pandas as pd
import numpy as np
import seaborn as sns

def plot_numeric(df, fig, axes):
	df_numeric = df.select_dtypes(include = np.number)

	num_plots = df_numeric.shape[1]*2

	for i in range(num_plots):
		row = i // 2
		col = i % 2
		data = df_numeric.iloc[:,row].dropna()
		# histograms
		if col == 0:
			sns.histplot(data = data, ax = axes[row, col])
		# boxplots
		else:
			sns.boxplot(data = data, orient = "h", ax = axes[row, col])
			axes[row, col].grid()
		axes[row, col].set_title(df_numeric.columns[row])

	fig.tight_layout()

def plot_cats(df, l_cat, fig, axes):
	num_plots = len(l_cat)
	y_name = df.columns[-1]

	for i in range(num_plots):
		x_name = l_cat[i]
		row = i // 2
		col = i % 2
		y = df[y_name]
		X = df[x_name].astype(object)
		# sort boxplots in ascending order
		my_order = df.groupby(x_name)[y_name].median().sort_values().index
		ax = axes[row, col]
		plot = sns.boxplot(x = X, y = y, order = my_order, ax = ax)
		if len(X.unique()) > 5:
			plot.set_xticklabels(plot.get_xticklabels(), rotation = 25,
				horizontalalignment = "right")
	fig.tight_layout()