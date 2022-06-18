from bs4 import BeautifulSoup
import requests
import time
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

BASE_URL = "https://www.osha.gov"
HEADERS = {"Content-Type": "text/html; charset=UTF-8"}
ID_URL = "id"

# Accident Search Results URLs
ACCIDENT_SEARCH_FORM_URL = "/pls/imis/accidentsearch.html"
ACCIDENT_SEARCH_URL = "/pls/imis/AccidentSearch.search"

ACCIDENT_DESCRIPTION_URL = "acc_description"
ACCIDENT_ABSTRACT_URL = "acc_Abstract"
ACCIDENT_KEYWORD_URL = "acc_keyword"

ACCIDENT_KEYWORD_LETTER_URL = (
    "/pls/imis/accidentsearch.display_keyword?v_keywordletter"
)

ACCIDENT_SIC_URL = "sic"
ACCIDENT_NAICS_URL = "naics"

ACCIDENT_OFFICE_URL = "Office"
ACCIDENT_OFFICE_TYPE_URL = "officetype"

ACCIDENT_END_MONTH_URL = "endmonth"
ACCIDENT_END_DAY_URL = "endday"
ACCIDENT_END_YEAR_URL = "endyear"

ACCIDENT_START_MONTH_URL = "startmonth"
ACCIDENT_START_DAY_URL = "startday"
ACCIDENT_START_YEAR_URL = "startyear"

ACCIDENT_FATAL_URL = "Fatal"

INSPECTION_NUMBER_URL = "InspNr"

PAGE_START_URL = "p_start" # This doesn't work
PAGE_FINISH_URL = "p_finish" # Returns results starting at the index input (it should be renamed to p_starting_at)
PAGE_SORT_URL = "p_sort" # This doen't work
PAGE_DESC_URL = "p_desc" # ASC or DESC (it should be renamed to p_order)
PAGE_DIRECTION_URL = "p_direction"
PAGE_SHOW_URL = "p_show"


# SIC Search Result URLs
SIC_SEARCH_URL = "/data/sic-search"

SIC_NUMBER_VALUE_URL = "field_sic_number_value"
SIC_KEYWORDS_URL = "title_and_body"

# SIC Details URLs
SIC_DETAILS_URL = "/sic-manual"


# Note: multiple details url can be fetched via id's
# EX: https://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=128574.015&id=108256.015
# Accident Details URLs (uses id)
ACCIDENT_DETAILS_URL = "/pls/imis/accidentsearch.accident_detail"

# Inspection URLs (uses id)
INSPECTION_DETAILS_URL = "/pls/imis/establishment.inspection_detail"


def is_accident_search(url):
    """
    Validates accident search url
    """
    return True if ACCIDENT_SEARCH_URL in url else False


def is_accident_detail(url):
    """
    Validates accident detail url
    """
    return True if ACCIDENT_DETAILS_URL in url else False


def is_inspection_detail(url):
    """
    Validates inspection detail url
    """
    return True if INSPECTION_DETAILS_URL in url else False


def is_sic_search(url):
    """
    Validate sic search url
    """
    return True if SIC_SEARCH_URL in url else False


def is_sic_detail(url):
    """
    Validates sic details url
    """
    return True if SIC_DETAILS_URL in url else False


"""
# Accident Search
def get_keywords():
    return


# Sic Search
def get_sic_keywords():
    return
"""
