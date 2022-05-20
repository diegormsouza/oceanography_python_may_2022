#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 13: Time Series
# Author: Diego Souza (INPE / CGCT / DISSM)
#---------------------------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset                # Read / Write NetCDF4 files
import matplotlib.pyplot as plt            # Plotting library
from datetime import datetime, timedelta   # Basic date and time types
import cartopy, cartopy.crs as ccrs        # Plot maps
import cartopy.feature as cfeature         # Common drawing and filtering operations
import cartopy.io.shapereader as shpreader # Import shapefiles
import numpy as np                         # Import the Numpy package
import matplotlib.colors                   # Matplotlib colors  
from datetime import datetime, timedelta   # Basic Dates and time types
import os                                  # Miscellaneous operating system interfaces
import time as t                           # Time access and conversion                                          
from ftplib import FTP                     # FTP protocol client
from utilities_ocean import download_OCEAN # Our function for download
#---------------------------------------------------------------------------------------------------------------------------
# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Time / Date for download
year = '2021'    # Year
month_ini = 1    # Starting month
month_end = 3    # End month
month_int = 1    # Interval

# Create the lists that will store our data
data_min = []; data_mean = []; data_max = []; dates = []

# For each month between start and end, increase one month
for month in range(month_ini, month_end + 1, month_int):

  # Time / Date for download
  month = str(month).zfill(2)    # Convert month to two digit
  date = year + month # YYYYMM   # Data is year (four digit) + month (two digit)

  # MIN SST - MONTHLY
  #---------------------------------------------------------------------------------------------------------------------------
  # Download the file (product, date, directory)
  file = download_OCEAN('SST-Monthly-Min', date, input) 
  
  # Open the file using the NetCDF4 library
  file = Dataset(f'{input}/{file}')

  # Reading lats and lons 
  lats = file.variables['lat'][:]
  lons = file.variables['lon'][:]
  
  # Reading the data from a coordinate
  lat_point = -30
  lon_point = -30
  lat_idx = np.argmin(np.abs(lats - lat_point))
  lon_idx = np.argmin(np.abs(lons - lon_point))
  data_point = file.variables['sea_surface_temperature'][ 0 , lat_idx , lon_idx ].round(2)
   
  # Add the data to the list
  data_min.append(data_point)

  # MEAN SST - MONTHLY
  #---------------------------------------------------------------------------------------------------------------------------
  # Download the file (product, date, directory)
  file = download_OCEAN('SST-Monthly-Mean', date, input) # options: 'SST', 'SST-A' (Anomaly), 'SST-T' (Trend), 'CLO' (Ocean Color), 'SLA' (Sea Level Anomaly), 'ASC-A-a', ASC-A-d, ASC-B-a, ASC-B-d, (ASCAT Winds), 'JAS' (JASON-3)
  
  # Open the file using the NetCDF4 library
  file = Dataset(f'{input}/{file}')

  # Reading lats and lons 
  lats = file.variables['lat'][:]
  lons = file.variables['lon'][:]
  
  # Reading the data from a coordinate
  lat_point = -30
  lon_point = -30
  lat_idx = np.argmin(np.abs(lats - lat_point))
  lon_idx = np.argmin(np.abs(lons - lon_point))
  data_point = file.variables['sea_surface_temperature'][ 0 , lat_idx , lon_idx ].round(2)

  # Add the data to the list
  data_mean.append(data_point)

  # MAX SST - MONTHLY
  #---------------------------------------------------------------------------------------------------------------------------
  # Download the file (product, date, directory)
  file = download_OCEAN('SST-Monthly-Max', date, input) # options: 'SST', 'SST-A' (Anomaly), 'SST-T' (Trend), 'CLO' (Ocean Color), 'SLA' (Sea Level Anomaly), 'ASC-A-a', ASC-A-d, ASC-B-a, ASC-B-d, (ASCAT Winds), 'JAS' (JASON-3)
  
  # Open the file using the NetCDF4 library
  file = Dataset(f'{input}/{file}')

  # Reading lats and lons 
  lats = file.variables['lat'][:]
  lons = file.variables['lon'][:]
  
  # Reading the data from a coordinate
  lat_point = -30
  lon_point = -30
  lat_idx = np.argmin(np.abs(lats - lat_point))
  lon_idx = np.argmin(np.abs(lons - lon_point))
  data_point = file.variables['sea_surface_temperature'][ 0 , lat_idx , lon_idx ].round(2)

  # Add the data to the list
  data_max.append(data_point)
  #---------------------------------------------------------------------------------------------------------------------------
  # Getting the file time and date 
  add_seconds = int(file.variables['time'][0])
  date = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
  date_formatted = date.strftime('%Y-%m')
  
  # Add the date to the list
  dates.append(date_formatted)
  #---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig, ax = plt.subplots(figsize=(16, 8))

# Plot title
plt.title(f'Temperatura da Superfície do Mar - Lat.: {lat_point}° - Lon.: {lon_point}°',  fontsize=12, fontweight='bold')

# X axis
x = dates
plt.xlabel("Datas", fontsize=12, fontweight='bold')
plt.xticks(rotation=90)

# Y axis
plt.ylabel("TSM Mensal (°C)", fontsize=12, fontweight='bold')
y_min = data_min
y_mean = data_mean
y_max = data_max

# Create the line plot
plt.plot(x,y_min, '-bo', label='TSM - Mínima Mensal')
plt.plot(x,y_mean, '-yo', label='TSM - Média Mensal')
plt.plot(x,y_max, '-ro', label='TSM - Máximo Mensal')

# Add a legend
plt.legend()

# Add grids
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')
#---------------------------------------------------------------------------------------------------------------------------
# Save the figure
plt.savefig('Output/image_13.png', bbox_inches='tight', pad_inches=0, dpi=300)

# Show the plot
plt.show()  