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


def weatherdf (siteList,startDate,endDate):
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

    #df.info()
    return df

print(f'1. Daily climate data for stations {" & ".join(str(x) for x in siteList)} between {startDate} and {endDate}:')
print(weatherdf(siteList,startDate,endDate))



pentadMean = df.groupby(['site']).resample('5D').mean()
print(f'2.  Pentad mean climate data for stations {" & ".join(str(x) for x in siteList)} between {startDate} and {endDate}:')
print(pentadMean)


# import list of weather stations in Lancaster county
columnNames=['station_id','name','state','longitude','latitude','elevation']
countydf = pd.read_csv("http://data.rcc-acis.org/StnMeta?county=31109&output=csv",sep=",",names = columnNames)

#need help here. This may not work, but thought by creating a definition for the df creation, question 3 would be simpler
#just need to 'station_id' column into siteList
#print(weatherdf(___________,startDate,endDate))

monthlyMean = df.groupby(['site']).resample('M').mean()
print(monthlyMean)

