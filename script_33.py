#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 33: Significant Height and Wind Direction
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
#---------------------------------------------------------------------------------------------------------------------------

# File list
files = ['WW_2021062500_hs_wind.nc',
         'WW_2021062600_hs_wind.nc',
         'WW_2021062700_hs_wind.nc',
         'WW_2021062800_hs_wind.nc',
         'WW_2021062900_hs_wind.nc',
         'WW_2021063000_hs_wind.nc',
         'WW_2021070100_hs_wind.nc',
         'WW_2021070200_hs_wind.nc']

for nc_file in files:
  # Open the file using the NetCDF4 library
  file = Dataset('Samples/' + nc_file)
  #---------------------------------------------------------------------------------------------------------------------------
  # Select the extent [min. lon, min. lat, max. lon, max. lat]
  extent = [-93.0, -60.00, -25.00, 18.00] # South America
        
  # Reading lats and lons 
  lats = file.variables['lat'][:]
  lons = file.variables['lon'][:] - 360

  # Latitude lower and upper index
  latli = np.argmin( np.abs( lats - extent[1] ) )
  latui = np.argmin( np.abs( lats - extent[3] ) )
  
  # Longitude lower and upper index
  lonli = np.argmin( np.abs( lons - extent[0] ) )
  lonui = np.argmin( np.abs( lons - extent[2] ) )

  # Extract the lats and lons again
  lats = file.variables['lat'][ latli:latui ]
  lons = file.variables['lon'][ lonli:lonui ]

  # Extract the Significant Height
  data = file.variables['hs'][ 0, latli:latui , lonli:lonui ]

  # Extract the U and V components
  u_comp = file.variables['uwnd'][ 0, latli:latui , lonli:lonui ]
  v_comp = file.variables['vwnd'][ 0, latli:latui , lonli:lonui ]

  #---------------------------------------------------------------------------------------------------------------------------
  # Choose the plot size (width x height, in inches)
  plt.figure(figsize=(15,15))

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
  colors = ["#0000cc", "#0166ff", "#00b6ff", "#00ffff", "#01db00", 
            "#01ff00", "#ffff00", "#ffcc00", "#fe9900", "#ff6700", 
            "#fe0001", "#ce1f8f", "#9c2f2b"]
  cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
  cmap.set_over('#9c2f2b')
  cmap.set_under('#0000cc')
  vmin = 0.0
  vmax = 12.0

  # Add a background image
  ax.stock_img()

  # Plot the image
  img = ax.imshow(data, vmin=vmin, vmax=vmax, origin='lower', extent=img_extent, cmap=cmap)

  # Plot the quiver
  img2 = ax.quiver(lons[::8], lats[::8], u_comp[::8,::8], v_comp[::8,::8], scale = 500, color='black')

  # Add a shapefile
  shapefile = list(shpreader.Reader('ne_10m_admin_1_states_provinces.shp').geometries())
  ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='gray',facecolor='none', linewidth=0.3)

  # Define the ticks to be shown
  ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

  # Add a colorbar
  plt.colorbar(img, label='Significant Height (m)', extend='both', orientation='vertical', pad=0.02, fraction=0.05, ticks=ticks)

  year = nc_file[-21:-17]
  month = nc_file[-17:-15]
  day = nc_file[-15:-13]

  # Getting the file time and date
  add_hours = int(file.variables['time'][0])
  date = datetime(int(year),int(month),int(day),0) + timedelta(hours=add_hours)
  date_formatted = date.strftime('%Y-%m-%d %H:%M UTC')
    
  # Add a title
  plt.title(f'Significant Height (m) and Wind Direction - {date_formatted}', fontweight='bold', fontsize=13, loc='left')
  plt.title('WWATCH', fontsize=13, loc='right')

  # Add a text inside the plot
  from matplotlib.offsetbox import AnchoredText
  text = AnchoredText("INPE / CGCT / DISSM", loc=4, prop={'size': 12}, frameon=True)
  ax.add_artist(text)
  #--------------------------------------------------------------------------------------------------------------------------- 
  # Save the image
  plt.savefig('Output/' + nc_file + '.png')

  # Show the image
  plt.show()