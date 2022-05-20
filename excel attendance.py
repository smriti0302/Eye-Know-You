import csv
import datetime

def from_excel_to_csv():
        df = pd.read_excel(filename,index=False)
        df.to_csv('./details.csv')

def getdata():
        with open('details.csv','r') as f:
            data = csv.reader(f)
            next(data)
            lines = list(data)
            for line in lines:
                names[int(line[0])] = line[1]


def markPresent(name):
     with open('details.csv','r') as f:
            data = csv.reader(f)
            lines = list(data)
            # for line in lines:
            #     line.pop(0)
            # print(lines)
            for line in lines:
                if line[1] == name:
                    line[-1] = '1'
                    with open('details.csv','w') as g:
                        writer = csv.writer(g,lineterminator='\n')
                        writer.writerows(lines)
                        break



def update_Excel():
     with open('details.csv') as f:
            data = csv.reader(f)
            lines = list(data)
            for line in lines:
                line.pop(0)
            with open('details.csv','w') as g:
                writer = csv.writer(g,lineterminator='\n')
                writer.writerows(lines)

     df = pd.read_csv('details.csv')
     df.to_excel('details.xlsx',index = False)
