import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from dc4ds.dataset import FeaturizedDataset
from dc4ds.constraint import DomainConstraint
from dc4ds.loaders.CSVLoader import CSVLoader


c = CSVLoader(fname="examples/datasets/missing_values.csv")

d = FeaturizedDataset(c)

e,f = d.test_train_split()

a = e.getFeatures(label_column="14")

print f.getTestFeatures("14", a)

