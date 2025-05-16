from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from vschool.database.orm import Database

class Server:
    def __init__(self, db_url='data/test.db', port=5000):
        print("db_url:", db_url)
        self.db = Database(db_url)
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.port = port

        # Enable CORS
        CORS(self.app)

    class classroom(Resource):
        def __init__(self, db: Database):
            self.db = db
        
        def get(self, location:str, week:int, weekday:int):
            """Retrieve classroom information"""
            room = self.db.get_classroom(location, week, weekday)
            return room, 200

    class course(Resource):
        def __init__(self, db: Database):
            self.db = db
        
        def get(self):
            """Retrieve course information"""
            course_name = request.args.get('course_name', None)
            if not course_name:
                return {"error": "Missing 'course_name' parameter."}, 400

            # Retrieve matching courses from the database
            course_info = self.db.get_course(course_name)
            if not course_info:
                return [], 200  # Return empty list for no results

            return course_info, 200

    def run(self, host="127.0.0.1"):
        # Registering resources with API
        self.api.add_resource(self.classroom, "/classroom/<string:location>/<int:week>/<int:weekday>", 
                              resource_class_args=[self.db])
        self.api.add_resource(self.course, "/course/search", 
                              resource_class_args=[self.db])
        self.app.run(host=host, port=self.port)


if __name__ == "__main__":
    server = Server("data/test.db")
    server.run()