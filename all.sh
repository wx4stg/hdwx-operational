#!/bin/sh
MY_DIR=`pwd`
cd $HOME/HDWX-operational/
productDirs=(*/)
for productDir in "${productDirs[@]}"
do
    bash $productDir/generate.sh
    rsync -r $productDir/output/. /var/www/html/wx4stg/
done
cd $MY_DIR
