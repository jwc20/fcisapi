from .core import *
from .accidents import Accidents  # Search Accident Results
from .accident_detail import AccidentDetail  # Accident Details
from .inspection_detail import InspectionDetail  # Inspection Details
from .sic import SIC  # Standard Industrial Classification


# Fatalities and Catastrophies Investigation Summaries
class FCIS(Accidents, AccidentDetail, InspectionDetail, SIC):
    def __init__(self, keywords=[], *args):
        Accidents.__init__(self, keywords=keywords, *args)
        AccidentDetail.__init__(self, keywords=keywords, *args)
        InspectionDetail.__init__(self, *args)
        SIC.__init__(self, keywords=keywords, *args)


__author__ = ["Jae W. Choi"]
__source__ = "https://github.com/jwc20/fcis-api"
__license__ = "MIT"
__all__ = ["FCIS"]
