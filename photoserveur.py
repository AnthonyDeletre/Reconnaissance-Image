# Serveur pour le détecteur de photo.

import photodetection
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from io import BytesIO


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Projet_Fin_Annee\\Image.db"
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


@app.route("/download")
def download():
    file_data = db.session.query(Image).order_by(Image.id.desc()).first()
    return send_file(BytesIO(file_data.data), attachment_filename="test.jpeg", as_attachment=True)

app.run()

#photodetection.main("test2.jpg")
