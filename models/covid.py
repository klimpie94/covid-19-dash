import os
import math
import json
import logging
import pandas as pd

from db import db
from scraper import get_init_data
from datetime import datetime
from sqlalchemy import func

logger = logging.getLogger("app.model")


class CovidCases(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Date_of_publication = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Total_reported = db.Column(db.Integer, nullable=False)
    Hospital_admission = db.Column(db.Integer, nullable=False)
    Deceased = db.Column(db.Integer, nullable=False)
    Province = db.Column(db.String(50), nullable=False)
    Municipality_name = db.Column(db.String(100),db.ForeignKey("populations.Municipality_name"), nullable=False, default="Unknown")
    population = db.relationship('PopulationModel')

    def __repr__(self):
        return f"CovidCase({self.Date_of_publication}', '{self.Province}', '{self.Municipality_name}', '{self.Total_reported}')"

    
    @classmethod
    def find_by_date(cls, date):
        return CovidCases.query.filter_by(Date_of_publication=date).all()
    
    @classmethod
    def find_unique_values_in_col(cls, column):
        values = [getattr(r, column) for r in CovidCases.query.with_entities(CovidCases.__table__.c[column]).distinct()]
        return values
    
    @classmethod
    def find_by_timerange(cls, start_date, end_date):
        return (CovidCases.query
                .filter(CovidCases.Date_of_publication <= end_date)
                .filter(CovidCases.Date_of_publication >= start_date)
                .all()
                )

    @classmethod
    def find_by_timerange_and_place(cls, start_date, end_date, input_col, place, investigation_type):
        """find_by_timerange_and_place 
        This function get's the absolute numbers for a
        selected timerange, place and investigation type

        Args:
            start_date ([datetime]): Start date of investigation.
            end_date ([datetime]): End date of investigation.
            input_col ([string]): Province or City
            place ([string]): Province or City Name
            investigation_type ([string]): Type of investigation.

        Returns:
            [Pandas DataFrame]: Dataframe containing the absolute numbers.
        """       
        data = (CovidCases.query
                .filter(CovidCases.Date_of_publication <= end_date)
                .filter(CovidCases.Date_of_publication >= start_date)
                .filter(CovidCases.__table__.c[input_col] == place)
                .all()
                )
        df = pd.DataFrame([(d.Date_of_publication, getattr(d, input_col), getattr(d, investigation_type)) for d in data], 
                  columns=['Date_of_publication', input_col, investigation_type])
        return df

    @classmethod
    def get_total_positives(cls, column):
        date = datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
        result = (CovidCases.query
        .with_entities(CovidCases.Date_of_publication, func.sum(CovidCases.__table__.c[column]))
        .group_by(CovidCases.Date_of_publication)
        .order_by(CovidCases.Date_of_publication.desc())
        .first()
        )
        return (result[0].strftime("%d %B, %Y"), result[1])
    
    @classmethod
    def init_db_data(cls):
        """init_db_data
        This function populates the SQLite3 with Covid data on startup 
        of the app.

        Returns:
            [String]: Message indicating the result of the insert statement.
        """        
        if CovidCases.query.count() >= 1:
            return None
        get_init_data()
        dirname = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        filename = os.path.join(dirname, 'data.txt')
        with open(filename, 'r') as f:
            data = json.load(f)

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
                logger.critical("An exception has occured:", e)
                return {"Message": "An error occured while inserting the record"}
            logger.info("All records have been succesfully created!")
        return {"Message": "All records have been succesfully created!"}

    def json(self):
        return {"Date_of_report": self.Date_of_publication.strftime("%Y-%m-%d %H:%M:%S"), "Municipality_name": self.Municipality_name, "Total_reported": self.Total_reported}

    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class PopulationModel(db.Model):

    __tablename__ = "populations"

    Municipality_name = db.Column(db.String(100), primary_key=True,
     default="Unknown")
    Population = db.Column(db.Integer, nullable=False)

    cases = db.relationship("CovidCases")

    def __repr__(self):
        return f"{self.Population}"

    @classmethod
    def get_relative_cases_by_timerange_and_place(cls, start_date, end_date, input_col, place, investigation_type):
        """get_relative_cases_by_timerange_and_place 
        This function get's the relative numbers per 100k residents for a
        selected timerange, place and investigation type

        Args:
            start_date ([datetime]): Start date of investigation.
            end_date ([datetime]): End date of investigation.
            input_col ([string]): Province or City
            place ([string]): Province or City Name
            investigation_type ([string]): Type of investigation.

        Returns:
            [Pandas DataFrame]: Dataframe containing the relative numbers.
        """        
        data = (CovidCases.query.join(PopulationModel,
                PopulationModel.Municipality_name 
                == 
                CovidCases.Municipality_name,
                isouter=True)
                .filter(CovidCases.Date_of_publication <= end_date)
                .filter(CovidCases.Date_of_publication >= start_date)
                .filter(CovidCases.__table__.c[input_col] == place)
                .all()
                )
        df = pd.DataFrame([(d.Date_of_publication, d.population, getattr(d, input_col), getattr(d, investigation_type)) for d in data], 
                  columns=['Date_of_publication', 'population', input_col, investigation_type])
        df['population'] = df['population']. fillna(0)
        df = df.astype({'population': 'str'}).astype({'population': 'int32'}) #query returns a Populationmodel, cannot convert directly to int... look for something cleaner later
        df[f"{investigation_type}_per_100000"] = df['population'] / 100000 * df[investigation_type]
        df[f"{investigation_type}_per_100000"] = df[[f"{investigation_type}_per_100000"]].apply(lambda x: pd.Series.round(x))
        return df

    @classmethod
    def init_db_data(cls):
        """init_db_data
        This function populates the SQLite3 with (local) Population data on 
        startup of the app.

        Returns:
            [String]: Message indicating the result of the insert statement.
        """   
        if PopulationModel.query.count() >= 1:
            return None
        dirname = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        filename = os.path.join(dirname, 'data/population_data.csv')
        df = pd.read_csv(filename)

        for _, row in df.iterrows():
            row = PopulationModel(
                            Municipality_name=row["Municipality_name"],
                            Population=row["Population"]
                            )
            try:
                row.save_to_db()
            except Exception as e:
                print("An exception has occured:", e)
                return {"Message": "An error occured while inserting the record"}
        return {"Message": "All records have been succesfully created!"}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    