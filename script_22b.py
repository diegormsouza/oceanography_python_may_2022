#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 22: Surface Winds (Barbs)
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
from pyhdf.SD import SD, SDC               # Import the PyHDF library
#---------------------------------------------------------------------------------------------------------------------------
# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Time / Date for download
date = '20220409' # YYYYMMDD

# Download the file (product, date, directory)
file = download_OCEAN('ASC-B-a-hdf', date, input)
#---------------------------------------------------------------------------------------------------------------------------

# Open the file using the PyHDF library
file = f'{input}/{file}'
hdf = SD(file, SDC.READ)

#---------------------------------------------------------------------------------------------------------------------------    

# Select the extent [min. lon, min. lat, max. lon, max. lat]
extent = [-93.0, -60.00, -25.00, 18.00] # South America

# Reading lats and lons 
sds_obj = hdf.select('latitude') 
lats = sds_obj.get() 
sds_obj = hdf.select('longitude') 
lons = sds_obj.get() 

# Getting the lat lon indexes
lats_idx0, lats_idx1 = np.where((lats >= extent[1]) & (lats <= extent[3]))
lons_idx0, lons_idx1 = np.where((lons >= extent[0]) & (lons <= extent[2]))
latli = lats_idx0.min()
latui = lats_idx0.max()
lonli = lons_idx1.min()
lonui = lons_idx1.max()

# Extract the lats and lons again
lats = lats[ latli:latui , lonli:lonui ]
lons = lons[ latli:latui , lonli:lonui ]

# Extract the U Wind
sds_obj = hdf.select('u_wind') 
u_wind = sds_obj.get() 
u_wind = u_wind[ latli:latui , lonli:lonui ].astype(float) 
u_wind[u_wind == -9999] = np.nan
u_wind = u_wind * 0.01

# Extract the U Wind
sds_obj = hdf.select('v_wind') 
v_wind = sds_obj.get() 
v_wind = v_wind[ latli:latui , lonli:lonui ].astype(float)  
v_wind[v_wind == -9999] = np.nan
v_wind = v_wind * 0.01

# Extract the wind speed
sds_obj = hdf.select('windspeed') 
wspeed = sds_obj.get() 
wspeed = wspeed[ latli:latui , lonli:lonui ].astype(float)  
wspeed[wspeed == -9999] = np.nan
wspeed = wspeed * 0.01

#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(8,8))

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

# Add a land mask
ax.add_feature(cfeature.LAND)
# Add an ocean mask
ax.add_feature(cfeature.OCEAN, facecolor='black')

# Create a custom color palette 
colors = ["#747474", "#00befe", "#0048ff", "#00c300", "#fedb12",
          "#f25505", "#ff1526", "#87422a", "#d100e1", "#7f00ad"]
cmap = matplotlib.colors.ListedColormap(colors)

# Plot the image
bounds = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
img = ax.barbs(lons[::2,::2], lats[::2,::2], u_wind[::2,::2], v_wind[::2,::2], wspeed[::2,::2], cmap=cmap, norm=norm, length = 3.0, sizes = dict(emptybarb=0.0, spacing=0.2, height=0.5), linewidth=0.5, pivot='middle')

# Getting the file time and date
sds_obj = hdf.select('cwdate') 
add_days = sds_obj.get().min() 
day = datetime(1970,1,1,0) + timedelta(days=int(add_days))

# Extract the time for each point
sds_obj = hdf.select('cwtime') 
cwtime = sds_obj.get() 
cwtime = cwtime[ latli:latui , lonli:lonui ].astype(float) 
cwtime[cwtime == -2147483647] = np.nan
cwtime = cwtime[::50,::20]
lons_text = lons[::50,::20]
lats_text = lats[::50,::20]

for (j,i),label in np.ndenumerate(cwtime):
    if (label > -9999):    
      date = day + timedelta(seconds=int(label))
      date_formatted = date.strftime('%H:%M')
      #ax.text(lons_text[j][i], lats_text[j][i],date_formatted,ha='center',va='center', color='white', fontsize=12, fontweight='bold', transform=ccrs.Geodetic())
      plt.annotate(date_formatted, xy=(lons_text[j][i], lats_text[j][i]), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=7, fontweight='bold', color='white', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0, 0.5), ec=(1., 1., 1.)), alpha = 1.0, clip_on=True, annotation_clip=True)

# Add a shapefile
shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

# Add a colorbar
plt.colorbar(img, label='Wind Speed (kt)', extend='neither', orientation='vertical', pad=0.02, fraction=0.05)

# Getting the file time and date
sds_obj = hdf.select('cwdate') 
add_days = sds_obj.get().min() 
date = datetime(1970,1,1,0) + timedelta(days=int(add_days))
date_formatted = date.strftime('%Y-%m-%d')

# Read the satellite
satellite = file[-10:-9]
if (satellite == 'B'):
  satellite = "METOP-B"
if (satellite == 'C'):
  satellite = "METOP-C"

# Read the orbit
orbit = file[-9:-8]
if (orbit == 'a'):
  orbit = "Ascending"
if (orbit == 'd'):
  orbit = "Descending"

# Add a title
plt.title(f'ASCAT Vector Winds [{satellite} - {orbit}] - {date_formatted}', fontweight='bold', fontsize=7, loc='left')
plt.title('Region: ' + str(extent), fontsize=7, loc='right')

# Add a text inside the plot
from matplotlib.offsetbox import AnchoredText
text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 7}, frameon=True)
ax.add_artist(text)

#---------------------------------------------------------------------------------------------------------------------------
# Save the image
plt.savefig('Output/image_22b.png')

# Show the image
plt.show()