#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 26: Reading Data from Buoys (PIRATA Project)
# Reference: http://www.goosbrasil.org/pirata/
# Author: Diego Souza (INPE / CGCT / DISSM)
#---------------------------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset                 # Read / Write NetCDF4 files
import matplotlib.pyplot as plt             # Plotting library    
#---------------------------------------------------------------------------------------------------------------------------
# Desired year (four digit)
year = '2022' 
# Desired month (two digit)
month = '01'
# Desired day (two digit)
day = '01' 
#---------------------------------------------------------------------------------------------------------------------------
# Read the buoy data
buoy = Dataset('http://goosbrasil.org:8080/pirata/B20n38w.nc')

# Read the 'time' dataset
time = buoy.variables['time'][:]
#---------------------------------------------------------------------------------------------------------------------------
# Calculate how many days passed since 0001-01-01
from datetime import date
d0 = datetime(1, 1, 1, 0)
d1 = datetime(int(year), int(month), int(day), 12)
delta = d1 - d0
delta_days = delta.total_seconds() / 86400
#---------------------------------------------------------------------------------------------------------------------------
# Get the array index for the desired date
index = np.where(time == delta_days)

# Extract the 1 m temperature, lat and lon for the desired date
temp_day = buoy.variables['temperature'][index[0],0]
lon = buoy.variables['longitude'][index[0]] - 360
lat = buoy.variables['latitude'][index[0]]
#---------------------------------------------------------------------------------------------------------------------------
# Print the result
print(f'The 1 m temperature for {year}-{month}-{day} at Lat:{str(lat[0].round(2))} and Lon:{str(lon[0].round(2))} is:')
print(temp_day[0], "°C")