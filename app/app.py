from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def enter_general():
    return render_template('web-branches/general.html')

@app.route("/superclasico")
def enter_page_superclasico():
    return render_template('web-branches/superclasico.html')

@app.route("/avellanedaclasico")
def enter_page_avellanedaclasico():
    return render_template('web-branches/avellanedaclasico.html')

@app.route("/rosarioclasico")
def enter_page_rosarioclasico():
    return render_template('web-branches/rosarioclasico.html')

@app.route("/zonasurclasico")
def enter_page_zonasurclasico():
    return render_template('web-branches/zonasurclasico.html')

if __name__ == "__main__":
    app.run(debug=True)

