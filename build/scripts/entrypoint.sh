#!/bin/bash

if [ -z $1 ]
then
   echo "OPTIONS word2vec|raw"
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
fi

if [[ $1 == "raw" ]]
then
  echo "Running raw commands: $ARGS"
  eval $ARGS
fi
