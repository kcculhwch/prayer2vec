#!/bin/bash


function run {
    case "$1" in
      word2vec)
        echo "Running word2vec with: $2"
            word2vec $2
        ;;
        train)
            echo "not implemented"
        ;;
        raw)
            echo "Running raw commands: $2"
            eval $2
        ;;
        pre)
            echo "Running preprocessor: $2"
            python ./pre_process.py $2
        ;;
        sync)
           sync
           exit 0
           # don't run anything else (including the sync tail runner 
        ;;
    esac
}

function submit {
    args=$(echo $1 | sed s/.$//)
    cmd='aws ecs run-task --task-definition p2v --cluster p2v --network-configuration awsvpcConfiguration={subnets=[subnet-0587fb42d95e1e389]} --overrides '"'"'{"containerOverrides":[{"name":"p2v","command":['$args']}]}'"'"
    eval $cmd
    echo "submitted for processing in cloud"
}

function sync {
    echo "sync corpus up/down"
    echo "sync normalized up/down"
    echo "sync models up/down"
}


if [ -z $1 ]
then
   echo "OPTIONS [queue] word2vec|pre|train|raw|sync"
fi

ARGS=""
iter=1

#Parse Command Arguments
for i in $*; do
  if [[ $iter > 1 ]]
  then  
    if [[ $1 == "queue" ]]
    then
      ARGS="${ARGS}\"${i}\","
    else
      ARGS="${ARGS}${i} "
    fi
  fi
  iter=$iter+1
done

if [[ $1 == "queue" ]]
then
  submit $ARGS
else
  run $1 $ARGS
fi

if [[ -v sync_auto ]]
then
  sync
fi
