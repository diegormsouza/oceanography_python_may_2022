#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 23: Surface Winds (Vectors)
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
date = '20220409' # YYYYMMDD

# Download the file (product, date, directory)
file = download_OCEAN('ASC-B-a-nc', date, input)
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file = Dataset(f'{input}/{file}')
#---------------------------------------------------------------------------------------------------------------------------
# Select the extent [min. lon, min. lat, max. lon, max. lat]
#extent = [-93.0, -60.00, -25.00, 18.00] # South America
extent = [-70.0, -60.00, -30.00, -10.00] # Brazilian Southeast

# Reading lats and lons 
lats = file.variables['rows'][:]
lons = file.variables['cols'][:]
 
# Latitude lower and upper index
latli = np.argmin( np.abs( lats - extent[1] ) )
latui = np.argmin( np.abs( lats - extent[3] ) )
 
# Longitude lower and upper index
lonli = np.argmin( np.abs( lons - extent[0] ) )
lonui = np.argmin( np.abs( lons - extent[2] ) )

# Extract the lats and lons again
lats = file.variables['rows'][ latui:latli ]
lons = file.variables['cols'][ lonli:lonui ]

# Extract the U Wind
u_wind = file.variables['u_wind'][ 0 , 0 , latui:latli , lonli:lonui ]

# Extract the U Wind
v_wind = file.variables['v_wind'][ 0 , 0 , latui:latli , lonli:lonui ]

# Extract the wind speed
wspeed = file.variables['windspeed'][ 0 , 0 , latui:latli , lonli:lonui ]
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(7,8))

# Use the Cilindrical Equidistant projection in cartopy
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]
ax.set_extent([extent[0], extent[2], extent[1], extent[3]], ccrs.PlateCarree())

# Add coastlines, borders and gridlines
ax.coastlines(resolution='10m', color='black', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
gl.top_labels = False
gl.right_labels = False

# Create a custom color palette 
colors = ["#747474", "#00befe", "#0048ff", "#00c300", "#fedb12",
          "#f25505", "#ff1526", "#87422a", "#d100e1", "#7f00ad"]
cmap = matplotlib.colors.ListedColormap(colors)

# Add a land mask
ax.add_feature(cfeature.LAND)
# Add an ocean mask
ax.add_feature(cfeature.OCEAN, facecolor='black')

# Plot the image
bounds = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
img = ax.quiver(lons[::2], lats[::2], u_wind[::2,::2], v_wind[::2,::2], wspeed[::2,::2], cmap=cmap, norm=norm, scale = 450, width = 0.0025) 

# Plot the legend
qk = ax.quiverkey(img, 0.58, 0.895, 20, '20 kt', labelpos='E', coordinates='figure', fontproperties={'size': '7'})

# Add a shapefile
shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

# Add a colorbar
plt.colorbar(img, label='Wind Speed (kt)', extend='neither', orientation='vertical', norm=norm, boundaries=bounds, ticks=bounds, pad=0.02, fraction=0.05)

# Getting the file time and date
add_seconds = int(file.variables['time'][0])
date = datetime(1970,1,1,1) + timedelta(seconds=add_seconds)
date_formatted = date.strftime('%Y-%m-%d')

# Read the satellite
satellite = getattr(file, 'platform')[-1]
if (satellite == '1'):
  satellite = "METOP-A"
if (satellite == '2'):
  satellite = "METOP-B"
if (satellite == '3'):
  satellite = "METOP-C"

# Read the orbit
orbit = getattr(file, 'cw:orbit_type').capitalize()

# Add a title
plt.title(f'ASCAT Vector Winds [{satellite} - {orbit}] - {date_formatted}', fontweight='bold', fontsize=6, loc='left')
plt.title('Region: ' + str(extent), fontsize=6, loc='right')

# Add a text inside the plot
from matplotlib.offsetbox import AnchoredText
text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 7}, frameon=True)
ax.add_artist(text)
#---------------------------------------------------------------------------------------------------------------------------
# Save the image
plt.savefig('Output/image_23.png')

# Show the image
plt.show() 