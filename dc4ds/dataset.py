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

        self.dconstraints = []


    def setColumnNames(self, new_names):
        """
        Sets logical names for each column
        """
        self.df.columns = new_names


    def addDomainConstraint(self,constraint):
        """
        Adds a domain constraint
        """
        self.dconstraints.append(constraint)


    def isConsistent(self):
        """
        Tests if the data frame is consistent
        """

        if len(self.dconstraints) == 0:
            warnings.warn("There are no constraints on this Dataset", SyntaxWarning)

        for const in self.dconstraints:
            if not const.isConsistent(self.df):
                return False

        return True


    def getErrorIndices(self):
        """
        Gets a set of rows, columns with errors
        """

        errors = set()

        for const in self.dconstraints:
            errorRows = const.eval(self.df)
            for col in const.column_list:
                for row in errorRows:
                    errors.add((row, col))

        return errors





class DomainConstraint(object):
    """
    This is a wrapper class for domain integrity constraints
    """

    def __init__(self, column_list, lambda_rule):
        """
        column_list defines a projection
        lambda_rule defines a function of the projection to {True, False}
        """

        self.column_list = column_list
        self.lambda_rule = lambda_rule


    def eval(self, df):
        """
        Returns a list of rows from the df that violate the rule
        """
        projection = df[self.column_list]
        inconsistent = set()

        for index, row in projection.iterrows():
            argument = tuple([row[col] for col in self.column_list])

            if not self.lambda_rule(argument):
                inconsistent.add(index)

        return inconsistent

    def isConsistent(self, df):
        """
        Is the df consistent w.r.t this rule
        """

        return (len(self.eval(df)) == 0)


