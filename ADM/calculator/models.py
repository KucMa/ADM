from flask_sqlalchemy import SQLAlchemy
from .view import app
import logging as lg

# Create database connection abject
db = SQLAlchemy(app)

def init_db():
    db.drop_all()
    db.create_all()
    ...
    db.session.commit()
    lg.warning("Database initialized!")


