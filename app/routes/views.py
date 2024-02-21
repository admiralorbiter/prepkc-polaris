from flask import render_template
from app import app, db

# Home Page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
