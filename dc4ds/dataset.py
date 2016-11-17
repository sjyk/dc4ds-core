"""
This module defines the main data structure in the dc4ds package.
A dataset is a wrapper class for a Pandas Data Frame that also 
contains logical assertions about data quality.
"""
import pandas
import numpy as np
import warnings
from dc4ds.loaders.TypeInference import TypeInference
from dc4ds.utils.feature_utils import *
import copy

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
        loadedData = loader.load()

        self.types = TypeInference().getDataTypes(loadedData)

        pandasData = {}
        for i in range(len(self.types)):
            pandasData[str(i)] = [row[i] for row in loadedData]

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


    def toList(self):
        return [ [row[c] for c in self.df.columns.values] for i, row in self.df.iterrows()]




class FeaturizedDataset(Dataset):
    """
    A featurized dataset extends a dataset to also include features
    """

    def __init__(self,
                loader, 
                index=None, 
                columns=None, 
                dtype=None, 
                copy=False):

        super(FeaturizedDataset, self).__init__(loader, index, columns, dtype, copy)


    def getFeatures(self, label_column=None):
        """
        Turns a data frame into a numpy matrix and label column if avail
        """

        if label_column == None:

            features, transforms, fmap = featurize(self.toList(), self.types)

            return FeatureStruct(features, transforms, fmap, None, None, None)

        else:

            index = np.where(self.df.columns.values == label_column)[0]
            features = [[col for i, col in enumerate(row) if i != index] for row in self.toList()]
            feature_types = [col for i, col in enumerate(self.types) if i != index]

            nfeatures, transforms, fmap = featurize(features, feature_types)

            labels = [row[index] for row in self.toList()]
            label_type = self.types[index]
            nlabels, label_transform = labelize(labels, label_type)
            
            return FeatureStruct(nfeatures, 
                                 transforms, 
                                 fmap, 
                                 label_column, 
                                 nlabels, 
                                 label_transform)



    def getTestFeatures(self, label_column, fstruct):
        """
        Turns a data frame into a numpy matrix and label column 
        """
        index = np.where(self.df.columns.values == label_column)[0]
        features = [[col for i, col in enumerate(row) if i != index] for row in self.toList()]
        feature_types = [col for i, col in enumerate(self.types) if i != index]

        nfeatures, transforms, fmap = featurizeFromList(features, feature_types, fstruct.transforms)

        labels = [row[index] for row in self.toList()]
        label_type = self.types[index]
        nlabels, label_transform = labelizeForTest(labels, fstruct.label_transform)
            
        return FeatureStruct(nfeatures, 
                             transforms, 
                             fmap, 
                             label_column, 
                             nlabels, 
                             label_transform)


    def test_train_split(self, fraction=0.8, random_state=42):
        """
        Splits a featurized datast into a test and training set
        """
        train=self.df.sample(frac=fraction,random_state=random_state)
        test=self.df.drop(train.index)

        trainDataset = copy.copy(self)
        trainDataset.df = train

        testDataset = copy.copy(self)
        testDataset.df = test

        return trainDataset,testDataset
        

class FeatureStruct(object):
    """
    This class defines a data structure that holds
    all of the important feature variables
    """

    def __init__(self,
                 features,
                 transforms,
                 fmap,
                 label_column,
                 labels,
                 label_transform):

        self.features = features
        self.labels = labels
        self.transforms = transforms
        self.fmap = fmap
        self.label_column = label_column
        self.label_transform = label_transform



