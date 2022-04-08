#-----------------------------------------------------------------------------------------------------------
# INPE / CGCT / DISSM - Training: Oceanography Data Processing With Python - Data Access with Python (NOAA FTP)
# Author: Diego Souza (INPE / CGCT / DISSM)
#-----------------------------------------------------------------------------------------------------------

# Required modules
from datetime import datetime, timedelta # Basic Dates and time types
import os                                # Miscellaneous operating system interfaces
import time as t                         # Time access and conversion                                          
from ftplib import FTP                   # FTP protocol client

#-----------------------------------------------------------------------------------------------------------

def download_OCEAN(product, date, path_dest):

  #-----------------------------------------------------------------------------------------------------------
  
  # FTP data description:

  # SEA SURFACE TEMPERATURE:
  # SST         (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst
  # SST-Anomaly (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/ssta
  # SST-Trend   (Global - 5 km): ftp.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst-trend-7d

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
  product = product # options: 'SST', 'SST-A' (Anomaly), 'SST-T' (Trend), 'CLO' (Ocean Color), 'SLA' (Sea Level Anomaly), 'ASW' (ASCAT Winds), 'JAS' (JASON-3)

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
  if (product == 'SST' or product == 'SST-A' or product == 'SST-T' or product == 'CLO'):
    ftp = FTP('ftp.star.nesdis.noaa.gov') 
  elif (product == 'ASC-A-a' or 'ASC-A-d' or 'ASC-B-a' or 'ASC-B-d' or product == 'SLA' or product == 'JAS'):
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

  elif (product == 'SST-A'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/ssta/' + year + '/')
      naming_convention = 'ct5km_ssta_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  elif (product == 'SST-T'):
      # FTP Path
      path = ('pub/socd/mecb/crw/data/5km/v3.1_op/nc/v1.0/daily/sst-trend-7d/' + year + '/')
      naming_convention = 'ct5km_sst-trend-7d_v3.1'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

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
      from datetime import datetime, timedelta # Basic Dates and time types
      # FTP Path
      path = ('pub/socd/lsa/rads/sla/daily/nrt/' + year + '/')
      naming_convention = 'rads_global_nrt_sla'
      extension = '.nc'
      date_1 = year + month + day
      date_2 = str(datetime(int(year), int(month), int(day)) + timedelta(days=1))
      date_2 = datetime.strptime(date_2, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')   
      file_name = naming_convention + '_' + date_1 + '_' + date_2 + '_' + '001' + extension

  elif (product == 'ASC-A-a'):
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
      file_name = naming_convention + year + jday + 'Aas_WW' + extension

  elif (product == 'ASC-A-d'):
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
      file_name = naming_convention + year + jday + 'Ads_WW' + extension

  elif (product == 'ASC-B-a'):
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

  elif (product == 'ASC-B-d'):
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

  elif (product == 'JAS'):
      # FTP Path
      path = ('pub/socd/lsa/johnk/coastwatch/j3/')
      naming_convention = 'j3'
      extension = '.nc'
      file_name = naming_convention + '_' + year + month + day + extension

  #-----------------------------------------------------------------------------------------------------------

  # Enter the FTP Path
  ftp.cwd(path)

  # Download the file
  print('\n---------------------')
  print('Downloading FTP File:') 
  print('---------------------')
  print('Product: ' + product)
  print('Date: ' + year + month + day)
  print('File Name: ' + file_name)

  try:
    # Download the file
    ftp.retrbinary("RETR " + file_name, open(dir + '//' + file_name, 'wb').write)  
  except:
    print("\nFile not available!")

  # Quit the FPT connection
  ftp.quit()

  #-----------------------------------------------------------------------------------------------------------

  # End the time counter
  print('\nTotal Download Time:', round((t.time() - start_time),2), 'seconds.') 

  # Return the file name
  return f'{file_name}'
#-----------------------------------------------------------------------------------------------------------