import sys
import os
from os import listdir
from os.path import join
import re
import datetime as dt
import json

MAX_SEPARATION = 120
OUTPUT_LINE = "%s,%s,%s,%s,%s,%s"

outputpath = "output.csv"

def extract_interactions(filepath):
    dict = {}
    block = 0
    is_new_block = True
    is_marked = False
    
    time_prev = dt.datetime.strptime("00:00:00", '%H:%M:%S')    
    with open (filepath, 'rt', encoding="utf8") as file:
        for line in file:
            m = re.search('^(\d\d:\d\d:\d\d)', line)
            if m:
                time_str = m.group(1)
                time = dt.datetime.strptime(time_str, '%H:%M:%S')
                diff = time - time_prev
                seconds = diff.total_seconds()
                is_new_block = False
                if block == 0 or seconds > MAX_SEPARATION:
                    block += 1
                    is_new_block = True
                    is_marked = False
                    #print(time_str)
                time_prev = time
            
            m = re.search('^<v [\w|\s]+>\[.+\]?', line)
            if m:
                is_marked = True
                    
            m = re.search('^<v ([\w|\s]+)>', line)
            if m:
                interactor = m.group(1)
                points = {
                    'base': 0, 
                    'bloque_1ro': 0,
                    'felicitacion': 0,
                    'bloque_marcado': 0,
                }
                if interactor in dict:
                    points = dict[interactor]
                points['base'] += 1
                if is_new_block:
                    points['bloque_1ro'] += 1
                if is_marked:
                    points['bloque_marcado'] += 1
                dict[interactor] = points
            
            m = re.search('^<v [\w|\s]+>\[bien:([\w|\s]+)\]?', line)
            if m:
                interactor = m.group(1) 
                if interactor in dict:
                    dict[interactor]['felicitacion'] += 1
    return dict

arguments = len(sys.argv) - 1
folderpath = ""
if arguments == 1:
    folderpath = sys.argv[1]
else:
    print("usar: extract_interactions.py %FOLDER_PATH%")
    sys.exit()

data = None
for file in listdir(folderpath):
    filename, file_extension = os.path.splitext(file)        
    if file_extension == ".json":
        filepath = join(folderpath, file)
        with open(filepath) as source:
            data = json.load(source)            
            break

with open (outputpath, 'w', encoding="utf-8-sig") as output:
    for file in listdir(folderpath):
        filepath = join(folderpath, file)
        print(file)
        #LENG.PROGRA. &#x2F; 601 - recording_1_chat.txt
        m = re.search('_(\d+)_', file)
        if not m:
            continue
        id = m.group(1)
        
        if data:
            name = "LENG.PROGRA. / 601 - recording_" + id
            result = list(filter(lambda e: e['name'] == name, data))
            if len(result) > 0:
                id = result[0]['startTime']
                print(id)
        
        dict = extract_interactions(filepath)
        for key in dict:            
            output.write(OUTPUT_LINE % (id, key, 
                                 dict[key]['base'],
                                 dict[key]['bloque_1ro'],
                                 dict[key]['felicitacion'],
                                 dict[key]['bloque_marcado']))
            output.write("\n")
output.close()
