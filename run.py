from app import app
from db import db

db.init_app(app)


@app.before_first_request  # Registers a function to be run before the first request to this instance of the application
def create_tables():
    db.create_all()