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
    outDir=`realpath $startingDir/$productDir/output/`/.
    rsync -r $outDir /var/www/html/wx4stg/
done
cd $startingDir
