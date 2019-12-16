#import pandas
import csv
import os

cwd = os.getcwd()

# def PandasRead():
#     df = pandas.read_csv("static/uploads/Sirville_Sirville.csv")
#     print(df)

# PandasRead()
def GetFiles(location):
    files = os.listdir(os.path.join(cwd, location))
    return files
    
def Delete(location, name):
    os.remove(os.path.join(location, name))
    return "{} deleted".format(name)

def Read(fileName, location):
    content = []
    file = fileName
    # newWorkingDIr 
    os.chdir(os.path.join(cwd, location))
    files = os.listdir(".")
    if file in files:
        try:
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    content.append(row)
        except:
            pass
    else:
        print("file absent")
    os.chdir(cwd)
    return content

# data = Read("Sirville_Sirville.csv", "static/uploads")
# print(data)