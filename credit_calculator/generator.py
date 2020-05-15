#-*- coding:utf-8 -*-
import os
import numpy as np
import pandas as pd

WORK_AREA,_=os.path.split(os.path.abspath(__file__))
df=pd.read_excel("temp.xlsx",header=1)

total_credit=0
required_course_credit=0
elective_course_credit=0
public_course_credit=0
quality_debelopmentA_credit=0
quality_developmentB_credit=0
health_credit=0
main_course_credit=0
main_course_GPA=0
CET_4=0


for row in df.iterrows():
    ctype=row[1].get("性质",None)
    course=row[1].get("课程\n名称",None)
    # print(row[1])

    # 总学分
    t=row[1].get("学分",0)
    if not np.isnan(t):
        total_credit+=t

    # 必修学分
    if ctype=="必修":
        t=row[1].get("学分",0)
        if not np.isnan(t):
            required_course_credit+=t
    if ctype=="公选":
        t=row[1].get("学分",0)
        if not np.isnan(t):
            public_course_credit+=t
    if course=="体质健康测试":
        t=row[1].get("总评","无")
        health_credit=t
    if course=="全国大学英语四级(CET4)":
        t=row[1].get("总评",0)
        if not np.isnan(t):
                CET_4=t
    if course[-1]=="*":
        t=row[1].get("学分",0)
        if not np.isnan(t):
            main_course_credit+=t
        t=row[1].get("绩点",0)
        if not np.isnan(t):
            main_course_GPA+=t

print("总学分:{}".format(total_credit))
print("必修课学分:{}".format(required_course_credit))
print("公选课学分:{}".format(public_course_credit))   

print("体质健康成绩:{}".format(health_credit))
print("主干课平均绩点:{}".format(main_course_GPA/main_course_credit))
print("CET4:{}".format(CET_4))


