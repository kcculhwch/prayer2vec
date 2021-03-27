import re
import sys
import os
import os.path
from smart_open import open
from corpus_indexer import CorpusIndexer

class PreProcessor:

    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            self.original_content = f.read()

    def basic(self):
        self.processed_content = self.normalization_setting_1(self.original_content)        

    def separated(self):
        self.processed_content = self.normalization_setting_2(self.original_content)

    def stripped(self):
        self.processed_content = self.normalization_setting_3(self.original_content)

    # normalization 1
    # basic text each paragraph separated by 
    # a double new line
    def normalization_setting_1(self, contents):
      contents = self.remove_symbols(contents)
      contents = self.remove_line_breaks(contents)
      contents = self.set_lower_case(contents)
      return contents

    # normalization 2
    # for extracting rubric elements not spoken
    # and placing them at the beginning
    def normalization_setting_2(self, contents):
      instructions, contents = self.extract_instructions_and_speakers(contents)
      titles, contents = self.extract_titles(contents)
      contents = instructions + titles + contents
      contents = self.normalization_setting_1(contents)
      return contents

    def normalization_setting_3(self, contents):
      instructions, contents = self.extract_instructions_and_speakers(contents)
      titles, contents = self.extract_titles(contents)
      contents = self.normalization_setting_1(contents)
      return contents

    def set_lower_case(self, contents):
        return contents.lower()

    def remove_symbols(self, contents):
      contents = re.sub("[^a-zA-Z\s]", "", contents)
      return contents

    def remove_line_breaks(self, contents):
      # join lines that are broken for spacing
      contents = re.sub(r"\n([^\n])", r" \1", contents, 0, re.M)
      # join lines that are part of the same text
      contents = re.sub(r"\n([^\n])", r" \1", contents, 0, re.M)

      # remove space at beginning of line
      contents = re.sub(r"\n\s*", "\n", contents, 0, re.M)

      # remove extraneous new lines
      contents = re.sub(r"^\n", "", contents, 0, re.M)
      contents = re.sub(r"\s{2,}", " ", contents, 0, re.M)

      # remove short lines - 5 words or fewer
      contents = re.sub(r"^(\w*\s?){1,5}$", "", contents, 0, re.M)

      contents = re.sub(r"[\n]{2,}", "\n", contents, 0, re.M)

      return contents 

        # _xxx_ instruction or person name or latin name
        # __xxx__ prayer name
        # ___xxx___ spoken response
        # # xx heading
        # ## xx sub heading
        # ### heading 3
        # [ xxx ] Scripture notation
        # **xx** prayer name

    def extract_instructions_and_speakers(self, contents):
        patterns = [
            r"([^_]|^)(_{1}[^_]+_{1})([^_])",
        ]
        instructions = ""
        for pattern in patterns:
            results = re.finditer(pattern, contents)
            for m in results:
                instructions += f"{m.groups()[1]}\n\n"
                #print(m.groups()[1])
            contents = re.sub(pattern, r"\1\3", contents, 0, re.M)
        return instructions, contents

    def extract_titles(self, contents):
        patterns = [
            r"([^#]|^)(#{1,3}[^#|^\n]+)()",
            r"([^_]|^)(_{2}[^_|^\n]+_{2})([^_])",      
        ]

        titles = ""
        for pattern in patterns:
            results = re.finditer(pattern, contents)
            for m in results:
                titles += f"{m.groups()[1]}\n\n"
                #print(m.groups()[1])
            contents = re.sub(pattern, r"\1\3", contents, 0, re.M)
        return titles, contents

    def create_output_paths(self, input_path):
      without_corpus = re.sub("^\/?corpus\/", "", input_path)
      without_file = re.sub("\/[^\/]+$", "", without_corpus)
      dirNames = [
        f"/normalized/{without_file}/1",
        f"/normalized/{without_file}/2",
        f"/normalized/{without_file}/3"
      ]
      try:
        os.makedirs(dirNames[0])
      except FileExistsError:
        print("Type 1 Directory Already Exists")
      try:
        os.makedirs(dirNames[1])
      except FileExistsError:
        print("Type 2 Directory Already Exists")
      try:
        os.makedirs(dirNames[2])
      except FileExistsError:
        print("Type 3 Directory Already Exists")


      return dirNames

    def get_name(self, input_path):
      segs = input_path.split("/")
      result = segs[len(segs) - 1]
      return result

    def write_file(self, text, dirName, name):
      oFile = open(f"{dirName}/{name}", "w")
      oFile.write(text)
      oFile.close()


    def normalize(self):        
        outDirs = self.create_output_paths(self.filename)
        name = self.get_name(self.filename)
        self.basic()
        self.write_file(self.processed_content, outDirs[0], name)
        self.separated()
        self.write_file(self.processed_content, outDirs[1], name)
        self.stripped()
        self.write_file(self.processed_content, outDirs[2], name)
 
class CorpusConcatenator:
    def __init__(self, num):
        self.num = num

    def create_corpus_file(self):
        with open(f"/normalized/{self.num}.cor", "w") as f:
            f.write("")
    def concat_normalized_corpus(self, path = "/normalized"): 
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    self.concat_normalized_corpus(f"{path}/{entry.name}")
                if not entry.name.startswith('.') and entry.is_file():
                    if path.endswith(f"{self.num}"):
                        self.concat_out(path, entry.name)

    def concat_out(self, input_path, input_file):
        file_contents = self.get_file(f"/normalized/{self.num}.cor")
        next_file_contents = self.get_file(f"{input_path}/{input_file}")
        if(next_file_contents[-1] != "\n"):
            next_file_contents += "\n"
        self.index_next_file(f"{input_path}/{input_file}")
        file_contents += next_file_contents
        with open(f"/normalized/{self.num}.cor", "w") as f:
            f.write(file_contents)

    def get_file(self, path): 
        with open(f"/{path}", "r") as iFile:
            file_text = iFile.read()
        return file_text

    def create_index(self):
        self.corpus_index = CorpusIndexer(f"/normalized/{self.num}.json")
        self.corpus_index.clear()

    def index_next_file(self, filename):
        length = self.get_file_length(filename) - 1
        index_length = len(self.corpus_index.index)
        if index_length > 0:
            low = self.corpus_index.index[index_length - 1]["high"] + 1
        else:
            low = 0           
        description = re.sub("\/[\d]+\/", "/", filename) 
        description = re.sub("[\/]?normalized\/", "", description)
        self.corpus_index.add_entry(low, low + length, description)        

    def get_file_length(self, filename):
        with open(filename) as f:
            length = 0
            for i in enumerate(f):
                length += 1
        return length

if len(sys.argv) > 1:	
  for file_name in sys.argv:
    if file_name != "./pre_process.py":
        preprocessor = PreProcessor(f"/{file_name}")
        preprocessor.normalize()
  for i in range(1, 4):
        concatenator = CorpusConcatenator(i)
        concatenator.create_index()
        concatenator.create_corpus_file()
        concatenator.concat_normalized_corpus()
        concatenator.corpus_index.save()
else:
  display_help()


def display_help():
   print("Must supply path to corpus text")  

