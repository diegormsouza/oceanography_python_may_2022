#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 31: Comparing SST (Night and Day)
# Author: Diego Souza (INPE / CGCT / DISSM)
#---------------------------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset                     # Read / Write NetCDF4 files
import matplotlib.pyplot as plt                 # Plotting library
from datetime import datetime                   # Basic Dates and time types
import cartopy, cartopy.crs as ccrs             # Plot maps
import os                                       # Miscellaneous operating system interfaces
from osgeo import gdal                          # Python bindings for GDAL
import numpy as np                              # Scientific computing with Python
from utilities_goes import download_PROD        # Our function for download
from utilities_goes import reproject            # Our function for reproject
gdal.PushErrorHandler('CPLQuietErrorHandler')   # Ignore GDAL warnings
#-----------------------------------------------------------------------------------------------------------
# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Parameters to process
product_name = 'ABI-L2-SSTF'

# Desired extent
#extent = [-140.0, -60.00, -25.00, 18.00] # Min lon, Max lon, Min lat, Max lat
extent = [-140.0, -60.00, -10.00, 50.00]

# Date structure
yyyymmddhhmn = '202201010400'

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
#-----------------------------------------------------------------------------------------------------------
# Reproject the file
filename_ds = f'{output}/{file_name}_ret.nc'
reproject(filename_ds, img, ds, extent, undef)
#-----------------------------------------------------------------------------------------------------------
# Open the reprojected GOES-R image
file = Dataset(filename_ds)

# Get the pixel values
data_night = file.variables['Band1'][:]
#-----------------------------------------------------------------------------------------------------------
# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Parameters to process
product_name = 'ABI-L2-SSTF'

# Desired extent
extent = [-140.0, -60.0, -10.0, 50.0] # Min lon, Max lon, Min lat, Max lat

# Date structure
yyyymmddhhmn = '202201011500'

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
#-----------------------------------------------------------------------------------------------------------
# Reproject the file
filename_ds = f'{output}/{file_name}_ret.nc'
reproject(filename_ds, img, ds, extent, undef)
#-----------------------------------------------------------------------------------------------------------
# Open the reprojected GOES-R image
file = Dataset(filename_ds)

# Get the pixel values
data_day = file.variables['Band1'][:]
#-----------------------------------------------------------------------------------------------------------
# Calculate the difference
data_diff = data_day - data_night
#-----------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
fig, ax = plt.subplots(figsize=(16, 8))

# Plot title
plt.title('Comparação: TSM Diurno (15:00 UTC) - Noturno (04:00 UTC)', fontsize=12, fontweight='bold')

# X axis limits and label
#plt.xlim(-0.1, 0.1)
plt.xlabel("Diferença (°C)",  fontsize=12, fontweight='bold')

# Y axis limits and label
plt.ylim(0, 600)
plt.ylabel("Pixels",  fontsize=12, fontweight='bold')

# Add grids
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')

# Show the histogram
plt.hist(data_diff[:], facecolor='blue')
#-----------------------------------------------------------------------------------------------------------
# Save the image
plt.savefig('Output/image_31.png')

# Show the image
plt.show()