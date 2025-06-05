from flask_sqlalchemy import SQLAlchemy
from linked import db

class Matches(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    local_team = db.Column(db.String(40), nullable=False)
    local_result = db.Column(db.Integer, nullable=False, default=0)
    visit_result = db.Column(db.Integer, nullable=False, default=0)
    visit_team = db.Column(db.String(40), nullable=False)