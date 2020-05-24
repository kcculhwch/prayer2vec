import re
import sys
import os
def process_file(contents):
  cleaned = re.sub("[^a-zA-Z\s]", "", contents)
  return cleaned.lower()

def get_file(path):

  print(f"try to read /{sys.argv[1]}")
  try:
    iFile = open(f"/{sys.argv[1]}", "r")
    file_text = iFile.read()
    iFile.close()
  except FileNotFoundError:
    display_help()
    sys.exit()
  return file_text

def display_help():
   print("Must supply path to corpus text")  

def create_output_path(input_path):
  without_corpus = re.sub("^corpus\/", "", input_path)
  without_file = re.sub("\/[^\/]+$", "", without_corpus)
  dirName = f"/normalized/{without_file}"
  try:
    os.makedirs(dirName)
  except FileExistsError:
    return dirName
  return dirName

def get_name(input_path):
  segs = input_path.split("/")
  result = segs[len(segs) - 1]
  return result


def write_file(text, dirName, name):
  oFile = open(f"{dirName}/{name}", "w")
  oFile.write(text)
  oFile.close()

if len(sys.argv) > 1:	
  file_text = get_file(sys.argv[1])
  cleaned = process_file(file_text)
  outDir = create_output_path(sys.argv[1])
  name = get_name(sys.argv[1])
  write_file(cleaned, outDir, name)
else:
  display_help()



