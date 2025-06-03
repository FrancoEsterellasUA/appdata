from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Matches(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    local_team = db.Column(db.String)
    local_result = db.Column(db.Integer)
    visit_result = db.Column(db.Integer)
    visit_team = db.Column(db.String)