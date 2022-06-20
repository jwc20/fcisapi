# fcis-api

A scraper API for Fatality and Catastrophe Investigation Summaries


## Installation 
To install, you can clone the project:
```
git clone git@github.com:jwc20/fcis-api.git
cd fcis-api
pip install -r requirement.txt
```


## Usage

### Create client for searching accident reports

You can use description, abstract, and keyword words to search the reports.
Note that "abstract" served the same purpose as "description" for older reports.

```
import fcis

desc = ["employee"]
abst = ["employee"]
keyw = ["fire"]

client = fcis.FCIS(description=desc, keywords=keyw)
```

### Scrape accident reports

```
client.get_accidents(p_show=100)
```

And you will get:

```
[{'accident_id': '141245.015',
  'summary_url': 'https://www.osha.gov/pls/imis/accidentsearch.accident_detail?id=141245.015',
  'summary_nr': '141245.01',
  'event_date': '11/17/2021',
  'report_id': '0213900',
  'fatality': None,
  'sic_url': None,
  'sic_number': None,
  'event_description': 'Employee Is Killed After Falling Through Elevator Shaft',
  'fatility': 'X'},
  ...
```

### Create client for getting details

```
import fcis
client = fcis.FCIS()
```

### Scrape accident details

You can use use the id of the accident details (found in searching the results) to get the details.

```
client.get_accident_details(ids=["171061435"])
```

To get:

```
{'accident_number': '570341',
 'report_id': '0522300',
 'event_date': '08/15/1984',
 'inspection_url': 'establishment.inspection_detail?id=1667450',
 'inspection_number': '1667450',
 'open_date': '08/16/1984',
 'sic_number': '4741',
 'establishment_name': 'Mobile Tank Car Services',
 'detail_description': 'THREE EMPLOYEES WERE CLEANING A RAILROAD TANK CAR CONTAINING RESIDUES OF COAL TAR LIGHT OIL, A FLAMMABLE LIQUID. ONE WAS ON TOP OF THE CAR, THE OTHER TWO WERE INSIDE. THEY WERE USING STEEL SHOVELS AND A NON EXPLOSION-PROOF LIGHT INSIDE THE CAR. THE VAPORS IGNITED, KILLING THE TWO EMPLOYEES INSIDE AND BURNING THE ONE ON TOP. THE OTHER EMPLOYEES WERE INJURED IN THE RESCUE ATTEMPT.',
 'keywords': ['burn',
  ' coal tar light oil',
  ' flammable vapors',
  ' railroad tank car',
  ' cleaning',
  ' explosion'],
 'Employee': [{'Employee #': '1',
   'Inspection': '1667450',
   'Age': '',
   'Sex': '',
   'Degree': 'Fatality',
   'Nature': 'Asphyxia',
   'Occupation': 'Occupation not reported',
   '': ''},
  {'Employee #': '2',
   'Inspection': '1667450',
   'Age': '',
   'Sex': '',
   'Degree': 'Fatality',
   'Nature': 'Asphyxia',
   'Occupation': 'Occupation not reported',
   '': ''},
  ...
}
```

### Links

[Accident Search](https://www.osha.gov/pls/imis/accidentsearch.html)

[Accident Investigation Search Help](https://www.osha.gov/help/accident-investigation)
