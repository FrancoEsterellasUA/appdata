from flask import Flask,render_template
from plots import *

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)

