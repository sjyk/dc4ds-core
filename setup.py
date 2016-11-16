from setuptools import setup, find_packages

setup(
  name = 'dc4ds-core',
  packages = find_packages(), # this must be the same as the name above
  version = '0.0.1',
  description = 'The core library for data cleaning for data science',
  author = 'Sanjay Krishnan and Eugene Wu',
  author_email = 'sanjay@eecs.berkeley.edu',
  url = 'https://github.com/sjyk/dc4ds-core/', # use the URL to the github repo
  download_url = 'https://github.com/sjyk/dc4ds-core/tarball/0.0.1', 
  keywords = ['error', 'detection', 'cleaning'], # arbitrary keywords
  classifiers = [],
  install_requires=[
          'numpy',
          'sklearn',
          'pandas',
          'scipy'
      ]
)