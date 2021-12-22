#!/bin/bash
source config.txt
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
    outDir=`realpath $myDir/$productDir/output/`/.
    rsync -ur $outDir $targetDir
done
python3 cleanupHDWX.py $purgePlotsAfter $targetDir
cd $startingDir
