#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 7: Adding Shapefiles and Texts
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
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file = Dataset("coraltemp_v3.1_20220101.nc")
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
colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", 
          "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", 
          "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", 
          "#ab1900", "#6b0200", '#3c0000']
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
cmap.set_over('#3c0000')
cmap.set_under('#28000a')
vmin = -2.0
vmax = 35.0

# Add a background map
ax.stock_img()

# Plot the image
img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='lower', extent=img_extent, cmap=cmap)

# Add a shapefile
shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

# Add a shapefile
shapefile = list(shpreader.Reader('Metareas.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=1.0)

# Add a colorbar
plt.colorbar(img, label='Sea Surface Temperature (°C)', extend='both', orientation='vertical', pad=0.02, fraction=0.05)

# Getting the file time and date
add_seconds = int(file.variables['time'][0])
date = datetime(1981,1,1,0) + timedelta(seconds=add_seconds)
date_formatted = date.strftime('%Y-%m-%d')
	
# Add a title
plt.title(f'NOAA Coral Reef Watch Daily 5 km SST - {date_formatted}', fontweight='bold', fontsize=7, loc='left')
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
# Save the image
plt.savefig('image_07.png')

# Show the image
plt.show()