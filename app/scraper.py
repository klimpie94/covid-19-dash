import requests
import json
import os
import logging
import geopandas as gpd 

from datetime import datetime

logger = logging.getLogger("app.scraper")

def get_init_data():
   """get_init_data 
   This functions retrieves covid data from RIVM.nl and stores it
   in a .txt file

   Returns:
       [bool]: True if succeeded.
   """   
   URL = "https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_per_dag.json"
   logger.info(f"Retrieving data from f{URL}")
   response = requests.get(URL)
   data = response.json()

   dirname = os.path.join(os.path.dirname(__file__), "data.txt")
   logger.info(f"Storing data into f{dirname}")
   with open(dirname, 'w') as f:
      json.dump(data, f, ensure_ascii=False)
   
   return True

if __name__ == "__main__":
   get_init_data()

