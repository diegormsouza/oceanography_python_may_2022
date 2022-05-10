#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 5.2: Custom Color Palettes (Discrete)
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

# Extract the Sea Surface Temperature
data = file.variables['analysed_sst'][0,:,:]

# Reading the lats and lons 
lats = file.variables['lat'][:]
lons = file.variables['lon'][:]
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(13,7))

# Use the Cilindrical Equidistant projection in cartopy
ax = plt.axes(projection=ccrs.PlateCarree())

# Define the image extent
img_extent = [lons.min(), lons.max(), lats.min(), lats.max()]

# Add coastlines, borders and gridlines
ax.coastlines(resolution='50m', color='black', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 30), ylocs=np.arange(-90, 90, 10), draw_labels=True)
gl.top_labels = False
gl.right_labels = False

# Create a custom color scale:
# Reference color scale from NOAA: https://psl.noaa.gov/map/clim/sst.shtml
# HEX values got from: https://imagecolorpicker.com/:
colors = ["#0000a1", "#0000fe", "#0034ff", "#0356fc", "#0199fc", 
          "#01daff", "#238e25", "#00a001", "#4bcc4e", "#62fe64", 
          "#f5fe81", "#ffff02", "#ffb200", "#fd5106", "#ff2600", 
          "#fb6a94", "#b52c64"]
cmap = matplotlib.colors.ListedColormap(colors)
cmap.set_over('#b52c64')
cmap.set_under('#0000a1')
vmin = 0.0
vmax = 34.0

# Add a land mask
ax.add_feature(cfeature.LAND)

# Plot the image
img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='lower', extent=img_extent, cmap=cmap)

# Define the ticks to be shown
ticks = [-2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34]

# Add a colorbar
plt.colorbar(img, label='Sea Surface Temperature (°C)', extend='both', orientation='horizontal', pad=0.05, fraction=0.05, ticks=ticks)

# Getting the file time and date
add_seconds = int(file.variables['time'][0])
date = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
date_formatted = date.strftime('%Y-%m-%d')
	
# Add a title
plt.title(f'NOAA Coral Reef Watch Daily 5 km SST - {date_formatted}', fontweight='bold', fontsize=10, loc='left')
plt.title('INPE / CGCT / DISSM', fontsize=10, loc='right')
#--------------------------------------------------------------------------------------------------------------------------- 
# Save the image
plt.savefig('image_05b.png')

# Show the image
plt.show()