from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import requests
import json


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Chemin Base de donnée
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Projet_Fin_Annee\\Image.db"
db = SQLAlchemy(app)


# Table Image
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Team page
@app.route("/team")
def setting():
    return render_template("setting.html")


# Upload POST
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Recuperation du fichier
        file = request.files["inputFile"]

        # Insertion dans la base donnée
        insert = Image(name=file.filename, data=file.read())
        db.session.add(insert)
        db.session.commit()

        # Recuperation du derniere element dans la base
        last_element = db.session.query(Image).order_by(Image.id.desc()).first()

        # JSON contenant l'id
        file_json = {"id": str(last_element.id)}

        # Envoi du JSON vers l'url
        post = requests.post("https://reqres.in/api/users", json=file_json)

        # Recuperation de la réponse
        data = json.loads(post.text)

        # Nom du batiment
        #batiment = data["Batiment"]

        map_data = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2126.6282985838366!2d3.5122635687822696!3d50.32313768950786!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c2ed11058b6523%3A0x63b3867ba97e7164!2sB%C3%A2timent+Abel+de+Pujol%2C+59300+Famars!5e0!3m2!1sfr!2sfr!4v1557771544177!5m2!1sfr!2sfr'

        # Batiment : ISTV1
        #if batiment == "istv1":
            #map_data = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2126.6282985838366!2d3.5122635687822696!3d50.32313768950786!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c2ed11058b6523%3A0x63b3867ba97e7164!2sB%C3%A2timent+Abel+de+Pujol%2C+59300+Famars!5e0!3m2!1sfr!2sfr!4v1557771544177!5m2!1sfr!2sfr'
            #return render_template("search.html", json=map_data)

        # Batiment : ISTV2
        #if batiment == "istv2":
            #map_data = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2126.6947153303863!2d3.511610135130436!3d50.321653301192846!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c2ed11244cd9a5%3A0xc4acf45da2bc3313!2sB%C3%A2timent+Abel+de+Pujol+2%2C+59300+Famars!5e0!3m2!1sfr!2sfr!4v1557771601194!5m2!1sfr!2sfr'
            #return render_template("search.html", json=map_data)

        # Batiment : ISTV3
        #if batiment == "istv3":
            #map_data = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2126.7400140506998!2d3.5115668416801302!3d50.32064087420671!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47c2ed16d3fa1195%3A0xafaf75735f7fc3f0!2sB%C3%A2timent+Abel+de+Pujol+3%2C+59300+Famars!5e0!3m2!1sfr!2sfr!4v1557771662315!5m2!1sfr!2sfr'
            #return render_template("search.html", json=map_data)

        return render_template("search.html", json=map_data)
        #return data["Batiment"]

    else:
        return render_template("search.html")


# Recuperation du derniere fichier
@app.route("/download")
def download():
    file_data = db.session.query(Image).order_by(Image.id.desc()).first()

    return send_file(BytesIO(file_data.data), attachment_filename="test.jpeg", as_attachment=True)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
