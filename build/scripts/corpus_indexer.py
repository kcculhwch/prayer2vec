from smart_open import open
import json
import os.path
class CorpusIndexer:
    def __init__(self, sourceFile):
        self.sourceFile = sourceFile
        self.load()

    def load(self):
        if(os.path.exists(self.sourceFile)):
            with open(self.sourceFile) as f:
                content = f.read()
                self.index = json.loads(content)
        else:   
            with open(self.sourceFile, "w+") as f:
                empty_content = json.dumps([])
                f.write(empty_content)
                self.index = []

    def add_entry(self, low, high, description):
        self.index.append({ "low": low, "high": high, "description": description })

    def remove_entry(self, num):
        self.index.pop(num)

    def clear(self):
        self.index = []

    def save(self):
        content = json.dumps(self.index)
        with open(self.sourceFile, "w") as f:
            f.write(content)
    def get_description(self, num):
        for elet in self.index:
            try:
                index = list(range(elet["low"], elet["high"] + 1)).index(num)
                return elet["description"]
            except ValueError:
                next
        return None
