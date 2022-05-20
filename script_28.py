#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 28: Comparing Satellite and Buoys (Function)
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
import pandas as pd                        # Read and manipulate a CSV file               
#---------------------------------------------------------------------------------------------------------------------------

def plot_PIRATA(buoy_name, lat_nominal, lon_nominal, year, month, day):
  # Reading the data from a buoy
  # Desired year (four digit)
  year = year
  # Desired month (two digit)
  month = month
  # Desired day (two digit)
  day = day

  #---------------------------------------------------------------------------------------------------------------------------

  # Read the buoy data
  buoy = Dataset('http://goosbrasil.org:8080/pirata/' + buoy_name + '.nc')

  # Read the 'time' dataset
  time = buoy.variables['time'][:]
  #---------------------------------------------------------------------------------------------------------------------------
  # Calculate how many days passed since 0001-01-01
  from datetime import date
  d0 = date(1, 1, 1)
  d1 = date(int(year), int(month), int(day))
  delta = d1 - d0
  delta_days = delta.days + 0.5
  #---------------------------------------------------------------------------------------------------------------------------
  # Get the array index for the desired date
  index = np.where(time == delta_days)

  lon_buoy  = buoy.variables['longitude'][index[0]] - 360
  lat_buoy  = buoy.variables['latitude'][index[0]]

  # Extract the 1 m temperature, lat and lon for the desired date
  try:
    temp_buoy = buoy.variables['temperature'][index[0],0][0].round(2)
    
    if (temp_buoy == -9999 or temp_buoy == -99999):
      print("Bóia " + buoy_name + " com dados inválidos para esta data.")
      return
  except:
    print("Bóia " + buoy_name + " sem dados para esta data.")
    return
  #---------------------------------------------------------------------------------------------------------------------------
  # Reading the data from a coordinate (satellite)
  lat_point = lat_buoy[0]
  lon_point = lon_buoy[0]

  lat_idx = np.argmin(np.abs(lats - lat_point))
  lon_idx = np.argmin(np.abs(lons - lon_point))

  temp_sat = file.variables['analysed_sst'][ 0 , lat_idx , lon_idx ].round(2)
  delta = temp_sat - temp_buoy

  # Append the parameters to the lists
  lats_list.append(lat_point)
  lons_list.append(lon_point)
  sate_list.append(temp_sat)
  buoy_list.append(temp_buoy)
  #---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
# Input and output directories
input = "/content/Samples"; os.makedirs(input, exist_ok=True)
output = "/content/Output"; os.makedirs(output, exist_ok=True)

# Time / Date for download
date = '20220409' # YYYYMMDD
#---------------------------------------------------------------------------------------------------------------------------
# Download the file (product, date, directory)
file = download_OCEAN('SST', date, input)

# Open the file using the NetCDF4 library
file = Dataset(f'{input}/{file}')
#---------------------------------------------------------------------------------------------------------------------------
# Reading lats and lons 
lats = file.variables['lat'][:]
lons = file.variables['lon'][:]
#---------------------------------------------------------------------------------------------------------------------------
# Get the year, month and day
year = date[0:4]
month = date[4:6]
day = date[6:8]

# Create the lists
lats_list = []; lons_list = []; buoy_list = []; sate_list = []

# Call the function to read the buoys and compare with the satellite data
plot_PIRATA('B20n38w',  0, -38, year, month, day)
plot_PIRATA('B15n38w', 15, -38, year, month, day)
plot_PIRATA('B12n38w', 12, -38, year, month, day)
plot_PIRATA('B8n38w',   8, -38, year, month, day)
plot_PIRATA('B4n38w',   4, -38, year, month, day)
plot_PIRATA('B0n35w',   0, -35, year, month, day)
plot_PIRATA('B8s30w',  -8, -30, year, month, day)
plot_PIRATA('B19s34w',-19, -34, year, month, day)
plot_PIRATA('B21n23w', 21, -23, year, month, day)
plot_PIRATA('B12n23w', 12, -23, year, month, day)
plot_PIRATA('B4n23w',   4, -23, year, month, day)
plot_PIRATA('B0n23w',   0, -23, year, month, day)
plot_PIRATA('B2n10w',   2, -10, year, month, day)
plot_PIRATA('B2s10w',  -2, -10, year, month, day)
plot_PIRATA('B5s10w',  -5, -10, year, month, day)
plot_PIRATA('B6s10w',  -6, -10, year, month, day)
plot_PIRATA('B10s10w',-10, -10, year, month, day)
plot_PIRATA('B0n0e',    0,   0, year, month, day)
#---------------------------------------------------------------------------------------------------------------------------
# Create a table with Pandas
tab_tsm = pd.DataFrame(columns=["LON","LAT","BÓIA","SATÉLITE"])

# Fill the table with the values
for idx in range(len(buoy_list)):
  tab_tsm.loc[idx,"LON"] = lons_list[idx]
  tab_tsm.loc[idx,"LAT"] = lats_list[idx]
  tab_tsm.loc[idx,"BÓIA"] = buoy_list[idx]
  tab_tsm.loc[idx,"SATÉLITE"] = sate_list[idx]
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig, ax = plt.subplots(figsize=(16, 8))

# Plot title
plt.title('Comparação: Bóias x Satélite', fontsize=12, fontweight='bold')

# Create the scatter plot
ax.scatter(x = tab_tsm['BÓIA'], y = tab_tsm['SATÉLITE'])

# X axis limits (°C) and label
plt.xlim(20, 30)
plt.xlabel("Bóias (°C)",  fontsize=12, fontweight='bold')

# Y axis limits (°C) and label
plt.ylim(20, 30)
plt.ylabel("Satélite (°C)",  fontsize=12, fontweight='bold')

# Create the reference line
ax.plot([20, 30], [20, 30], ls="--", c="r")

# Add grids
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')
#---------------------------------------------------------------------------------------------------------------------------
# Calculate the R²
from sklearn.metrics import r2_score
r_score = r2_score(buoy_list, sate_list).round(3)

# Calculate the RMSE
from sklearn.metrics import mean_squared_error
mean_squared_error = mean_squared_error(buoy_list, sate_list).round(3)

# Calculate the Bias
array1 = np.array(buoy_list)
array2 = np.array(sate_list)
bias = np.mean(np.subtract(array1, array2)).round(3)

# Add an anotation with R², RMSE and Bias 
plt.annotate(f'R² = {r_score}\nRMSE = {mean_squared_error} °C\nBIAS = {bias} °C', xy=(0.01, 0.88), xycoords = ax.transAxes, fontsize=14, fontweight='bold', color='gold', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0, 0.5), ec=(1., 1., 1.)), alpha = 1.0)
#---------------------------------------------------------------------------------------------------------------------------
# Save the figure
plt.savefig(f'{output}/Image_28.png', bbox_inches='tight', pad_inches=0, dpi=300)

# Show the plot
plt.show()