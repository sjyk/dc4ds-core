# dc4ds-core
This repository defines the core package for all of the "Data Cleaning for Data Science" projects 

## Data Cleaning for Data Science (dc4ds)
Databases can be corrupted with various errors such as missing, incorrect, or inconsistent values. Increasingly, modern data analysis pipelines involve Machine Learning, and the effects of dirty data can be difficult to debug. Traditional models for relational data cleaning, rooted in logical assertions, have to be revisited in such use cases. This package defines core python utilities used in three projects: PrivateClean, ActiveClean, and BoostClean.

### References

Krishnan, S., Haas, D., Franklin, M.J. and Wu, E., 2016, June. Towards reliable interactive data cleaning: a user survey and recommendations. In HILDA@ SIGMOD 2016.

Krishnan, S., Wang, J., Franklin, M.J., Goldberg, K. and Kraska, T., PrivateClean: Data Cleaning and Differential Privacy. In SIGMOD 2016.

Krishnan, S., Wang, J., Wu, E., Franklin, M.J. and Goldberg, K., 2016. ActiveClean: interactive data cleaning for statistical modeling. In VLDB 2016.

Krishnan, S., Franklin, M.J., Goldberg, K. and Wu, E., BoostClean: Automating Error Detection and Repair For Machine Learning. Under Review.

## Installation
First, create a virtual environment for the project. First of all this is a good practice and isolates the dependencies.
```
virtualenv dc4ds 
```

To activate the virtual environment, run
```
cd dc4ds
source bin/activate
```

Then, install the core package
```
pip install dc4ds-core
```