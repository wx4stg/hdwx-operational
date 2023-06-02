#!/bin/bash
startingDir=`pwd`
relMyDir=`dirname $BASH_SOURCE`
myDir=`realpath $relMyDir`
productDirs=(*/)
for productDir in "${productDirs[@]}"
do
    cd $productDir
    python3 cleanup.py
    cd $myDir
done
cd $startingDir
