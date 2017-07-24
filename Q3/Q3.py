import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from geopy.geocoders import Nominatim

#------------------Data Pre-Processing-------------------------

building_permit_raw = pd.read_csv('Building_Permits___Current.csv')
building_permit = building_permit_raw[['Application/Permit Number','Permit Type','Status','Category','Expiration Date','Location']]

#select building that are under construction and have permit issued or finaled
building_permit = building_permit[building_permit['Permit Type'] == 'Construction']
bp_finaled = building_permit[building_permit['Status'] == 'Permit Finaled']
bp_issued = building_permit[building_permit['Status'] == 'Permit Issued']
bp = pd.concat([bp_finaled,bp_issued])

#check NaN in dataframe
num_nan = bp.isnull().sum().sum()
#The number of NaN in dataframe is 44, which is smaller than 0.5% in the dataframe
#So we can directly delete the row containing NaN
bp.dropna(inplace = True)
bp.reset_index(drop=True,inplace = True)
bp.head(10)

# Generate zip code from latitude, longitude and address
start = time.time()

zipcode_list = []
year_list = []
month_list = []
for i in range(len(bp)):
    if '(' in bp['Location'][i]:
        lat_lon = bp['Location'][i].split('(')[-1].split(')')[0]
        geolocator = Nominatim(timeout=10)
        location = geolocator.reverse(lat_lon)
        zipcode = location.address.split(',')[-2].split()[0]
        zipcode_list.append(zipcode)
    else:
        address = bp['Location'][i].split('(')[-1].split(')')[0]
        geolocator = Nominatim(timeout=10)
        location = geolocator.geocode(address)
        zipcode = location.address.split(',')[-2].split()[0]
        zipcode_list.append(zipcode)

    year = bp['Expiration Date'][i].split('/')[-1]
    month = bp['Expiration Date'][i].split('/')[0]
    year_list.append(year)
    month_list.append(month)

bp['Zipcode'] = zipcode_list
bp['Expected Construct Year'] = year_list
bp['Expected Construct Month'] = month_list

bp.to_csv('bp.csv', index=False)

end = time.time()
run_time = end - start

print(run_time)


#-----------------------------Time Analysis------------------------------


# 2017
bp_2017 = bp[bp['Expected Construct Year'] == 2017].reset_index(drop=True)

construction_num_2017 = pd.DataFrame()
month_list = ['Jan.2017', 'Feb.2017', 'Mar.2017', 'Apr.2017', 'May.2017', 'Jun.2017', 'Jul.2017',
              'Aug.2017', 'Sep.2017', 'Oct.2017', 'Nov.2017', 'Dec.2017']
construction_num_2017['Month'] = month_list
category = ['MULTIFAMILY', 'SINGLE FAMILY / DUPLEX', 'COMMERCIAL', 'INSTITUTIONAL', 'INDUSTRIAL']

Total_Jan = 0
Total_Feb = 0
Total_Mar = 0
Total_Apr = 0
Total_May = 0
Total_Jun = 0
Total_Jul = 0
Total_Aug = 0
Total_Sep = 0
Total_Oct = 0
Total_Nov = 0
Total_Dec = 0

for i in category:
    bp_cat_2017 = bp_2017[bp_2017['Category'] == i]

    Jan = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 1])
    Feb = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 2])
    Mar = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 3])
    Apr = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 4])
    May = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 5])
    Jun = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 6])
    Jul = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 7])
    Aug = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 8])
    Sep = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 9])
    Oct = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 10])
    Nov = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 11])
    Dec = len(bp_cat_2017[bp_cat_2017['Expected Construct Month'] == 12])
    Total_Jan += Jan
    Total_Feb += Feb
    Total_Mar += Mar
    Total_Apr += Apr
    Total_May += May
    Total_Jun += Jun
    Total_Jul += Jul
    Total_Aug += Aug
    Total_Sep += Sep
    Total_Oct += Oct
    Total_Nov += Nov
    Total_Dec += Dec

    construction_num_2017['%s' % i] = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

construction_num_2017['TOTAL'] = [Total_Jan, Total_Feb, Total_Mar, Total_Apr, Total_May, Total_Jun,
                                  Total_Jul, Total_Aug, Total_Sep, Total_Oct, Total_Nov, Total_Dec]

# 2018
bp_2018 = bp[bp['Expected Construct Year'] == 2018].reset_index(drop=True)

