from flask import Flask,render_template
from plots import *
from linked import db
from modeldb import Matches
from sqlalchemy import create_engine,text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matches.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    engine = create_engine('sqlite:///matches.db', echo=False)
    df= pd.read_csv('dataset\liga_2023.csv')
    df.to_sql('matches', con=engine, if_exists='replace', index=False)


@app.route("/")
def enter_general():
    plots= {
        "frequency_of_winning" : frequencywins_local_or_visit()
    }

    return render_template('web-branches/general.html',plots=plots)

@app.route("/superclasico")
def enter_page_superclasico():
    plots={

    }
    return render_template('web-branches/superclasico.html',plots=plots)

@app.route("/avellanedaclasico")
def enter_page_avellanedaclasico():
    plots={
        
    }
    return render_template('web-branches/avellanedaclasico.html',plots=plots)

@app.route("/rosarioclasico")
def enter_page_rosarioclasico():
    plots={
        
    }
    return render_template('web-branches/rosarioclasico.html',plots=plots)

@app.route("/zonasurclasico")
def enter_page_zonasurclasico():
    plots={
        
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
    app.run(debug=True)

