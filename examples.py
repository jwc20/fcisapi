import fcis
from pprintpp import pprint

desc = ["employee"]
abst = ["employee"]
keyw = ["fire"]

# Search for accident reports
client = fcis.FCIS(descriptions=desc, keywords=keyw)
reports = client.get_accidents(p_show=100)
pprint(reports)

# Get details for an accident
# client = fcis.FCIS()
# details = client.get_accident_details(ids=["570341"])
# print(details)

# Get valid keywords
# keys1 = [
#     "Gas",
#     "Gas Can",
#     "gas can",
#     "ack",
#     "guard",
#     "alskjdhaksd",
#     "hellppp!",
#     "saw",
#     "sus",
#     "cat",
# ]

# client = fcis.FCIS(keys1)
# print(client._get_validated_keywords(keys1))
