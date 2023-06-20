# Python HDWX
---
~ Modular, future-proofed, clusterable, portable HDWX product generation with metadata/API for custom clients

## Installation

### Pre-requisites

- Python HDWX has been tested on Fedora 38, CentOS 7, and Ubuntu 20.04 and 22.04. You'll need an operating system (duh), generally Linux with systemd. macOS might work as a server host with the `systemd` pacakge from [homebrew](https://brew.sh), but that's not really intended. At the time of writing this, I don't ever intend to add support for Windows, and I wouldn't recommend anyone trying (it will be very difficult).
- Clone this repository. `git clone https://github.com/wx4stg/hdwx-operational --recursive` (*important: with the* `--recursive` *flag*) to somewhere on your computer. This can realistically be anywhere, but on everything I've done, I've always just shoved it in my home folder, `~/hdwx-operational/`. You need to clone the repository as the user you want to generate the products as. You should NOT clone the repository as root or with sudo -s or sudo git clone, unless you actually want the root user to be generating products which just seems like a bad idea to me.

### Installation process

The install of Python HDWX is generally two parts: setting up a python environment and installing the systemd services. Both steps can be handled by the automatic install script, or you do these manually. I highly highly recommend you use the automatic install script because it'll be much faster and less likely to do something bad, but I've included a general process for doing it manually. I also worked really hard on that script and it will make me sad if no one uses it :(

#### Automatic install

To use the automatic install script, you need to have python installed on your system. You can install python using the appropriate command below for your OS:

Fedora:
`sudo dnf install python3`

CentOS:
`sudo yum install python3`

Ubuntu:
`sudo apt install python3`

macOS: get python from https://python.org and use the installer. As previously noted, you'll need to install homebrew from https://brew.sh and use it to install systemd, `brew install systemd`

You can run the install script using "flavored" python, anaconda or conda or mamba or micromamba or whatever other newfangled python managers there are these days, but you should run the script from the "base" environment, and I recommend letting the script install micromamba and an HDWX environment rather than doing that manually (but if you insist to do it manually, see the "Manual install -- python environment" section of this document)

To run the automatic install, `cd` to the directory you cloned the repository to, if you're following verbatim, `cd ~/hdwx-operational/` and then simply run `sudo python3 install.py --install`.
The install script will require some input for configuration. I have set the default options of this script in such a way that it will configure HDWX in the exact way that it was on wxgen3.geos.tamu.edu when I wrote this documentation, so if you're trying to replicate (or recover) that, then just accept the defaults for everything

- Where would you like product images and metadata to be rsynced to? \[`/wxgen3/products`\]:

You need to input where you would like the image files and JSON metadata to be sent to. This can be a local directory or a remote target in the format \<user>@\<host>:\<remote-path> (if using the latter, see the "Clustered Install" section of this document for additional considerations) If you specify a local directory, if the directory does not exist, the install script will attempt to create it. If this fails, you'll be prompted to specify another path. If you specify a remote directory, no such check is performed.

- How long (in hours) should products be retained before cleanup? \[168\]:

Every two hours, a cleanup script is run to purge old data from the output directory. This prevents the output from becoming too large. If you want to disable this cleanup completely, input 0.

- If you already have conda/mamba installed and configured with an 'HDWX' environment, please enter the path to your install. If an HDWX environment is not detected, you will be given the option to install micromamba in the location provided. \[`/opt/mamba`\]:

Product generation requires several niche python libraries to be installed. I recommend specifying a path outside your home folder, especially if the user account you want to generate products with has a network home folder. I chose /opt/mamba and have had no issues keeping the HDWX environment separate from my development environments on other machines. 

Assuming you don't already have an environment at the location you provide, you will then be prompted whether you want to automatically install micromamba and the correct packages for HDWX. Answer "yes" to that. *This will install micromamba for x86_64 linux. If you're using macOS or a different processor architecture (like arm64 on a raspberry pi or something), then you'll need to answer "no" and perform the manual install instructions.*

The install script will then handle the installation of the python environment and the systemd services.

#### Manual install -- python evnironment

The python environment can also be installed manually. You will need to install and use one of the following python distributions (or something that's conda compatible):

- [Anaconda](https://www.anaconda.com/download/) -- comes with a fancy GUI and a very large base environment. Closed source/proprietary, licenscing disallows commercial use. Included in the ATMO lab image at /opt/conda/ 

- [miniconda](https://docs.conda.io/en/latest/miniconda.html) -- same as above but no GUI or preinstalled pacakges.

- [miniforge](https://github.com/conda-forge/miniforge) -- miniconda, but open source/community maintained and without the licenscing restrictions.

- [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) -- miniforge, but rewritten in C++ to be much faster. **This is the one I use and the one I'd recommend.**

Once you have your preferred package manager installed, you'll need to import the HDWX environment. For Anaconda/miniconda/miniforge, you can do this by typing `conda env create -f hdwx-env.yml`, or for micromamba, `micromamba env create --file hdwx-env.yml`. This environment file will install the correct packages and the versions of the packages that worked when I wrote this documentation. If that doesn't work, the old versions of these packages may have been removed. You can attempt to install the latest versions by running `conda env create -f hdwx-dev-env.yml` or `micromamba env create --file hdwx-dev-env.yml`. 

If all else fails, you can try to manually install by running:

`conda create --name HDWX`

`conda activate HDWX`

`conda install metpy natsort cfgrib atomicwrites scikit-learn lxml xarray arm_pyart bs4 siphon html5lib -c conda-forge`. 

Replace "conda" at the start of each line with "micromamba" if you're using that.

Regardless of if the import worked or not, you still have a few more packages to get via pip that are not available from conda-forge. To install these, you'll need to run:

`conda activate HDWX` (or `micromamba activate HDWX`)

`pip install maidenhead aprslib ecmwf-opendata`

`pip install git+https://github.com/deeplycloudy/xlma-python`

Finally, you'll need to take note of where you just installed conda. This location can be obtained using `conda info` or `micromamba info` and looking at the path listed as "base environment". You can now proceed to use the install script to install systemd services, just provide the path you just got from conda info when asked if you already have conda/mamba installed.

#### Manual install -- systemd services

I'm not sure why you wouldn't just use the install scripts to handle this, as there isn't really an advantage to doing it manually, but alright. hdwx-operational contains many subdirectories, each one is a different submodule that generates its own products. Each submodule has a subdirectory called "services". These subdirectories contain systemd unit files. There are also two more unit files, `hdwx_productTypeManagement.service` and `hdwx_cleanup.service` in the top level of this repository. You need to manually edit each systemd unit file to replace:

`$targetDir` with the path or remote host you want to rsync product generation data to

`$pathToPython` with the path to the python executable you want to use to generate products. This is usually your conda install directory with /envs/HDWX/bin/python3 appended to it, for example, `/opt/mamba/envs/HDWX/bin/python3`

`$pathToClone` with the absolute path that this repository has been cloned to

`$timeToPurge` with the number of hours until you want old data to be deleted

`$myUsername` with the user that you want to run the product generation. That user must have the proper permissions set to access both the input and output locations for product generation.

Once you're done wasting your time by editing the unit files, you'll have to copy all of them to `/etc/systemd/system/` along with the `hdwx.target` file in the top level of this repository. For each of the files, type:

`sudo systemctl enable <filename>`

`sudo systemctl start <filename>`

I promise, the install script is much easier.

#### Clustered install

HDWX can be installed in a clustered format if you want to have different servers processing different modules. Simply clone this repository to multiple machines, divide the submodules into groups for each machine, and delete all except the submodules you want to run on each. One server needs to be the "master" which rsyncs its output to a local directory, but you can have as many other workers as you like, just point their rsync output to user@host:path of the master server.

It is important to have the master server running at least the productTypeManagement service and the cleanup service as these cannot be run remotely. Both of these services can be run using only the packages included with python, so conda/mamba are not required if that's all you're doing on the main server.

All of the "worker" servers will need to have SSH public key authentication or some other way of noninteractive auth for this to work.

#### TAMU-specific install considerations

*This section is redacted from the public document. The original was shared with several professors and Geosciences IT members in June 2023.*

#### HDWX frontend

Please see https://github.tamu.edu/geos-it/hdwx-atmo for installation instructions. During the installation process, you can set up the api in api/config.php. This requires a "relative path to metadata directory". The "metadata directory" refers to a directory called "metadata" which is contained in the rsync target path that you configure during the install of this repository. You will then need to specify the relative path to that directory from api/ in config.php.

This is overly confusing but I have no idea how it could be less so. PRs accepted, I guess...


## Current state of affairs

In the current operational deployment, this repository is cloned under the 'hdwx' user of wxgen3.geos.tamu.edu and outputs to /wxgen3/products/. Through the magic of NFS mounts, this is somehow transferred to https://hdwx.tamu.edu/products/wxgen3/. ALL of the current configuration parameters are set up as the defaults for the installation script.


## Development

### Creating new products/submodules

A submodule in this repository can create post-processed weather data (this has so far been png images, but technically this is not a strict requirement! I've thought about creating kml or even json products before, just never got around to it) and metadata required to describe them. A submodule CAN generate as many products in as many productTypes as it wants to. I have grouped them somewhat, but again, this is only for organization and not a strict requirement. Also, so far, all of these modules do the post-processing using python, but this is also not a strict requirement, products can be generated using whatever language you want.

So now that we've gotten through the freedoms of what you can do with submodules, here are the limitations:

- Submodule names must take the form hdwx-\<name\>
- Submodules must define at least one systemd service that allows the product to function automatically, which must be stored as a .service.template file in a subdirectory called "services". All services must be prefixed with the submodule's name, ex "hdwx-mymodule.service.template". This service MUST declare `PartOf=hdwx.target` under the `[Unit]` section and `WantedBy=hdwx.target` in the `[Install]` section. The service must also define `User=$myUsername` and `WorkingDirectory=$pathToClone/hdwx-<name>` in the `[Service]` section. If the service uses python, use $pathToPython to represent the python3 executable.
- Submodules must contain a subdirectory called "output" that contains the data and metadata for each product generated by the submodule. productType JSON metadata in particular is especially important to store in output/metadata/productTypes/
- The systemd service is responsible for getting the data to the target directory, I recommend doing this by declaring an `ExecStop=rsync -ulrH ./output/. $targetDir --exclude=productTypes/ --exclude="*.tmp"` in the `[Service]` section of any systemd service that performs postprocessing of data. If you need the rsync to take place more frequently than "once per product generation cycle", you can define a completely separate service just for rsync, see [hdwx-modelplotter](https://github.com/wx4stg/hdwx-modelplotter) as an example of this.
- Metadata outputs should be defined in HDWX_helpers.py. This file automatically gets copied from the top level of the clone of hdwx-operational, where it can then be imported by a plotting script. Add new products to the long if/elif chain under the "writeJson" function, then call import HDWX_helpers and call "HDWX_helpers.writeJson" from your plotting script (see the file history/git blame for HDWX_helpers.py for examples). This keeps an inherent record of all products that currently exist.
- Data outputs should be branded using HDWX_helpers.dressImage for standard branding

From a "theory of operation" point of view, most submodules have a "data ingest" stage and a "processing/output" stage. I generally use separate scripts for each, hdwx-adrad, hdwx-hlma, and hdwx-modelplotter all follow this general principle. Sometimes the data ingest can be combined into the processing, like in hdwx-satellite or hdwx-mesonetplotter. As long as the data and metadata end up in ./output/, you should be alright. 

I have uploaded a video to YouTube describing the creation of a submodule, specificially, hdwx-wpcsfc: https://youtu.be/gGlU4K3E-cI It is over an hour long and probably best enjoyed at 2x speed. I was very detailed, perhaps overly so.

If you just want to add new model products, you probably don't need to create a whole new submodule for that. 

The modelFetch.py script is designed to be somewhat modular to allow bringing new data easily. Near the top of the file, there are dictionaries for parameters to fetch from the ECMWF and NCEP models. The keys of the dictionary define either (A) the filename to save the grib data or (B) for a composite of multiple variables, the parameter to pass to modelPlot.py. The values of the dictionary define how to donwload the file. For ECMWF, this is a list of variable names to request via ecmwf-opendata, [the documentation](https://pypi.org/project/ecmwf-opendata/) has a list of all possible variables. For NCEP models, this interfaces with [NOMADS' GRIB filter](https://nomads.ncep.noaa.gov). From the linked page, you can click "GRIB Filter" on any model, then select the variable and levels you want. The website has a nice feature where if you click the name of a variable, it will highlight the levels that variable is valid for. Your goal should be to keep the download size as small as possible. "Least power to accomplish the mission" as they say in amateur radio. NCEP also allows getting a subregion instead of downloading the whole global dataset. I've always used a subset of -144.5 through -44.5 longitude and 14.5 through 54.5 latitude. Once you have your variables, levels, and subregion selected, click "show URL" at the bottom. You need to copy the &lev=, &var=, and &subregion= parameters from the URL and paste it as the value for the key you created in the dictionary. For composites of multiple variables, the files are downloaded in order from first key to last key of the dictionary, so for example, the NCEP variable list starts with temperature at 2m, winds at 10m, and surface barometric pressure and orography. The fourth key is "sfccomposite", which is 2m T, 10m wind, and surface MSLP. This requires the previous three files, hence why "sfccomposite" is listed after those three. The value for that key is an empty string, which tells the fetch script that everything needed is already downloaded, just pass "sfccomposite" to modelPlot.py. For ECMWF models, use an empty list instead of an empty string to denote this.

The modelPlot.py script is significantly less modular and is designed to be a dumpster fire. At the bottom of the file, there's a long if-elif chain checking what the requested field to plot is (these are identical to the keys of the dictionary in the modelFetch script), and making sure the paths of the files they require actually exist. 

I uploaded another video to YouTube describing the addition of a new model product, https://youtu.be/FVvbpelOcl0. This one is just under an hour, so I did a little better than the first one, but it still gets a little rambly so probably watch it at 1.5x speed.

### API Specification

#### Object Types

*Definitions of expected format when requesting data.*

productType


productTypes represent groups of products that should be sorted together.

- productTypeID: (int) unique numerical identifier for the productType
- productTypeDescription: (string) description of the productType
- products: (array) list of product objects associated with the productType

product

products represent individual compiled data sources

- productID: (int) unique numerical identifier for the product.
- productDescription: (string) description of the product.
- productPath: (string) Either a URI, assumed to be relative to the hdwx server, to reach this product, OR a full URL to an external product. If productPath contains the substring "http", it is an external product, if not, it is a local product. See "URL Requests" for more information.
- productReloadTime: (string) the minimum time delay in seconds after the lastReloadTime that a product could publish new data. There may not be new data immediately after this delay, but there definitely won't be any before.
- lastReloadTime: (string) Date and time the product was last reloaded by the server, formatted as "yyyyMMddHHmm" [NSDateFormatter](https://nsdateformatter.com/) or "%Y%m%d%H%M" [strftime](https://strftime.org/).
- isForecast: (bool) true if the product is a prognostic forecast, false if the product is diagnostic observational data.
- isGIS: (bool) true if the product has GIS metadata for mapping its frames to a map.
- fileExtension: (string) The file type of the frame for the product.

productRun

ProductRuns represent one particular initialization of a product

- publishTime: (string) Date and time the run was originally published to the hdwx server, formatted as "yyyyMMddHHmm" [NSDateFormatter](https://nsdateformatter.com/) or "%Y%m%d%H%M" [strftime](https://strftime.org/).
- pathExtension: (string) appended to the productPath to reach a particular run of a product. See "URL Requests" for more information.
- runName: (string) the display name of the run
- availableFrameCount: (int) products may take a long time for a run to complete in its entirety. This represents the number of frames that have completed generation and are ready to be displayed. If a run has completed, this will be equal to the totalFrameCount
- totalFrameCount: (int) the total number of frames a productRun has when all frames have been generated.
- productFrames: (array) an array of productFrame objects that represent available frames for a product.

productFrame

productFrames are the metadata associated with a single time of a single product

- filename: (string) the name of the file for a frame, to be appended to the pathExtension string. See "URL Requests" for more information.
- gisInfo: (array) An array of the southwest and northeast lat/lon coordinates formatted as "lat,lon". The southwest corner will be the first object in the array, the northeast corner will be the second object. For non-GIS aware products ("isGIS" is False), both corners will be 0,0 and should be ignored.
- fhour: (int) for products that are forecasts, the number of hours after initialization that the frame is valid for. Will always be 0 for non-forecasts and should be ignored.
- valid: (string) Date and time the frame is valid for, formatted as "yyyyMMddHHmm" [NSDateFormatter](https://nsdateformatter.com/) or "%Y%m%d%H%M" [strftime](https://strftime.org/).
