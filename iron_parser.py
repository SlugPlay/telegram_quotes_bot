import json
import random

def find_quote():
    file = open('iron_quotes.json', 'r')
    data = json.load(file)
    return data.get(str(random.randint(1, len(data))))