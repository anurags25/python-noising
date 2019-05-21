import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

sys_path = '/home/anurag/.local/lib/python3.5/site-packages'

count = 0

file_counter = 0

for path, dirs, files in os.walk(sys_path):
    for file in files:
        if(count > 3000):
            break
        if ('.py' in file):
            try:
                with open(f'input_{file_counter}.txt', 'a', encoding="utf-8") as f:
                    with open(os.path.join(path, file), 'r') as data:
                        contents = data.read()
                    f.write(contents)
                    f.write('\n')
                    f.flush()
                    count = count + 1
                    if(count % 100 == 0):
                        file_counter = file_counter + 1
            except Exception as e:
                #print (str(e))
                pass

count = 0
for path, dirs, files in os.walk(sys_path):
    for file in files:
        if('.py' in file):
            count = count + 1
print (count)

contents = []
for i in range(19):
    with open(f'input_{i}.txt') as f:
        contents.append(f.read())

d = {'text':contents, 'valid':False}
df = pd.DataFrame(data=d)

df.to_csv('sys_code_final.csv', index=False)
