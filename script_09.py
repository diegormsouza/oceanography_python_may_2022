#---------------------------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Products - Script 9: Downloading Data Using Funtions 
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
from datetime import datetime, timedelta   # Basic Dates and time types
import os                                  # Miscellaneous operating system interfaces
import time as t                           # Time access and conversion                                          
from ftplib import FTP                     # FTP protocol client
#---------------------------------------------------------------------------------------------------------------------------

def download_OCEAN(product, date, path_dest):

  #-----------------------------------------------------------------------------------------------------------
  
  # FTP data description:

  # SEA SURFACE TEMPERATURE:
  # SST         (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst
  # SST Monthly - min / mean / max (Global - 5 km)          : ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly
  # SST Annual - min / mean / max (Global - 5 km)          : ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual

  # SEA SURFACE TEMPERATURE ANOMALY:
  # SST-Anomaly (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/ssta
  # SST-Anomaly Monthly - - min / mean / max (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly
  # SST-Anomaly Annual - - min / mean / max (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual

  # SEA SURFACE TEMPERATURE - 7 DAY TREND:
  # SST-Trend   (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst-trend-7d

  # BLEACHING ALERT AREA:
  # BAA (Global - 5 km)              : ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/baa
  # BAA Monthly - max (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly
  # BAA Annual - max (Global - 5 km) : ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual

  # CORAL BLEACHING HOTSPOT:
  # BHS (Global - 5 km)              : ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/hs
  # BHS Monthly - max (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly
  # BHS Annual - max (Global - 5 km) : ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual

  # CORAL BLEACHING HEAT STRESS DEGREE HEATING WEEK:
  # DHW (Global - 5 km)              : ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/dhw
  # DHW Monthly - max (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly
  # DHW Annual - max (Global - 5 km) : ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual

  # OCEAN COLOR:
  # OC [filled] (Global - 9 km): ftp.star.nesdis.noaa.gov/pub/socd1/mecb/coastwatch/viirs/nrt/L3/global/chlora/dineof
  # OC Granules (S-NPP)        : ftpcoastwatch.noaa.gov/pub/socd1/mecb/coastwatch/viirs/nrt/L2/
  # OC Granules (NOAA-20)      : ftpcoastwatch.noaa.gov/pub/socd2/mecb/coastwatch/viirs/n20/nrt/L2/

  # ALTIMETRY
  # Sea Level Anomaly          : ftpcoastwatch.noaa.gov/pub/socd/lsa/rads/sla/daily/nrt
  # Granules (JASON 2)         : ftp-oceans.ncei.noaa.gov/pub/data.nodc/jason2
  # Granules (JASON 3)         : ftp-oceans.ncei.noaa.gov/pub/data.nodc/jason2
  # JASON 3                    : ftpcoastwatch.noaa.gov/pub/socd/lsa/johnk/coastwatch/j3 

  # ASCAT WINDS:
  # (NetCDF) Daily             : ftpcoastwatch.noaa.gov/pub/socd7/coastwatch/metop/ascat/netcdf/day
  # (NetCDF) 4hr               : ftpcoastwatch.noaa.gov/pub/socd7/coastwatch/metop/ascat/netcdf/4hr
  # (HDF) Daily and 4hr        : ftpcoastwatch.noaa.gov/pub/socd1/coastwatch/products/ascat/4hr/hdf

  # SST LEO Global (0.02°)     : ftpcoastwatch.noaa.gov/pub/socd2/coastwatch/sst/nrt/l3s/leo/pm/
  #-----------------------------------------------------------------------------------------------------------

  print('-----------------------------------')
  print('NOAA FTP Download - Script started.')
  print('-----------------------------------')

  # Start the time counter
  start_time = t.time()  

  #-----------------------------------------------------------------------------------------------------------

  # Download directory
  #dir = "Samples"; os.makedirs(dir, exist_ok=True)
  # Download directory
  dir = path_dest; os.makedirs(dir, exist_ok=True)

  # Product selection
  product = product 
  # Options: 
  # 'SST', 'SST-A' (Anomaly), 'SST-T' (Trend), 'BAA' (Bleaching Alert), 'BHS' (Bleaching Hotspot), 'DHW' (Degree Heating Week), 'CLO' (Ocean Color), 'SLA' (Sea Level Anomaly), 'JAS' (JASON-3), 
  # 'SST-Monthly-Min', 'SST-Monthly-Mean', 'SST-Monthly-Max', 
  # 'SST-Annual-Min', 'SST-Annual-Mean', 'SST-Annual-Max'
  # 'SST-A-Monthly-Min', 'SST-A-Monthly-Mean', 'SST-A-Monthly-Max'
  # 'SST-A-Annual-Min', 'SST-A-Annual-Mean', 'SST-A-Annual-Max'
  # 'BAA-Monthly-Max', 'BAA-Annual-Max'
  # 'BHS-Monthly-Max', 'BHS-Annual-Max'
  # 'DHW-Monthly-Max', 'DHW-Annual-Max'
  # 'SST-LEO'
  # 'ASC-A-a-nc', 'ASC-A-d-nc', 'ASC-B-a-nc, 'ASC-A-d-nc' (ASCAT Winds)
  # 'ASC-A-a-hdf', 'ASC-A-d-hdf', 'ASC-B-a-hdf, 'ASC-A-d-hdf' (ASCAT Winds)

  # Desired year (four digit)
  year = date[0:4]
  #year = '2021'

  # Desired month (two digit)
  month = date[4:6]
  #month = '06'

  # Desired day (two digit)
  day = date[6:8] 
  #day = '28' 

  #-----------------------------------------------------------------------------------------------------------

  # FTP Address
  if (product == 'SST' or product == 'SST-A' or product == 'SST-T' or product == 'BAA' or 
      product == 'BHS' or product == 'DHW' or product == 'CLO' or product == 'SST-Monthly-Min' or product == 'SST-Monthly-Mean' or 
      product == 'SST-Monthly-Max' or product == 'SST-Annual-Min' or product == 'SST-Annual-Mean' or 
      product == 'SST-Annual-Max' or product == 'SST-A-Monthly-Min' or product == 'SST-A-Monthly-Mean' or 
      product == 'SST-A-Monthly-Max' or product == 'SST-A-Annual-Min' or product == 'SST-A-Annual-Mean' or 
      product == 'SST-A-Annual-Max' or product == 'BAA-Monthly-Max' or product == 'BHA-Annual-Max' or
      product == 'BHS-Monthly-Max' or product == 'BHS-Annual-Max' or 
      product == 'DHW-Monthly-Max' or product == 'DHW-Annual-Max'):
    ftp = FTP('ftp.star.nesdis.noaa.gov') 
  elif (product == 'ASC-B-a-nc' or 'ASC-B-d-nc' or 'ASC-C-a-nc' or 'ASC-C-d-nc' or product == 'SLA' or product == 'JAS' or product == 'SST-LEO' or
        product == 'ASC-B-a-hdf' or 'ASC-B-d-hdf' or 'ASC-C-a-hdf' or 'ASC-C-d-hdf'):
    ftp = FTP('ftpcoastwatch.noaa.gov') 

  # FTP Credentials 
  ftp.login('', '') 

  #-----------------------------------------------------------------------------------------------------------

  # Access the FTP folder, based on the desired product
  if (product == 'SST'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst/' + year + '/')
      naming_convention = 'coraltemp_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  elif (product == 'SST-Monthly-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_sst-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'SST-Monthly-Mean'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_sst-mean_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'SST-Monthly-Min'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_sst-min_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'SST-Annual-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_sst-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'SST-Annual-Mean'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_sst-mean_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'SST-Annual-Min'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_sst-min_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'SST-A'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/ssta/' + year + '/')
      naming_convention = 'ct5km_ssta_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  elif (product == 'SST-A-Monthly-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_ssta-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'SST-A-Monthly-Mean'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_ssta-mean_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'SST-A-Monthly-Min'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_ssta-min_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'SST-A-Annual-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_ssta-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'SST-A-Annual-Mean'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_ssta-mean_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'SST-A-Annual-Min'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_ssta-min_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'SST-T'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst-trend-7d/' + year + '/')
      naming_convention = 'ct5km_sst-trend-7d_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  elif (product == 'BAA'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/baa/' + year + '/')
      naming_convention = 'ct5km_baa_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  elif (product == 'BAA-Monthly-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_baa-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'BAA-Annual-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_baa-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'BHS'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/hs/' + year + '/')
      naming_convention = 'ct5km_hs_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  elif (product == 'BHS-Monthly-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_hs-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'BHS-Annual-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_hs-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'DHW'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/dhw/' + year + '/')
      naming_convention = 'ct5km_dhw_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  elif (product == 'DHW-Monthly-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/monthly/' + year + '/')
      naming_convention = 'ct5km_dhw-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + extension

  elif (product == 'DHW-Annual-Max'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/annual/')
      naming_convention = 'ct5km_dhw-max_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + extension

  elif (product == 'CLO'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd1/mecb/coastwatch/viirs/nrt/L3/global/chlora/dineof/' + year + '/')
      naming_convention = '_a1_WW00_chlora'
      extension = '.nc'
      file_name = 'V' + year + jday + naming_convention + extension

  elif (product == 'SLA'):
      # FTP Path
      path = ('pub/socd/lsa/rads/sla/daily/nrt/' + year + '/')
      naming_convention = 'rads_global_nrt_sla'
      extension = '.nc'
      date_1 = year + month + day
      date_2 = str(datetime(int(year), int(month), int(day)) + timedelta(days=1))
      date_2 = datetime.strptime(date_2, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')   
      file_name = naming_convention + '_' + date_1 + '_' + date_2 + '_' + '001' + extension

  elif (product == 'ASC-B-a-nc'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd7/coastwatch/metop/ascat/netcdf/day/')
      naming_convention = 'AS'
      extension = '.nc'
      file_name = naming_convention + year + jday + 'Bas_WW' + extension

  elif (product == 'ASC-B-d-nc'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd7/coastwatch/metop/ascat/netcdf/day/')
      naming_convention = 'AS'
      extension = '.nc'
      file_name = naming_convention + year + jday + 'Bds_WW' + extension

  elif (product == 'ASC-C-a-nc'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd7/coastwatch/metop/ascat/netcdf/day/')
      naming_convention = 'AS'
      extension = '.nc'
      file_name = naming_convention + year + jday + 'Cas_WW' + extension

  elif (product == 'ASC-C-d-nc'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd7/coastwatch/metop/ascat/netcdf/day/')
      naming_convention = 'AS'
      extension = '.nc'
      file_name = naming_convention + year + jday + 'Cds_WW' + extension
      
  elif (product == 'ASC-B-a-hdf'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd1/coastwatch/products/ascat/4hr/hdf/')
      naming_convention = 'AS'
      extension = '.hdf'
      file_name = naming_convention + year + jday + 'Bas_WW' + extension

  elif (product == 'ASC-B-d-hdf'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd1/coastwatch/products/ascat/4hr/hdf/')
      naming_convention = 'AS'
      extension = '.hdf'
      file_name = naming_convention + year + jday + 'Bds_WW' + extension

  elif (product == 'ASC-C-a-hdf'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd1/coastwatch/products/ascat/4hr/hdf/')
      naming_convention = 'AS'
      extension = '.hdf'
      file_name = naming_convention + year + jday + 'Cas_WW' + extension

  elif (product == 'ASC-C-d-hdf'):
      # Converting date to julian day
      import datetime
      fmt = '%Y%m%d'
      s = year + month + day
      dt = datetime.datetime.strptime(s, fmt)
      tt = dt.timetuple()
      jday = str(tt.tm_yday).zfill(3)
      # FTP Path
      path = ('pub/socd1/coastwatch/products/ascat/4hr/hdf/')
      naming_convention = 'AS'
      extension = '.hdf'
      file_name = naming_convention + year + jday + 'Cds_WW' + extension

  elif (product == 'JAS'):
      # FTP Path
      path = ('pub/socd/lsa/johnk/coastwatch/j3/')
      naming_convention = 'j3'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  elif (product == 'SST-LEO'):
    # Converting date to julian day
    import datetime
    fmt = '%Y%m%d'
    s = year + month + day
    dt = datetime.datetime.strptime(s, fmt)
    tt = dt.timetuple()
    jday = str(tt.tm_yday).zfill(3)
    # FTP Path
    path = ('pub/socd2/coastwatch/sst/nrt/l3s/leo/pm/' + year + '/' + jday)
    naming_convention = '120000-STAR-L3S_GHRSST-SSTsubskin-LEO_PM_D-ACSPO_V2.80-v02.0-fv01.0'
    extension = '.nc'
    file_name = year + month + day + naming_convention + extension

#-----------------------------------------------------------------------------------------------------------

  # Download the file
  print('\n---------------------')
  print('Checking the FTP File:') 
  print('---------------------')
  print('Product: ' + product)
  print('Date: ' + year + month + day)
  print('File Name: ' + file_name)

  try:
    # Enter the FTP Path
    ftp.cwd(path)
    # Check if the file exists
    if os.path.exists(dir + '//' + file_name):
      print("")
      print('The file ' + dir + '/' + file_name + ' already exists.')
      print("")
    else:
      # If not, download the file
      print("Downloading the file...")
      ftp.retrbinary("RETR " + file_name, open(dir + '//' + file_name, 'wb').write)  
      print("")
      print('\n---------------------')
      print('Download Finished.') 
      print('---------------------')
      print("")
      # End the time counter
      print('\nTotal Download Time:', round((t.time() - start_time),2), 'seconds.') 
      print("")
  except:
    print("\nFile not available!")
    print("")

  # Quit the FPT connection
  ftp.quit()

  #-----------------------------------------------------------------------------------------------------------
  # Return the file name
  return f'{file_name}'
  #-----------------------------------------------------------------------------------------------------------

# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Time / Date for download
date = '20220102' # YYYYMMDD

# Download the file (product, date, directory)
file = download_OCEAN('SST', date, input)

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

# Add a background image
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

# Reading the data from a coordinate
lat_point = -30
lon_point = -30
lat_idx = (np.abs(lats - lat_point)).argmin()
lon_idx = (np.abs(lons - lon_point)).argmin()
data_point = file.variables['analysed_sst'][ : , lat_idx , lon_idx ][0].round(2)

# Adding the data as an annotation
# Add a circle
ax.plot(lon_point, lat_point, 'o', color='red', markersize=5, transform=ccrs.Geodetic(), markeredgewidth=1.0, markeredgecolor=(0, 0, 0, 1))
# Add a text
txt_offset_x = 0.8
txt_offset_y = 0.8
plt.annotate("Lat: " + str(lat_point) + "\n" + "Lon: " + str(lon_point) + "\n" + "SST: \n" + str(data_point) + ' °C', xy=(lon_point + txt_offset_x, lat_point + txt_offset_y), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=7, fontweight='bold', color='gold', bbox=dict(boxstyle="round",fc=(0.0, 0.0, 0.0, 0.5), ec=(1., 1., 1.)), alpha = 1.0)
#--------------------------------------------------------------------------------------------------------------------------- 
# Save the image
plt.savefig('Output/image_09.png')

# Show the image
plt.show()