from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from decimal import Decimal

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
        rooms = self.session.query(Course).join(Schedule).filter(
            Schedule.location == location,
            Schedule.start_week <= week,
            Schedule.end_week >= week,
            Schedule.weekday == weekday,
            Course.class_id == Schedule.class_id,
            Course.course_id == Schedule.course_id,
        ).all()

        if rooms:
            return list(map(lambda x: x.to_dict(), rooms))
        else:
            return None

    def excute_sql(self, sql):
        self.session.execute(sql)

    def __del__(self):
        self.session.close()

if __name__ == '__main__':
    db = Database("data/test.db")

    rooms = db.get_classroom("二教211", 1, 1)
    print(rooms)

