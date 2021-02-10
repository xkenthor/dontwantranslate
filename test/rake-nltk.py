#!/usr/bin/python
from rake_nltk import Rake

filename = '/run/media/lockheed117/Base/english-nltk/text-ex.txt'

with open(filename, 'r') as file:
	txt = file.read()

print(txt)

r = Rake()
r.extract_keywords_from_text(txt)
print(r.get_ranked_phrases()[0:10])
