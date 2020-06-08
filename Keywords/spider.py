import os
import json
import requests
import logging
import jieba
jieba.set_dictionary("./dict.txt")
jieba.initialize()
from jieba import analyse
analyse.set_idf_path("./idf.txt")
import multiprocessing

logging.basicConfig(format="%(asctime)s[%(levelname)s]:%(message)s",level=logging.INFO)
stopwords=[]
code="utf-8"
threshold=50
outfile=None


def BDQuery(word):
    """
    从百度百科接口获取词含义
    """
    url="http://baike.baidu.com/api/openapi/BaikeLemmaCardApi"
    params={
        "scope":103,
        "format":"json",
        "appid":379020,
        "bk_key":word,
        "bk_length":600
    }
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    while True:
        try:
            r=requests.get(url,params=params,headers=headers)
            data=json.loads(r.text)
            # text=json.dumps(data,indent=4,separators=(',',':'),ensure_ascii=False)
            if not data:
                logging.warning("No result")
                return None
            else:
                if data.get("errno",None)==2:
                    logging.info(r.text)
                    continue
                ret=data.get("abstract",None)
                if ret==None:
                    ret=data.get("desc",None)
                logging.info(ret)
                return ret
        except:
            continue

def loadfile(path):
    """
    读取待处理文本
    """
    global code
    if not os.path.exists(path):
        logging.warning("file not exists")
        return None
    if os.path.isdir(path):
        logging.info("detect directory get")
        filelist=[]
        for i in os.listdir(path):
            if i.strip().split('.')[-1]=="txt":
                logging.info("find file:[{}]".format(i))
                filelist.append(path+"/"+i)
        ret=[]
        for i in filelist:
            with open(i,"r",encoding=code) as f:
                ret.append(f.read())
                f.close()
                logging.info("load file:[{}]".format(i))
        return dict(zip(filelist,ret))
    else:
        with open(path,"r+",encoding=code) as f:
            data=f.read()
            f.close()
            logging.info("load complete")
            return {path:data}
        logging.warning("loading error")
        return {}

def loadStopWords(path="./stopwords.txt"):
    """
    读取停止词
    """
    global stopwords,code
    with open(path,"r+",encoding=code) as f:
        stopwords=f.readlines()
        logging.info("load stopwords")
        f.close()

def extractWords(data,threshold=50):
    """
    提取关键词
    """
    global stopwords
    words=analyse.extract_tags(data,threshold,withWeight=False)
    ret=[]
    for word in words:
        if word in stopwords:
            continue
        ret.append(word)
    logging.info("extract words complete")
    return ret

def out(desc):
    global outfile
    outfile.write("{}:{}\n".format(word,desc))


def extractResult(path,words):
    """
    处理每个关键词的解意并保存到对应文本文件
    """
    global code,outfile
    outfile=open(path,"w+",encoding=code)
    cores=multiprocessing.cpu_count()
    pool=multiprocessing.Pool(processes=cores)

    with open(path+".csv","w+",encoding=code) as f:
        for word in words:
            desc=None
            desc=BDQuery(word)
            if desc==None:
                continue
            f.write("{}:{}\n".format(word,desc))
            logging.info(word)

def loadConfig(path="./config.json"):
    """
    读取配置文件
    """
    global code,threshold
    with open(path,"r+",encoding="gb2312") as f:
        try:
            data=json.load(f)
            code=data.get("code","utf-8")
            threshold=data.get("threshold",50)
        except:
            pass
    logging.info("code:[{}]".format(code))
    logging.info("threshold:[{}]".format(threshold))



if __name__=="__main__":
    """
    主程序
    """
    loadConfig()
    loadStopWords()
    path=input("请输入需要处理的文本路径或者目录:")
    datas=loadfile(path)
    for k,v in datas.items():
        words=extractWords(v,threshold=threshold)
        extractResult(k,words)

    