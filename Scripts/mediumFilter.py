import pandas as pd
import os
import csv
import re


def check_filtering(content, keylist):
    for key in keylist:
        if key in content:
            return True
    return False


def getKeyList(filename):
    df = pd.read_csv(filename)
    return df['Keywords'].values.tolist()


def checkFileContent(row, keywords):
    keywords_found = ""
    for key in keywords:
        keyword_found = ""
        if re.search('[A-Za-z]+', row['title']) is None and re.search('[A-Za-z]+', row['title']) is None:
            return ""
        if key in str(row['title']) or key in str(row['text']):
            keyword_found = key
            keywords_found += keyword_found + "_"
    if keywords_found == "":
        return ""
    else:
        return keywords_found


def analyzeYears():
    path = f'./results'
    dirs = os.listdir(path)
    for dir in dirs:
        print("Filtering Year " + dir + "...")
        analyzeMonths(dir)


def analyzeMonths(dir):
    path = f'./results/' + dir
    dirs = os.listdir(path)
    for month_dir in dirs:
        analyzeFiles(path, month_dir)


def analyzeFiles(basepath, dir):
    path = basepath + "/" + dir
    # collect for each year and stop.
    dirs = os.listdir(path)
    df = pd.read_csv('filter.csv')
    keywords = df['Keywords'].values
    for file in dirs:
        df = pd.read_csv(path + "/" + file)
        for index, row in df.iterrows():
            result = checkFileContent(row, keywords)
            if result != "":
                row['keywords'] = result
                filename = formatFileName(file)
                resultpath = basepath + "/" + filename
                print(resultpath)
                resultpath = resultpath.replace(".csv", "")
                resultpath += '_filtered.csv'
                if not os.path.exists(resultpath):
                    with open(resultpath, "w") as file_result:
                        writer = csv.writer(file_result, delimiter=',')
                        writer.writerow(['id', 'date', 'title', 'text', 'keywords'])
                with open(resultpath, "a") as file_result:
                    writer = csv.writer(file_result, delimiter=',')
                    writer.writerow(row)

def formatFileName(file):
    file = file.replace('.csv', "")
    file_vec = file.split('_')
    resulting_string = file_vec[0] + "_" + file_vec[1] + "_" + file_vec[2] + ".csv"
    return resulting_string

def cleanResults():
    path = f'./results'
    pattern = "(.*_filtered.csv)|(.DS_Store)"
    for dir in os.listdir(path):
        dirpath = f'./results/' + dir
        for f in os.listdir(dirpath):
            if re.search(pattern, f):
                os.remove(os.path.join(dirpath, f))

def mergeResults():
    path = f'./results'
    pattern = ".*_filtered.csv"
    file_merged = []
    for dir in os.listdir(path):
        dirpath = f'./results/' + dir
        for f in os.listdir(dirpath):
            if re.search(pattern, f):
                f_path = dirpath +"/"+f
                df_app = pd.read_csv(f_path)
                file_merged.append(df_app)
    df_merged = pd.concat(file_merged)
    df_merged.to_csv("resulting_medium_dataset.csv", index=False)
    print(df_merged.shape)

def filterProcess():
    cleanResults()
    analyzeYears()
    mergeResults()

filterProcess()
