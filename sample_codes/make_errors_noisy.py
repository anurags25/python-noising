import random
import numpy as np
import re

program = """import sqlite3
dataset_path = 'prutor-deepfix-09-12-2017.db'
with sqlite3.connect(dataset_path) as conn:
   cur = conn.cursor()
   query = "SELECT user_id, tokenized_code FROM Code;"
   code = []
   coder = ()
   for row in cur.execute(query):
      user_id, tokenized_code = map(str, row)
      code.append((user_id, tokenized_code))"""

error_types = ['name_error_variables', 'indentation_error', 'missing_quotes',
               'extra_quotes', 'name_error_keywords'
               'missing_paranthesis', 'missing_colon', 'extra_quotes']

#import errors, keyboard based levenshtein errors, function/class names
#keywords, return, int,input, list, set, for, in if, else, try, except
#['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class',
#'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
#'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or',
#'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
#common typos single quotes to double quotes, forgetting caps
keyboard_cartesian = {'q': {'x':0, 'y':0}, 'w': {'x':1, 'y':0},
                      'e': {'x':2, 'y':0}, 'r': {'x':3, 'y':0},
                      't': {'x':4, 'y':0}, 'y': {'x':5, 'y':0},
                      'u': {'x':6, 'y':0}, 'i': {'x':7, 'y':0},
                      'o': {'x':8, 'y':0}, 'p': {'x':9, 'y':0},
                      'a': {'x':0, 'y':1}, 'z': {'x':0, 'y':2},
                      's': {'x':1, 'y':1}, 'x': {'x':1, 'y':2},
                      'd': {'x':2, 'y':1},'c': {'x':2, 'y':2},
                      'f': {'x':3, 'y':1}, 'b': {'x':4, 'y':2},
                      'm': {'x':6, 'y':2}, 'j': {'x':6, 'y':1},
                      'g': {'x':4, 'y':1}, 'h': {'x':5, 'y':1},
                      'j': {'x':6, 'y':1}, 'k': {'x':7, 'y':1},
                      'l': {'x':8, 'y':1}, 'v': {'x':3, 'y':2},
                      'n': {'x':5, 'y':2}, '[': {'x': 10, 'y': 0},
                      '[': {'x': 11, 'y': 0}, '"': {'x': 10, 'y': 1},
                      '{': {'x': 11, 'y': 0}, "'": {'x': 10, 'y': 1},
                      '}': {'x': 10, 'y': 0}, ':': {'x': 9, 'y': 1},
                      ';': {'x': 9, 'y': 1}, ',': {'x': 7, 'y': 2},
                      '.': {'x': 7, 'y': 2}}

##def make_dist_dict():
##   dist_dict = {}
##   for key in keyboard_cartesian.keys():
##      
##   return dist_dict

def find_vars(program_string):
   code_vars = []
   res = re.finditer(r'(\s)*(\w)+(\s)?=(\s)?[(\w)+\[\(\"\']', program_string)
   for r in res:
      var_group = r.group()
      c_var = var_group.split('=')[0]
      if '\n' in var_group:
         var = c_var.replace(' ', '')
         code_vars.append(var.replace('\n', ''))
      else:
         idx = r.start()
        if program_string[idx - 1] == ',':
            while program_string[idx - 1] != ' ' and idx >= 0:
               idx -= 1
         c_var = program[idx: r.start()] + c_var
         for c in c_var.split(','):
            var = c.replace(' ', '')
            code_vars.append(var.replace('\n', ''))
   print (code_vars)

def make_typo(string):
   l = len(string)
   typo_string = string
   max_edits = np.random.choice([1,2], 1, p=[6,4])[0]
   edit_types = ['switch', 'insert', 'delete']
   for edit in range(max_edits):
      choice = np.random.choice(edit_types, 1)[0]
      if choice == 'switch':
         i = np.random.randint(low=1, high=l, size=1)
         j = i + np.random.choice([1,-1], 1)[0]
         t = typo_string[i]
         typo_string[i] = typo_string[j]
         typo_string[j] = t
      elif choice == 'delete':
         i = np.random.randint(low=1, high=l-1, size=1)
         typo_string = typo_string[:i] + typo_string[i+1:]
      else:
         print (1)
   return typo_string

find_vars(program)
