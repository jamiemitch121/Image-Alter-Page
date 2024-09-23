from flask import Flask, session, redirect, url_for, render_template,request
from random import randint
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed
import os
from timbrooks import process
app = Flask(__name__)
app.config['SECRET_KEY'] = str(randint(10000,99999))
app.config['UPLOAD_FOLDER'] = "static/files"

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    string = StringField("String", validators=[InputRequired()])
    submit = SubmitField("Generate")


@app.route('/', methods = ["GET","POST"])
def upload():

    form = UploadFileForm()
    print(form.validate_on_submit())
    if session.get('var') == None:
        var = "Upload an image and provide a prompt on how to change it:"
    else:
        var ="Accepted file formats:jpeg,png"
    if form.validate_on_submit() and (str((form.file.data).filename)).lower().endswith(('.png', '.jpg', '.jpeg')):
        file=form.file.data
        prompt = form.string.data
        location = (os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        print (file.filename)
        file.save(location)
        session['FileLocation'] = location
        session['Prompt'] = prompt
        session.pop('var')
        return redirect (url_for ('loadingpage'))
    else:
        session['var']=False
    return render_template("upload.html", form = form, var = var)

@app.route('/loading', methods = ["GET","POST"])
def loadingpage():
    return render_template("loadingpage.html")


@app.route("/processing", methods=['GET','POST'])
def processing():
    process(session['FileLocation'],session['Prompt'])

@app.route("/resultspage", methods=['GET','POST'])
def resultspage():
    return render_template("resultspage.html")

if __name__=="__main__":
    app.run (debug=True)