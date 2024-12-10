import pandas as pd

print("hi")

filename='Experiment Design.xlsx'
sheet='Experiment Design V2'
cols=[1,2,3,4,5,6,7,8,9, 12]

dataframe = pd.read_excel(filename, sheet_name=sheet, usecols=cols, header=1, nrows=234, index_col=2)

print(dataframe)

print("done")

print(dataframe.loc["A2"]["Angle"])