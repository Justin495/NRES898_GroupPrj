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
        concatURL = concatUrl(sites, startDate, endDate)
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

def concatUrl(sites, startDate, endDate):
    concatURL = f'http://data.rcc-acis.org/StnData?sid={sites}&sdate={startDate}&edate={endDate}&elems=1,2,4&output=csv'
    return concatURL

print(f'1. Daily climate data for stations {" & ".join(str(x) for x in siteList)} between {startDate} and {endDate}:')
print(weatherdf(siteList,startDate,endDate))

df = weatherdf(siteList,startDate,endDate)

pentadMean = df.groupby(['site']).resample('5D').mean()
print(f'2.  Pentad mean climate data for stations {" & ".join(str(x) for x in siteList)} between {startDate} and {endDate}:')
print(pentadMean)


############################################################################################
######### part 3 - monthly mean climate data for a given county for a given period #########
############################################################################################

# County FIPS Codes: https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697
#countyNumber = 31109  # Lancaster County
countyNumber = 31041   # Custer County

# import list of weather stations in Lancaster county
columnNames=['station_id','name','state','longitude','latitude','elevation']
countySites = pd.read_csv(f'http://data.rcc-acis.org/StnMeta?county={countyNumber}&output=csv',sep=",",names = columnNames)

countySites.head(20)
countySites.info()

#myCountySites = countySites['station_id'].tolist() #get list of county sites
appendedCounty_df = []

siteList = []

for index, row in countySites.iterrows():
# for coSite in myCountySites:        #code
    concatURL = concatUrl(row.station_id,startDate,endDate)
    try:
        newCountyData = pd.read_csv(concatURL,sep=',',skiprows=1,header=None)
        newCountyData['countySite'] = row.station_id     # add column to identifiy the site for this data
        appendedCounty_df.append(newCountyData) # list of separate data frames, one for each site    
        siteList.append(row.station_id) 
    except:
        continue

county_df = pd.concat(appendedCounty_df)     # combine list of separate data frames into a single dataframe

county_df.columns = ['date','maxTemp','minTemp','precip','countySite']

county_df.info()


# convert weather data to numeric and date to datetime
# also handle errors as some data may be reported as 
# "missing data values are returned as 'M' and trace values of
# precipitation, snowfall or snow depth are returned as 'T'"
county_df.minTemp = pd.to_numeric(county_df.minTemp, errors='coerce')
county_df.maxTemp = pd.to_numeric(county_df.maxTemp, errors='coerce')
county_df.precip = pd.to_numeric(county_df.precip, errors='coerce')
county_df.date = pd.to_datetime(county_df.date)

county_df.set_index('date',inplace=True)

county_df.info()

monthlyCountyMean = county_df.groupby(['countySite']).resample('M').mean()
countyMean = county_df.mean()
nl='\n'
print(F'3.  Monthly mean climate data for Sites:{nl}{" & ".join(str(x) for x in siteList)}{nl}between {startDate} and {endDate}:')
print(monthlyCountyMean)
print(countyMean)

