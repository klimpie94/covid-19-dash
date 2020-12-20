from flask import Flask
from flask_restful import Api

from resources.covid import Covid
from db import db
from visualizations.dash_App import create_dash
from models.covid import CovidCases, PopulationModel

import webbrowser
server = Flask(__name__)
api = Api(server)
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db.init_app(server)

api.add_resource(Covid,
                 "/covid/<string:date>",
                 "/covid/")

@server.before_first_request
def create_tables():
    db.create_all()
    CovidCases.init_db_data()
    PopulationModel.init_db_data()
    create_dash(server)


if __name__ == "__main__":
    server.run(port=4999, debug=True)

