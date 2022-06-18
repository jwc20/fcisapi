from .core import *


class Accidents(object):
    def __init__(self, descriptions=[], abstracts=[], keywords=[], *args):
        self.descriptions = descriptions
        self.abstracts = abstracts
        self.keywords = keywords

    def _get_validated_keywords(self, words):
        """
        Validates a list of words to see if they are in the keyword list and returns a new list.
        """
        search_keyword_list = []
        for word in words:
            if word.lower() in self._get_keywords(word[0]):
                search_keyword_list.append(word)
        return search_keyword_list

    def _make_accidents_search_url(self, starting_at, _range):
        # +descriptions
        # +abstracts
        # +keywrods

        payload = {}

        if self.descriptions:
            payload[ACCIDENT_DESCRIPTION_URL] = ""
            for item in self.descriptions:
                payload[ACCIDENT_DESCRIPTION_URL] += item + " "
            payload[ACCIDENT_DESCRIPTION_URL] = payload[
                ACCIDENT_DESCRIPTION_URL
            ].strip()

        if self.abstracts:
            payload[ACCIDENT_ABSTRACT_URL] = ""
            for item in self.abstracts:
                payload[ACCIDENT_ABSTRACT_URL] += item + " "
            payload[ACCIDENT_ABSTRACT_URL] = payload[ACCIDENT_ABSTRACT_URL].strip()

        if self.keywords:
            payload[ACCIDENT_KEYWORD_URL] = ""
            for item in self.keywords:
                payload[ACCIDENT_KEYWORD_URL] += item + " "
            payload[ACCIDENT_KEYWORD_URL] = payload[ACCIDENT_KEYWORD_URL].strip()

        if starting_at:
            payload[PAGE_FINISH_URL] = starting_at
        print(urlencode(payload, safe="+"))
        print(payload)

        return urlencode(payload, safe="+")

    def _load_accidents_search_page(self, starting_at=None, _range=None):

        search_url = BASE_URL + ACCIDENT_SEARCH_URL + "?"
        if self.descriptions:
            search_url += ACCIDENT_DESCRIPTION_URL

        if self.abstracts:
            search_url += ACCIDENT_ABSTRACT_URL

        if self.keywords:
            search_url += ACCIDENT_KEYWORD_URL

        r = requests.get(
            search_url,
            params=self._make_accidents_search_url(starting_at, _range),
            headers=HEADERS,
        )

        # print(search_url)
        # r = requests.get(BASE_URL + ACCIDENT_SEARCH_URL, params)
        html = r.text
        # return BeautifulSoup(html, "lxml")
        return

    def _load_accidents_keywords_page(self, first_letter):
        """
        For loading the list of keywords page by letters.
        """
        r = requests.get(BASE_URL + ACCIDENT_KEYWORD_LETTER_URL + first_letter)
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _extract_accidents_0(self):
        return

    def _extract_accidents_1(self):
        return

    def _extract_accidents_2(self):
        return

    def _transform_accidents(self):
        return

    def _get_keywords(self, first_letter):
        if len(first_letter) != 1:
            print("Must input a letter.")
        else:
            keyword_list = []
            page = self._load_accidents_keywords_page(first_letter)
            a_hrefs = page.find("div", {"class": "well"}).find_all("a")
            for a_href in a_hrefs:
                keyword_list.append(a_href.text.lower())
            return keyword_list

    def get_accidents(self):
        return
