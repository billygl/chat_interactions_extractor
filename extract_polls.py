import sys
from os import listdir
from os.path import isfile, join
import re
import datetime as dt

SEPARATOR = ","
outputpath = "output.csv"

arguments = len(sys.argv) - 1
folderpath = ""
if arguments == 1:
    folderpath = sys.argv[1]
else:
    print("usar: extract_interactions.py %FOLDER_PATH%")
    sys.exit()

with open (outputpath, 'w', encoding="utf-8-sig") as output:
    for f in listdir(folderpath):
        filepath = join(folderpath, f)
        if isfile(filepath):
            m = re.search('\_([\d|\-]+)', f)
            date = m.group(1)[0:10]
            time = m.group(1)[11:].replace("-",":")
            datetime = date + " " + time
            with open (filepath, 'r', encoding="utf8") as file:
                next(file)
                lines = []
                min_datetime = "{"
                lineA = None
                for lineB in file:                    
                    if not lineA:
                        lineA = lineB
                        continue
                    lines.append(lineA)
                    valuesA = lineA.split(",")
                    valuesB = lineB.split(",")
                    datetimeA = valuesA[5].rstrip()
                    if min_datetime > datetimeA and datetimeA != "":
                        min_datetime = datetimeA
                    lineA = lineB                    
                    if valuesB[0] < valuesA[0]:
                        for line in lines:
                            output.write(datetime + SEPARATOR + min_datetime + SEPARATOR + line)
                        lines = []
                        min_datetime = "{"
                lines.append(lineA)
            for line in lines:                
                output.write(datetime + SEPARATOR + min_datetime + SEPARATOR + line)
            #

output.close()