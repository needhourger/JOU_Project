#-*- coding:utf-8 -*-
class Message:

    REQUIRE_COURSE_INCOMPLETE=0x0001
    CET4_INCOMPLETE=0x0002
    CHEAT=0x0003
    MAIN_COURSE_AVERAGE_GPA_INCOMPLETE=0x0004
    INNOVATION_REWORD_A_INCOMPLETE=0x0005
    INNOVATION_REWORD_B_INCOMPLETE=0x0006
    REQUIRE_COUSE_CREDIT_INCOMPLETE=0x0007
    ELECTIVE_COURSE_CREDIT_INCOMPLETE=0x0008
    PUBLIC_COUSE_CREDIT_INCOMPLETE=0x0009

    __code_map__={
        0x0001:"主干课程未完成",
        0x0002:"四级未达标",
        0x0003:"作弊",
        0x0004:"主干课程平均绩点未达标",
        0x0005:"创新奖励学分A未达标",
        0x0006:"创新奖励学分B未达标",
        0x0007:"必修课学分未达标",
        0x0008:"选修课学分未达标",
        0x0009:"公选课学分未达标",
    }

    @staticmethod
    def getMessage(mCode:int):
        return Message.__code_map__[mCode]
    
print(Message.getMessage(0x0001))