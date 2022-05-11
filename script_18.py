#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 18: Coral Bleaching Heat Stress Degree Heating Week
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

# Time / Date for download
date = '20190401' # YYYYMMDD

# Download the file (product, date, directory)
file = download_OCEAN('DHW', date, input)
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file = Dataset(f'{input}/{file}')
#---------------------------------------------------------------------------------------------------------------------------
# Select the extent [min. lon, min. lat, max. lon, max. lat]
extent = [-93.0, -60.00, -25.00, 18.00] # South America
       
# Reading lats and lons 
lats = file.variables['lat'][:]
lons = file.variables['lon'][:]
 
# Latitude lower and upper index
latli = np.argmin( np.abs( lats - extent[1] ) )
latui = np.argmin( np.abs( lats - extent[3] ) )
 
# Longitude lower and upper index
lonli = np.argmin( np.abs( lons - extent[0] ) )
lonui = np.argmin( np.abs( lons - extent[2] ) )
 
# Extract the Degree Heating Week
data = file.variables['degree_heating_week'][ 0 , latui:latli , lonli:lonui ]

# NaN if smaller than 0
data[data <= 0] = np.nan
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(9,9))

# Use the Cilindrical Equidistant projection in cartopy
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Add coastlines, borders and gridlines
ax.coastlines(resolution='10m', color='black', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 10), ylocs=np.arange(-90, 90, 10), draw_labels=True)
gl.top_labels = False
gl.right_labels = False

# Create a custom color scale:
colors = ["#463278", "#645096", "#826eb4", "#a08cd2", "#ffff00","#ffdc00", "#ffb900", "#ff9600", "#ff0000", "#d20000",
          "#a00000", "#6e0000", "#e67d46", "#b45a28", "#7d3c1e","#552d14", "#f000f0", "#c800c8", "#a000a0", "#780078"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#320032')
vmin = 0
vmax = 20

# Add a land mask
ax.add_feature(cfeature.LAND)
# Add an ocean mask
ax.add_feature(cfeature.OCEAN, facecolor='#c8fafa')

# Plot the image
img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='upper', extent=img_extent, cmap=cmap)

# Add a shapefile
shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

# Define the ticks to be shown
ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Add a colorbar
cbar = plt.colorbar(img, label='Coral Bleaching Heat Stress Degree Heating Week (°C-Weeks)', extend='max', orientation='horizontal', pad=0.05, fraction=0.04, ticks=ticks)

# Getting the file time and date
add_seconds = int(file.variables['time'][0])
date = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
date_formatted = date.strftime('%Y-%m-%d')

# Add a title
plt.title(f'NOAA Coral Reef Watch Daily 5km Bleaching HotSpot Coral Bleaching Heat Stress Degree Heating Week - {date_formatted}', fontweight='bold', fontsize=4, loc='left')
plt.title('Region: ' + str(extent), fontsize=4, loc='right')

# Add a text inside the plot
from matplotlib.offsetbox import AnchoredText
text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 7}, frameon=True)
ax.add_artist(text)
#--------------------------------------------------------------------------------------------------------------------------- 
# Save the image
plt.savefig('Output/image_18.png')

# Show the image
plt.show()