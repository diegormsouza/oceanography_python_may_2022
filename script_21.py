#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 21: Sea Level Anomaly + Geostrophic Velocity (multi-mission)
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
input = "/content/Samples"; os.makedirs(input, exist_ok=True)
output = "/content/Output"; os.makedirs(output, exist_ok=True)

# Time / Date for download
date = '20210630' # YYYYMMDD

# Download the file (product, date, directory)
file = download_OCEAN('SLA', date, input) 
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file = Dataset(f'{input}/{file}')
#---------------------------------------------------------------------------------------------------------------------------

# Select the extent [min. lon, min. lat, max. lon, max. lat]
#extent = [-93.0, -60.00, -25.00, 18.00] # South America
extent = [-65.0, -45.00, -42.00, -24.00] # Southeast Coast

# Reading lats and lons 
lats = file.variables['latitude'][:]
lons = file.variables['longitude'][:]
 
# Latitude lower and upper index
latli = np.argmin( np.abs( lats - extent[1] ) )
latui = np.argmin( np.abs( lats - extent[3] ) )
 
# Longitude lower and upper index
lonli = np.argmin( np.abs( lons - extent[0] ) )
lonui = np.argmin( np.abs( lons - extent[2] ) )
 
# Extract the Sea Level Anomaly
data = file.variables['sla'][ 0 , latli:latui , lonli:lonui ]

# Extract the lats and lons again
lats = file.variables['latitude'][ latli:latui ]
lons = file.variables['longitude'][ lonli:lonui ]

# Extract the Absolute Geostrophic Velocity (azonal and meridian)
u_geo = file.variables['ugos'][ 0 , latli:latui , lonli:lonui ]
v_geo = file.variables['vgos'][ 0 , latli:latui , lonli:lonui ]

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
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.50, xlocs=np.arange(-180, 180, 1), ylocs=np.arange(-90, 90, 1), draw_labels=True)
gl.top_labels = False
gl.right_labels = False

# Create a custom color scale:
cmap = 'seismic'
vmin = -0.18
vmax = 0.18

# Plot the image
img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='lower', interpolation='bilinear', extent=img_extent, cmap=cmap)

# Plot the quiver
img2 = ax.quiver(lons[::1], lats[::1], u_geo[::1,::1], v_geo[::1,::1], scale = 25, color='black')

# Plot the legend
qk = ax.quiverkey(img2, 0.65, 0.892, 0.5, '50 cm/s', labelpos='E', coordinates='figure', fontproperties={'size': '7'})

# Add a land mask
ax.add_feature(cfeature.LAND, zorder=10)

# Add a shapefile
shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3, zorder=11)

# Add a colorbar
plt.colorbar(img, label='Sea Level Anomaly (m)', extend='both', orientation='horizontal', pad=0.05, fraction=0.05)

# Getting the file time and date
add_days = int(file.variables['time'][0])
date = datetime(1950,1,1,0) + timedelta(days=add_days)
date_formatted = date.strftime('%Y-%m-%d')

# Add a title
plt.title(f'NOAA Coast Watch Daily Sea Level Anomaly + Geostrophic Velocity - {date_formatted}', fontweight='bold', fontsize=7, loc='left')
plt.title('Region: ' + str(extent), fontsize=7, loc='right')

# Add a text inside the plot
from matplotlib.offsetbox import AnchoredText
text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 7}, frameon=True)
ax.add_artist(text)

ax.set_facecolor('xkcd:black')

#---------------------------------------------------------------------------------------------------------------------------
# Save the image
plt.savefig('Output/image_15.png')

# Show the image
plt.show()