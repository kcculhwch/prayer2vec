#!/bin/bash

if [ -z $1 ]
then
   echo "OPTIONS word2vec|pre|train|raw"
fi

ARGS=""
 iter=1
 for i in $*; do
   if [[ $iter > 1 ]]
   then  
     ARGS="${ARGS}${i} "
   fi
   iter=$iter+1
 done

if [[ $1 == "word2vec" ]]
then
 echo "Running word2vec with: $ARGS"
 word2vec $ARGS
elif [[ $1 == "train" ]]
then
 echo "not implemented"
elif [[ $1 == "raw" ]]
then
  echo "Running raw commands: $ARGS"
  eval $ARGS
elif [[ $1 == "pre" ]]
then
  echo "Running preprocessor: $ARGS"
  python ./pre_process.py $ARGS
fi
