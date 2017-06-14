## We want to make sure the run is completed, so we should 
## work in pairs of pickles and logs...

## arguments: filename, parameter with = and level, level 

#! /usr/bin/env sh

filename=$1
logf=$filename'.log' ## log
dataf=$filename'.p' ## data

par=$2 ## parameter and level to look for
lvl=$3
di='/home/daniel/Documents/ABM/FA/sweeps/results/endo_disp/disp'$lvl


if [ -e "$dataf" ] && [ -e "$logf" ]; then
    clear
    ## look for the par value given:
    if head -n 2 $logf | grep $par -q; then
        echo "found it, moving it"
        mv $dataf $di; mv $logf $di  
    else 
        echo "wrong level?"
    fi
    echo "$a is."
elif [ -e "$dataf" ] && [ ! -e "$logf" ]; then
    clear
    echo "$a is not finished."
elif [ ! -e "$dataf" ] && [ ! -e "$logf" ]; then 
    clear
    echo "According to my records, $a does not exist"
fi

echo $dataf; echo $logf; echo $par

## so if it has both files, we move it to its own directory. 

