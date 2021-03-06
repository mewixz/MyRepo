import logging
import math
import random
import sys
import gzip
import os
from datetime import datetime


class Record(object):
    """Represents a record."""

class Donations(Record):
    """Represents a record."""

class Table(object):

    def __init__(self):
        self.records = []

    def __len__(self):
        return len(self.records)

    def ReadFile(self, data_dir,  constructor, n=None):

#        filename = os.path.join(data_dir, filename)

#        if filename.endswith('gz'):
#            fp = gzip.open(filename)
#        else:
        fp = open(data_dir)

        for i, line in enumerate(fp):
            if i == n:
                break
            inner_list = [elt.strip() for elt in line.split('|')]

            s = inner_list[13]
            try:
                date = datetime(year=int(s[4:8]), month=int(s[0:2]), day=int(s[2:4]))
            except:
                continue



            zip = inner_list[10]
            zip_dgts = zip[0:5]

            if (len(zip_dgts)< 5 or len(zip_dgts) > 11):
                continue;

            if(inner_list[15] != ''):
                continue;
            else:
                inner_list[15] = 'empty'

            if (inner_list[0]=='' or inner_list[14]==''):
                continue;

            fields = [
                ('CMTE_ID', inner_list[0]),
                ('NAME', inner_list[7]),
                ('ZIP_CODE', zip_dgts),
                ('TRANSACTION_DT', date),
                ('TRANSACTION_AMT', inner_list[14]),
                ('OTHER_ID', inner_list[15]),
                ('OTHER_ID', inner_list[15]),
                 ]
            record = self.MakeRecord(line, fields, constructor)
            self.AddRecord(record)
        fp.close()

    def MakeRecord(self, line, fields, constructor):
        obj = constructor()
        for (field, val) in fields:
            setattr(obj, field, val)
        return obj

    def AddRecord(self, record):
        self.records.append(record)


class Donors(Table):
    def ReadRecords(self, data_dir, n=None):
#        filename = self.GetFilename()
        self.ReadFile(data_dir, Donations, n)

#    def GetFilename(self):
#        return 'itcont.txt'

def PrintInput(table):
    for p in table.records:
        print ("CMTE_ID: ", p.CMTE_ID)
        print ("NAME: ", p.NAME)
        print ("Zip Code: ", p.ZIP_CODE)
        print ("TRANSACTION_DT: ", p.TRANSACTION_DT)
        print ("TRANSACTION_AMT: ", p.TRANSACTION_AMT)
        print ("OTHER_ID: ", p.OTHER_ID)
        print ('**********************************************')


def percentile(N, P=0.3):
    N.sort()
    n = int(round(P * len(N) + 0.5))
    return N[n-1]


def ProcessReciiepients(cmt, zip, pcnt, Rec):

    amt=0.
    NN=[]
    pnt = pcnt
    n=1
    for q in Rec.records:
        if (cmt== q.CMTE_ID and zip == q.ZIP_CODE):
            ppnt = float(q.TRANSACTION_AMT)
            amt += float(q.TRANSACTION_AMT)
            NN.append(q.TRANSACTION_AMT)
            n += 1
    if(len(NN) > 0):
        pnt = percentile(NN)
    return amt, pnt, n

def MakeTables(data_dir):
    table = Donors()
    table.ReadRecords(data_dir)
    return table

def GetPercentile(percentile_dir):
#    fname = os.path.join(data_dir, fname)
    fp = open(percentile_dir)
    p=50
    for i, line in enumerate(fp):
        p = int(line)
    return p


def main(name, data_dir='', percentile_dir='', out_dir=''):

    table = MakeTables(data_dir)
    Percentile = GetPercentile(percentile_dir)
#    PrintInput(table)
    Repeaters = Donors()
    i=0
    names =[]
    for p in table.records[:-1]:
        if any(p.NAME in item for item in names):
            continue;
        names.append(p.NAME)
        t=None                
        i += 1
        for q in table.records[i:]:               
            if (p.NAME == q.NAME and p.ZIP_CODE == q.ZIP_CODE ):
                t=p
                if (p.TRANSACTION_DT.year < q.TRANSACTION_DT.year):
                    t=q
                p=t
                    
        if(t!= None ):
            Repeaters.AddRecord(t)
            


    Recipients = Donors()
    f = open(out_dir,"w")
    for p in Repeaters.records:
        year = p.TRANSACTION_DT.year
        amount, percentile, num = ProcessReciiepients(p.CMTE_ID, p.ZIP_CODE, p.TRANSACTION_AMT, Recipients)
        totamount = int(float(p.TRANSACTION_AMT)+amount)
        f.write(p.CMTE_ID+"|"+p.ZIP_CODE+"|"+str(year)+"|"+percentile+"|"+str(totamount)+"|"+str(num)+"\n")
        Recipients.AddRecord(p)
    f.close()

if __name__ == '__main__':
    import sys
    main(*sys.argv)
