#!/bin/bash
if [ ! -f ~/mambaforge/envs/HDWX/bin/python3 ]
then
    if [ ! -f ~/miniconda3/envs/HDWX/bin/python3 ]
    then
        echo "HDWX requires a python environment named 'HDWX'"
        echo "Please install mambaforge and run 'mamba env create -f hdwx-env.yml'"
        echo "or instal miniconda and run 'conda env create -f hdwx-env.yml'"
        exit
    fi
fi
if [ "${BASH_VERSINFO:-0}" -lt 5 ]
then
    echo "HDWX requires bash 5.0 or newer. Please upgrade."
    exit
fi
startingDir=`pwd`
relMyDir=`dirname $BASH_SOURCE`
myDir=`realpath $relMyDir`
cd $myDir
source $myDir/config.txt
if [ -z $targetDir ]
then
    echo "Please configure a destination directory in config.txt"
    exit
fi
if [ -z $purgePlotsAfter ]
then
    echo "Please configure how long data should be kept in config.txt"
    exit
fi
productDirs=(*/)
for productDir in "${productDirs[@]}"
do
    cd $productDir
    bash generate.sh
    cd $myDir
    outDir=`realpath $myDir/$productDir/output/`/.
    rsync -ur $outDir $targetDir
done
python3 cleanupHDWX.py $purgePlotsAfter $targetDir
cd $startingDir
