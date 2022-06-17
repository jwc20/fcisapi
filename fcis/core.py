from bs4 import BeautifulSoup
import requests
import time

BASE_URL = "https://www.osha.gov"
HEADERS = {"Content-Type": "text/html; charset=UTF-8"}

# Search Results URLs
SEARCH_URL = "/pls/imis/AccidentSearch.search"

ACCOUNT_DESCRIPTION_URL = "acc_description="
ACCOUNT_ABSTRACT_URL = "acc_Abstract="
ACCOUNT_KEYWORD = "acc_keyword="

SIC_URL = "sic="
NAICS_URL = "naics="

OFFICE_URL = "Office="
OFFICE_TYPE_URL = "officetype="

END_MONTH_URL = "endmonth="
END_DAY_URL = "endday="
END_YEAR_URL = "endyear="

START_MONTH_URL = "startmonth="
START_DAY_URL = "startday="
START_YEAR_URL = "startyear="

INSPECTION_NUMBER_URL = "InspNr="

# SIC Search Result URLs
SIC_SEARCH_URL = "/data/sic-search"

SIC_NUMBER_VALUE_URL = "field_sic_number_value="
SIC_KEYWORDS_URL = "title_and_body="
