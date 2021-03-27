import os
import sys
import gensim
import smart_open
import collections
import random
import json
import os.path
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile
import time
from corpus_indexer import CorpusIndexer

class CorpusModeler:
    def __init__(self, model_name, corpus_name=""):
        self.model_name = model_name
        self.corpus_name = corpus_name
        self.corpus_file = f"{self.corpus_name}.cor"
        self.corpus_index = f"{self.corpus_name}.json"
        self.settings_file = f"/models/{self.model_name}.json"
        self.model_file = f"/models/{self.model_name}.model"
        self.load()

    def build(self):
        self.__build_model()


    def load(self):
        self.__load_or_create_settings()
        self.__load_model()        


    def save(self):
        self.__save_settings()
        self.__save_model()



    def __load_or_create_settings(self):
        if(os.path.exists(self.settings_file)):
            with open(self.settings_file) as f:
                content = f.read()
                self.settings = json.loads(content)
                self.corpus_file = self.settings["corpus_file"]
                self.corpus_index = self.settings["corpus_index"]
                self.model_file = self.settings["model_file"]
                self.corpus_name = self.settings["corpus_name"]
                self.model_name = self.settings["model_name"]
                
        else:   
            with open(self.settings_file, "w+") as f:
                empty_content = json.dumps({})
                f.write(empty_content)
                self.settings = {
                    "vector_size": 70,
                    "min_count":2,
                    "epochs":20,
                    "dm":0,
                    "corpus_name": self.corpus_name,
                    "corpus_file": self.corpus_file,
                    "corpus_index": self.corpus_index,
                    "model_file": self.model_file,
                    "model_name": self.model_name
                }
            self.__save_settings()


    def __save_settings(self):
        content = json.dumps(self.settings)
        with open(self.settings_file, "w") as f:
            f.write(content)

    def __save_model(self):
        fname = get_tmpfile(self.model_file)
        self.model.save(fname)

    def __read_corpus(self, fname, tokens_only=False):
        with smart_open.open(fname, encoding="iso-8859-1") as f:
            for i, line in enumerate(f):
                tokens = gensim.utils.simple_preprocess(line)
                if tokens_only:
                    yield tokens
                else:
                    # For training data, add tags
                    yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

    def __build_model(self):
      train_corpus = list(self.__read_corpus(self.corpus_file))
      model = gensim.models.doc2vec.Doc2Vec(vector_size=self.settings["vector_size"],
                                            min_count=self.settings["min_count"],
                                            epochs=self.settings["epochs"],
                                            dm=self.settings["dm"])
      model.build_vocab(train_corpus)
      model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
      self.model = model

    def __load_model(self):
        if (os.path.exists(self.model_file)):
            self.model = Doc2Vec.load(self.model_file)
        else:
            model = None


    def gen_data(self, test_file):
        if(self.model == None):
            print("Must Load of Build a Model to test")
        else:
            self.__gen_data(test_file)

    def __gen_data(self, test_file):
        test_corpus = list(self.__read_corpus(test_file, tokens_only=True))
        data = []
        for doc in test_corpus:
            inferred_vector = self.model.infer_vector(doc)
            sims = self.model.docvecs.most_similar([inferred_vector], topn=len(self.model.docvecs))
            ranks = self.__build_ranks(sims)
            data.append({"doc": doc, "ranks": ranks})
        self.__save_data(data)

      #print('Test Document ({}): «{}»\n'.format(doc_id, ' '.join(test_corpus[doc_id])))
      #print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % self.model)
      #for label, index in [('MOST', 0), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
      #  print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(train_corpus[sims[index][0]].words)))

    def __save_data(self, data):
        content = json.dumps(data)
        with open(f"/outputs/{self.model_name}-{time.time()}output.json", "w") as f:
            f.write(content)

 
    
    def __build_ranks(self, sims):
        corpus_indexer = CorpusIndexer(self.corpus_index)
        data = []
        for sim in sims:
            desc = corpus_indexer.get_description(sim[0]) 
            point = {"id": int(sim[0]), "rank": float(sim[1]), "description": desc} 
            data.append(point)
        return data
