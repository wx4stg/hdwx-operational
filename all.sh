#!/bin/sh
MY_DIR=`pwd`
cd $HOME/hdwx-operational/
productDirs=(*/)
for productDir in "${productDirs[@]}"
do
    cd $productDir
    bash generate.sh
    cd $HOME/hdwx-operational/
    rsync -r $productDir/output/. /var/www/html/wx4stg/
done
mkdir -p $HOME/hdwx-operational/metadata/
~/miniconda3/envs/HDWX/bin/python3 writeProductTypeData.py
rsync -r $HOME/hdwx-operational/metadata/. /var/www/html/wx4stg/metadata
rm -rf $HOME/hdwx-operational/metadata/
cd $MY_DIR
