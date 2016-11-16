"""
This module defines the main data structure in the dc4ds package.
A dataset is a wrapper class for a Pandas Data Frame that also 
contains logical assertions about data quality.
"""
import pandas
from dc4ds.loaders.TypeInference import TypeInference

class Dataset(pandas.DataFrame):
    """
    The dataset class extends the pandas DataFrame
    """

    def __init__(loader, 
                 index=None, 
                 columns=None, 
                 dtype=None, 
                 copy=False)

        #loads the data with the provided args
        self.loadedData = loader.load()
        self.types = TypeInference().getTypes()

        super(Dataset).__init__(data=loadedData,
                                index=index,
                                columns=columns,
                                dtype=dtype,
                                copy=copy)