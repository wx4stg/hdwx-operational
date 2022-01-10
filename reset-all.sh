#!/bin/bash
startingDir=`pwd`
relMyDir=`dirname $BASH_SOURCE`
myDir=`realpath $relMyDir`
productDirs=(*/)
for productDir in "${productDirs[@]}"
do
    cd $productDir
    bash reset.sh
    cd $myDir
done
cd $startingDir
