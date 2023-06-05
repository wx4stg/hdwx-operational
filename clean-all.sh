#!/bin/bash
startingDir=`pwd`
relMyDir=`dirname $BASH_SOURCE`
myDir=`realpath $relMyDir`
productDirs=(*/)
for productDir in "${productDirs[@]}"
do
    cd $productDir
    if [ -f HDWX_helpers.py ]; then
        rm HDWX_helpers.py
    fi
    cp ../HDWX_helpers.py ./
    python3 cleanup.py
    cd $myDir
done
cd $startingDir
