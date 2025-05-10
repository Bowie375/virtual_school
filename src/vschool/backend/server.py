from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from vschool.database.orm import Database

class Server:
    def __init__(self, db_url='data/test.db'):
        self.db = Database(db_url)
        self.app = Flask(__name__)
        self.api = Api(self.app)

        # Enable CORS
        CORS(self.app)

    class classroom(Resource):
        def __init__(self, db: Database):
            self.db = db
        
        def get(self, location, week, weekday):
            """Retrieve user profile"""
            room = self.db.get_classroom(location, week, weekday)
            if room is not None:
                return room, 200
            else:
                return {"error": "User not found"}, 404

    def run(self, host="127.0.0.1", port=5000):
        # Registering resources with API
        self.api.add_resource(self.classroom, "/classrom/<string:location>/<int:week>/<int:weekday>", 
                              resource_class_args=[self.db])
        self.app.run(host=host, port=port)


if __name__ == "__main__":
    server = Server("data/test.db")
    server.run()