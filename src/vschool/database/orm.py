from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from decimal import Decimal
from sqlalchemy import literal, and_, or_, text

from vschool.database.entities import *

def serialize(l : list):
    for i in range(len(l)):
        if isinstance(l[i], datetime):
            l[i] = l[i].strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(l[i], Decimal):
            l[i] = float(l[i])
    return l


class Database:
    def __init__(self, db_url='data/test.db'):
        engine = create_engine(f'sqlite:///{db_url}')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        print("[INFO]database constructed")

    def confirm_user(self, username, password_hash):
        user = self.session.query(Course).filter_by(
            username=username, password_hash=password_hash).first()
        if user:
            return user.user_id
        else:
            return None
    
    def get_classroom(self, location:str, week:int, weekday:int):
        freq = (((week % 2) == 0) << 1) + (week % 2)
        rooms = self.session.query(Course, Schedule.start_time, Schedule.end_time)\
            .join(Schedule, (Course.course_id == Schedule.course_id) & (Course.class_id == Schedule.class_id))\
            .filter(
                Schedule.location == location,
                Schedule.start_week <= week,
                Schedule.end_week >= week,
                Schedule.weekday == weekday,
                (Schedule.frequency.op('&')(literal(freq)) != 0),
            ).all()

        if rooms:
            ret = []
            for room in rooms:
                d = room[0].to_dict()
                d['start_time'] = room[1]
                d['end_time'] = room[2]
                ret.append(d)
            return ret
        else:
            return None

    def get_classroomMeta(self, location:str, week:int, weekday:int):
        freq = (((week % 2) == 0) << 1) + (week % 2)
        rooms = self.session.query(Schedule.location)\
            .join(Course, (Course.course_id == Schedule.course_id) & (Course.class_id == Schedule.class_id))\
            .filter(
                Schedule.location.startswith(location),
                Schedule.start_week <= week,
                Schedule.end_week >= week,
                Schedule.weekday == weekday,
                (Schedule.frequency.op('&')(literal(freq)) != 0),
            ).all()

        if rooms:
            start_idx = len(location)
            ret = [room[0][start_idx:] for room in rooms]
            return ret
        else:
            return None

    def get_course(self, course_name:str):
        courses = self.session.query(Course, Schedule)\
            .outerjoin(Schedule, (Course.course_id == Schedule.course_id) & (Course.class_id == Schedule.class_id))\
            .filter(Course.course_name.ilike(f"%{course_name}%"))\
            .order_by(Course.course_name, Course.class_id, Schedule.weekday, Schedule.start_time)\
            .all()
        
        if courses:
            ret = {}
            for c in courses:
                course = c[0].to_dict()
                if ret.get((course["course_id"], course["class_id"]), None) is None:
                    ret[(course["course_id"], course["class_id"])] = {"course": course, "schedule": []}
                if c[1]:
                    s = c[1].to_dict()
                    schedule = f"第{s['start_week']}至{s['end_week']}周 "
                    schedule += f"{['单','双','每'][s['frequency']-1]}周"
                    schedule += f"星期{['一', '二', '三', '四', '五', '六', '日'][s['weekday']-1]}"
                    schedule += f"{s['start_time']}~{s['end_time']}节"
                    ret[(course["course_id"], course["class_id"])]["schedule"]\
                        .append(dict(time=schedule, location=s['location']))
            return list(ret.values())

    def excute_sql(self, sql):
        self.session.execute(sql)

    def __del__(self):
        self.session.close()

if __name__ == '__main__':
    db = Database("data/test.db")

    """ example usage of get_classroom()
    rooms = db.get_classroomMeta("二教", 1, 1)
    print(rooms)
    """

    """ example usage of get_course()
    """
    courses = db.get_course("实习")
    print(courses)

