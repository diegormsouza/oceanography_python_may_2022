#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 27: Comparing Satellite and Buoys (Function)
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

def plot_PIRATA(buoy_name, lat_nominal, lon_nominal, year, month, day):

  # Reading the data from a buoy

  # Desired year (four digit)
  year = year
  # Desired month (two digit)
  month = month
  # Desired day (two digit)
  day = day

  #---------------------------------------------------------------------------------------------------------------------------

  # Read the buoy data
  buoy = Dataset('http://goosbrasil.org:8080/pirata/' + buoy_name + '.nc')

  # Read the 'time' dataset
  time = buoy.variables['time'][:]

  #---------------------------------------------------------------------------------------------------------------------------

  # Calculate how many days passed since 0001-01-01
  from datetime import date
  d0 = date(1, 1, 1)
  d1 = date(int(year), int(month), int(day))
  delta = d1 - d0
  delta_days = delta.days + 0.5

  #---------------------------------------------------------------------------------------------------------------------------

  # Get the array index for the desired date
  index = np.where(time == delta_days)

  lon_buoy  = buoy.variables['longitude'][index[0]] - 360
  lat_buoy  = buoy.variables['latitude'][index[0]]

  # Extract the 1 m temperature, lat and lon for the desired date
  try:
    
    temp_buoy = buoy.variables['temperature'][index[0],0][0].round(2)
    
    if (temp_buoy == -9999 or temp_buoy == -99999):
    
      print("Bóia " + buoy_name + " com dados inválidos para esta data.")
      # Add a yellow circle
      ax.plot(lon_buoy[0], lat_buoy[0], 'o', color='yellow', markersize=4, transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1))
      # Add a text
      txt_offset_x = 0.8
      txt_offset_y = 0.8
      text = "Dado inválido"
      plt.annotate(text, xy=(int(lon_buoy[0] + txt_offset_x), int(lat_buoy[0] + txt_offset_y)), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=7, fontweight='bold', color='gold', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0, 0.5), ec=(1., 1., 1.)), alpha = 1.0)
    
      return
  
  except:
    
    print("Bóia " + buoy_name + " sem dados para esta data.")
    # Add a red circle
    ax.plot(lon_nominal, lat_nominal, 'o', color='red', markersize=4, transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1))
    # Add a text
    txt_offset_x = 0.8
    txt_offset_y = 0.8
    text = "Sem dados"
    plt.annotate(text, xy=((lon_nominal + txt_offset_x), (lat_nominal + txt_offset_y)), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=7, fontweight='bold', color='gold', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0, 0.5), ec=(1., 1., 1.)), alpha = 1.0)
    
    return

  #---------------------------------------------------------------------------------------------------------------------------

  # Reading the data from a coordinate (satellite)
  lat_point = lat_buoy[0]
  lon_point = lon_buoy[0]

  lat_idx = np.argmin(np.abs(lats - lat_point))
  lon_idx = np.argmin(np.abs(lons - lon_point))

  temp_sat = file.variables['analysed_sst'][ 0 , lat_idx , lon_idx ].round(2)
  delta = temp_sat - temp_buoy

  #---------------------------------------------------------------------------------------------------------------------------

  # Adding Annotations
  # Add a circle
  ax.plot(lon_point, lat_point, 'o', color='lightgreen', markersize=4, transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1))
  # Add a text
  txt_offset_x = 0.8
  txt_offset_y = 0.8
  #text = "Lat: " + str(lat_point.round(2)) + "\n" + "Lon: " + str(lon_point.round(2)) + "\n" + "Satélite: " + str(temp_sat) + " °C" + "\n" + "Bóia: " + str(temp_buoy) + " °C" + "\n" + "\u0394 = "  + str(delta.round(4)) + " °C"
  text = "Satélite: " + str(temp_sat) + " °C" + "\n" + "Bóia: " + str(temp_buoy) + " °C" + "\n" + "\u0394 = "  + str(delta.round(4)) + " °C"
  plt.annotate(text, xy=(int(lon_point + txt_offset_x), int(lat_point + txt_offset_y)), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=7, fontweight='bold', color='gold', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0, 0.5), ec=(1., 1., 1.)), alpha = 1.0)

#---------------------------------------------------------------------------------------------------------------------------

# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Time / Date for download
date = '20220409' # YYYYMMDD

# Download the file (product, date, directory)
file = download_OCEAN('SST', date, input)

#---------------------------------------------------------------------------------------------------------------------------

# Open the file using the NetCDF4 library
file = Dataset(f'{input}/{file}')

#---------------------------------------------------------------------------------------------------------------------------

# Select the extent [min. lon, min. lat, max. lon, max. lat]
extent = [-93.0, -60.00, 20.00, 30.00] # South Atlantic
       
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
plt.figure(figsize=(13,10))

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
colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", 
          "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", 
          "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", 
          "#ab1900", "#6b0200"]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
cmap.set_over('#6b0200')
cmap.set_under('#2d001c')
vmin = -2.0
vmax = 35.0

# Add a land mask
ax.add_feature(cfeature.LAND)

# Plot the image
img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='lower', extent=img_extent, cmap=cmap)

# Add a shapefile
shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

# Add a shapefile
shapefile = list(shpreader.Reader('Metareas.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=1.0)

# Add a colorbar
plt.colorbar(img, label='Sea Surface Temperature (°C)', extend='both', orientation='horizontal', pad=0.03, fraction=0.05)

# Getting the file time and date
add_seconds = int(file.variables['time'][0])
date_satellite = datetime(1981,1,1,1) + timedelta(seconds=add_seconds)
date_formatted = date_satellite.strftime('%Y-%m-%d')

# Add a title
plt.title(f'NOAA Coral Reef Watch Daily 5 km SST + PIRATA Project Buoys - {date_formatted}', fontweight='bold', fontsize=7, loc='left')
plt.title('Region: ' + str(extent), fontsize=7, loc='right')

# Add a text inside the plot
from matplotlib.offsetbox import AnchoredText
text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 7}, frameon=True)
ax.add_artist(text)

# Add texts
txt1 = ax.annotate("METAREA V", xy=(-28, 9), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt2 = ax.annotate("A", xy=(-48, -32), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt3 = ax.annotate("B", xy=(-43, -27), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt4 = ax.annotate("C", xy=(-46, -25), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt5 = ax.annotate("D", xy=(-38, -22), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt6 = ax.annotate("E", xy=(-36, -17), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt7 = ax.annotate("F", xy=(-33, -10), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt8 = ax.annotate("G", xy=(-36, -2), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt9 = ax.annotate("H", xy=(-46, 2), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt10 = ax.annotate("N", xy=(-22, -13), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())
txt11 = ax.annotate("S", xy=(-22, -17), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), color='black', size=10, clip_on=True, annotation_clip=True, horizontalalignment='center', verticalalignment='center', transform=ccrs.PlateCarree())

#---------------------------------------------------------------------------------------------------------------------------

# Get the same date from the satellite data
year = date[0:4]
month = date[4:6]
day = date[6:8]

# Call the function to read the buoys and compare with the satellite data
plot_PIRATA('B20n38w',  0, -38, year, month, day)
plot_PIRATA('B15n38w', 15, -38, year, month, day)
plot_PIRATA('B12n38w', 12, -38, year, month, day)
plot_PIRATA('B8n38w',   8, -38, year, month, day)
plot_PIRATA('B4n38w',   4, -38, year, month, day)
plot_PIRATA('B0n35w',   0, -35, year, month, day)
plot_PIRATA('B8s30w',  -8, -30, year, month, day)
plot_PIRATA('B19s34w',-19, -34, year, month, day)
plot_PIRATA('B21n23w', 21, -23, year, month, day)
plot_PIRATA('B12n23w', 12, -23, year, month, day)
plot_PIRATA('B4n23w',   4, -23, year, month, day)
plot_PIRATA('B0n23w',   0, -23, year, month, day)
plot_PIRATA('B2n10w',   2, -10, year, month, day)
plot_PIRATA('B2s10w',  -2, -10, year, month, day)
plot_PIRATA('B5s10w',  -5, -10, year, month, day)
plot_PIRATA('B6s10w',  -6, -10, year, month, day)
plot_PIRATA('B10s10w',-10, -10, year, month, day)
plot_PIRATA('B0n0e',    0,   0, year, month, day)

#---------------------------------------------------------------------------------------------------------------------------

# Save the image
plt.savefig('Output/image_27.png')

# Show the image
plt.show()