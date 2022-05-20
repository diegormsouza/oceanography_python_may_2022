#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 17: Coral Bleaching Heat Stress HotSpot
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
date = '20190401' # YYYYMMDD

# Download the file (product, date, directory)
file = download_OCEAN('BHS', date, input)
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
 
# Extract the Hotspot
data = file.variables['hotspot'][ 0 , latui:latli , lonli:lonui ]

# NaN if smaller than 0
data[data < 0] = np.nan
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
colors = ["#6e50ff", "#7355ff", "#785aff", "#7d5fff", "#8264ff","#9678ff", "#9b7dff", "#a082ff", "#a587ff", "#aa8cff",
          "#edff00", "#eff700", "#f1ef00", "#f3e700", "#f5df00","#f7c500", "#f9bd00", "#fbb500", "#fdad00", "#ffa500",
          "#ff8700", "#fd8200", "#fb7d00", "#f97800", "#f77300","#f55f00", "#f35a00", "#f15500", "#ef5000", "#ed4b00",
          "#ff3200", "#fa2d00", "#f52800", "#f02300", "#eb1e00","#dc1400", "#d70f00", "#d20a00", "#cd0500", "#c80000",
          "#aa2400", "#a52000", "#a01c00", "#9b1800", "#961400","#821000", "#7d0c00", "#7d0c00", "#780800", "#6e0000",]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#6e0000')
vmin = 0
vmax = 5

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
ticks = [0, 1, 2, 3, 4, 5]

# Add a colorbar
cbar = plt.colorbar(img, label='Coral Bleaching Heat Stress HotSpot (°C)', extend='max', orientation='horizontal', pad=0.05, fraction=0.04, ticks=ticks)

# Getting the file time and date
add_seconds = int(file.variables['time'][0])
date = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
date_formatted = date.strftime('%Y-%m-%d')

# Add a title
plt.title(f'NOAA Coral Reef Watch Daily 5km Bleaching HotSpot - {date_formatted}', fontweight='bold', fontsize=7, loc='left')
plt.title('Region: ' + str(extent), fontsize=7, loc='right')

# Add a text inside the plot
from matplotlib.offsetbox import AnchoredText
text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 7}, frameon=True)
ax.add_artist(text)
#--------------------------------------------------------------------------------------------------------------------------- 
# Save the image
plt.savefig('Output/image_17.png')

# Show the image
plt.show()