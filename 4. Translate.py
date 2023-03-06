import pandas as pd
import numpy as np
import pprint
import googletrans
from googletrans import Translator

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

translator = Translator()

messages = pd.read_csv('C://Users//pawel//Datasets//Bike Trip//Final//Messages.csv', index_col='Date', delimiter=',', encoding='utf-8')
messages = pd.DataFrame(messages)

messages.rename(columns={'Message':'Message_PL'}, inplace=True)
messages.dropna(inplace=True)
messages['Message_EN'] = ''

translations = {}

for msg in messages:
    unique_elements = messages['Message_PL'].unique()
    for element in unique_elements:
        translations[element] = translator.translate(element, dest='english').text

messages['Message_EN'] = messages['Message_PL'].replace(translations)