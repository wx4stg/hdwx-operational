#!/usr/bin/env python3
# Helper functions for python-based HDWX
# Created 9 July 2022 by Sam Gardner <stgardner4@tamu.edu>

from datetime import datetime as dt, timedelta
from os import path, chmod, remove, urandom
from pathlib import Path
import json
from atomicwrites import atomic_write
from natsort import natsorted

def writeJson(basePath, productID, runTime, fileName, validTime, gisInfo, reloadInterval):
    """
    Updates the JSON data required for the server to provide API data to users. When adding a new frame to a product, this function should be called.
    Parameters:
    ----------
    basePath: the path of the calling module
    productID: the productID of the product
    runTime: the run this frame belongs to
    validTime: the time the frame is valid for
    gisInfo: The lat/long corners of the frame
    reloadInterval: the amount of time in seconds before the next frame is expected to be posted

    """
    publishTime = dt.utcnow()
    runPathExtension = runTime.strftime("%Y/%m/%d/%H00/")
    if productID == 0:
        productDesc = "MRMS Reflectivity At Lowest Altitude"
        productPath = "gisproducts/radar/RALA/"
        isFcst = False
        fileExt = "png"
        dispFrames = 30
        productTypeID = 0
        totalFrameCount = -1
    elif productID == 1:
        productDesc = "MRMS National Reflectivity At Lowest Altitude"
        productPath = "products/radar/national/"
        isFcst = False
        fileExt = "png"
        dispFrames = 30
        productTypeID = 0
        totalFrameCount = -1
    elif productID == 2:
        productDesc = "MRMS Regional Reflectivity At Lowest Altitude"
        productPath = "products/radar/regional/"
        isFcst = False
        fileExt = "png"
        dispFrames = 30
        productTypeID = 0
        totalFrameCount = -1
    elif productID == 3:
        productDesc = "MRMS Local Reflectivity At Lowest Altitude"
        productPath = "products/radar/local/"
        isFcst = False
        fileExt = "png"
        dispFrames = 30
        productTypeID = 0
        totalFrameCount = -1
    elif productID == 4:
        productDesc = "CONUS GeoColor"
        productPath = "gisproducts/satellite/goes16/geocolor/"
        isFcst = False
        fileExt = "png"
        dispFrames = 24
        productTypeID = 0
        totalFrameCount = -1
    elif productID == 5:
        productDesc = "GOES-16 CONUS GeoColor"
        productPath = "products/satellite/goes16/geocolor/"
        isFcst = False
        fileExt = "png"
        dispFrames = 24
        productTypeID = 0
        totalFrameCount = -1
    elif productID == 100:
        productDesc = "Mesonet Farm WxCenter"
        productPath = "products/mesonet/Farm/wxcenter/"
        isFcst = False
        fileExt = "png"
        dispFrames = 1
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 101:
        productDesc = "Mesonet Farm Timeseries"
        productPath = "products/mesonet/Farm/timeseries/"
        runPathExtension = "last24hrs"
        isFcst = False
        fileExt = "png"
        dispFrames = 1
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 102:
        productDesc = "Mesonet Gardens WxCenter"
        productPath = "products/mesonet/Gardens/wxcenter/"
        isFcst = False
        fileExt = "png"
        dispFrames = 1
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 103:
        productDesc = "Mesonet Gardens Timeseries"
        productPath = "products/mesonet/Gardens/timeseries/"
        runPathExtension = "last24hrs"
        isFcst = False
        fileExt = "png"
        dispFrames = 1
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 120:
        productDesc = "ADRAD 0.5° Reflectivity PPI"
        productPath = "gisproducts/radar/ADRAD/"+str(productID)
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 121:
        productDesc = "ADRAD 0.5° Reflectivity PPI"
        productPath = "products/radar/ADRAD/"+str(productID)
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 122:
        productDesc = "ADRAD 0.5° Reflectivity PPI (Quality-controlled)"
        productPath = "gisproducts/radar/ADRAD/"+str(productID)
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 123:
        productDesc = "ADRAD 0.5° Reflectivity PPI (Quality-controlled)"
        productPath = "products/radar/ADRAD/"+str(productID)
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 124:
        productDesc = "ADRAD 0.5° Signal Quality Index"
        productPath = "products/radar/ADRAD/"+str(productID)
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 125:
        productDesc = "ADRAD 0.5° Velocity PPI"
        productPath = "gisproducts/radar/ADRAD/"+str(productID)
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 126:
        productDesc = "ADRAD 0.5° Velocity PPI"
        productPath = "products/radar/ADRAD/"+str(productID)
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 140:
        productDesc = "HLMA VHF 1-minute Sources"
        productPath = "gisproducts/hlma/vhf-1min/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 141:
        productDesc = "HLMA VHF 1-minute Sources"
        productPath = "products/hlma/vhf-1min/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 142:
        productDesc = "GR2Analyst HLMA VHF Sources (1 minute)"
        productPath = "gr2a/"
        isFcst = False
        fileExt = "php"
        dispFrames = 1
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 143:
        productDesc = "HLMA VHF 10-minute Sources"
        productPath = "gisproducts/hlma/vhf-10min/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 144:
        productDesc = "HLMA VHF 10-minute Sources"
        productPath = "products/hlma/vhf-10min/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 145:
        productDesc = "GR2Analyst HLMA VHF Sources (10 minutes)"
        productPath = "gr2a/"
        isFcst = False
        fileExt = "php"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 146:
        productDesc = "HLMA 1-minute Flash Extent Density"
        productPath = "gisproducts/hlma/flash-1min/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 147:
        productDesc = "HLMA 1-minute Flash Extent Density"
        productPath = "products/hlma/flash-1min/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 148:
        productDesc = "HLMA 10-minute Flash Extent Density"
        productPath = "gisproducts/hlma/flash-10min/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 149:
        productDesc = "HLMA 10-minute Flash Extent Density"
        productPath = "products/hlma/flash-10min/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 150:
        productDesc = "HLMA VHF 1-minute Sources + ADRAD Reflectivity"
        productPath = "products/hlma/adrad-src/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 151:
        productDesc = "HLMA VHF 1-minute Sources + MRMS Reflectivity At Lowest Altitude"
        productPath = "products/hlma/mrms-src/"
        isFcst = False
        fileExt = "png"
        dispFrames = 30
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 152:
        productDesc = "HLMA 1-minute Flash Extent Density + ADRAD Reflectivity"
        productPath = "products/hlma/adrad-flash/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 153:
        productDesc = "HLMA 1-minute Flash Extent Density + MRMS Reflectivity At Lowest Altitude"
        productPath = "products/hlma/mrms-flash/"
        isFcst = False
        fileExt = "png"
        dispFrames = 30
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 154:
        productDesc = "HLMA VHF 1-minute Sources Analysis Plot"
        productPath = "products/hlma/vhf-1min-analysis/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 155:
        productDesc = "HLMA VHF 1-minute Sources Analysis Plot"
        productPath = "products/hlma/vhf-10min-analysis/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 156:
        productDesc = "HLMA VHF 1-minute Sources Analysis Plot + MRMS Reflectivity At Lowest Altitude"
        productPath = "products/hlma/mrms-src-analysis/"
        isFcst = False
        fileExt = "png"
        dispFrames = 60
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 190:
        productDesc = "TASC Location"
        productPath = "gisproducts/tasc/"
        isFcst = False
        fileExt = "png"
        dispFrames = 0
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 191:
        productDesc = "TASC Location + MRMS Reflectivity"
        productPath = "products/tasc/rala/"
        isFcst = False
        fileExt = "png"
        dispFrames = 0
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 192:
        productDesc = "TASC Location + GeoColor"
        productPath = "products/tasc/geocolor/"
        isFcst = False
        fileExt = "png"
        dispFrames = 0
        productTypeID = 1
        totalFrameCount = -1
    elif productID == 300:
        productDesc = "GFS Surface Temperature"
        productPath = "gisproducts/gfs/sfcT/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 301:
        productDesc = "GFS Surface Winds"
        productPath = "gisproducts/gfs/sfcWnd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 302:
        productDesc = "GFS Surface MSLP"
        productPath = "gisproducts/gfs/sfcMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 303:
        productDesc = "GFS Surface Temperature, Winds, MSLP"
        productPath = "products/gfs/sfcTWndMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 308:
        productDesc = "GFS Simulated Composite Reflectivity"
        productPath = "gisproducts/gfs/simrefc/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 309:
        productDesc = "GFS 1hr Max Updraft Helicity"
        productPath = "gisproducts/gfs/udhelicity/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 310:
        productDesc = "GFS Simulated Composite Reflectivity"
        productPath = "products/gfs/refccomposite/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 316:
        productDesc = "GFS 500 hPa Winds"
        productPath = "gisproducts/gfs/500wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 318:
        productDesc = "GFS 500 hPa Heights"
        productPath = "gisproducts/gfs/500hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 320:
        productDesc = "GFS 500 hPa Heights, Winds, Vorticity"
        productPath = "products/gfs/500staticvort/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 321:
        productDesc = "GFS 250 hPa Winds"
        productPath = "gisproducts/gfs/250wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 322:
        productDesc = "GFS 250 hPa Heights"
        productPath = "gisproducts/gfs/250hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 324:
        productDesc = "GFS 250 hPa Heights, Winds, Isotachs"
        productPath = "products/gfs/250staticjet/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 325:
        productDesc = "GFS 850 hPa Winds"
        productPath = "gisproducts/gfs/850wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 326:
        productDesc = "GFS 850 hPa Heights"
        productPath = "gisproducts/gfs/850hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 327:
        productDesc = "GFS 850 hPa Temperatures"
        productPath = "gisproducts/gfs/850temps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 328:
        productDesc = "GFS 850 hPa Heights, Winds, Temperatures"
        productPath = "products/gfs/850statictemps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 329:
        productDesc = "GFS 700 hPa Relative Humidity"
        productPath = "gisproducts/gfs/700rh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 331:
        productDesc = "GFS 700 hPa Relative Humidity, MSLP, 1000->500 hPa Thickness"
        productPath = "products/gfs/700staticrh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 332:
        productDesc = "GFS 4-Panel"
        productPath = "products/gfs/4pnl/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 380:
        productDesc = "GFS Simulated 1km AGL Reflectivity"
        productPath = "gisproducts/gfs/simrefd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 381:
        productDesc = "GFS Simulated 1km AGL Reflectivity"
        productPath = "products/gfs/refdcomposite/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 129
    elif productID == 500:
        productDesc = "NAM Surface Temperature"
        productPath = "gisproducts/nam/sfcT/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 501:
        productDesc = "NAM Surface Winds"
        productPath = "gisproducts/nam/sfcWnd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 502:
        productDesc = "NAM Surface MSLP"
        productPath = "gisproducts/nam/sfcMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 503:
        productDesc = "NAM Surface Temperature, Winds, MSLP"
        productPath = "products/nam/sfcTWndMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 508:
        productDesc = "NAM Simulated Composite Reflectivity"
        productPath = "gisproducts/nam/simrefc/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 509:
        productDesc = "NAM 1hr Max Updraft Helicity"
        productPath = "gisproducts/nam/udhelicity/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 510:
        productDesc = "NAM Simulated Composite Reflectivity"
        productPath = "products/nam/refccomposite/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 516:
        productDesc = "NAM 500 hPa Winds"
        productPath = "gisproducts/nam/500wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 518:
        productDesc = "NAM 500 hPa Heights"
        productPath = "gisproducts/nam/500hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 520:
        productDesc = "NAM 500 hPa Heights, Winds, Vorticity"
        productPath = "products/nam/500staticvort/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 521:
        productDesc = "NAM 250 hPa Winds"
        productPath = "gisproducts/nam/250wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 522:
        productDesc = "NAM 250 hPa Heights"
        productPath = "gisproducts/nam/250hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 524:
        productDesc = "NAM 250 hPa Heights, Winds, Isotachs"
        productPath = "products/nam/250staticjet/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 525:
        productDesc = "NAM 850 hPa Winds"
        productPath = "gisproducts/nam/850wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 526:
        productDesc = "NAM 850 hPa Heights"
        productPath = "gisproducts/nam/850hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 527:
        productDesc = "NAM 850 hPa Temperatures"
        productPath = "gisproducts/nam/850temps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 528:
        productDesc = "NAM 850 hPa Heights, Winds, Temperatures"
        productPath = "products/nam/850statictemps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 529:
        productDesc = "NAM 700 hPa Relative Humidity"
        productPath = "gisproducts/nam/700rh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 531:
        productDesc = "NAM 700 hPa Relative Humidity, MSLP, 1000->500 hPa Thickness"
        productPath = "products/nam/700staticrh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 532:
        productDesc = "NAM 4-panel"
        productPath = "products/nam/4pnl/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 580:
        productDesc = "NAM Simulated 1km AGL Reflectivity"
        productPath = "gisproducts/nam/simrefd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 581:
        productDesc = "NAM Simulated 1km AGL Reflectivity"
        productPath = "products/nam/refdcomposite/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 600:
        productDesc = "NAM NEST Surface Temperature"
        productPath = "gisproducts/namnest/sfcT/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 601:
        productDesc = "NAM NEST Surface Winds"
        productPath = "gisproducts/namnest/sfcWnd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 602:
        productDesc = "NAM NEST Surface MSLP"
        productPath = "gisproducts/namnest/sfcMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 603:
        productDesc = "NAM NEST Surface Temperature, Winds, MSLP"
        productPath = "products/namnest/sfcTWndMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 608:
        productDesc = "NAM NEST Simulated Composite Reflectivity"
        productPath = "gisproducts/namnest/simrefc/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 609:
        productDesc = "NAM NEST 1hr Max Updraft Helicity"
        productPath = "gisproducts/namnest/udhelicity/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 610:
        productDesc = "NAM NEST Simulated Composite Reflectivity"
        productPath = "products/namnest/refccomposite/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 616:
        productDesc = "NAM NEST 500 hPa Winds"
        productPath = "gisproducts/namnest/500wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 618:
        productDesc = "NAM NEST 500 hPa Heights"
        productPath = "gisproducts/namnest/500hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 620:
        productDesc = "NAM NEST 500 hPa Heights, Winds, Vorticity"
        productPath = "products/namnest/500staticvort/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 621:
        productDesc = "NAM NEST 250 hPa Winds"
        productPath = "gisproducts/namnest/250wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 622:
        productDesc = "NAM NEST 250 hPa Heights"
        productPath = "gisproducts/namnest/250hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 624:
        productDesc = "NAM NEST 250 hPa Heights, Winds, Isotachs"
        productPath = "products/namnest/250staticjet/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 625:
        productDesc = "NAM NEST 850 hPa Winds"
        productPath = "gisproducts/namnest/850wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 626:
        productDesc = "NAM NEST 850 hPa Heights"
        productPath = "gisproducts/namnest/850hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 627:
        productDesc = "NAM NEST 850 hPa Temperatures"
        productPath = "gisproducts/namnest/850temps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 628:
        productDesc = "NAM NEST 850 hPa Heights, Winds, Temperatures"
        productPath = "products/namnest/850statictemps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 629:
        productDesc = "NAM NEST 700 hPa Relative Humidity"
        productPath = "gisproducts/namnest/700rh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 631:
        productDesc = "NAM NEST 700 hPa Relative Humidity, MSLP, 1000->500 hPa Thickness"
        productPath = "products/namnest/700staticrh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 632:
        productDesc = "NAM NEST 4-panel"
        productPath = "products/namnest/4pnl/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 680:
        productDesc = "NAM NEST Simulated 1km AGL Reflectivity"
        productPath = "gisproducts/namnest/simrefd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 681:
        productDesc = "NAM NEST Simulated 1km AGL Reflectivity"
        productPath = "products/namnest/refdcomposite/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 800:
        productDesc = "HRRR Surface Temperature"
        productPath = "gisproducts/hrrr/sfcT/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 801:
        productDesc = "HRRR Surface Winds"
        productPath = "gisproducts/hrrr/sfcWnd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 802:
        productDesc = "HRRR Surface MSLP"
        productPath = "gisproducts/hrrr/sfcMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 803:
        productDesc = "HRRR Surface Temperature, Winds, MSLP"
        productPath = "products/hrrr/sfcTWndMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 808:
        productDesc = "HRRR Simulated Composite Reflectivity"
        productPath = "gisproducts/hrrr/simrefc/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 809:
        productDesc = "HRRR 1hr Max Updraft Helicity"
        productPath = "gisproducts/hrrr/udhelicity/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 810:
        productDesc = "HRRR Simulated Composite Reflectivity"
        productPath = "products/hrrr/refccomposite/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 816:
        productDesc = "HRRR 500 hPa Winds"
        productPath = "gisproducts/hrrr/500wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 818:
        productDesc = "HRRR 500 hPa Heights"
        productPath = "gisproducts/hrrr/500hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 820:
        productDesc = "HRRR 500 hPa Heights, Winds, Vorticity"
        productPath = "products/hrrr/500staticvort/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 821:
        productDesc = "HRRR 250 hPa Winds"
        productPath = "gisproducts/hrrr/250wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 824:
        productDesc = "HRRR 250 hPa Winds, Isotachs"
        productPath = "products/hrrr/250staticjet/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 825:
        productDesc = "HRRR 850 hPa Winds"
        productPath = "gisproducts/hrrr/850wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 826:
        productDesc = "HRRR 850 hPa Heights"
        productPath = "gisproducts/hrrr/850hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 827:
        productDesc = "HRRR 850 hPa Temperatures"
        productPath = "gisproducts/hrrr/850temps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 828:
        productDesc = "HRRR 850 hPa Heights, Winds, Temperatures"
        productPath = "products/hrrr/850statictemps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 829:
        productDesc = "HRRR 700 hPa Relative Humidity"
        productPath = "gisproducts/hrrr/700rh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 831:
        productDesc = "HRRR 700 hPa Relative Humidity, MSLP, 1000->500 hPa Thickness"
        productPath = "products/hrrr/700staticrh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 832:
        productDesc = "HRRR 4-panel"
        productPath = "products/hrrr/4pnl/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 880:
        productDesc = "HRRR Simulated 1km AGL Reflectivity"
        productPath = "gisproducts/hrrr/simrefd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 881:
        productDesc = "HRRR Simulated 1km AGL Reflectivity"
        productPath = "products/hrrr/refdcomposite/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 8
        if runTime.hour in [0, 6, 12, 18]:
            totalFrameCount = 49
        else:
            totalFrameCount = 19
    elif productID == 1000:
        productDesc = "ECMWF-HRES Surface Temperature"
        productPath = "gisproducts/ecmwf-hres/sfcT/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1001:
        productDesc = "ECMWF-HRES Surface Winds"
        productPath = "gisproducts/ecmwf-hres/sfcWnd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1002:
        productDesc = "ECMWF-HRES Surface MSLP"
        productPath = "gisproducts/ecmwf-hres/sfcMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1003:
        productDesc = "ECMWF-HRES Surface Temperature, Winds, MSLP"
        productPath = "products/ecmwf-hres/sfcTWndMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1016:
        productDesc = "ECMWF-HRES 500 hPa Winds"
        productPath = "gisproducts/ecmwf-hres/500wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1018:
        productDesc = "ECMWF-HRES 500 hPa Heights"
        productPath = "gisproducts/ecmwf-hres/500hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1020:
        productDesc = "ECMWF-HRES 500 hPa Heights, Winds, Vorticity"
        productPath = "products/ecmwf-hres/500staticvort/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1021:
        productDesc = "ECMWF-HRES 250 hPa Winds"
        productPath = "gisproducts/ecmwf-hres/250wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1022:
        productDesc = "ECMWF-HRES 250 hPa Heights"
        productPath = "gisproducts/ecmwf-hres/250hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1024:
        productDesc = "ECMWF-HRES 250 hPa Heights, Winds, Isotachs"
        productPath = "products/ecmwf-hres/250staticjet/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1025:
        productDesc = "ECMWF-HRES 850 hPa Winds"
        productPath = "gisproducts/ecmwf-hres/850wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1026:
        productDesc = "ECMWF-HRES 850 hPa Heights"
        productPath = "gisproducts/ecmwf-hres/850hgt/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1027:
        productDesc = "ECMWF-HRES 850 hPa Temperature"
        productPath = "gisproducts/ecmwf-hres/850temps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1028:
        productDesc = "ECMWF-HRES 850 hPa Heights, Winds, Temperatures"
        productPath = "products/ecmwf-hres/850statictemps/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1029:
        productDesc = "ECMWF-HRES 700 hPa Relative Humidity"
        productPath = "gisproducts/ecmwf-hres/700rh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1031:
        productDesc = "ECMWF-HRES 700 hPa Relative Humidity, MSLP, 1000->500 hPa Thickness"
        productPath = "products/ecmwf-hres/700staticrh/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1032:
        productDesc = "ECMWF-HRES 4-panel"
        productPath = "products/ecmwf-hres/4pnl/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    elif productID == 1200:
        productDesc = "WPC Surface Bulletin"
        productPath = "gisproducts/noaa/wpcsfcbull/"
        isFcst = False
        fileExt = "png"
        dispFrames = 1
        productTypeID = 12
        totalFrameCount = 1
    elif productID == 1201:
        productDesc = "WPC Surface Bulletin"
        productPath = "products/noaa/wpcsfcbull/"
        isFcst = False
        fileExt = "png"
        dispFrames = 1
        productTypeID = 12
        totalFrameCount = 1
    if isFcst:
        fHour = validTime - runTime
        fHour = int(fHour.total_seconds() / 3600)
    else:
        fHour = 0

    if gisInfo == ["0,0", "0,0"]:
        isGIS = False
    else:
        isGIS = True
    
    productDict = {
        "productID" : productID,
        "productDescription" : productDesc,
        "productPath" : productPath,
        "productReloadTime" : reloadInterval,
        "lastReloadTime" : publishTime.strftime("%Y%m%d%H%M"),
        "isForecast" : isFcst,
        "isGIS" : isGIS,
        "fileExtension" : fileExt,
        "displayFrames" : dispFrames
    }
    productDictJsonPath = path.join(basePath, "output", "metadata", str(productID)+".json")
    Path(path.dirname(productDictJsonPath)).mkdir(parents=True, exist_ok=True)
    with atomic_write(productDictJsonPath, overwrite=True) as jsonWrite:
        json.dump(productDict, jsonWrite, indent=4)
    chmod(productDictJsonPath, 0o644)

    productRunDictPath = path.join(basePath, "output", "metadata", "products", str(productID), runTime.strftime("%Y%m%d%H00")+".json")
    productRunLockPath = path.join(basePath, "output", "metadata", "products", str(productID), runTime.strftime("%Y%m%d%H00")+".lock")
    Path(path.dirname(productRunDictPath)).mkdir(parents=True, exist_ok=True)
    while path.exists(productRunLockPath):
        if dt.utcnow() - timedelta(minutes=2) > publishTime:
            break
    try:
        lockFile = open(productRunLockPath, "x")
        lockFile.close()
        if path.exists(productRunDictPath):
            with open(productRunDictPath, "r") as jsonRead:
                oldData = json.load(jsonRead)
            # Add previously generated frames to a list, framesArray
            framesArray = oldData["productFrames"]
        else:
            # If that file didn't exist, then create an empty list instead
            framesArray = list()
        frmDict = {
                "fhour" : fHour,
                "filename" : fileName,
                "gisInfo" : gisInfo,
                "valid" : validTime.strftime("%Y%m%d%H%M"),
                "publishTime" : publishTime.strftime("%Y%m%d%H%M")
        }
        for frame in framesArray:
            if frame["filename"] == frmDict["filename"]:
                framesArray.remove(frame)
        framesArray.append(frmDict)
        if totalFrameCount == -1:
            totalFrameCount = len(framesArray)
        productRunDict = {
            "publishTime" : publishTime.strftime("%Y%m%d%H%M"),
            "pathExtension" : runPathExtension,
            "runName" : runTime.strftime("%d %b %Y %HZ"),
            "availableFrameCount" : len(framesArray),
            "totalFrameCount" : totalFrameCount,
            "productFrames" : sorted(framesArray, key=lambda dict: int(dict["valid"])) # productFramesArray, sorted by increasing valid Time
        }
        with atomic_write(productRunDictPath, overwrite=True) as jsonWrite:
            json.dump(productRunDict, jsonWrite, indent=4)
        chmod(productRunDictPath, 0o644)
        remove(productRunLockPath)
    except Exception as e:
        remove(productRunLockPath)
        raise e
    
    if productTypeID == 0:
        productTypeDesc = "Radar & Satellite"
    elif productTypeID == 1:
        productTypeDesc = "TAMU Observations"
    elif productTypeID == 3:
        productTypeDesc = "GFS"
    elif productTypeID == 5:
        productTypeDesc = "NAM"
    elif productTypeID == 6:
        productTypeDesc = "NAM NEST"
    elif productTypeID == 8:
        productTypeDesc = "HRRR"
    elif productTypeID == 10:
        productTypeDesc = "ECMWF-HRES"
    elif productTypeID == 12:
        productTypeDesc = "NOAA"
    productTypeDictPath = path.join(basePath, "output", "metadata", "productTypes", str(productTypeID)+".json")
    Path(path.dirname(productTypeDictPath)).mkdir(parents=True, exist_ok=True)
    productsInType = list()
    if path.exists(productTypeDictPath):
        with open(productTypeDictPath, "r") as jsonRead:
            oldProductTypeDict = json.load(jsonRead)
        for productInOldDict in oldProductTypeDict["products"]:
            if productInOldDict["productID"] != productID:
                productsInType.append(productInOldDict)
    productsInType.append(productDict)
    productTypeDict = {
        "productTypeID" : productTypeID,
        "productTypeDescription" : productTypeDesc,
        "products" : natsorted(productsInType, key=lambda dict: dict["productID"])
    }
    with atomic_write(productTypeDictPath, overwrite=True) as jsonWrite:
        json.dump(productTypeDict, jsonWrite, indent=4)
    chmod(productTypeDictPath, 0o644)

