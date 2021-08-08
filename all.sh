#!/bin/sh
startingDir=`pwd`
myDir=`dirname $BASH_SOURCE`
cd $myDir
productDirs=(*/)
for productDir in "${productDirs[@]}"
do
    cd $productDir
    bash generate.sh
    cd $myDir
    rsync -r $productDir/output/. /var/www/html/wx4stg/
done
mkdir -p $myDir/metadata/
~/miniconda3/envs/HDWX/bin/python3 writeProductTypeData.py
rsync -r $myDir/metadata/. /var/www/html/wx4stg/metadata
rm -rf $myDir/metadata/
cd $startingDir
