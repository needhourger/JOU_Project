# -*- coding:utf-8 -*-
import os
import csv
import json
import logging
import pandas as pd

from message import Message
logging.basicConfig(
    format="%(asctime)s-[%(levelname)s]:%(message)s", level=logging.INFO)


def loadConfig():
    """
    载入配置文件
    文件默认路径当前目录下的config.json文件
    """
    with open("./config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        f.close()

    path = config.get("path", None)
    if not os.path.exists(path):
        logging.error("配置文件path目标文件不存在")
        return

    with open(path, "r", encoding="utf-8") as f:
        config["keys"] = [i.strip() for i in f.readlines()]
        f.close()

    logging.info("已载入配置文件,配置信息如下:")
    for k, v in config.items():
        if type(v) == list:
            print(" - {}:".format(k))
            for i in v:
                print("   - {}".format(i))
        else:
            print(" - {}:{}".format(k, v))

    return config


def loadFileList(config: dict):
    """
    读取config中所配置的待处理数据文件下所有的excel文件
    返回文件路径列表
    """
    ret = []
    for dirPath, _, filenames in os.walk(config["dataPath"]):
        for f in filenames:
            if f.endswith(".xls") or f.endswith(".xlsx"):
                ret.append(os.path.join(dirPath, f))

    logging.info("检测到待处理文件如下:")
    for i in ret:
        print("\t{}".format(i))

    return ret


def checkCheat(row):
    """
    检测总评,补考,重修中是否存在作弊
    """
    return row[1].get("总评", 0) == "作弊" or row[1].get("补考", 0) == "作弊" or row[1].get("重修") == "作弊"


def processFile(path: str, config: dict):
    """
    处理单个文件
    """
    output = {
        "序号": "",
        "学号": "",
        "姓名": "",
        "总计": "",
        "必修课": "",
        "选修课": "",
        "公选课": "",
        "创新选修": "",
        "创新必修": "",
        "主干课程平均绩点": "",
        "CET4": "",
        "处分类型/是否解除": "",
        "毕业结论": "",
        "学位结论": "",
        "不授予学位或待定原因": "",
        "培养方案": "",
        "备注（预科转本，留学生等）": "",
    }

    sId = 0
    sName = ""

    df = pd.read_excel(path, header=None, nrows=1)
    for row in df.iterrows():
        data = row[1].get(0)
        data = data.split()
        for i in data:
            if "学号" in i:
                sId = i.replace("学号：", "")
            if "姓名" in i:
                sName = i.replace("姓名：", "")
        break

    dfs = []
    for i in range(3):
        df = pd.read_excel(
            path,
            header=None,
            skiprows=[0,1],
            names=["课程名称", "性质", "学分", "总评", "补考", "重修", "绩点"],
            usecols=range(i*7, (i+1)*7)
        )
        dfs.append(df)

    rCourseSet = set(config["keys"])
    rCourseCredit = 0
    mCourseCreditGPA = 0
    mCourseCredit = 0
    pCourseCredit = 0
    eCourseCredit = 0
    totalCredit = 0
    sportsHealth = None
    CET4 = 0
    cRewordCreditA = 0
    cRewordCreditB = 0

    cFlag = False

    for df in dfs:
        for row in df.iterrows():
            # print(row)
            ctype = row[1].get("性质", None)
            course = row[1].get("课程名称", "")
            if type(course) == str:
                course = course.strip()
            credit = row[1].get("学分", 0)
            GPA = row[1].get("绩点")

            if not cFlag:
                cFlag = checkCheat(row)

            if GPA > 0:
                # 总学分统计
                totalCredit += credit

                # 统计完成的必修科目
                if ctype == "必修":
                    rCourseCredit += credit
                    if course.replace("*", "") in rCourseSet:
                        rCourseSet.remove(course.replace("*", ""))

                # 公选课学分
                elif ctype == "公选":
                    pCourseCredit += credit

                # 选修课学分
                elif ctype == "选修":
                    eCourseCredit += credit

                # 主干课学分绩点
                if course.endswith("*"):
                    mCourseCredit += credit
                    mCourseCreditGPA += credit*GPA

                # 创新奖励学分
                if course == "创新奖励学分A":
                    cRewordCreditA = credit
                if course == "创新奖励学分B":
                    cRewordCreditB = credit

            if course == "体质健康测试":
                sportsHealth = row[1].get("总评", None)
            if course == "全国大学英语四级(CET4)":
                CET4 = row[1].get("重修", 0)

    # 输出结果
    print("==================================")
    print("=学号:{}  姓名:{}".format(sId, sName))
    output["学号"] = sId
    output["姓名"] = sName
    print("总学分:{}".format(totalCredit))
    output["总计"] = totalCredit
    print("必修课学分:{}\t学分要求:{}\t达标还需:{} 分".format(rCourseCredit,
                                                config["a"], (0 if config["a"] <= rCourseCredit else config["a"]-rCourseCredit)))
    output["必修课"] = rCourseCredit
    print("选修课学分:{}\t\t学分要求:{}\t达标还需:{} 分".format(eCourseCredit,
                                                  config["b"], (0 if config["b"] <= eCourseCredit else config["b"]-eCourseCredit)))
    output["选修课"] = eCourseCredit
    print("公选课学分:{}\t\t学分要求:{}\t达标还需:{} 分".format(pCourseCredit,
                                                  config["n"], (0 if config["n"] <= pCourseCredit else config["n"]-pCourseCredit)))
    output["公选课"] = pCourseCredit
    if mCourseCredit == 0:
        aMainCourseCredit = 0
    else:
        aMainCourseCredit = mCourseCreditGPA/mCourseCredit
    print("主干课平均绩点:{:.4f}\t达标要求:{}\t{}".format(aMainCourseCredit,
                                               config["m"], ("已达标" if aMainCourseCredit >= config["m"] else "未达标")))
    output["主干课程平均绩点"] = aMainCourseCredit
    if aMainCourseCredit < config["m"]:
        output["不授予学位或待定原因"] += "主干课程平均绩点不满足\n"
    print("体质健康成绩:{}".format(sportsHealth))
    print("CET4:{}\t{}".format(CET4, ("CET不达标" if CET4 < config["c"] else "")))
    output["CET4"] = CET4
    if CET4 < config["c"]:
        output["不授予学位或待定原因"] += "CET4不达标"
    print("创新奖励学分A:{}\t{}".format(cRewordCreditA,
                                  ("创新奖励学分A不足" if cRewordCreditA < config["x"] else "")))
    output["创新选修"] = cRewordCreditA
    if cRewordCreditA < config["x"]:
        output["不授予学位或待定原因"] += "创新奖励学分A不满足\n"
    print("创新奖励学分B:{}\t{}".format(cRewordCreditB,
                                  ("创新奖励学分B不足" if cRewordCreditB < config["y"] else "")))
    output["创新必修"] = cRewordCreditB
    if cRewordCreditB < config["y"]:
        output["不授予学位或待定原因"] += "创新奖励学分B不满足\n"
    if cFlag:
        print("处分类型/是否解除:作弊")
        output["处分类型/是否解除"] = "作弊"
        output["不授予学位或待定原因"] += "作弊\n"
    if rCourseSet == {}:
        print("所有必修学科已完成")
    else:
        print("未完成必修课如下:")
        for i in rCourseSet:
            print(" - {}".format(i))
            output["不授予学位或待定原因"] += i+"\n"

    # 输出至文件
    oDf = pd.DataFrame(data=[[v for v in output.values()]])
    oDf.to_csv(config["outputPath"],mode="a",header=False,index=False,encoding="GB2312")
