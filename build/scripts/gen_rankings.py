import sys
from corpus_modeler import CorpusModeler 

def display_help():
  print("Must Supply Model Name  and Doc to gen ranks for")

if len(sys.argv) > 2:	
    cm = CorpusModeler(sys.argv[1])
    cm.gen_data(sys.argv[2])

else:
  display_help()

