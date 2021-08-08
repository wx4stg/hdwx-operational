#!/usr/bin/env python3
# JSON/Metadata pre-push script for python-based HDWX
# Created 7 August 2021 by Sam Gardner <stgardner4@tamu.edu>
import json
from pathlib import Path
from datetime import datetime as dt

if __name__ == "__main__":
    timeInt = int(dt.utcnow().strftime("%Y%m%d%H%M"))
    radarAndSatelliteDescriptions = ["Local Radar Mosaic", "Local Radar Mosaic", "Regional Radar Mosaic", "Regional Radar Mosaic", "National Radar Mosaic", "National Radar Mosaic"]
    radarAndSatellitePaths = ["gisproducts/radar/local/", "products/radar/local/", "gisproducts/radar/regional/", "products/radar/regional/", "gisproducts/radar/national/", "products/radar/national/"]
    radarAndSatelliteProducts = list()
    for i in range(6):
        productDict = {
            "productID" : i,
            "productDescription" : radarAndSatelliteDescriptions[i],
            "productPath" : radarAndSatellitePaths[i],
            "productReloadTime" : 300,
            "lastReloadTime" : timeInt,
            "isForecast" : False,
            "isGIS" : "gis" in radarAndSatellitePaths[i]
        }
        radarAndSatelliteProducts.append(productDict)
        productSavePath = Path(__file__).parent.joinpath("metadata").joinpath("products").joinpath(str(i)+".json")
        Path.mkdir(productSavePath.parent, parents=True, exist_ok=True)
        with open(productSavePath, "w") as jsonWrite:
            json.dump(productDict, jsonWrite, indent=4)
    radarAndSatelliteType = {
        "productTypeID" : 0,
        "productTypeDescription" : "Radar & Satellite",
        "products" : radarAndSatelliteProducts
    }
    typeSavePath = Path(__file__).parent.joinpath("metadata").joinpath("productTypes").joinpath("0.json")
    Path.mkdir(typeSavePath.parent, parents=True, exist_ok=True)
    with open(typeSavePath, "w") as jsonWrite:
        json.dump(radarAndSatelliteType, jsonWrite, indent=4)