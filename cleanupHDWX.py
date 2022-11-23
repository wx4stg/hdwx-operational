#!/usr/bin/env python3
# Cleanup/resource management for python-based HDWX server root
# Created 21 December 2021 by Sam Gardner <stgardner4@tamu.edu>

import sys
from datetime import datetime as dt, timedelta
from os import path, listdir, remove
from shutil import rmtree
import json

# cleanupHDWX.py <purgeAfterHours> <HDWX server root>
if __name__ == "__main__":
    # Get desired time to purge files after from arg 1
    hoursToPurgeAfter = timedelta(hours=int(sys.argv[1]))
    # If hours to purge after is 0, exit immediately
    if hoursToPurgeAfter == 0:
        exit()
    # Get current time for comparison
    now = dt.utcnow()
    # Get the supplied path to the HDWX root. This will be the basis for everything we work with.
    hdwxRootPath = sys.argv[2]
    # Get path to hdwxRootPath/metadata/ This is a surprise tool that will help us later...
    metadataTopDir = path.join(hdwxRootPath, "metadata")
    # If this path exists, clean out any temporary files there
    if path.exists(metadataTopDir):
        [remove(fileInTopDir) for fileInTopDir in listdir(metadataTopDir) if fileInTopDir.startswith("tmp") and "." not in fileInTopDir]
        # Get path to hdwxRootPath/metadata/products/
        runsMetadataDir = path.join(metadataTopDir, "products")
        # if there's no data, at all, then we don't need to do any cleaning, so to be sure these paths exist first
        if path.exists(runsMetadataDir):
            # metadataTopDir contains a subdirectory for each productID
            for productID in listdir(runsMetadataDir):
                # Get path to the product's subdir
                productMetadataDir = path.join(runsMetadataDir, productID)
                # Each product subdir contains a json file for every run of the product
                for runFileName in listdir(productMetadataDir):
                    try:
                        # The filename of the json file is a time in UTC, formatted as %Y%m%d%H%M, so convert this to a datetime object
                        runTime = dt.strptime(runFileName, "%Y%m%d%H%M.json")
                    except:
                        remove(path.join(productMetadataDir, runFileName))
                        continue
                    # The "associated data" is stored in hdwxRootPath+productPath+pathExtension
                    # First we need the productPath, which can be obtained from hdwxRootPath/metadata/<productID>.json (This is where that "metadataTopDir" comes in)
                    with open(path.join(metadataTopDir, productID+".json"), "r") as jsonRead:
                        # Read the json file
                        productData = json.load(jsonRead)
                    # For satellite data, we only want to keep half of the purge threshold
                    if "satellite" in productData["productPath"]:
                        thresholdTime = now - hoursToPurgeAfter/2
                    else:
                        thresholdTime = now - hoursToPurgeAfter
                    # If the time older than the purge threshold then we want to purge it and all associated data
                    if runTime < thresholdTime:
                        # We want to keep ADRAD data for one year though
                        if "ADRAD" in productData["productDescription"]:
                            if runTime > now - timedelta(days=365):
                                continue
                        # Now we retrieve the productPath from the freshly read in dict
                        productPath = productData["productPath"]
                        # Now we need the pathExtension which can be obtained from the run's json file, in hdwxRootPath/metadata/products/<productID>/<runtime>.json
                        runFilePath = path.join(productMetadataDir, runFileName) 
                        with open(runFilePath) as jsonRead:
                            runData = json.load(jsonRead)
                        runPathExtension = runData["pathExtension"]
                        if "gr2a" not in productPath:
                            # Now we know where the frames for this product are located, and we can purge them!
                            if path.exists(path.join(hdwxRootPath, productPath, runPathExtension)):
                                rmtree(path.join(path.join(hdwxRootPath, productPath), runPathExtension))
                            # Also remove the json data
                            if path.exists(runFilePath):
                                remove(runFilePath)
