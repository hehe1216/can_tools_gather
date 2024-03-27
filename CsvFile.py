import csv

def readcsv(filename):
    reader = ""
    with open(filename, 'r') as f:
        reader = csv.reader(f)
    return reader

def parsecsv(reader):
    print(reader)
    # for row in reader:
    #     print(row)


if __name__ == '__main__':
    filename = 'test.csv'
    reader = readcsv(filename)
    parsecsv(reader)