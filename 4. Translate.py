import pandas as pd
import numpy as np
import pprint

pd.set_option('display.max_columns', None)

messages = pd.read_csv('C://Users//pawel//Datasets//Bike Trip//Final//Messages.csv', names = ['Date', 'Message_PL'], delimiter=',')
messages = pd.DataFrame(messages)
