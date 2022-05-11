#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 12: Operations Between Files
# Author: Diego Souza (INPE / CGCT / DISSM)
#---------------------------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset                # Read / Write NetCDF4 files
import matplotlib.pyplot as plt            # Plotting library
from datetime import datetime, timedelta   # Library to convert julian day to dd-mm-yyyy
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
#---------------------------------------------------------------------------------------------------------------------------
# Time / Date for download
date1 = '202202' # YYYYMM

# Download the file (product, date, directory)
file1 = download_OCEAN('SST-Monthly-Mean', date1, input)

# Open the file using the NetCDF4 library
file1 = Dataset(f'{input}/{file1}')
#---------------------------------------------------------------------------------------------------------------------------
# Time / Date for download
date2 = '202203' # YYYYMM

# Download the file (product, date, directory)
file2 = download_OCEAN('SST-Monthly-Mean', date2, input) # options: 'SST', 'SST-A' (Anomaly), 'SST-T' (Trend), 'CLO' (Ocean Color), 'SLA' (Sea Level Anomaly), 'ASC-A-a', ASC-A-d, ASC-B-a, ASC-B-d, (ASCAT Winds), 'JAS' (JASON-3)

# Open the file using the NetCDF4 library
file2 = Dataset(f'{input}/{file2}')
#---------------------------------------------------------------------------------------------------------------------------
# Select the extent [min. lon, min. lat, max. lon, max. lat]
extent = [-70.0, -50.00, 25.00, 30.00]  # South America
#extent = [-180.0, -50.00, 180.00, 50.00]  # South America

# Reading lats and lons 
lats = file1.variables['lat'][:]
lons = file1.variables['lon'][:]

# Latitude lower and upper index
latli = np.argmin( np.abs( lats - extent[1] ) )
latui = np.argmin( np.abs( lats - extent[3] ) )
 
# Longitude lower and upper index
lonli = np.argmin( np.abs( lons - extent[0] ) )
lonui = np.argmin( np.abs( lons - extent[2] ) )
 
# Extract the Sea Surface Temperature - Monthly Mean
data1 = file1.variables['sea_surface_temperature'][ 0 , latui:latli , lonli:lonui ]

# Extract the Sea Surface Temperature - Monthly Mean
data2 = file2.variables['sea_surface_temperature'][ 0 , latui:latli , lonli:lonui ]

# Calculate the difference
data = data2 - data1
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(7,6))

# Use the Cilindrical Equidistant projection in cartopy
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Add coastlines, borders and gridlines
ax.coastlines(resolution='50m', color='black', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 10), ylocs=np.arange(-90, 90, 10), draw_labels=True)
gl.top_labels = False
gl.right_labels = False

# Create a custom color scale:
cmap = 'coolwarm'
vmin = -3.0
vmax = 3.0

# Add a background image
ax.stock_img()

# Plot the image
img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='upper', extent=img_extent, cmap=cmap)

# Add a shapefile
shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

# Add a colorbar
plt.colorbar(img, label='SST Difference (°C)', extend='both', orientation='horizontal', pad=0.04, fraction=0.05)

# Getting the file time and date 1
add_seconds = int(file1.variables['time'][0])
date1 = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
date_formatted_1 = date1.strftime('%Y-%m')

# Getting the file time and date 2
add_seconds = int(file2.variables['time'][0])
date2 = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
date_formatted_2 = date2.strftime('%Y-%m')
	
# Add a title
plt.title(f'NOAA Coral Reef Watch Monthly 5 km SST Difference - {date_formatted_1} and {date_formatted_2}', fontweight='bold', fontsize=6, loc='left')
plt.title('Region: ' + str(extent), fontsize=6, loc='right')

# Add a text inside the plot
from matplotlib.offsetbox import AnchoredText
text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 7}, frameon=True)
ax.add_artist(text)
#--------------------------------------------------------------------------------------------------------------------------- 
# Save the image
plt.savefig('Output/image_12.png')

# Show the image
plt.show()  