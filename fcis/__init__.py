from .core import *
from .results import Results
from .accident import Accident
from .inspection import Inspection
from .sic import SIC # Standard Industrial Classification


# Fatalities and Catastrophies Investigation Summaries
class FCIS(Results, Accident, Inspection, Sic):
    def __init__(self, keywords=[], *args):
        Results.__init__(self, keywords=keywords, *args)
        Accident.__init__(self, keywords=keywords, *args)
        Inspection.__init__(self, *args)
        SIC.__init__(self, keywords=keywords, *args)


__author__ = ["Jae W. Choi"]
__source__ = "https://github.com/jwc20/fcis-api"
__license__ = "MIT"
__all__ = ["FCIS"]
