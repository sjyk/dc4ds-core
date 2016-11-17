"""
This module defines the main data structure in the dc4ds package.
A dataset is a wrapper class for a Pandas Data Frame that also 
contains logical assertions about data quality.
"""
import pandas
import warnings
from dc4ds.loaders.TypeInference import TypeInference

class Dataset(object):


    def __init__(self,
                 loader, 
                 index=None, 
                 columns=None, 
                 dtype=None, 
                 copy=False):
        """
        Initializes a dataset object that wraps around a dataframe
        """

        #loads the data with the provided args
        self.loadedData = loader.load()
        self.types = TypeInference().getDataTypes(self.loadedData)

        pandasData = {}
        for i in range(len(self.types)):
            pandasData[str(i)] = [row[i] for row in self.loadedData]

        self.df = pandas.DataFrame(data=pandasData,
                                   index=index,
                                   columns=columns,
                                   dtype=dtype,
                                   copy=copy)

        self.constraints = []

    def setColumnNames(self, new_names):
        """
        Sets logical names for each column
        """
        self.df.columns = new_names


    def addConstraint(self,constraint):
        """
        Adds a constraint
        """
        self.constraints.append(constraint)


    def isConsistent(self):
        """
        Tests if the data frame is consistent
        """

        if len(self.constraints) == 0:
            warnings.warn("There are no constraints on this Dataset", SyntaxWarning)

        for const in self.constraints:
            if not const.isConsistent(self.df):
                return False

        return True


    def getErrorIndices(self):
        """
        Gets a set of rows, columns with errors
        """

        errors = set()

        for const in self.constraints:
            errorRows = const.eval(self.df)
            for col in const.getColumnList(self.df):
                for row in errorRows:
                    errors.add((row, col))

        return errors