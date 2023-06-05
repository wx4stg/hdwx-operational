#!/usr/bin/env python3
# Installer for python HDWX
# Created 31 May 2023 by Sam Gardner <stgardner4@tamu.edu>

import sys
from os import path, system, remove, listdir, getuid, environ
from pathlib import Path
import shutil
import pwd

def installServiceFile(fileName, fileContents, destDir, pathToPython, cloneDir ,timeToPurge, user):
    fileContents = fileContents.replace("$targetDir", destDir)
    fileContents = fileContents.replace("$pathToPython", pathToPython)
    fileContents = fileContents.replace("$pathToClone", cloneDir)
    fileContents = fileContents.replace("$timeToPurge", str(timeToPurge))
    fileContents = fileContents.replace("$myUsername", user)
    with open(f"/etc/systemd/system/{fileName}", "w") as f:
        f.write(fileContents)
    system(f"systemctl enable {fileName}")
    system(f"systemctl start {fileName}")


if __name__ == "__main__":
    if getuid() != 0:
        print("This script needs to be run as root.")
        exit()
    if len(sys.argv) >= 2:
        if sys.argv[1] == "--install":
            if path.exists("/etc/systemd/system/hdwx.target"):
                print("HDWX is already installed, please run with --uninstall to remove the existing installation first.")
                exit()
            cloneDir = path.abspath(path.dirname(__file__))
            print("New HDWX Configuration:")
            while True:
                destDir = input("Where would you like product images and metadata to be rsynced to? [/wxgen3/products]: ")
                if destDir == "":
                    destDir = "/wxgen3/products"
                if path.exists(destDir):
                    if path.isdir(destDir):
                        print("Products will be sent to " + destDir)
                        break
                print("That path does not seem to be a valid directory, please try again...")
            timeToPurge = input("How long (in hours) should products be retained before cleanup? [168]: ")
            if timeToPurge == "":
                timeToPurge = 168
            else:
                timeToPurge = int(timeToPurge)
            print("HDWX will purge product files older than " + str(timeToPurge) + " hours.")
            backwardsCompatibility = input("Would you like to enable backwards compatibility with the upstream JSImagePlayer y/n? [N]: ")
            if "y" in backwardsCompatibility.lower():
                backwardsCompatibility = True
            else:
                backwardsCompatibility = False
            
            myUsername = Path(cloneDir).owner()
            myGroup = Path(cloneDir).group()
            while True:
                print("\n\n")
                print("If you already have conda/mamba installed and configured with an 'HDWX' environment, please enter the path to your conda install.")
                pathToConda = input("If an HDWX environment is not detected, you will be given the option to install micromamba in the loaction provided. [/opt/mamba]: ")
                if pathToConda == "":
                    pathToConda = "/opt/mamba"
                    pathToEnv = path.join(pathToConda, "envs", "HDWX")
                    if path.exists(pathToEnv):
                        break
                    print("\n\n")
                    print("I can install micromamba x86_64 to "+pathToConda+" for you with an environment 'HDWX' for hdwx to run in if you'd like.")
                    print("If you have conda/mamba installed, but no HDWX environment, you should answer NO to the next question.")
                    autoInstall = input("Proceed with installing micromamba? [Y/n]: ")
                    if "y" in autoInstall.lower():
                        print("Downloading micromamba...")
                        system("curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba")
                        Path(pathToConda).mkdir(parents=True, exist_ok=True)
                        shutil.move("bin/micromamba", pathToConda)
                        shutil.rmtree("./bin")
                        environ["MAMBA_ROOT_PREFIX"] = pathToConda
                        shutil.chown(pathToConda, user=myUsername, group=myGroup)
                        shutil.chown(path.join(pathToConda, "micromamba"), user=myUsername, group=myGroup)
                        system(f"sudo -u {myUsername} {pathToConda}/micromamba shell init -s bash -p {pathToConda}")
                        tmpInstallContent = f"#!/bin/bash\nexport MAMBA_ROOT_PREFIX=\"{pathToConda}\"\n{pathToConda}/micromamba env create --file {cloneDir}/hdwx-env.yml -y\n{pathToConda}/envs/HDWX/bin/pip3 install maidenhead ecmwf-opendata aprslib\n{pathToConda}/envs/HDWX/bin/pip3 install git+https://github.com/deeplycloudy/xlma-python"
                        with open("tmpInstall.sh", "w") as f:
                            f.write(tmpInstallContent)
                        shutil.chown("tmpInstall.sh", user=myUsername, group=myGroup)
                        system(f"sudo -u {myUsername} bash tmpInstall.sh")
                        remove("tmpInstall.sh")
                        break
                    elif "n" in autoInstall.lower():
                        print("Ok, please install conda or mamba and import the 'hdwx-env.yml' file in the root of the this repository.\nYou will then need to install maidenhead, ecmwf-opendata, aprslib, and xlma-python via pip.")
                        exit()
            pathToPython = path.join(pathToEnv, "bin", "python3")
            with open("hdwx.target", "r") as f:
                targetFileContents = f.read()
            with open("hdwx_cleanup.service.template", "r") as f:
                cleanupFileContents = f.read()
            with open("hdwx_productTypeManagement.service.template", "r") as f:
                productTypeManagementFileContents = f.read()
            print("Installing HDWX services...")
            installServiceFile("hdwx.target", targetFileContents, destDir, pathToPython, cloneDir, timeToPurge, myUsername)
            installServiceFile("hdwx_cleanup.service", cleanupFileContents, destDir, pathToPython, cloneDir, timeToPurge, myUsername)
            installServiceFile("hdwx_productTypeManagement.service", productTypeManagementFileContents, destDir, pathToPython, cloneDir, timeToPurge, myUsername)
            print("Installing product modules...")
            for submoduleName in listdir(cloneDir):
                submodulePath = path.join(cloneDir, submoduleName)
                if path.isdir(submodulePath) and submoduleName != "operational-metadata":
                    servicesPath = path.join(submodulePath, "services")
                    if path.exists(servicesPath) and path.isdir(servicesPath):
                        for serviceFile in listdir(servicesPath):
                            serviceFilePath = path.join(servicesPath, serviceFile)
                            with open(serviceFilePath, "r") as f:
                                serviceFileContents = f.read()
                            installServiceFile(serviceFile.replace(".service.template", ".service"), serviceFileContents, destDir, pathToPython, cloneDir, timeToPurge, myUsername)
            print(">>> DONE! HDWX has been installed.")
        elif sys.argv[1] == "--uninstall":
            for serviceFile in listdir("/etc/systemd/system/"):
                if serviceFile.startswith("hdwx"):
                    system(f"systemctl stop {serviceFile}")
                    system(f"systemctl disable {serviceFile}")
                    if path.isdir(f"/etc/systemd/system/{serviceFile}"):
                        shutil.rmtree(f"/etc/systemd/system/{serviceFile}")
                    else:
                        remove(f"/etc/systemd/system/{serviceFile}")
            print("HDWX has been uninstalled.")
        else:
            print("Unknown argument: " + sys.argv[1])
            print("Please specify --install or --uninstall")
    else:
        print("Please specify --install or --uninstall")
