import csv
import os
cwd = os.getcwd()


def Read(path, filename):
    data = []
    file = os.path.join(path, filename)
    with open(file, mode="r") as read_file:
        csv_reader = csv.reader(read_file, delimiter=',')
        for row in csv_reader:
            data.append(row)          
    return data


def Write(path, filename, data):
    file = os.path.join(path, filename)
    with open(file, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(data)
        
        
def AddWrite(path, filename, data):
    oldData = Read(path, filenameR)
    file = os.path.join(path, filename)
    with open(file, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(oldData)
        csv_writer.writerow(data)
        
def Join(data):
    cards = []
    totals = []
    newData= []
    Gross = 0
    Nett = 0
    for row in data:
        if row[7] in cards:
            totals[cards.index(row[7])] += (int(row[6])/100)
            pass
        else:
            cards.append(row[7])
            totals.append(0)
            totals[cards.index(row[7])] += int(row[6])
        Gross += int(row[3])
        Nett += int(row[6])
        
    newData.append(Gross)
    newData.append(Nett)
    final = {}
    x=0
    for card in cards:
        final.update({cards[x] : totals[x]})
        x+=1
    final.update({"total" : Gross})
    return final
    
        
def Split(path, filenameR):
    data = Read(path, filenameR)
    head = data[:9]
    body = data[9:-2]
    tail = data[-2:]
    joined = Join(body)
    joined = [["cow", "goat", "sheep", "donky"],["cow", "goat", "sheep", "donky"]]
    for line in joined:
        AddWrite(path, filenameW, line)
    
    print(joined)
    
    

filenameR = "Sirville_Sirville.csv"
filenameW = "Sirville.csv"
path = "static/uploads"

def Manage():
    data = Read(path, filenameR)
    data = data[:10]
    for da in data:
        print(da)

Split(path, filenameR)

# data = ["this","this","this","this","this"]
# Read(path, filename)
# Write(path, filename, data)