construction_num_2018 = pd.DataFrame()
month_list = ['Jan.2018', 'Feb.2018', 'Mar.2018', 'Apr.2018', 'May.2018', 'Jun.2018', 'Jul.2018',
              'Aug.2018', 'Sep.2018', 'Oct.2018', 'Nov.2018', 'Dec.2018']
construction_num_2018['Month'] = month_list
category = ['MULTIFAMILY', 'SINGLE FAMILY / DUPLEX', 'COMMERCIAL', 'INSTITUTIONAL', 'INDUSTRIAL']

Total_Jan = 0
Total_Feb = 0
Total_Mar = 0
Total_Apr = 0
Total_May = 0
Total_Jun = 0
Total_Jul = 0
Total_Aug = 0
Total_Sep = 0
Total_Oct = 0
Total_Nov = 0
Total_Dec = 0

for i in category:
    bp_cat_2018 = bp_2018[bp_2018['Category'] == i]

    Jan = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 1])
    Feb = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 2])
    Mar = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 3])
    Apr = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 4])
    May = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 5])
    Jun = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 6])
    Jul = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 7])
    Aug = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 8])
    Sep = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 9])
    Oct = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 10])
    Nov = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 11])
    Dec = len(bp_cat_2018[bp_cat_2018['Expected Construct Month'] == 12])
    Total_Jan += Jan
    Total_Feb += Feb
    Total_Mar += Mar
    Total_Apr += Apr
    Total_May += May
    Total_Jun += Jun
    Total_Jul += Jul
    Total_Aug += Aug
    Total_Sep += Sep
    Total_Oct += Oct
    Total_Nov += Nov
    Total_Dec += Dec

    construction_num_2018['%s' % i] = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

construction_num_2018['TOTAL'] = [Total_Jan, Total_Feb, Total_Mar, Total_Apr, Total_May, Total_Jun,
                                  Total_Jul, Total_Aug, Total_Sep, Total_Oct, Total_Nov, Total_Dec]

construction_num = pd.concat([construction_num_2017,construction_num_2018]).reset_index(drop = True)

x = range(len(construction_num))
plt.style.use('ggplot')
plt.figure(figsize=(15,10))

plt.plot(x,construction_num['TOTAL'],label = 'TOTAL')
plt.plot(x,construction_num['MULTIFAMILY'],label = 'MULTIFAMILY')
plt.plot(x,construction_num['SINGLE FAMILY / DUPLEX'],label = 'SINGLE FAMILY / DUPLEX')
plt.plot(x,construction_num['COMMERCIAL'],label = 'COMMERCIAL')
plt.plot(x,construction_num['INSTITUTIONAL'],label = 'INSTITUTIONAL')
plt.plot(x,construction_num['INDUSTRIAL'],label = 'INDUSTRIAL')

plt.title("Numbers of Constructed building permit trend")
plt.xlabel("Time")
plt.ylabel("Number of Building Permits")
plt.xticks(x,[i for i in construction_num['Month']],rotation=45)

plt.legend(loc=2, prop={'size': 10})
plt.grid(True)
plt.savefig('time_trend.png' , dpi=400)
plt.show()

#-----------------------------------Regional Analysis---------------------------------------

#get zipcode list and corresponding counts
zipcode_list = []
for i in range(len(bp)):
    zipcode = bp['Zipcode'][i]
    if zipcode not in zipcode_list:
        zipcode_list.append(zipcode)
zipcode_list.remove('98109-5210')
zipcode_counts = pd.DataFrame()
zipcode_counts['Zipcode'] = zipcode_list
counts_list = []
for i in zipcode_list:
    counts = len(bp[bp['Zipcode'] == i])
    counts_list.append(counts)
zipcode_counts['TOTAL'] = counts_list

category = ['MULTIFAMILY','SINGLE FAMILY / DUPLEX','COMMERCIAL','INSTITUTIONAL','INDUSTRIAL']

for i in category:
    bp_cat = bp[bp['Category'] == i]
    cat_counts_list = []
    for j in zipcode_list:
        cat_counts = len(bp_cat[bp_cat['Zipcode'] == j])
        cat_counts_list.append(cat_counts)
    zipcode_counts['%s' % i] = cat_counts_list


zipcode_counts['Zipcode'] = zipcode_counts['Zipcode'].astype(int)

zipcode_counts.to_csv('Zipcode_counts.csv',index=False)