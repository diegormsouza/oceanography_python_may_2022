#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 6: Plotting a Specific Region
# Author: Diego Souza (INPE / CGCT / DISSM)
#---------------------------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset               # Read / Write NetCDF4 files
import matplotlib.pyplot as plt           # Plotting library
from datetime import datetime, timedelta  # Library to convert julian day to dd-mm-yyyy
import cartopy, cartopy.crs as ccrs       # Plot maps
import cartopy.feature as cfeature        # Common drawing and filtering operations
import numpy as np                        # Import the Numpy package
import matplotlib.colors                  # Matplotlib colors  
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file = Dataset("coraltemp_v3.1_20220101.nc")
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
 
# Extract the Sea Surface Temperature
data = file.variables['analysed_sst'][ 0 , latli:latui , lonli:lonui ]
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(7,7))

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
# Reference color scale from NASA Wordview: https://worldview.earthdata.nasa.gov/
# HEX values got from: https://imagecolorpicker.com/:
colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", 
          "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", 
          "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", 
          "#ab1900", "#6b0200", '#3c0000']
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
cmap.set_over('#3c0000')
cmap.set_under('#2d001c')
vmin = -2.0
vmax = 35.0

# Add a land mask
ax.add_feature(cfeature.LAND)

# Plot the image
img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='lower', extent=img_extent, cmap=cmap)

# Add a colorbar
plt.colorbar(img, label='Sea Surface Temperature (°C)', extend='both', orientation='vertical', pad=0.05, fraction=0.05)

# Getting the file time and date
add_seconds = int(file.variables['time'][0])
date = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
date_formatted = date.strftime('%Y-%m-%d')
	
# Add a title
plt.title(f'NOAA Coral Reef Watch Daily 5 km SST - {date_formatted}', fontweight='bold', fontsize=7, loc='left')
plt.title('Region: ' + str(extent), fontsize=7, loc='right')
#--------------------------------------------------------------------------------------------------------------------------- 
# Save the image
plt.savefig('image_06.png')

# Show the image
plt.show()