from .core import *


class Accidents(object):
    def __init__(self, keywords=[], *args):
        self.keywords = keywords
    

    def _make_accidents_search_url(self):
        return

    def _load_accidents_search_page(self):
        r = requests.get(BASE_URL + ACCIDENT_SEARCH_URL)
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _load_accidents_keywords_page(self, first_letter):
        r = requests.get(BASE_URL + ACCIDENT_KEYWORD_LETTER_URL + first_letter )
        html = r.text
        return BeautifulSoup(html, "lxml")

    # def _load_accidents_search_form_page(self):
    #     r = requests.get(BASE_URL + ACCIDENT_SEARCH_FORM_URL)
    #     html = r.text
    #     return BeautifulSoup(html, "lxml")

    def _extract_accidents_0(self):
        return

    def _extract_accidents_1(self):
        return

    def _extract_accidents_2(self):
        return

    def _transform_accidents(self):
        return

    def get_keywords(self, first_letter):
        # TODO: add validator
        page = self._load_accidents_keywords_page(first_letter)
        return page

    def get_accidents(self):
        return


