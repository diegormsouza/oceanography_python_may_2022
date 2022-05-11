#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 11: Creating an Animation
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
year = '2021'
month_ini = 1
month_end = 5
month_int = 1

for month in range(month_ini, month_end + 1, month_int):
  # Time / Date for download
  month = str(month).zfill(2)
  date = year + month # YYYYMM

  # Download the file (product, date, directory)
  file = download_OCEAN('SST-Monthly-Mean', date, input) # options: 'SST', 'SST-A' (Anomaly), 'SST-T' (Trend), 'CLO' (Ocean Color), 'SLA' (Sea Level Anomaly), 'ASC-A-a', ASC-A-d, ASC-B-a, ASC-B-d, (ASCAT Winds), 'JAS' (JASON-3)
  #---------------------------------------------------------------------------------------------------------------------------
  # Open the file using the NetCDF4 library
  file = Dataset(f'{input}/{file}')
  #---------------------------------------------------------------------------------------------------------------------------
  # Select the extent [min. lon, min. lat, max. lon, max. lat]
  extent = [-93.0, -60.00, -10.00, 18.00] # South America
        
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
  data = file.variables['sea_surface_temperature'][ 0 , latui:latli , lonli:lonui ]
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
  colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", 
            "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", 
            "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", 
            "#ab1900", "#6b0200", '#3c0000']
  cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
  cmap.set_over('#3c0000')
  cmap.set_under('#28000a')
  vmin = -2.0
  vmax = 35.0

  # Add a background image
  ax.stock_img()

  # Plot the image
  img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='upper', extent=img_extent, cmap=cmap)

  # Add a shapefile
  shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
  ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

  # Add a colorbar
  plt.colorbar(img, label='Sea Surface Temperature (°C)', extend='both', orientation='vertical', pad=0.02, fraction=0.05)

  # Getting the file time and date
  add_seconds = int(file.variables['time'][0])
  date_satellite = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
  date_formatted = date_satellite.strftime('%Y-%m')
    
  # Add a title
  plt.title(f'NOAA Coral Reef Watch Daily 5 km SST - {date_formatted}', fontweight='bold', fontsize=7, loc='left')
  plt.title('Region: ' + str(extent), fontsize=7, loc='right')

  # Add a text inside the plot
  from matplotlib.offsetbox import AnchoredText
  text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 7}, frameon=True)
  ax.add_artist(text)
  #--------------------------------------------------------------------------------------------------------------------------- 
  # Save the image
  plt.savefig(f'{output}/SSTAVG_{date}.png', bbox_inches='tight', pad_inches=0, dpi=100)
#---------------------------------------------------------------------------------------------------------------------------
import imageio        # Python interface to read and write a wide range of image data
import glob           # Unix style pathname pattern expansion
import os             # Miscellaneous operating system interfaces

# Images we want to include in the GIF
files = sorted(glob.glob(f'{output}/SSTAVG_*.png'), key=os.path.getmtime)

# Create the GIF
images = []
for file in files:
    images.append(imageio.imread(file))
imageio.mimsave(f'{output}/animation.gif', images, fps=1)
  