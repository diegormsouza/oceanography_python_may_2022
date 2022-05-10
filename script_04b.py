#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 4.2: Cartopy Projections (Robinson)
# Author: Diego Souza (INPE / CGCT / DISSM)
#---------------------------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset               # Read / Write NetCDF4 files
import matplotlib.pyplot as plt           # Plotting library
from datetime import datetime, timedelta  # Library to convert julian day to dd-mm-yyyy
import cartopy, cartopy.crs as ccrs       # Plot maps
import cartopy.feature as cfeature        # Common drawing and filtering operations
import numpy as np                        # Import the Numpy package
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file = Dataset("coraltemp_v3.1_20220101.nc")

# Extract the Sea Surface Temperature
data = file.variables['analysed_sst'][0,:,:]
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(13,7))

# Use the Mercator projection in cartopy
ax = plt.axes(projection=ccrs.Robinson(central_longitude=0.0))

# Method used for "global" plots
ax.set_global()

# Add a background map
ax.stock_img()

# Add coastlines, borders and gridlines
ax.coastlines(resolution='50m', color='black', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.5)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='white', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 30), ylocs=np.arange(-90, 90, 10), draw_labels=False)

# Plot the image
plt.imshow(data, vmin=-2, vmax=35, origin='lower', cmap='jet', transform=ccrs.PlateCarree())

# Add a colorbar
plt.colorbar(label='Sea Surface Temperature (°C)', extend='both', orientation='horizontal', pad=0.05, fraction=0.05)

# Getting the file time and date
add_seconds = int(file.variables['time'][0])
date = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
date_formatted = date.strftime('%Y-%m-%d')
	
# Add a title
plt.title(f'NOAA Coral Reef Watch Daily 5 km SST - {date_formatted}', fontweight='bold', fontsize=10, loc='left')
plt.title('Robinson Projection', fontsize=10, loc='right')
#--------------------------------------------------------------------------------------------------------------------------- 
# Save the image
plt.savefig('image_04b.png')

# Show the image
plt.show()