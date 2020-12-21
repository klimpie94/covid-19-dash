from server import init_app
from models.covid import CovidCases, PopulationModel


app = init_app()

@app.before_first_request
def create_tables():
    app.logger.info("Populating tables with data... (approx. 5minutes)")
    CovidCases.init_db_data()
    PopulationModel.init_db_data()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4999)