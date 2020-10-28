import pandas as pd
import numpy as np

class Loader:
	@staticmethod
	def load_data(filename):
		if filename[-5:] == ".xlsx":
			return pd.read_excel(filename)
		elif filename[-4:] == ".csv":
			return pd.read_csv(filename)
		else:
			raise Exception("Invalid file type")