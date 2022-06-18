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
        not_keyword_list = []
        for word in words:
            if word.lower() in self._get_keywords(word[0]):
                search_keyword_list.append(word)
            else:
                not_keyword_list.append(word)
        print(not_keyword_list)
        return search_keyword_list

    def _make_accidents_search_url(self, starting_at, _range):

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

        if _range:
            payload[PAGE_SHOW_URL] = _range

        return payload

    def _load_accidents_keywords_page(self, first_letter):
        """
        For loading the list of keywords page by letters.
        """
        r = requests.get(BASE_URL + ACCIDENT_KEYWORD_LETTER_URL + first_letter)
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _load_accidents_search_page(self, starting_at=None, _range=None):

        search_url = BASE_URL + ACCIDENT_SEARCH_URL

        payload_str = urlencode(
            self._make_accidents_search_url(starting_at, _range), safe="+"
        )

        r = requests.get(
            search_url,
            params=payload_str,
            headers=HEADERS,
        )

        html = r.text
        return BeautifulSoup(html, "lxml")

    def _extract_accidents_search_results(self, soup_data):
        """
        Number of results
        Summary Nr
        Event Date
        Report ID
        Fat
        SIC
        Event Description
        """
        '''
        data = {
            "accident_id": None,
            "summary_url": None,
            "summary_nr": None,
            "event_date": None,
            "report_id": None,
            "fatality": None,
            "sic_num": None,
            "event_description": None,
        }
        '''
        data = {}
        table = soup_data.find_all("table", {"class": "table table-bordered table-striped"})[1]
        # print(table)
        table_rows = table.find_all("tr")

        for tr in table_rows[1:]:
            print(tr)
            # table_data = tr.find_all("td")
            # for td in Vtable_data:
            # data["accident_id"] = tr.find("td", {"value"}).text 
            # data["summary_url"] = tr.find("td", {})
            data["accident_id"] = tr.find_all("td")[1]


        return data

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
