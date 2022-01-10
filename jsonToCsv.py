import json
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Create Csv from Json')
# argument1: json file name
parser.add_argument('-f','--file', help='Insert Json file path.', required=True)
# argument2: list name(optional)
parser.add_argument('-l','--list', help='Insert List filed name in Json.', required=False)
# argument3: select cols(optional) 
parser.add_argument('-c','--cols', help='Insert Cols to select.', required=False)
# argument4: header(optional) 
parser.add_argument('-d','--header', help='Insert Headers to display.', required=False)
# argument5: csv name(optional) 
parser.add_argument('-o','--output', help='Insert Output file name.', required=False)
args = parser.parse_args()

fileName = args.file 
listName = args.list 
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

# get index
def getIndex(df):
    indexList = []

    # get hashable col
    for index, r in df.iterrows():
        for colName in r.index:
            col = r[colName]
            if not isinstance(col, list):
                if colName not in indexList:
                    indexList.append(colName)

    # delete non hashable col
    for index, r in df.iterrows():
        for colName in r.index:
            col = r[colName]
            if isinstance(col, list):
                if colName in indexList:
                    indexList.remove(colName)

    # delete non hashable col
    for index, r in df.iterrows():
        for colName in r.index:
            col = r[colName]
            if type(col) == dict:
                if colName in indexList:
                    indexList.remove(colName)
    return indexList

# check row has list or dictionary
def checkRow(df):
    result = {
        'hasList': False,
        'hasDict': False
    } 

    for index, r in df.iterrows():
        for colName in r.index:
            col = r[colName]

            # row has list to expand
            if isinstance(col, list):
                # if len(col)>0:
                #     result['hasList'] = True
                result['hasList'] = True

            # row has dictionary to expand
            if type(col) == dict:
                result['hasDict'] = True
    return result

# expand column from dictionary
def addcolumns(r):
    for colName in r.index:
        col = r[colName]
        if type(col) == dict:
            deleteList.append(colName)
            for key in col:
                r[f'{colName}.{key}'] = col[key]
    return r

# open file
jsonFile = open(fileName, 'r', encoding='utf-8')
data = json.load(jsonFile)

# define list
if listName != None:
    df = pd.json_normalize(data[listName])
else:
    df = pd.json_normalize(data)

# loop until df has nothing to expand
while(True):
    checkResult = checkRow(df)
    
    # if row has list
    if checkResult['hasList']:
        idx = None
        indexList = getIndex(df)

        # explode and fill data 
        if len(indexList) > 0:
            df = df.set_index(indexList)

        for col in df.columns:
            df = df.explode(col)
        idx = df.index
        df = df.reset_index()

    # if row has dictionary
    if checkResult['hasDict']:
        idxList = [] 
        if idx is not None:
            for i in idx.names:
                if i is not None:
                    idxList.append(i)
            if len(idxList) > 0:
                df = df.set_index(idxList)

        # append col and fill data 
        deleteList=[]
        df = df.apply(addcolumns, axis=1)
        deleteSet = set(deleteList)
        df = df.drop(deleteSet, axis = 1)
        if len(idxList) > 0:
            df = df.reset_index()

    # if row not has list or dictionary end loop
    if not checkResult['hasList'] and not checkResult['hasDict']:
        break

# delete index cols
df = df[df.columns.drop(list(df.filter(regex='^level_\d+$|^index$')))]

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
