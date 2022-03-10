#########################################################################
#   File:   pr1_DataPreperation.py
#   Name:   John Smutny
#   Course: ECE-5984: Applications of Machine Learning
#   Date:   03/05/2022
#   Description:
#       For Project1; perform initial data preparation to get NOAA provided
#       data into a usable state to model.
#
#   Readme:
#   https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_station/readme-by_station.txt
#
#   Next Steps:
#   1) Make 'quickDQR()' fct. Replace in here.
#   2) Only extract CORE5 data headers in original dataframe.
#   3) (offline) Make data edit suggestions for next meeting.
#
#   Can:
#       Read in a csv, create an initial dataframe of data with headers.
#       Identify every unique Day and process some ELEMENT possibilities into
#           a single list. Then place that list into a resulting dataframe.
#       Publish a DataQualityReport for a day's summary of data.
#
#   Cannot:
#       'DataQualityReport.py' lib file cannot handle string entries.
#       Publish a DataQualityReport for initial data.
#       End Goal headers do not contain units.
#       Process all possible ELEMENT values for an unique Day's events
##########################################################################

import pandas
import numpy as np
from vt_ApplicationsOfML.Libraries.DataExploration.DataQualityReport import \
    DataQualityReport

#####################################
# Initial loading of header-less data and adding a header
#   Date = yyyymmdd
#   OBS-Time = hhmm
FILENAME = 'C:/Data/USW00013880-Test.csv'
INIT_HEADER = ['ID', 'Date', 'Element', 'Value', 'MeasurementFlag',
               'QualityFlag', 'SourceFlag', 'OBS-Time']
df = pandas.read_csv(FILENAME, header=None)
df.columns = INIT_HEADER
print(df[1:5])

#####################################
# Establish user settings for the program, dataframe headers, etc
MODEL_VERSION = 1

BASE_COLUMNS = ['Date']
CORE5_FEATURES = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN']
ELEMENT_TYPES = df.Element.unique()
TARGET_VARIABLES = ['PRECIPFLAG', 'PRECIPAMT', 'NEXTDAYPRECIPFLAG',
                    'NEXTDAYPRECIPAMT']

CORE5_HEADER = BASE_COLUMNS + CORE5_FEATURES + TARGET_VARIABLES
DETAILED_HEADER = BASE_COLUMNS + ELEMENT_TYPES.tolist() + TARGET_VARIABLES


##########################################################################
# TODO - Add logic to remove/change data points from the starting dataset.
# Based on desired quality, remove/change certain data points.
# Actions List:
# 1) ...
# 2) ...

##########################################################################
# TODO - Do work necessary to print a Data Quality Report before cleaning.
# Create an organized data set summary for the console using a data frame.
report1 = DataQualityReport()

#print(type(df.ID.loc[0]))
#print(type(df.MeasurementFlag.loc[0]))
#print(type(df.QualityFlag.loc[0]))

for thisLabel in INIT_HEADER:  # for each column, report basic stats
    if thisLabel == 'MeasurementFlag' \
            or thisLabel == 'QualityFlag':
        print('WARN: DataQualityReport.py cannot process label = ' + thisLabel)
        # TODO - 'DataQualityReport.py' cannot process [0] index 'nan' values.
        #  Clean data before this step? (fill in nan, replace categorical chars)
        continue
    else:
        thisCol = df[thisLabel]
        report1.addCol(thisLabel, thisCol)

print("DataQualityReport - 1/2")
print(report1.to_string())


##########################################################################
# Create a new dataframe that will have one column per ELEMENT designation.
#   Every entry into the new dataframe is a day and columns of every event
#   that day.

# 1) Create final Dataframe header, define features and target variables.
if MODEL_VERSION == 1:
    NEW_HEADER = CORE5_HEADER
else:
    NEW_HEADER = DETAILED_HEADER

# print("New Headers:")
# print(NEW_HEADER)

# 2) Isolate a single day's total events into a dictionary.
daysMeasured = df.Date.unique()

# TODO - When ready, create another loop to loop over all unique days below.
oneDayEvents = df.loc[df['Date'] == daysMeasured[0]]
print("Example isoDaysEvents:")
print(oneDayEvents)

# 3) Summarize the day's events into a single entry
#       Create a blank entry.
keys = NEW_HEADER
blankValues = [0] * len(NEW_HEADER)
entry = dict(zip(keys, blankValues))
# print("Blank Entry pre-processing")
# print(entry)

# 4) Loop through each datapoint on a particular day. Find what part of the
#       dictionary the datapoint's ELEMENT corresponds too. Do math based on
#       that ELEMENT value.
numEntries = len(oneDayEvents.index)
for i in range(numEntries):
    entryList = oneDayEvents.loc[i, :].values.tolist()
    # TODO - ^^^ Maybe make 'entryList' a map of the keys equal to initial
    #  'header' to simply value accessing and placement?
    # print(i)
    # print(entryList)
    entry['Date'] = entryList[1]
    element = entryList[2]

    # SWITCH statement to process the ELEMENT + VALUE
    if element == 'TMAX':
        entry[element] = entryList[3]
        # print('TempMax was ' + str(entryList[3]))
    elif element == 'PRCP':
        entry[element] = entryList[3]
        # print('Precipitation was ' + str(entryList[3]))
    elif element == 'SNOW':
        entry[element] = entryList[3]
        # print('Snow fall was ' + str(entryList[3]))
    elif element == 'TMIN':
        entry[element] = entryList[3]
        # print('TempMin was ' + str(entryList[3]))
    elif element == 'SNWD':
        entry[element] = entryList[3]
        # print('Snow depth was ' + str(entryList[3]))
    # TODO - Add more 'elif' statements for the rest of the ELEMENT/VALUE pairs.
    else:
        print('Found element ' + str(entryList[2]))

print('Resulting Single Day Entry')
df_entry = pandas.DataFrame([entry])
print(df_entry)

# 5) Add a new TOTAL DAY entry of weather events in a data frame.
df_dataSummary = pandas.DataFrame(columns=NEW_HEADER)
df_dataSummary = pandas.concat([df_dataSummary, df_entry], ignore_index=True)
print('Resulting Dataframe with ONLY single day summaries.')
print(df_dataSummary)

############################################
# Publish a new DataQualityReport on the list of single day data entries.
report2 = DataQualityReport()

for thisLabel in NEW_HEADER:  # for each column, report basic stats
    thisCol = df_dataSummary[thisLabel]
    report2.addCol(thisLabel, thisCol)

# print("DataQualityReport - 2/2")
# print(report2.to_string())
