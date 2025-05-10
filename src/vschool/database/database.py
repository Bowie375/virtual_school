import os
import argparse
import sqlite3
import hashlib

def create_table(conn: sqlite3.Connection):
    cursor = conn.cursor()

    ## drop old tables if exist
    cursor.executescript("""
    DROP TABLE IF EXISTS Course;
    DROP TABLE IF EXISTS Schedule;
    """)

    ## create new tables
    cursor.executescript("""
    -- 课程表
    CREATE TABLE Course(
        course_id TEXT CHECK (length(course_id) = 8 AND course_id GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
        class_id INTEGER NOT NULL,
        course_name TEXT NOT NULL,
        department TEXT NOT NULL,
        teacher TEXT NOT NULL,
        PRIMARY KEY (course_id, class_id)
    );

    -- 安排表
    CREATE TABLE Schedule(
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id TEXT NOT NULL,
        class_id INTEGER NOT NULL,
        start_week INTEGER NOT NULL,
        end_week INTEGER NOT NULL,
        weekday INTEGER NOT NULL,
        start_time INTEGER NOT NULL,
        end_time INTEGER NOT NULL,
        location TEXT NOT NULL,
        frequency INTEGER NOT NULL, -- 单双周：1单周，2双周，3每周
        FOREIGN KEY (course_id, class_id) REFERENCES Course(course_id, class_id)
    );                                                          
    """)


    data = [
        ["04835730", "蛋白质设计中的人工智能方法", "张铭(教授)", "1", "信息科学技术学院", ["5~5周 每周周一2~4节 二教319", "5~5周 每周周二2~4节 二教319", "5~5周 每周周四2~4节 二教319", "5~5周 每周周三2~4节 二教319", "5~5周 每周周五2~4节 二教319"]],
        ["04835720", "机器学习理论中的连续时间扩散过程", "王若松(助理教授)", "1", "信息科学技术学院", ["3~4周 每周周一5~8节 二教211", "3~4周 每周周二5~7节 二教211", "3~4周 每周周三5~7节 二教211", "3~4周 每周周四5~7节 二教211", "3~4周 每周周五5~7节 二教211"]],
        #["04830810", "可编程逻辑电路设计(I)", "蒋伟(副教授)", "1", "信息科学技术学院", ["1~5周 每周周一5~8节", "1~5周 每周周四5~8节"]],
        ["04835520", "网络与系统安全实验", "王昭(教学副教授)", "1", "信息科学技术学院", ["3~4周 每周周一5~8节 三教103", "3~4周 每周周二5~8节 三教103", "3~4周 每周周三5~8节 三教103", "3~4周 每周周四5~8节 三教103", "3~4周 每周周五5~8节 三教103"]],
        ["04835500", "大模型：从基础到前沿", "邓志鸿(教授)", "1", "信息科学技术学院", ["1~2周 每周周一10~12节 二教211", "1~2周 每周周二10~12节 二教211", "1~2周 每周周三10~12节 二教211", "1~2周 每周周四10~12节 二教211", "1~2周 每周周五10~12节 二教211"]],
        ["04835490", "计算机科学高级专题", "周明辉(教授),刘先华(副教授),边凯归(长聘副教授),罗国杰(长聘副教授)等", "1", "信息科学技术学院", ["1~2周 每周周一2~4节 二教307","1~2周 每周周三2~4节 二教307","1~2周 每周周四2~8节 二教307","1~2周 每周周五2~4节 二教307"]]
    ]

    ## add data to tables'
    for c in data:
        cursor.executescript(f"""
        INSERT INTO Course(course_id, class_id, course_name, department, teacher)
        VALUES ('{c[0]}', {c[3]}, '{c[1]}', '{c[4]}', '{c[2]}')
        """)
        for s in c[5]:
            t1, t2, location = s.split(' ')
            start_week, end_week = [int(t) for t in t1[:-1].split('~')]
            freq = 1 if '单' in t2[:2] else 2 if '双' in t1[:2] else 3
            weekday = [1,2,3,4,5,6,7][['一', '二', '三', '四', '五', '六', '日'].index(t2[3])]
            start_time, end_time = [int(t) for t in t2[4:-1].split('~')]
            cursor.executescript(f"""
            INSERT INTO Schedule(course_id, class_id, start_week, end_week, weekday, start_time, end_time, location, frequency)
            VALUES ('{c[0]}', {c[3]}, {start_week}, {end_week}, {weekday}, {start_time}, {end_time}, '{location}', {freq})
            """)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', type=str, default='data/test.db', help='database file name')
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    print('Opened database successfully')
    create_table(conn)
    print('Table created successfully')

    """ Validate data in tables
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Course")
    result = cursor.fetchall()
    print(result)
    """

    conn.close()