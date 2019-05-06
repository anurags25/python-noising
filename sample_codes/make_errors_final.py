import argparse
from mutator import make_error
from os import listdir
from os.path import isfile, join

if __name__ == '__main__':
   #do something
   parser = argparse.ArgumentParser()
   parser.add_argument('-f', '--input_file', help="Input Source Code")
   parser.add_argument('-d', '--input_dir', help="Source Code Dir")
   args = parser.parse_args()
   source_files = []
   source_codes = []
   if args.input_file:
      with open(args.input_file, 'r') as f:
         source_code = f.read()
         source_files.append(args.input_file)
         source_codes.append(source_code)
      print (source_codes)
      print (source_files)
   if args.input_dir:
      source_files = [f for f in listdir(args.input_dir) if isfile(join(mypath, f)) and '.py' in f]
      for f in source_files:
         with open(args.input_file, 'r') as f:
            source_code = f.read()
            source_codes.append(source_code)
      print (source_codes)
      print (source_files)      
      
