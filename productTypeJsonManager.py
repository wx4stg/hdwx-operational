#!/usr/bin/env python3
# Combines product metadata of the same productType distributed across different submodules
# Created 10 Janurary 2022 by Sam Gardner <stgardner4@tamu.edu>

from os import path, listdir
import json
import sys

if __name__ == '__main__':
    basePath = path.realpath(path.dirname(__file__))
    productModules = list()
    [productModules.append(productModule) for productModule in sorted(listdir(basePath)) if path.isdir(path.join(basePath, productModule)) and productModule != ".git"]
    productTypes = dict()
    for productMod in productModules:
        prodProductTypesDir = path.join(basePath, productMod, "output", "metadata", "productTypes")
        if path.exists(prodProductTypesDir):
            for jsonFile in sorted(listdir(prodProductTypesDir)):
                with open(path.join(prodProductTypesDir, jsonFile), "r") as jsonRead:
                    jsonForProdType = json.load(jsonRead)
                if jsonFile in productTypes.keys():
                    prevProdTypeJson = productTypes[jsonFile]
                    [prevProdTypeJson["products"].append(product) for product in jsonForProdType["products"]]
                else:
                    productTypes[jsonFile] = jsonForProdType
    targetDir = sys.argv[1]
    masterProductTypesDir = path.join(targetDir, "metadata", "productTypes")
    for jsonName in productTypes.keys():
        with open(path.join(masterProductTypesDir, jsonName), "w") as jsonWrite:
            json.dump(productTypes[jsonName], jsonWrite, indent=4)
