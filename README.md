# covid-19-dash
A working (WIP) personal project that integrates Dash into Flask and is able to display Covid-19 related info.

## Installation

```
docker-compose build
docker-compose up
```
If you would like to have the latest data (current data is from 27th February until 21st December 2020), then you'll have to delete the file ```data.db```. In this case, the app will fetch and ingest the latest data from ```RIVM.nl```
into a local sqlite3 database. This happens ```automatically before the first request```, however this also means that you have to wait for a few minutes
(approx. 6 minutes) before the app has started.

## Description of this project
I was interested in displaying Covid-19 data from RIVM.nl with Dash. However, in the end I was more interested in integrating a Dash App into a Flask App
without losing the ability to utilize Flask app in the backend. I also played around with SQLAlchemy without having prior experience in it. 
When you visit the route ```/app/covid/``` you will see a daily update of the latest numbers published by the Dutch Government and also a chart showing how
the numbers have developed in the last months. You have also the ability to 'drill-down' into a specific Province or Municipality of interest, select the timerange
of interest, select an investigation type (positive cases, hospitalizations, deaths) and whether you want to see absolute or relative numbers.

<img src="https://i.imgur.com/brMROUu.png" />

## Implementation

This project is implemented using Flask, Plotly Dash, SQLalchemy and Pandas.

The following routes are implemented:

```
GET  /covid/<string:date>
POST  /covid/
```
- The GET method returns all the records for the specified date.
- The POST method is used to insert data into the sqlite3 db.
