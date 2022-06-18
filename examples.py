import fcis


keys1 = [
    "Gas",
    "Gas Can",
    "gas can",
    "ack",
    "guard",
    "alskjdhaksd",
    "hellppp!",
    "saw",
    "sus",
    "cat",
]


client = fcis.FCIS(keys1)
print(client._get_validated_keywords(keys1))