def dressImage(fig, ax, title, validTime, fhour=None, notice=None, plotHandle=None, cbticks=None, tickhighlight=None, cbextend="neither", colorbarLabel=None, width=1920, height=1080, tax=None, lax=None):
    """
    Adds standardized HDWX branding to a figure 
    Parameters:
    ----------
    fig: the figure to be modified
    ax: the primary axes of the figure
    title: the title of the product
    validTime: the time the product is valid for
    fhour: the forecast hour of the model product
    notice: Copyright/disclaimer text
    plotHandle: the handle to the plot object that will be used to create the colorbar
    cbticks: the tick values for the colorbar
    tickhighlight: the tick values to be highlighted
    cbextend: whether or not to extend the colorbar, "min", "max", "both", or "neither"
    colorbarLabel: the label for the colorbar
    width: the width of the figure in pixels
    height: the height of the figure in pixels
    tax: the title axes, will create if not provided
    lax: the logo axes, will create if not provided
    
    """
    from matplotlib import pyplot as plt
    from matplotlib import image as mpimg
    px = 1/plt.rcParams["figure.dpi"]
    fig.set_size_inches(width*px, height*px)
    heightOfBottomBar = 100/height
    insetDistance = 75/width
    widthOfObjects = 500/width
    if plotHandle is not None:
        cbax = fig.add_axes([insetDistance, insetDistance+(10/height), widthOfObjects, .02])
        if cbticks is None:
            cb = fig.colorbar(plotHandle, cax=cbax, orientation="horizontal", extend=cbextend)
        else:
            cb = fig.colorbar(plotHandle, cax=cbax, orientation="horizontal", extend=cbextend).set_ticks(cbticks)
            if tickhighlight is not None:
                targetIdx = list(list(plt.xticks())[0]).index(32)
                plt.xticks()[-1][targetIdx].set_color("red")
        if colorbarLabel is not None:
            cbax.set_xlabel(colorbarLabel)
    else:
        if colorbarLabel is not None:
            cbax = fig.add_axes([insetDistance, insetDistance+(10/height), widthOfObjects, .02])
            plt.setp(cbax.spines.values(), visible=False)
            cbax.tick_params(left=False, labelleft=False)
            cbax.tick_params(bottom=False, labelbottom=False)
            cbax.set_xlabel(colorbarLabel)
    if tax is None:
        tax = fig.add_axes([0.5-(widthOfObjects/2), insetDistance, widthOfObjects, heightOfBottomBar])
    if fhour is None:
        titleStr = title+"\n Valid "+validTime.strftime("%a %-d %b %Y %H%MZ")
    else:
        titleStr = title+"\n"+"f"+str(fhour)+" Valid "+validTime.strftime("%a %-d %b %Y %H%MZ")
    tax.text(0.5, 0.3, titleStr, horizontalalignment="center", verticalalignment="center", fontsize=16)
    xlabel = "Python HDWX -- Send bugs to stgardner4@tamu.edu"
    if notice is not None:
        xlabel = xlabel+"\n"+notice
    tax.set_xlabel(xlabel)
    tax.set_facecolor("#00000000")
    plt.setp(tax.spines.values(), visible=False)
    tax.tick_params(left=False, labelleft=False)
    tax.tick_params(bottom=False, labelbottom=False)
    if lax is None:
        lax = fig.add_axes([0,0,(ax.get_position().width/3),heightOfBottomBar])
    lax.set_aspect(2821/11071)
    lax.axis("off")
    lax.set_position([(1-(lax.get_position().width+insetDistance)), (lax.get_position().y0), (lax.get_position().width), (lax.get_position().height)])
    plt.setp(lax.spines.values(), visible=False)
    atmoLogoPath = path.join(path.abspath(path.dirname(path.dirname(__file__))), "atmoLogo.png")
    atmoLogo = mpimg.imread(atmoLogoPath)
    lax.imshow(atmoLogo)
    if ax is not None:
        ax.set_position([insetDistance, .025+heightOfBottomBar, 1-2*insetDistance, 1-(insetDistance+heightOfBottomBar)])
        ax.set_box_aspect(height/width)
    fig.set_facecolor("white")
    return fig

def saveImage(fig, outputPath, transparent=False, bbox_inches=None):
    gifPath = outputPath.replace(path.basename(outputPath), "gif-"+path.basename(outputPath))
    fig.savefig(gifPath, format="png", transparent=transparent, bbox_inches=bbox_inches)
    from PIL import Image
    im = Image.open(gifPath)
    im = im.convert("RGB").convert("P", palette=Image.WEB)
    im.save(outputPath)
