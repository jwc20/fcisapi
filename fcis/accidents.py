
from .core import *

import urllib.parse

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

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
                # print(word)
                search_keyword_list.append(word)
            else:
                not_keyword_list.append(word)
        # print(not_keyword_list)
        return search_keyword_list

    def _make_accidents_search_url(self, p_start, p_finish, p_sort, p_desc, p_direction,  p_show):
        
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
            # If there are double quotes surrounding the word
            if len(self.keywords) == 1 and self.keywords[0].find("\"") != -1:
                existing_keywords = self.keywords
                payload[ACCIDENT_KEYWORD_LIST_URL] = "on"
            else:
                existing_keywords = self._get_validated_keywords(self.keywords)
            
            payload[ACCIDENT_KEYWORD_URL] = ""
            for item in existing_keywords:
                payload[ACCIDENT_KEYWORD_URL] += item + " "
            payload[ACCIDENT_KEYWORD_URL] = payload[ACCIDENT_KEYWORD_URL].strip()

        if p_finish:
            payload[PAGE_START_URL] = ""
            payload[PAGE_FINISH_URL] = p_finish
            payload[PAGE_SORT_URL] = p_sort if p_sort else ""
            payload[PAGE_DESC_URL] = p_desc if p_desc else ""
            payload[PAGE_DIRECTION_URL] = p_direction if p_direction else ""
            payload[PAGE_SHOW_URL] = p_show if p_show else "20"

        if p_show and not p_finish:
            payload[PAGE_SHOW_URL] = p_show

        return payload

    def _load_accidents_keywords_page(self, first_letter):
        """
        For loading the list of keywords page by letters.
        """
        # print(first_letter)
        search_url = BASE_URL + ACCIDENT_KEYWORD_LETTER_URL
        r = requests.get(search_url + "=" + first_letter, headers=HEADERS)
        # print(r.url)
        html = r.text
        return BeautifulSoup(html, "lxml")

    # def _load_accidents_search_page_by_keyword(self, p_start=None, p_finish=None, p_sort=None, p_desc=None, p_direction=None, p_show=None):
    #     # print(self._get_validated_keywords(self.keywords))
    #     # print(is_accident_search(r.url))
    #     # if len(
    #     #     self._get_validated_keywords(self.keywords)
    #     # ) == 1 and not is_accident_search(r.url):
        
    #     payload_keyword = {} 

    #     keyword_url = self._get_validated_keywords(self.keywords)[0]
    #     # print(url)
        
        
    #     # # TODO: use urlencode or urllib.parse
    #     # search_url = (
    #     #     BASE_URL
    #     #     + ACCIDENT_SEARCH_URL
    #     #     + "?"
    #     #     + ACCIDENT_KEYWORD_URL
    #     #     + "="
    #     #     + '"'
    #     #     + keyword_url
    #     #     + '"'
    #     #     + ACCIDENT_KEYWORD_LIST_URL
    #     # )
    #     # print(search_url)
    #     # payload_str = urlencode(
    #     #     self._make_accidents_search_url(p_start, p_finish, p_sort, p_desc, p_direction, p_show), safe=""
    #     # )
        
    #     search_url = BASE_URL + ACCIDENT_SEARCH_URL
        
    #     payload_keyword[ACCIDENT_KEYWORD_URL] = keyword_url
    #     payload_keyword[ACCIDENT_KEYWORD_LIST_URL] = "on"
        
    #     # payload_str = urlencode(
    #     #     self._make_accidents_search_url(p_start, p_finish, p_sort, p_desc, p_direction, p_show), safe=""
    #     # )
        
    #     payload_str = self._make_accidents_search_url(p_start, p_finish, p_sort, p_desc, p_direction, p_show)
        
        
        
    #     payload = Merge(payload_str, payload_keyword)
        
    #     print(payload)
        
    #     r = requests.get(search_url, params=payload, headers=HEADERS)
    #     print(r.url)
    #     html = r.text
    #     # print(html)
    #     return BeautifulSoup(html, "lxml")
    



    def _load_accidents_search_page(self, p_start=None, p_finish=None, p_sort=None, p_desc=None, p_direction=None, p_show=None):
        search_url = BASE_URL + ACCIDENT_SEARCH_URL
        payload_str = urlencode(
            self._make_accidents_search_url(p_start, p_finish, p_sort, p_desc, p_direction, p_show), safe="+"
        )
        # print(payload_str)

        r = requests.get(
            search_url,
            params=payload_str,
            headers=HEADERS,
        )
        # print(r.url)

        # If there is only one keyword and the site form can not fetch, go to the list of keywords and fetch from there.
        if is_accident_search(r.url):
            print(r.url)
            html = r.text
            return BeautifulSoup(html, "lxml")

        else:
            print("Your search did not return any result.")
            pass

    def _scrape_accidents_search_results(self, soup_data):
        """
        Number of results
        Summary Nr
        Event Date
        Report ID
        Fat
        SIC
        Event Description
        """

        if not soup_data:
            return

        else:

            data = {
                "accident_id": None,
                "summary_url": None,
                "summary_nr": None,
                "event_date": None,
                "report_id": None,
                "fatality": None,
                "sic_url": None,
                "sic_num": None,
                "event_description": None,
            }
            results = []
            # data = {}
            table = soup_data.find_all(
                "table", {"class": "table table-bordered table-striped"}
            )[1]
            # print(table)
            table_rows = table.find_all("tr")

            for tr in table_rows[1:]:
                data["accident_id"] = tr.find_all("td")[0].input.get("value")
                data["summary_url"] = (
                    BASE_URL + "/pls/imis/" + tr.find_all("td")[2].a.get("href")
                )
                data["summary_nr"] = tr.find_all("td")[2].a.text
                data["event_date"] = tr.find_all("td")[3].text
                data["report_id"] = tr.find_all("td")[4].text
                data["fatility"] = tr.find_all("td")[5].text
                # data["sic_url"] = tr.find_all("td")[6].a.get("href")
                data["sic_num"] = tr.find_all("td")[6].text
                data["sic_url"] = (
                    BASE_URL + SIC_DETAILS_URL + "/" + tr.find_all("td")[6].text
                )
                data["event_description"] = tr.find_all("td")[7].text
                results.append(data)

            return self._transform_accidents_search_results(results)

    # arguments can be id, url,
    def _scrape_accident_details(self):
        return

    def _transform_accidents_search_results(self, results):
        # clean some scraped results
        # Examples:
        # 'sic_url': 'sic_manual.display?id=&tab=description',
        # 'sic_num': ''
        # 'fatility': 'X'
        new_results = []

        # TODO: maybe use regular expressions here
        for data in results:
            if (
                data["sic_url"] == "sic_manual.display?id=&tab=description"
                or data["sic_url"] == "https://www.osha.gov/sic-manual/"
            ):
                data["sic_url"] = None
            if data["sic_num"] == "":
                data["sic_num"] = None
            if data["fatality"] != "X":
                data["fatality"] = None
            new_results.append(data)
        return new_results

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

    def DictListUpdate(lis1, lis2):
        for aLis1 in lis1:
            if aLis1 not in lis2:
                lis2.append(aLis1)
        return lis2

    def get_accidents(self):
        return
