import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO,format="%(asctime)s-[%(levelname)s]:%(message)s")

WORK_AREA,_=os.path.split(os.path.abspath(__file__))



def detect_files():
    ret={}
    for path,_,files in os.walk(os.path.join(WORK_AREA,"data")):
        for f in files:
            if f.endswith(".xls") or f.endswith(".xlsx"):
                ret[f]=os.path.join(path,f)
    return ret

def handle(flist):
    for filename,path in flist.items():
        logging.info("Working on {}".format(filename))
        df=pd.read_excel(path,header=2)
        for row in df.iterrows():
            print(row)
            return

if __name__ == "__main__":
    fileList=detect_files()
    handle(fileList)