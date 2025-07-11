from flask import Flask,render_template, request, url_for, redirect, flash
from plots import *
from linked import db
from modeldb import Matches
from ML_prediction import modelo


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
        "frequency_of_winning" : frequencywins_local_or_visit(),
        "goles_eachone" : goles_eachone()
    }

    return render_template('web-branches/general.html',plots=plots)

@app.route("/superclasico")
def enter_page_superclasico():
    plots={
        'victoria_acumulada_super' : victoria_acumulada_super(),
        'regresion_lineal_super' : regresion_linear_superclasico()
    }
    return render_template('web-branches/superclasico.html',plots=plots)

@app.route("/avellanedaclasico")
def enter_page_avellanedaclasico():
    plots={
        'victoria_acumulada_avellaneda' : victoria_acumulada_avellaneda(),
        'regresion_lineal_avellaneda' : regresion_linear_avellaneda()
    }
    return render_template('web-branches/avellanedaclasico.html',plots=plots)

@app.route("/rosarioclasico")
def enter_page_rosarioclasico():
    plots={
        'victoria_aculumativa_rosario' : victoria_acumulativa_rosario(),
        'regresion_lineal_rosario' : regresion_linear_rosario()
    }
    return render_template('web-branches/rosarioclasico.html',plots=plots)

@app.route("/zonasurclasico")
def enter_page_zonasurclasico():
    plots={
        'victoria_acumulado_zonasur' : victoria_acumulado_zonasur(),
        'regresion_lineal_zonasur' : regresion_linear_zonasur()
    }
    return render_template('web-branches/zonasurclasico.html',plots=plots)


@app.route("/viewdataset")
def enter_page_viewdataset():
    page = request.args.get('page', 1, type=int)
    per_page = 25
    
    pagination = Matches.query.paginate(page=page, per_page=per_page)
    matches = pagination.items

    # matches = Matches.query.all()
    return render_template('web-branches/viewdataset.html', matches=matches, pagination=pagination)

@app.route("/ML_prediction", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        selected_team = request.form['selected_team']
        selected_local_goals = int(request.form['selected_local_goals'])
        selected_decade = int(request.form['selected_decade'])

        if selected_local_goals > -1 and 1930 <= selected_decade and selected_decade <= 2020:
            equipos = ['Banfield','Boca Juniors','Independiente','Lanus','Newells','Racing Club','River Plate','Rosario Central']
            registro_base = dict.fromkeys(equipos, False)
            registro_base[selected_team] = True

            registro_base.update({
                'local_result': selected_local_goals,
                'year': selected_decade
            })

            nuevo_sample = pd.DataFrame([registro_base])

            pred_value = modelo.predict_proba(nuevo_sample)
            pred_value= int(pred_value[0][1] *100) 
            return render_template('web-branches/ML_prediction.html', pred_value=pred_value)


    return render_template("web-branches/ML_prediction.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

