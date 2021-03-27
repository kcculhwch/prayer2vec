import sys
from corpus_modeler import CorpusModeler 

def display_help():
  print("Must Supply Path to and Model File and Corpus")

if len(sys.argv) > 2:	
    cm = CorpusModeler(sys.argv[1], sys.argv[2])
    cm.build()
    cm.save()

else:
  display_help()

