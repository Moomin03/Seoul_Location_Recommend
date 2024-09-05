import pandas as pd

a = pd.read_csv('/Users/hack/PycharmProjects/Project_1/csv/FRAME.csv')
b = pd.read_csv('/Users/hack/PycharmProjects/Project_1/home_data5.csv')
new_file = pd.concat([a, b], axis=0)
new_file.to_csv('FRAME.csv')