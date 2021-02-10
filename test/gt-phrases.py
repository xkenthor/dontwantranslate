#!/usr/bin/python
import nltk
from nltk.collocations import *

filename = 'text-ex.txt'

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

# change this to read in your data
finder = BigramCollocationFinder.from_words(
    nltk.corpus.genesis.words('/run/media/lockheed117/Base/english-nltk/text-ex.txt'))

# only bigrams that appear 3+ times
finder.apply_freq_filter(3)

# return the 10 n-grams with the highest PMI
result = finder.nbest(bigram_measures.pmi, 10)

print(result)
