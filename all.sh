#!/bin/sh
MY_DIR=`pwd`
cd $HOME/hdwx-operational/
productDirs=(*/)
for productDir in "${productDirs[@]}"
do
    cd $productDir
    bash generate.sh
    cd $MY_DIR
    rsync -r $productDir/output/. /var/www/html/wx4stg/
done

