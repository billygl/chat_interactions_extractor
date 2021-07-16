import sys
import os
from os import walk
from os.path import join,isdir
import re
import datetime as dt
import json
import pathlib

MAX_SEPARATION = 120
OUTPUT_LINE = "%s,%s,%s,%s,%s,%s"

outputpath = "output.csv"

def extract_interactions(filepath):
    dict = {}
    block = 0
    is_new_block = True
    is_marked = False
    
    time_prev = dt.datetime.strptime("00:00:00", '%H:%M:%S')   
    #07:08:26 From  Hernan Nina Hanco  to  Everyone :  
    with open (filepath, 'rt', encoding="utf8") as file:
        for index, line in enumerate(file):
            #print(line)

            m = re.search(
                '^(\d\d:\d\d:\d\d) From  ([\w\s]+) {1,2}to  {1,2}Everyone {0,1}:(.*)', 
                line
                )
            if m:
                time_str = m.group(1)
                if time_str == None:
                    print(line)
                    print(m)
                if index == 0:
                    time_prev = dt.datetime.strptime(time_str, '%H:%M:%S')

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
            
                interactor = m.group(2)
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
                dict[interactor] = points
    return dict

arguments = len(sys.argv) - 1
folderpath = ""
if arguments == 1:
    folderpath = sys.argv[1]
else:
    print("usar: extract_interactions.py %FOLDER_PATH%")
    sys.exit()

with open (outputpath, 'w', encoding="utf-8-sig") as output:
    for root, subdirs, files in walk(folderpath):
        for filename in files:
            filepath = join(root, filename)
            print(filepath)
            
            fname = pathlib.Path(filepath)
            mtime = dt.datetime.fromtimestamp(fname.stat().st_mtime)
            
            id = mtime.strftime("%d/%m/%y %H:%M")
            
            dict = extract_interactions(filepath)
            for key in dict:            
                output.write(OUTPUT_LINE % (id, key, 
                                    dict[key]['base'],
                                    dict[key]['bloque_1ro'],
                                    dict[key]['felicitacion'],
                                    dict[key]['bloque_marcado']))
                output.write("\n")
output.close()
