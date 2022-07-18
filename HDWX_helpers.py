 #!/usr/bin/env python3
# Helper functions for python-based HDWX
# Created 9 July 2022 by Sam Gardner <stgardner4@tamu.edu>

from datetime import datetime as dt, timedelta
from os import path, chmod, remove
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
        productPath = "products/mesonet/Farm/timeseries/"
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
    elif productID == 300:
        productDesc = "GFS Surface Temperature"
        productPath = "gisproducts/gfs/sfcT/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 209
    elif productID == 301:
        productDesc = "GFS Surface Winds"
        productPath = "gisproducts/gfs/sfcWnd/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 209
    elif productID == 302:
        productDesc = "GFS Surface MSLP"
        productPath = "gisproducts/gfs/sfcMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 209
    elif productID == 303:
        productDesc = "GFS Surface Temperature, Winds, MSLP"
        productPath = "products/gfs/sfcTWndMSLP/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 209
    elif productID == 316:
        productDesc = "GFS 500 hPa Winds"
        productPath = "gisproducts/gfs/500wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 209
    elif productID == 321:
        productDesc = "GFS 250 hPa Winds"
        productPath = "gisproducts/gfs/250wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 209
    elif productID == 325:
        productDesc = "GFS 850 hPa Winds"
        productPath = "gisproducts/gfs/850wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 209
    elif productID == 390:
        productDesc = "GFS Surface Wind Divergence"
        productPath = "products/gfs/divergence/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 3
        totalFrameCount = 209
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
    elif productID == 516:
        productDesc = "NAM 500 hPa Winds"
        productPath = "gisproducts/nam/500wind/"
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
    elif productID == 525:
        productDesc = "NAM 850 hPa Winds"
        productPath = "gisproducts/nam/850wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 5
        totalFrameCount = 53
    elif productID == 590:
        productDesc = "NAM Surface Wind Divergence"
        productPath = "products/nam/divergence/"
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
    elif productID == 616:
        productDesc = "NAM NEST 500 hPa Winds"
        productPath = "gisproducts/namnest/500wind/"
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
    elif productID == 625:
        productDesc = "NAM NEST 850 hPa Winds"
        productPath = "gisproducts/namnest/850wind/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 6
        totalFrameCount = 61
    elif productID == 690:
        productDesc = "NAM NEST Surface Wind Divergence"
        productPath = "products/namnest/divergence/"
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
    elif productID == 890:
        productDesc = "HRRR Surface Wind Divergence"
        productPath = "products/hrrr/divergence/"
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
    elif productID == 1090:
        productDesc = "ECMWF-HRES Surface Wind Divergence"
        productPath = "products/ecmwf-hres/divergence/"
        isFcst = True
        fileExt = "png"
        dispFrames = 0
        productTypeID = 10
        if runTime.hour in [0, 12]:
            totalFrameCount = 61
        else:
            totalFrameCount = 31
    
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
                "fhour" : 0, # forecast hour is 0 for non-forecasts
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

def dressImage():
    pass