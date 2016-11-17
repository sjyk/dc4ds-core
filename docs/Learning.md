#Learning: Part 1

Machine Learning is an increasingly important part of Data Science. This document describes
how dc4ds supports common Machine Learning operations.

## Featurization

In addtion to the Dataset class, dc4ds also supports a FeaturizedDataset:
```
from dc4ds.dataset import FeaturizedDataset

featurized_data = FeaturizedDataset(c)
```

Featurized Datasets can be split into training and test sets easily:
```
train, test = featurized_data.test_train_split(frac=0.8)
```

To get the feature vectors from these objects apply:
```
features = train.getFeatures(label_column=...)
```
where label_column is the name of the column that is defined to be the label (or None for unsupervised learning)


Sometimes, we may want to apply the same featurization model to the test set:
```
test_features = test.getTestFeatures(label_column=...)
```