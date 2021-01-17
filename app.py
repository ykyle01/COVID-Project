import pandas as pd

def find_top_confirmed(n = 15):
    corona_df = pd.read_csv('datasets/covid-19-dataset-1.csv')
    by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return cdf