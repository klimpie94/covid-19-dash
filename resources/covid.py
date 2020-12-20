from flask import request
from flask_restful import Resource, reqparse
from models.covid import CovidCases
from datetime import datetime


class Covid(Resource):

    parser = reqparse.RequestParser()

    def get(self, date):
        datetime_obj = datetime.strptime(date, "%Y-%m-%d")
        covid_data = CovidCases.find_by_date(datetime_obj)
        
        if covid_data:
            return {"records": [row.json() for row in covid_data]}
        return {"Message": "No data found for this date"}, 404


    def post(self):
        data = request.get_json()

        for record in data:
            row = CovidCases(Date_of_publication=datetime.strptime(record["Date_of_publication"], "%Y-%m-%d"),
                            Total_reported=record["Total_reported"],
                            Hospital_admission=record["Hospital_admission"],
                            Deceased=record["Deceased"],
                            Province=record["Province"],
                            Municipality_name=record["Municipality_name"]
                            )
            try:
                row.save_to_db()
            except Exception as e:
                print("An exception has occured:", e)
                return {"Message": "An error occured while inserting the record"}, 500

        return {"Message": "All records have been succesfully created!"}, 201
