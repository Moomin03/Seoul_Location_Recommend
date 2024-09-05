import pandas as pd

a = pd.read_csv('../csv/FRAME.csv')
b = pd.read_csv('home_data4.csv')
new_file = pd.concat([a, b], axis=0)
new_file.to_csv('FRAME.csv')