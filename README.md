# prayer2vec

## Directories

- [corpus](corpus)
  - Repository of texts
- [models](models)
  - Storage for models
- [normalized](normalized)
  - Storage for normalized texts
- [build](build)
  - Code for the project

## Installing and Building

[Build Instructions Here](BUILD.md)


## Running the tools
From the root of the project run
`p2v OPTIONS`

### Options
`word2vec ARGS` to run word2vec command directly

`pre corpus/x/x` to normalize the text

`raw COMMANDS` to run raw commands in the env

#### TODO
Will add more options for particular functions as we need them.
- train /corpus/x/x/ /model/x/x/
- etc


## Corpus
Corpus will be bundled in /corpus in the container. It is also mounted over the top of the container so you will not need to rebuild if yout make changes to it.

## Models
Models will be bundled in /models in the container. It is also mounted over the top of the container so you will n
ot need to rebuild if yout make changes to it.

## Normalized
Normalized text filed are bundled in /normalized in the container. It is also mounted over the top of the container so you will not need to rebuild if yout make changes to it.
