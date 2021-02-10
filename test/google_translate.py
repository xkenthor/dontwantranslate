#!/usr/bin/python
from google_trans_new import google_translator

translator = google_translator()
translate_text = translator.translate('you know what im talking to right now', lang_tgt='ru')
print(translate_text)
