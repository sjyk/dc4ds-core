import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from dc4ds.dataset import Dataset
from dc4ds.constraint import ConditionalFunctionalDependency
from dc4ds.loaders.CSVLoader import CSVLoader


c = CSVLoader(fname="examples/datasets/cfd1.csv")

d = Dataset(c)

d.addConstraint(ConditionalFunctionalDependency(["0"],["1"], lambda x: True))

print d.isConsistent()

c = CSVLoader(fname="examples/datasets/cfd2.csv")

d = Dataset(c)

d.addConstraint(ConditionalFunctionalDependency(["0"],["1"], lambda x: True))

print d.getErrorIndices()

print d.isConsistent()
