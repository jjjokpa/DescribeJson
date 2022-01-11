import pandas as pd
import json
import argparse

parser = argparse.ArgumentParser(description='Create Csv from Json')
# argument: json file name
parser.add_argument('-f','--file', help='Insert Json file path.', required=True)
# argument: select cols(optional) 
parser.add_argument('-c','--cols', help='Insert Cols to select.', required=False)
# argument: header(optional) 
parser.add_argument('-d','--header', help='Insert Headers to display.', required=False)
# argument: csv name(optional) 
parser.add_argument('-o','--output', help='Insert Output file name.', required=False)
args = parser.parse_args()

# get file name
fileName = args.file 
outputName = args.output
if outputName is None:
    outputName = 'myCsv.csv'

# select cols
selectedCols = args.cols 
selectedColsList = []

if selectedCols is not None and len(selectedCols)>0: 
    selectedColsList = selectedCols.split(',')
    selectedColsList = list(map(lambda n: n.strip(), selectedColsList))

# headers
headers = args.header 
headerList = []

if headers is not None and len(headers)>0: 
    headerList = headers.split(',')
    headerList = list(map(lambda n: n.strip(), headerList))

def addcolumns(r):
    for colName in r.index:
        col = r[colName]
        if type(col) == dict:
            for key in col:
                r[f'{colName}.{key}'] = col[key]
            r = r.drop(colName)
    return r

def checkHasList(r):
    for col in r:
        if isinstance(col, list):
            return 1 
    return 0 

def checkHasDict(r):
    for col in r:
        if type(col) == dict:
            return 1
    return 0


# open file
jsonFile = open('sample.json', 'r', encoding='utf-8')
data = json.load(jsonFile)

df = pd.json_normalize(data)

# expand data
while (True):
    r1 = df.apply(checkHasList, axis=1)
    r2 = df.apply(checkHasDict, axis=1)
    hasList = any(r1)
    hasDict = any(r2)

    for col in df.columns:
        df = df.explode(col)

    df = df.apply(addcolumns, axis=1)

    if hasList is False and hasDict is False:
        break

# select Cols
if len(selectedColsList)>0: 
    df = df[selectedColsList]
    df = df.drop_duplicates(subset=selectedColsList)
else:
    selectedColsList = df.columns.values
    df = df[selectedColsList]
    df = df.drop_duplicates(subset=selectedColsList)

if len(headerList)>0:
    df = df.set_axis(headerList, axis=1, inplace=False)

# create csv
df.to_csv(outputName, index=False, encoding='utf-8')
