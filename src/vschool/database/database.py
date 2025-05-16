import json
import argparse
import sqlite3

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

    ## add data to tables
    with open('data/info.json', 'r', encoding='utf-8') as f:
        while data := f.readline():
            c = json.loads(data)
            cursor.executescript(f"""
            INSERT INTO Course(course_id, class_id, course_name, department, teacher)
            VALUES ('{c["course_id"]}', {c["class_id"]}, '{c["course_name"]}', '{c["department"]}', '{c["teacher"]}')
            """)
            for s in c["schedule"]:
                try:
                    t1, t2, location = s.split(' ')
                except:
                    (t1, t2), location = s.split(' '), "无"
                start_week, end_week = [int(t) for t in t1[:-1].split('~')]
                freq = 1 if '单' in t2[:2] else 2 if '双' in t1[:2] else 3
                weekday = [1,2,3,4,5,6,7][['一', '二', '三', '四', '五', '六', '日'].index(t2[3])]
                start_time, end_time = [int(t) for t in t2[4:-1].split('~')]
                cursor.executescript(f"""
                INSERT INTO Schedule(course_id, class_id, start_week, end_week, weekday, start_time, end_time, location, frequency)
                VALUES ('{c["course_id"]}', {c["class_id"]}, {start_week}, {end_week}, {weekday}, {start_time}, {end_time}, '{location}', {freq})
                """)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', type=str, default='data/test.db', help='database file name')
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    """
    print('Opened database successfully')
    create_table(conn)
    conn.commit()
    print('Table created successfully')
    """

    """ Validate data in tables
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        WITH tmp AS (
            SELECT 
                Course.course_id AS cid, 
                Course.course_name AS cname, 
                Schedule.location AS sloc 
            FROM Course
            JOIN Schedule 
                ON Course.course_id = Schedule.course_id 
                AND Course.class_id = Schedule.class_id
        )
        
        SELECT * 
        FROM tmp t1
        JOIN tmp t2 ON t1.sloc = t2.sloc;
        """
    )
    result = cursor.fetchall()
    print(result)

    conn.close()