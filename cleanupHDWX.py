#!/usr/bin/env python3
# Cleanup/resource management for next-gen HDWX server root
# Created 21 December 2021 by Sam Gardner <stgardner4@tamu.edu>

import sys
from datetime import datetime as dt, timedelta
from os import path, listdir, remove
from shutil import rmtree
import json

# cleanupHDWX.py <purgeAfterHours> <HDWX server root>
if __name__ == "__main__":
    # Get current time for comparison
    now = dt.utcnow()
    # Get desired time to purge files after from arg 1
    hoursToPurgeAfter = timedelta(hours=int(sys.argv[1]))
    # Get the supplied path to the HDWX root. This will be the basis for everything we work with.
    hdwxRootPath = sys.argv[2]
    # Get path to hdwxRootPath/metadata/ This is a surprise tool that will help us later...
    metadataTopDir = path.join(hdwxRootPath, "metadata")
    # Get path to hdwxRootPath/metadata/products/
    runsMetadataDir = path.join(metadataTopDir, "products")
    # if there's no data, at all, then we don't need to do any cleaning, so to be sure these paths exist first
    if path.exists(metadataTopDir) and path.exists(runsMetadataDir):
        # metadataTopDir contains a subdirectory for each productID
        for productID in listdir(runsMetadataDir):
            # Get path to the product's subdir
            productMetadataDir = path.join(runsMetadataDir, productID)
            # Each product subdir contains a json file for every run of the product
            for runFileName in listdir(productMetadataDir):
                # The filename of the json file is a time in UTC, formatted as %Y%m%d%H%M, so convert this to a datetime object
                runTime = dt.strptime(runFileName, "%Y%m%d%H%M.json")
                # If the time older than the purge threshold then we want to purge it and all associated data
                if runTime < now - hoursToPurgeAfter:
                    # The "associated data" is stored in hdwxRootPath+productPath+pathExtension
                    # First we need the productPath, which can be obtained from hdwxRootPath/metadata/<productID>.json (This is where that "metadataTopDir" comes in)
                    with open(path.join(metadataTopDir, productID+".json"), "r") as jsonRead:
                        # Read the json file
                        productData = json.load(jsonRead)
                    # Now we retrieve the productPath from the freshly read in dict
                    productPath = productData["productPath"]
                    # Now we need the pathExtension which can be obtained from the run's json file, in hdwxRootPath/metadata/products/<productID>/<runtime>.json
                    runFilePath = path.join(productMetadataDir, runFileName) 
                    with open(runFilePath) as jsonRead:
                        runData = json.load(jsonRead)
                    runPathExtension = runData["pathExtension"]
                    if "gr2a" not in productPath:
                        # Now we know where the frames for this product are located, and we can purge them!
                        rmtree(path.join(path.join(hdwxRootPath, productPath), runPathExtension))
                        # Also remove the json data
                        remove(runFilePath)