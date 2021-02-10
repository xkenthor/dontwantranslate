#!/usr/bin/python
import json

import RAKE
import operator

def sort_tuple(utuple):
	utuple.sort(key = lambda x: x[1])
	return utuple

# filepath = '/run/media/lockheed117/Base/english-nltk/text-ex.txt'
# filepath = '/run/media/lockheed117/Base/downloads/30071.full.txt'
filepath = 'result.txt'

with open(filepath, 'r') as file:
	txt = file.read()

stopfile = '/run/media/lockheed117/Base/english-nltk/stopwords.txt'

rake_object = RAKE.Rake(stopfile)
keywords = sort_tuple(rake_object.run(txt))#[-10:]

print(json.dumps(keywords, indent=3))
print(type(keywords))
