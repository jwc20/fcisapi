from .core import *
from .accidents import Accidents  # Search Accident Results


# Fatalities and Catastrophies Investigation Summaries
class FCIS(Accidents):
    def __init__(self, descriptions=[], abstracts=[], keywords=[], *args, **kwargs):
        Accidents.__init__(self, descriptions, abstracts, keywords, *args, **kwargs)


__author__ = ["Jae W. Choi"]
__source__ = "https://github.com/jwc20/fcis-api"
__license__ = "MIT"
__all__ = ["FCIS"]
