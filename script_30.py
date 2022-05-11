#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 30: Comparing LEO and GEO products
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
date = '20220101' # YYYYMMDD

# Download the file (product, date, directory)
file_leo = download_OCEAN('SST-LEO', date, input)
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file_leo = Dataset(f'{input}/{file_leo}')
#---------------------------------------------------------------------------------------------------------------------------
# Select the extent [min. lon, min. lat, max. lon, max. lat]
extent = [-93.0, -60.00, -25.00, 18.00] # South America
       
# Reading lats and lons 
lats = file_leo.variables['lat'][:]
lons = file_leo.variables['lon'][:]

# Latitude lower and upper index
latli = np.argmin( np.abs( lats - extent[1] ) )
latui = np.argmin( np.abs( lats - extent[3] ) )
 
# Longitude lower and upper index
lonli = np.argmin( np.abs( lons - extent[0] ) )
lonui = np.argmin( np.abs( lons - extent[2] ) )
 
# Extract the Sea Surface Temperature
data_leo = file_leo.variables['sea_surface_temperature'][ 0 , latui:latli , lonli:lonui ] - 273.15
#---------------------------------------------------------------------------------------------------------------------------
# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Parameters to process
yyyymmdd = '20220101'
product_name = 'ABI-L2-SSTF'

# Desired extent
extent = [-93.0, -60.00, -25.00, 18.00] # Min lon, Max lon, Min lat, Max lat

########################################################################
# Sea Surface Temperature - "X" Hours
########################################################################

sum_ds = np.zeros((5424,5424))
count_ds = np.zeros((5424,5424))
#-----------------------------------------------------------------------------------------------------------
for hour in np.arange(14,19+1,1):

    # Date structure
    yyyymmddhhmn = f'{yyyymmdd}{hour:02.0f}00'

    # Download the file
    file_name = download_PROD(yyyymmddhhmn, product_name, input)
    #-----------------------------------------------------------------------------------------------------------
    # Variable
    var = 'SST'

    # Open the GOES-R image
    file = Dataset(f'{input}/{file_name}.nc')        

    # Open the file
    img = gdal.Open(f'NETCDF:{input}/{file_name}.nc:' + var)

    # Data Quality Flag (DQF)
    dqf = gdal.Open(f'NETCDF:{input}/{file_name}.nc:DQF')

    # Read the header metadata
    metadata = img.GetMetadata()
    scale = float(metadata.get(var + '#scale_factor'))
    offset = float(metadata.get(var + '#add_offset'))
    undef = float(metadata.get(var + '#_FillValue'))
    dtime = metadata.get('NC_GLOBAL#time_coverage_start')

    # Load the data
    ds = img.ReadAsArray(0, 0, img.RasterXSize, img.RasterYSize).astype(float)
    ds_dqf = dqf.ReadAsArray(0, 0, dqf.RasterXSize, dqf.RasterYSize).astype(float)

    # Apply the scale, offset and convert to celsius
    ds = (ds * scale + offset) - 273.15

    # Apply NaN's where the quality flag is greater than 1
    ds[ds_dqf > 1] = np.nan
    
    # Calculate the sum
    sum_ds = np.nansum(np.dstack((sum_ds,ds)),2)
    count_ds = np.nansum(np.dstack((count_ds,(ds/ds))),2)
    #-----------------------------------------------------------------------------------------------------------
    
# Calculate the sum
ds_day = np.empty((5424,5424))
ds_day[::] = np.nan
ds_day[count_ds!=0] = sum_ds[count_ds!=0]/count_ds[count_ds!=0]
#-----------------------------------------------------------------------------------------------------------
# Reproject the file
filename_ds = f'{output}/{file_name}_ret.nc'
reproject(filename_ds, img, ds_day, extent, undef)
#-----------------------------------------------------------------------------------------------------------
# Open the reprojected GOES-R image
file = Dataset(filename_ds)

# Get the pixel values
data_geo = file.variables['Band1'][:]
#-----------------------------------------------------------------------------------------------------------
# Resize the array
from skimage.transform import resize
data_geo = resize(data_geo, (data_leo.shape[0], data_leo.shape[1]))

# Calculate the difference
data_diff = data_leo - data_geo
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig, ax = plt.subplots(figsize=(16, 8))

# Plot title
plt.title('Comparação: GEO e LEO', fontsize=12, fontweight='bold')

# X axis limits and label
plt.xlim(-2, 2)
plt.xlabel("Diferença (°C)",  fontsize=12, fontweight='bold')

# Y axis limits and label
plt.ylim(0, 1000)
plt.ylabel("Pixels",  fontsize=12, fontweight='bold')

# Add grids
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')

# Show the histogram
plt.hist(data_diff[:], facecolor='blue')
#-----------------------------------------------------------------------------------------------------------
# Save the image
plt.savefig('Output/image_30.png')

# Show the image
plt.show()