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
    return (code_vars)

def make_typo(string, choice=None):
    l = len(string)
    #print (string)
    typo_string = string
    max_edits = np.random.choice([1,2], 1, p=[.7,.3])[0]
    edit_types = ['switch', 'insert', 'delete', 'substitute']
    for edit in range(max_edits):
        if choice is None:
            choice = np.random.choice(edit_types, 1)[0]
        if choice == 'switch':
            tmp_str = list(typo_string)
            l = len(tmp_str)
            if l == 1:
                continue
            elif l == 2:
                i = 0
                j = 1
            elif l == 3:
                i = 1
                j = i + np.random.choice([1,-1], 1)[0]
            else:
                i = np.random.randint(low=1, high=l-2, size=1)[0]
                j = i + np.random.choice([1,-1], 1)[0]
            #print (tmp_str)
            #print (i,j)
            t = tmp_str[i]
            tmp_str[i] = tmp_str[j]
            tmp_str[j] = t
            typo_string = ''.join(tmp_str)
        elif choice == 'delete':
            i = np.random.randint(low=0, high=l-1, size=1)[0]
            #print (i)
            typo_string = typo_string[:i] + typo_string[i+1:]
        elif choice == 'insert':
            i = np.random.randint(low=0, high=l, size=1)[0]
            dist = np.random.randint(low=0, high=2, size=1)[0]
            candidates = dist_dict[string[i]][dist]
            selected = np.random.choice(candidates, size=1)[0]
            typo_string = typo_string[:i] + selected + typo_string[i:]
        else:
            tmp_str = list(typo_string)
            i = np.random.randint(low=0, high=l-1, size=1)[0]
            if string[i].isalpha():
                dist = np.random.randint(low=1, high=2, size=1)[0]
            else:
                dist = np.random.randint(low=0, high=2, size=1)[0]
            candidates = dist_dict[string[i]][dist]
            selected = np.random.choice(candidates, size=1)[0]
            tmp_str[i] = selected
            typo_string = ''.join(tmp_str)
    return typo_string

def find_keywords(program_string):
    keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class',
                'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
                'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or',
                'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
    final_keywords = []
    for k in keywords:
        if k in program_string:
            final_keywords.append(k)
    
    funcs = re.finditer(r'def (.*):', program_string)
    for f in funcs:
        res = f.group()
        final_keywords.append(res.split('(')[0].split()[1])
    classes = re.finditer(r'class (.*):', program_string)
    for c in classes:
        res = c.group()
        if '(' in res:
            r = res.split('(')[0]
        else:
            r = res.split(':')[0]
        final_keywords.append(r.split()[1])
    #print (final_keywords)
    return final_keywords

def make_dist_dict(keyboard_cartesian):
    dist_dict = {}
    keys = list(keyboard_cartesian.keys())
    
    for k in keys:
        dist_dict[k] = {0: [], 1: [], 2: []}
    for i, key in enumerate(keys):
        for j in range(len(keys)):
            curr_key = keys[j]
            x1, y1 = keyboard_cartesian[key]['x'], keyboard_cartesian[key]['y']
            x2, y2 = keyboard_cartesian[curr_key]['x'], keyboard_cartesian[curr_key]['y']
            dist = np.square((x2 - x1)) + np.square((y2 - y1))
            dist = np.sqrt(dist)
            dist = np.round(dist)
            if dist < 3:
                dist_dict[key][dist].append(curr_key)
    return dist_dict

def dist_dict_manual_rules(dist_dict):
   dist_dict['_'] = {0: ['-'], 1: ['-'], 2: ['-']}
   dist_dict['-'] = {0: ['_'], 1: ['_'], 2: ['_']}
   dist_dict[' '] = {0: [''], 1: ['  '], 2: ['  ']}
   dist_dict['('] = {0: [''], 1: ['(('], 2: ['((']}
   dist_dict[')'] = {0: [''], 1: ['))', '_'], 2: ['))', '-']}
   return dist_dict

def replace_nth_occurance(string, replace, n, replace_with):
    count = 0
    res = re.finditer(re.escape(replace), string)
    for r in res:
        if count == n:
            string = string[:r.start()] + replace_with + string[r.end():]
            break
        count += 1
    return string

def get_rand_n(string, v):
    count = re.findall(re.escape(v), string)
    n = np.random.randint(0, len(count), 1)[0]
    return n

def mutate(program_string, dist_dict, code_vars, keywords):
    selected = np.random.choice(error_types, size=1)[0]
    if selected == 'name_error_variables':
        v = np.random.choice(code_vars, size=1)[0]
        n = get_rand_n(program_string, v)
        typo = make_typo(v)
        print ('Variable mismatch error: Replacing occurrence ', n, ' of ', v, ' with "', typo, '"')
        program_string = replace_nth_occurance(program_string, v, n, typo)
    elif selected == 'name_error_keywords':
        v = np.random.choice(keywords, size=1)[0]
        n = get_rand_n(program_string, v)
        typo = make_typo(v)
        print ('Keyword mismatch error: Replacing occurrence ', n, ' of "', v, '" with "', typo, '"')
        program_string = replace_nth_occurance(program_string, v, n, typo)
    elif selected == 'indentation_error':
        n = get_rand_n(program_string, ' ')
        typo = np.random.choice(['', '  '], size=1)[0]
        print ('Indentation error: Replacing occurrence ', n, ' of ', '" "', ' with "', typo, '"')
        program_string = replace_nth_occurance(program_string, ' ', n, typo)
    else:
        candidates = ['"', "'", ',', '.', ':', ';', '(', ')', '[', ']', '{', '}']
        final_candidates = [c for c in candidates if c in program_string]
        final_candidate = np.random.choice(final_candidates, size=1)[0]
        
        n = get_rand_n(program_string, final_candidate)
        
        dist = np.random.randint(low=0, high=1, size=1)[0]
        error_candidates = dist_dict[final_candidate][dist] + ['', final_candidate + final_candidate]
        
        typo = typo = np.random.choice(error_candidates, size=1)[0]
        program_string = replace_nth_occurance(program_string, final_candidate, n, typo)
        
        print ('Misc Syntax Error: Replacing occurrence ', n, ' of ', final_candidate, ' with "', typo, '"')
        #misc errors
    return (program_string)

def make_error(program_string):
    dist_dict = make_dist_dict(keyboard_cartesian)
    dist_dict = dist_dict_manual_rules(dist_dict)
    code_vars = find_vars(program_string)
    keywords = find_keywords(program_string)
    noisy_code = mutate(program_string, dist_dict, code_vars, keywords)
    return noisy_code

if __name__ == '__main__':
   noisy_code = make_error(program)
   print (noisy_code)
