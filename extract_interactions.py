import sys
import re
import datetime as dt

MAX_SEPARATION = 120
mylines = []
dict = {}
block = 0
is_new_block = True
is_marked = False

arguments = len(sys.argv) - 1
filepath = ""
if arguments == 1:
    filepath = sys.argv[1]
else:
    print("usar: extract_interactions.py %PATH%")
    sys.exit()

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
        
        
for key in dict:
    print(key,",",
        dict[key]['base'], ",",
        dict[key]['bloque_1ro'], ",",
        dict[key]['felicitacion'], ",",
        dict[key]['bloque_marcado'], #",",
        )
    
