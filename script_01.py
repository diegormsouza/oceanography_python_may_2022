#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 1: Basic Plot
# Author: Diego Souza (INPE / CGCT / DISSM)
#---------------------------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset      # Read / Write NetCDF4 files
import matplotlib.pyplot as plt  # Plotting library
#---------------------------------------------------------------------------------------------------------------------------
# Open the file using the NetCDF4 library
file = Dataset("coraltemp_v3.1_20220101.nc")

# Extract the Sea Surface Temperature
data = file.variables['analysed_sst'][0,:,:]
#---------------------------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(10,5))
 
# Plot the image
plt.imshow(data, vmin=-2, vmax=35, origin='lower', cmap='jet')
#--------------------------------------------------------------------------------------------------------------------------- 
# Save the image
plt.savefig('image_01.png')

# Show the image
plt.show()