from flask import Flask
from flask_restful import Api

from db import db
from resources.covid import Covid



def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our core Flask app
        api = Api(app)
        api.add_resource(Covid,
                 "/covid/<string:date>",
                 "/covid/")

        db.init_app(app)

        # Import Dash application
        from visualizations.dashboard import init_dashboard
        app = init_dashboard(app)

        return app