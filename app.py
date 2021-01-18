import matplotlib.pyplot as plt
import seaborn
import pandas as pd

rin_df = pd.read_csv("dataset.csv")
by_category = rin_df.groupby(['Fuel Category', 'Month']).sum()[['RINs','Volume (Gal.)']].reset_index()
df = by_category.pivot(index='Month',columns='Fuel Category', values='RINs')
df.plot()
plt.show()
