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

macOS: get python from https://python.org and use the installer

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

If you want the API to work, you'll need to clone [hdwx-api](https://github.tamu.edu/samgardner4/hdwx-api) to a location that will be served to the internet by your website stack and edit `config.php` to contain the parameters it's asking for.


