import sys
import re

mylines = []
dict = {}

arguments = len(sys.argv) - 1
filepath = ""
if arguments == 1:
    filepath = sys.argv[1]
else:
    print("usar: extract_interactions.py %PATH%")
    sys.exit()
    
with open (filepath, 'rt', encoding="utf8") as myfile:
    for myline in myfile:    
        m = re.search('<>', myline)
        m = re.search('^<v ([\w|\s]+)>', myline)
        if m:
            interactor = m.group(1)
            if interactor in dict:
                dict[interactor] += 1
            else:
                dict[interactor] = 1
for key in dict:
    print(key,",",dict[key])