import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

start_date = dt.datetime(2020, 1, 22)
end_date = dt.datetime(2020, 6, 20)

covid_data = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
covid_data = covid_data.drop(
    ['FIPS', 'Admin2', 'Lat', 'Long_', 'iso2', 'iso3', 'UID', 'code3', 'Country_Region', 'Combined_Key'], axis=1)
covid_data = covid_data.groupby('Province_State', axis=0).sum()
covid_data = covid_data.transpose()
covid_data.index = pd.to_datetime(covid_data.index)
covid_data['Total'] = covid_data.sum(axis=1)


def getTimeRange(startdate=start_date, enddate=end_date, state='Total'):
    return covid_data.loc[(covid_data.index >= startdate) &
                          (covid_data.index <= enddate)][state]


covid_normalized = np.log10(getTimeRange())
together = covid_normalized.to_frame()
together.rename(columns={'Total': 'COVID Cases'}, inplace=True)

benchmarks = ['^GSPC', '^DJI', '^IXIC']
for benchmark in benchmarks:
    ticker = benchmark.replace('^', '')
    stock_data = pdr.get_data_yahoo(
        benchmark, start=start_date, end=end_date)
    stock_data.rename(columns={'Adj Close': ticker}, inplace=True)
    together = pd.concat([together, stock_data[ticker]], axis=1)

together = together.dropna()
corr = together.corr()['COVID Cases'].drop('COVID Cases')
with open('output.txt', 'w') as f:
    for row in corr.index:
        f.write(row + ': ' + str(corr[row]) + '\n')
