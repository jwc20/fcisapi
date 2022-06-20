from .core import *

# import unicodedata


def DictListUpdate(lis1, lis2):
    for aLis1 in lis1:
        if aLis1 not in lis2:
            lis2.append(aLis1)
    return lis2


def remove_non_printable_ascii(s):
    return "".join([c if 32 < ord(c) < 127 else None for c in s])


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

    def _make_accidents_search_url(
        self, p_start, p_finish, p_sort, p_desc, p_direction, p_show
    ):

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
            if len(self.keywords) == 1 and self.keywords[0].find('"') != -1:
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

    def _load_accidents_keywords_page(self, first_letter):  # None
        """
        For loading the list of keywords page by letters.
        """
        # print(first_letter)
        search_url = BASE_URL + ACCIDENT_KEYWORD_LETTER_URL
        r = requests.get(search_url + "=" + first_letter, headers=HEADERS)
        # print(r.url)
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _load_accidents_search_page(
        self,
        p_start=None,
        p_finish=None,
        p_sort=None,
        p_desc=None,
        p_direction=None,
        p_show=None,
    ):
        search_url = BASE_URL + ACCIDENT_SEARCH_URL
        payload_str = urlencode(
            self._make_accidents_search_url(
                p_start, p_finish, p_sort, p_desc, p_direction, p_show
            ),
            safe="+",
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

        results = []
        # data = {}
        table = soup_data.find_all(
            "table", {"class": "table table-bordered table-striped"}
        )[1]
        # print(table)
        table_rows = table.find_all("tr")

        for tr in table_rows[1:]:
            data = {
                "accident_id": None,
                "summary_url": None,
                "summary_nr": None,
                "event_date": None,
                "report_id": None,
                "fatality": "",
                "sic_url": None,
                "sic_number": None,
                "event_description": None,
            }
            data["accident_id"] = tr.find_all("td")[0].input.get("value")
            data["summary_url"] = (
                BASE_URL + "/pls/imis/" + tr.find_all("td")[2].a.get("href")
            )
            data["summary_nr"] = tr.find_all("td")[2].a.text
            data["event_date"] = tr.find_all("td")[3].text
            data["report_id"] = tr.find_all("td")[4].text
            data["fatility"] = tr.find_all("td")[5].text
            data["sic_number"] = tr.find_all("td")[6].text
            data["sic_url"] = (
                BASE_URL + SIC_DETAILS_URL + "/" + tr.find_all("td")[6].text
            )
            data["event_description"] = tr.find_all("td")[7].text
            # print(data)
            results.append(data)

        return self._transform_accidents_search_results(results)

    # arguments can be id, url,

    def _transform_accidents_search_results(self, results):
        new_results = []

        # TODO: maybe use regular expressions here
        for data in results:
            if (
                data["sic_url"] == "sic_manual.display?id=&tab=description"
                or data["sic_url"] == "https://www.osha.gov/sic-manual/"
            ):
                data["sic_url"] = None
            if data["sic_number"] == "":
                data["sic_number"] = None

            # TODO: /xa0 not utf-8, fix this later.
            if data["fatality"] != "X":
                # data["fatality"].replace(u'\xa0', u'')
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

    def _make_accident_details_url(self, ids, url=None):  # url
        # TODO: need to do url
        if url:
            return
        else:
            payload = {}
            search_url = BASE_URL + ACCIDENT_DETAILS_URL
            if len(ids) == 1:
                search_url += "?" + ID_URL + "=" + ids[0]
            else:
                search_url += "?" + ID_URL + "=" + ids[0]
                for details_id in ids[1:]:
                    search_url += "&" + ID_URL + "=" + details_id
        return search_url

    def _load_accident_details_page(self, ids=None, url=None):  # ids is a list
        details_url = self._make_accident_details_url(ids, url)
        # print(details_url)
        r = requests.get(details_url, headers=HEADERS)
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _scrape_accident_details(self, soup_data):
        # TODO: need to do this for multiple ids.
        details = []
        main_container = soup_data.find("div", {"id": "maincontain"})

        for div_table in main_container.find_all("div", {"class": "table-responsive"}):
            # print(div_table)
            data = {
                "accident_number": None,
                # "event_description": None,
                "report_id": None,
                "event_date": None,
                "inspection_url": None,
                "inspection_number": None,
                "open_date": None,
                "sic_number": None,
                "establishment_name": None,
                "detail_description": None,
                "keywords": [],
                "Employee": [],
            }
            # End Use	Proj Type	Proj Cost	Stories	NonBldgHt	Fatality
            # Employee #	Inspection	Age	Sex	Degree	Nature	Occupation
            data["accident_number"] = (
                div_table.find("div", {"class": "text-center"})
                .text.split("--")[0]
                .strip()
                .split(":")[1]
                .strip()
            )
            data["report_id"] = (
                div_table.find("div", {"class": "text-center"})
                .text.split("--")[1]
                .strip()
                .split(":")[1]
                .strip()
            )
            data["event_date"] = (
                div_table.find("div", {"class": "text-center"})
                .text.split("--")[2]
                .strip()
                .split(":")[1]
                .strip()
            )
            data["inspection_url"] = (
                div_table.find_all("tr")[2].find_all("td")[0].a.get("href")
            )
            data["inspection_number"] = (
                div_table.find_all("tr")[2].find_all("td")[0].text
            )
            data["open_date"] = div_table.find_all("tr")[2].find_all("td")[1].text
            data["sic_number"] = div_table.find_all("tr")[2].find_all("td")[2].text
            data["establishment_name"] = (
                div_table.find_all("tr")[2].find_all("td")[3].text
            )
            data["detail_description"] = div_table.find_all("tr")[3].text.strip()
            # keywords = div_table.find_all("tr")[4].text.split(":")[1].strip().split(",")
            for keyword in (
                div_table.find_all("tr")[4].text.split(":")[1].strip().split(",")
            ):
                data["keywords"].append(keyword)

            # if div_table.find_all("tr")[5].find("th").text ==  :
            # print(div_table.find_all("tr")[6:])

            # employees = []
            # print(div_table.find_all("tr")[6].previous_sibling.previous_sibling.find_all("th")[0].text)

            # TODO: End Use	Proj Type	Proj Cost	Stories	NonBldgHt	Fatality
            # https://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=570341&id=116803.015&id=171061435
            # if div_table.find_all("tr")[6].previous_sibling.previous_sibling.find_all("th")[0].text != "Employee #":
            #     print(div_table.find_all("tr")[6].previous_sibling.previous_sibling.find_all("th")[0].text)
            #     for table_row in div_table.find_all("tr")[6:]:
            #         data[div_table.find_all("tr")[6].previous_sibling.previous_sibling.find_all("th")[0].text]  = table_row.find_all("td")

            # TODO: BRUTE FORCING, find better solution later
            if (
                div_table.find_all("tr")[6]
                .previous_sibling.previous_sibling.find_all("th")[0]
                .text
                == "Employee #"
            ):

                for table_row in div_table.find_all("tr")[6:]:
                    emp = {}
                    # print(table_row.previous_sibling.previous_sibling.find_all("th"))
                    emp[
                        div_table.find_all("tr")[6]
                        .previous_sibling.previous_sibling.find_all("th")[0]
                        .text
                    ] = table_row.find_all("td")[0].text
                    emp[
                        div_table.find_all("tr")[6]
                        .previous_sibling.previous_sibling.find_all("th")[1]
                        .text
                    ] = table_row.find_all("td")[1].text
                    emp[
                        div_table.find_all("tr")[6]
                        .previous_sibling.previous_sibling.find_all("th")[2]
                        .text
                    ] = table_row.find_all("td")[2].text
                    emp[
                        div_table.find_all("tr")[6]
                        .previous_sibling.previous_sibling.find_all("th")[3]
                        .text
                    ] = table_row.find_all("td")[3].text
                    emp[
                        div_table.find_all("tr")[6]
                        .previous_sibling.previous_sibling.find_all("th")[4]
                        .text
                    ] = table_row.find_all("td")[4].text
                    emp[
                        div_table.find_all("tr")[6]
                        .previous_sibling.previous_sibling.find_all("th")[5]
                        .text
                    ] = table_row.find_all("td")[5].text
                    emp[
                        div_table.find_all("tr")[6]
                        .previous_sibling.previous_sibling.find_all("th")[6]
                        .text
                    ] = table_row.find_all("td")[6].text
                    emp[
                        div_table.find_all("tr")[6]
                        .previous_sibling.previous_sibling.find_all("th")[7]
                        .text
                    ] = table_row.find_all("td")[7].text

                    data["Employee"].append(emp)

            else:
                for table_row in div_table.find_all("tr")[8:]:
                    emp = {}
                    # print(table_row.previous_sibling.previous_sibling.find_all("th"))
                    emp[
                        div_table.find_all("tr")[8]
                        .previous_sibling.previous_sibling.find_all("th")[0]
                        .text
                    ] = table_row.find_all("td")[0].text
                    emp[
                        div_table.find_all("tr")[8]
                        .previous_sibling.previous_sibling.find_all("th")[1]
                        .text
                    ] = table_row.find_all("td")[1].text
                    emp[
                        div_table.find_all("tr")[8]
                        .previous_sibling.previous_sibling.find_all("th")[2]
                        .text
                    ] = table_row.find_all("td")[2].text
                    emp[
                        div_table.find_all("tr")[8]
                        .previous_sibling.previous_sibling.find_all("th")[3]
                        .text
                    ] = table_row.find_all("td")[3].text
                    emp[
                        div_table.find_all("tr")[8]
                        .previous_sibling.previous_sibling.find_all("th")[4]
                        .text
                    ] = table_row.find_all("td")[4].text
                    emp[
                        div_table.find_all("tr")[8]
                        .previous_sibling.previous_sibling.find_all("th")[5]
                        .text
                    ] = table_row.find_all("td")[5].text

                    data["Employee"].append(emp)

            details.append(data)
        return data

    # TODO: get inspection details

    def get_accidents(
        self,
        p_start=None,
        p_finish=None,
        p_sort=None,
        p_desc=None,
        p_direction=None,
        p_show=None,
    ):
        results_data = self._scrape_accidents_search_results(
            self._load_accidents_search_page(
                p_start, p_finish, p_sort, p_desc, p_direction, p_show
            )
        )
        return results_data

    def get_accident_details(self, ids=None, url=None):
        details_data = self._scrape_accident_details(self._load_accident_details_page(ids, url))
        return details_data
