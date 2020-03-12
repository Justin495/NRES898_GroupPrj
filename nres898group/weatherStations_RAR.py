import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# http://www.rcc-acis.org/docs_webservices.html

# weather station IDs:
#   Rogers Farm #1: 2001
#   LINCOLN AIRPORT: 14939

siteList = ['2001','14939']
startDate = '2019-01-01'
endDate = '2019-12-31'
appended_df = []

# https://stackoverflow.com/questions/56892685/looping-through-urls-to-create-csv-and-dataframe-for-pandas
for sites in siteList:
    concatURL = f'http://data.rcc-acis.org/StnData?sid={sites}&sdate={startDate}&edate={endDate}&elems=1,2,4&output=csv'
    newData = pd.read_csv(concatURL,sep=',',skiprows=1,header=None)
    newData['site'] = sites     # add column to identifiy the site for this data
    appended_df.append(newData) # list of separate data frames, one for each site

df = pd.concat(appended_df)     # combine list of separate data frames into a single dataframe

df.columns = ['date','maxTemp','minTemp','precip','site']
df.head(20)
df.tail(20)

# convert weath data to numeric and date to datetime
# also handle errors as some data may be reported as 
# "missing data values are returned as 'M' and trace values of
# precipitation, snowfall or snow depth are returned as 'T'"
df.minTemp = pd.to_numeric(df.minTemp, errors='coerce')
df.maxTemp = pd.to_numeric(df.maxTemp, errors='coerce')
df.precip = pd.to_numeric(df.precip, errors='coerce')
df.date = pd.to_datetime(df.date)

df.set_index('date',inplace=True)

df.info()


monthlyMean = df.groupby(['site']).resample('M').mean()
print(monthlyMean)



# ax = plt.plot(df.date, df.minTemp)
# ax = plt.plot(df.date, df.maxTemp)
# plt.legend(['minTemp','maxTemp'])

# # https://geo-python.github.io/2017/lessons/L7/matplotlib.html

# plt.axis([20150101,20150201,40,70])

# # https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/date.html

# years = mdates.YearLocator()
# months = mdates.MonthLocator()

# ax.xaxis.set_major_locator(years)

# plt.show()

