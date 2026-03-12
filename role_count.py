import pandas as pd

df = pd.read_csv('ddat_data/roles.csv')
print('Total rows:', len(df))
print('Unique roles:', df['Role'].nunique())
print('\nRoles list:')
print(df['Role'].unique())
