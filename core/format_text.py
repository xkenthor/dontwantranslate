#!/usr/bin/python
from random import shuffle

import os
import csv
import json

from google_trans_new import google_translator

import RAKE
import operator

_translator = google_translator()

_stop_symbols_wpm = '0123456789=@#$%^&*_+[]{}\\/|<>'
_stop_symbols_pm = '0123456789=!@#$%^&*()_+[]{}\\/|<>.'
_stopfile_path = '/run/media/lockheed117/Base/english-nltk/stopwords.txt'

def sort_tuple(utuple):
	utuple.sort(key = lambda x: x[1])
	return utuple

def read_file(filepath):
	with open(filepath, 'r') as file:
		info = file.read()

	return info

def write_file(info, filepath):
	with open(filepath, 'w') as file:
		file.write(info)

def impoverish_list(user_list):
	"""
	Keyword arguments:
	user_list -- < list > of < list > of < str > & < float >.

	Return:
	< list > of < str >.

	"""
	new_list = []
	for string in user_list:
		new_list.append(string[0])

	return new_list

def delete_breaks(string):
	"""
	Keyword arguments:
	string -- < str >.

	Return -- < str >.

	"""
	string_list = string.splitlines()
	new_string = ''
	for string in string_list:
		while True:
			if len(string) != 0:
				if string[-1] == '-':
					string = string[:-1]
				else:
					new_string += (" "+string)
					break
			else:
				break

	return new_string

def get_next_symbol_index(string, current_index, symbol=' '):
	"""
	Keyword arguments:
	string -- < str > string where spaces will be scanned.
	current_index -- < int >

	Return:
	< None > / < int > -- if there is no symbol to the end of string / index
		with next symbol.

	"""
	length = len(string)
	result = None

	for index in range(current_index, length):
		if string[index] != symbol:
			result = index
			break

	return result

def delete_extra_symbols(string, symbol=' '):
	"""
	Keyword arguments:
	string -- < str >.
	symbol -- < str >, symbol that will be removed

	Return:
	< list > of < str >, where will be removed extra spaces.

	"""
	length = len(string)

	new_str = ''
	index = 0

	if length == 0:
		pass

	while string[index] == symbol:
		index +=1

		if index >= length:
			break

	while index < length:
		if string[index] == symbol:
			index = get_next_symbol_index(string, index, symbol=symbol)

			if index is None:
				break

			else:
				new_str += symbol

		new_str += string[index]
		index += 1

	return new_str

def delete_extra_symbols_list(string_list, symbol=' '):
	"""
	Keyword arguments:
	string_list -- < list > of < str >.

	Return:
	< list > of < str >, where will be removed extra spaces.

	"""
	new_list = []

	for string in string_list:

		new_str = delete_extra_symbols(string, symbol=symbol)

		# to prevent index exception
		if len(new_str) == 0:
			pass

		else:
			new_list.append(new_str)

	return new_list

def delete_symbols(string, stop_symbols):
	"""
	Keyword arguments:
	string -- < str > line where will be removed stop symbols.
	stop_symbols -- < string > of < str > with stop symbols that will be
		removed.

	Return:
	< list > of < str > with removed stop symbols inside.

	"""
	for stop_symbol in stop_symbols:
		string = string.replace(stop_symbol, '')

	return string

def delete_symbols_list(string_list, stop_symbols):
	"""
	Keyword arguments:
	string_list -- < list > of < str > where will be removed stop symbols.
	stop_symbols -- < set > of < str > with stop symbols that will be removed.

	Return:
	< list > of < str > with removed stop symbols inside.

	"""
	for index in range(len(string_list)):

		string_list[index] = delete_symbols(string_list[index], stop_symbols)

	return string_list

def get_keyword_list(string):
	"""
	Keyword arguments:
	string -- < str > that will be processed.

	Return:
	< list > of < list > of < str > & < float >.

	"""
	rake_object = RAKE.Rake(_stopfile_path)
	keyword_list = sort_tuple(rake_object.run(string))

	return keyword_list

def full_processing(string):

	string = delete_breaks(string)
	string = delete_symbols(string, _stop_symbols_wpm)
	string = delete_extra_symbols(string)
	string = delete_extra_symbols(string, '-')

	string = string.encode("ascii", "ignore")
	string = string.decode()

	string = get_keyword_list(string)

	string = impoverish_list(string)
	string = delete_extra_symbols_list(string, '-')
	string = delete_symbols_list(string, _stop_symbols_pm)

	return string[::-1]

def last_cell_index(string_list, max):
	"""
	Keyword arguments:
	string_list -- < list > of < string > where symbols will be counted.
	max -- < int > -- symbol limit count.

	Return:
	< None > / < int > -- if list is empty / number of cell where limit has
		been reached.

	"""
	list_length = len(string_list)
	if list_length == 0:
		return None

	symbol_count = 0
	for index in range(list_length):
		symbol_count += len(string_list[index])
		if symbol_count >= max:
			return index

def csv_write(data_list, filename='data_list.csv'):

	# opening the csv file in 'w+' mode
	# writing the data into the file
	with open(filename, 'w', newline ='') as file:
		write = csv.writer(file, delimiter=',')
		for data in data_list:
			write.writerow(data)

def crop_and_shuffle(string_list, max):
	"""
	Keyword arguments:
	stirng_list -- < list > of < str >.

	Return:
	< list > of < str >.

	"""
	max = 6500
	last_index = last_cell_index(string_list, max)

	string_list = string_list[:last_index]

	shuffle(string_list)

	return string_list

def translate(string, dst='ru'):
	"""
	Keyword arguments:
	< str >.

	Return:
	< str >.

	"""
	try:
		translation = _translator.translate(string, lang_tgt=dst)
	except Exception as error:
		print(error.__str__())
		translation = None

	return translation

def translate_list(string_list):
	"""
	Keyword arguments:
	string_list -- < list > of < str >.

	Return:
	< list > of < list > of < str >.

	"""
	result = []
	counter = 0
	persent_value = 100/len(string_list)

	for string in string_list:

		translation = translate(string)
		if translation is None:
			translation = '-'

		new_element = [string, translation]
		result.append(new_element)

		counter += 1
		print('{}% done.'.format(round(persent_value*counter, 2)))

	print('')
	return result

if __name__ == '__main__':

	textfile_path = '/run/media/lockheed117/Base/english-nltk/qq/PointShadows.txt'
	string = read_file(textfile_path)

	string_list = full_processing(string)
	string_list = crop_and_shuffle(string_list, 6500)

	translated_string = translate_list(string_list)

	csv_write(translated_string)
