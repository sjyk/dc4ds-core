import csv
import numpy as np
from AbstractLoader import AbstractLoader
import os.path

class CSVLoader(AbstractLoader):
	"""
	This class provides a wrapper to load csv files into the system
	"""

	def __init__(self, fname, delimiter=None, quotechar=None):
		"""
		You can create a CSV loader with a specified delimiter
		or quote character. Or it will just try them all.
		"""
		self.DELIMITERS = [',', '\t', ':', '~', '|']
		self.QUOTECHAR = ['"', "'", '|', ':']

		if delimiter != None:
			self.DELIMITERS = [delimiter]

		if quotechar != None:
			self.QUOTECHAR = [quotechar]

		if not os.path.isfile(fname): 
			raise ValueError("File not found!")

		self.fname = fname


	def load_csv(self, fname, delimiter, quotechar):
		"""
		Internal method to load a CSVfile given a delimiter and 
		quote character
		"""
		with open(fname,'rb') as file:
			try:
				return [r for r in csv.reader(file, 
							  delimiter=delimiter, 
							  quotechar=quotechar)]
			except:
				return None

		return None


	def __score(self,parsed_file):
		"""
		This method assigns a score to all of the parsed files.
		We count the variance in the row length
		"""
		lstcount = [len([r for r in row if r.strip() != '']) for row in parsed_file]
		rowstd = np.std(lstcount)

		#catch degenerate case
		if len(parsed_file[0]) == 1:
			return float("inf")
		else:
			return rowstd


	def load(self):
		"""
		External method to load a file
		"""
		parsed_files = []

		fname = self.fname

		#try out all of the options in the delimiter and quotechar set
		for delimiter in self.DELIMITERS:
			for quotechar in self.QUOTECHAR:
				loaded = self.load_csv(fname, delimiter, quotechar)
				if not loaded == None:
					parsed_files.append(((delimiter,quotechar), loaded))

		#score each of the parsed files
		scored_parses = [(self.__score(p[1]), p[0], p[1]) for p in parsed_files]

		scored_parses.sort()

		self.delim = scored_parses[0][1]

		#worst case just split on spaces
		if len(scored_parses[0][2][0]) == 1:
			return self.__load(fname, ' ', '"')
		else:
			return scored_parses[0][2]



