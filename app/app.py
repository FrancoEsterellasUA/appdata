from flask import Flask,render_template
from plots import *
from linked import db
from modeldb import Matches
from sqlalchemy import create_engine,text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matches.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

df = clasicos

with app.app_context():
    db.create_all()

    Matches.query.delete()
    db.session.commit()

    for _, row in clasicos.iterrows():
        match = Matches(
            date_name=row['date_name'],
            local_team=row['local_team'],
            local_result=row['local_result'],
            visit_result=row['visitor_result'],
            visit_team=row['visitor_team']
        )
        db.session.add(match)

    db.session.commit()


@app.route("/")
def enter_general():
    plots= {
        "frequency_of_winning" : frequencywins_local_or_visit()
    }

    return render_template('web-branches/general.html',plots=plots)

@app.route("/superclasico")
def enter_page_superclasico():
    plots={
        'victoria_acumulada_super' : victoria_acumulada_super()
    }
    return render_template('web-branches/superclasico.html',plots=plots)

@app.route("/avellanedaclasico")
def enter_page_avellanedaclasico():
    plots={
        'victoria_acumulada_avellaneda' : victoria_acumulada_avellaneda()
    }
    return render_template('web-branches/avellanedaclasico.html',plots=plots)

@app.route("/rosarioclasico")
def enter_page_rosarioclasico():
    plots={
        'victoria_aculumativa_rosario' : victoria_aculumativa_rosario()
    }
    return render_template('web-branches/rosarioclasico.html',plots=plots)

@app.route("/zonasurclasico")
def enter_page_zonasurclasico():
    plots={
        'victoria_acumulado_zonasur' : victoria_acumulado_zonasur()
    }
    return render_template('web-branches/zonasurclasico.html',plots=plots)

@app.route("/chargedataset")
def enter_page_chargedataset():
    return render_template('web-branches/chargedataset.html')

@app.route("/viewdataset")
def enter_page_viewdataset():
    matches = Matches.query.all()
    return render_template('web-branches/viewdataset.html', matches=matches)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

