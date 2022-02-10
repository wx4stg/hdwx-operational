#!/usr/bin/env python3
# Backwards compatibility script to port python HDWX products to GEMPAK HDWX viewer
# Created 2 Feburary 2022 by Sam Gardner <stgardner4@tamu.edu>

import json
from os import path, listdir, symlink, remove, chdir , getcwd
from shutil import copyfile
import imageio

if __name__ == "__main__":
    basePath = path.realpath(path.dirname(__file__))
    metadataDirs = [path.join(basePath, dirPath, "output", "metadata") for dirPath in listdir(basePath) if path.isdir(path.join(basePath, dirPath, "output", "metadata"))]
    productDirs = [[path.join(metadataDir, "products", productID) for productID in listdir(path.join(metadataDir, "products"))] for metadataDir in metadataDirs]
    for productDirGroup in productDirs:
        for productDir in productDirGroup:
            if len(listdir(productDir)) > 0:
                latestRunMetaName = sorted(listdir(productDir))[-1]
                runJsonPath = path.join(productDir, latestRunMetaName)
                with open(runJsonPath, "r") as jsonRead:
                    latestRunMetadata = json.load(jsonRead)
                productID = path.basename(productDir)
                productJsonPath = path.join(path.dirname(path.dirname(productDir)), productID+".json")
                with open(productJsonPath, "r") as jsonRead:
                    productMetadata = json.load(jsonRead)
                productOutPath = path.join(path.dirname(path.dirname(productJsonPath)), productMetadata["productPath"])
                chdir(productOutPath)
                latestRunPath = latestRunMetadata["pathExtension"]
                if latestRunPath != "":
                    symlinkSrc = "latest"
                    if path.exists(symlinkSrc):
                        remove(symlinkSrc)
                    symlink(latestRunPath, symlinkSrc)
                    if productMetadata["isGIS"] == False:
                        chdir(path.join(productOutPath, "latest"))
                        gifFile = ""
                        for pngFile in sorted(listdir(getcwd())):
                            if ".png" in pngFile:
                                for i in range(len(latestRunMetadata["productFrames"])):
                                    frameDict = latestRunMetadata["productFrames"][i]
                                    if pngFile[0] == "0" and pngFile[1:] != ".png":
                                        pngFileComp = pngFile[1:]
                                    else:
                                        pngFileComp = pngFile
                                    if pngFileComp == frameDict["filename"]:
                                        gifFile = "frame"+str(i)+".gif"
                                        if not path.exists(gifFile):
                                            with imageio.get_writer(gifFile, mode="I") as writer:
                                                imageToConvert = imageio.imread(pngFile)
                                                writer.append_data(imageToConvert)
                        if ".gif" in gifFile:
                            copyfile(gifFile, "thumb.gif")
