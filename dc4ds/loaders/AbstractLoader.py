"""
An abstract loader defines the basic data i/o
class for dc4ds. Specific loaders are instantiations
of this.
"""

class AbstractLoader(object):

    def load(self):
        raise NotImplemented("All loaders must implement a load method")