# coding: EUC_JP

import csv

class CsvData:
    def __init__(self, fname):
        self.fname  = fname
        self.lineno = 0

    def showinfo(self):
        print("Filename: %s"%(self.lineno))

    def load(self):
        fp     = open(self.fname, 'r')
        cr     = csv.reader(fp)

        csv_h  = cr.next()

        self.headers = []
        for i in range(0,len(csv_h)):
            if csv_h[i] in self.headers:
                self.headers.append("%s_%d"%(csv_h[i],i))
            else:
                self.headers.append(csv_h[i])
        self.data    = {}
        self.alldata = []

        for csv_d in cr:
            s_data = {}

            for i in range(0,len(self.headers)-1):
                s_data[self.headers[i]] = csv_d[i]
            self.alldata.append(s_data)

        fp.close()

        self.data = self.alldata[0]

    def __iter__(self):
        return(self)

    def next(self):
        self.lineno += 1
        if self.lineno >= len(self.alldata):
            raise StopIteration

        self.data    = self.alldata[self.lineno]
        return self.getData()

    def getData(self):
        return self.data

    def getHeaders(self):
        return self.headers

if __name__ == "__main__":
    print "todo"

