"""
This module defines classes of constraints
"""

class Constraint(object):

    def getColumnList(self, df):
        raise NotImplemented("Must define the columns over which the constraints are active")


    def eval(self, df):
        """
        The input to eval is a data frame the output is a set of indices
        """
        raise NotImplemented("All constraints must implement an eval function")


    def isConsistent(self, df):
        """
        Is the df consistent w.r.t this rule
        """

        return (len(self.eval(df)) == 0)



class DomainConstraint(Constraint):
    """
    This is a class for domain integrity constraints
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


    def getColumnList(self, df):
        return self.column_list




class ConditionalFunctionalDependency(Constraint):
    """
    This is a class that defines CFD style constraints
    """

    def __init__(self, 
                 column_list1, 
                 column_list2, 
                 lambda_rule):
        """
        column_list1 defines a projection
        column_list2 defines a projection
        lambda_rule defines a predicate
        """

        self.column_list1 = column_list1
        self.column_list2 = column_list2
        self.lambda_rule = lambda_rule


    def eval(self, df):
        """
        Returns a list of rows from the df that violate the rule
        """

        implication_table = {}

        for index, row in df.iterrows():
            argument1 = tuple([row[col] for col in self.column_list1])
            argument2 = tuple([row[col] for col in self.column_list2])
            full = tuple([row[col] for col in df.columns])

            if self.lambda_rule(full):
                if argument1 not in implication_table:
                    implication_table[argument1] = []

                implication_table[argument1].append((argument2,index))

        inconsistent = set()
        for k in implication_table:
            consequents = implication_table[k]

            rows = set([c[1] for c in consequents])
            vals = set([c[0] for c in consequents])

            if len(vals) != 1:
                inconsistent = inconsistent.union(rows)

        return inconsistent

    def getColumnList(self, df):
        rtn = []
        rtn.extend(self.column_list1)
        rtn.extend(self.column_list2)

        return rtn