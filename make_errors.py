import argparse
from mutator import make_error
from os import listdir
from os.path import isfile, join

def read_file(file_name):
   with open(file_name, 'r') as f:
         contents = f.read()
   return contents

if __name__ == '__main__':
   #do something
   parser = argparse.ArgumentParser()
   parser.add_argument('-f', '--input_file', help="Input Source Code")
   parser.add_argument('-d', '--input_dir', help="Source Code Dir")
   args = parser.parse_args()
   source_files = []
   source_codes = []
   if args.input_file:
      source_code = read_file(args.input_file)
      source_files.append(args.input_file)
      source_codes.append(source_code)
   elif args.input_dir:
      source_files = [f for f in listdir(args.input_dir) if isfile(join(args.input_dir, f)) and '.py' in f]
      for s_f in source_files:
         source_code = read_file(s_f)
         source_codes.append(source_code)
   else:
      print ('Invalid Arguments!!')
   print (source_files)
   print ()
   for index, contents in enumerate(source_codes):
      source_code_noisy = make_error(contents)
      result_file = source_files[index].replace('.py', '_noisy.py')
      if args.input_dir:
         result_file = args.input_dir + '/' + result_file
      with open(result_file, 'w') as f:
         f.write(source_code_noisy)
