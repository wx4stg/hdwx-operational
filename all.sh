#!/bin/bash
startingDir=`pwd`
relMyDir=`dirname $BASH_SOURCE`
myDir=`realpath $relMyDir`
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
