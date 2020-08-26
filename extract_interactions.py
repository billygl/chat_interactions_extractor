import re

mylines = []
dict = {}

with open ('20200824.txt', 'rt', encoding="utf8") as myfile:
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
    print(key,dict[key])