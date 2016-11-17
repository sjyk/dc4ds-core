# Getting Started with DC4DS

This document describes how to get started with dc4ds.

## Your First Program

The basic data type in dc4ds is the Dataset class.
Datasets take as an argument a loader (which loads data)
from a specified source. For example, one may want to load 
data from a CSV file.
```
from dc4ds.dataset import Dataset
from dc4ds.loaders.CSVLoader import CSVLoader

loader = CSVLoader(fname="examples/datasets/missing_values.csv")
my_dataset = Dataset(loader)
``` 

This class is fully compatible with Pandas Data Frames:
```
print my_dataset.df
```

By default the columns are given string valued names "0", "1", and so on.
We can set these names to be human readable with:
```
my_dataset.setColumnNames([...])
```

## Adding Constraints

The example dataset missing_values.csv contains one row with a missing
value:
```
38, Private,?, HS-grad, 9, Divorced, Handlers-cleaners, Not-in-family, 
White, Male, 0, 0, 40, United-States, <=50K
```

To account for such problems, we can add a domain integrity constraint
 on our dataset:
```
DomainConstraint([column_names...], [lambda x: boolen_formula])
```

In code, this looks like:
```
from dc4ds.constraint import DomainConstraint
constraint = DomainConstraint(["2"], lambda x: '?' not in x[0])
my_dataset.addConstraint(constraint)
```

You can use these constraints in programmatic assertions
```
assert(my_dataset.isConsistent())
```

## Adding More Complicated Constraints
We can also add more complicated constraints such as conditional functional 
dependencies. cfd1.csv contains:
```
95129, CA
95014, CA
95720, CA
```

cfd2.csv contains:
```
95129, CA
95014, CA
95720, CA
95129, NY
```

Consider the program:
```
c = CSVLoader(fname="examples/datasets/cfd1.csv")

d = Dataset(c)

d.addConstraint(ConditionalFunctionalDependency(["0"],["1"], lambda x: True))

print d.isConsistent()

c = CSVLoader(fname="examples/datasets/cfd2.csv")

d = Dataset(c)

d.addConstraint(ConditionalFunctionalDependency(["0"],["1"], lambda x: True))

print d.isConsistent()
```

The output is:
```
True
False
```