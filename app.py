from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_data
import os
from flask_xcaptcha import XCaptcha



app = Flask(__name__)  # instance of class Flask


app.config['XCAPTCHA_SITE_KEY'] = os.environ["XCAPTCHA_SITE_KEY"] 
app.config['XCAPTCHA_SECRET_KEY'] = os.environ["XCAPTCHA_SECRET_KEY"] 
app.config['XCAPTCHA_VERIFY_URL'] = "https://hcaptcha.com/siteverify"
app.config['XCAPTCHA_API_URL'] = "https://hcaptcha.com/1/api.js"
app.config['XCAPTCHA_DIV_CLASS'] = "h-captcha"

sk = os.environ["XCAPTCHA_SITE_KEY"]
xcaptcha = XCaptcha(app=app)


@app.route("/")  # any website has a route. a part of the url after the url
# this is going to match the empty route
def home():
    jobs = load_jobs_from_db()
    return render_template('home.html', jobs=jobs, name="Pier")


@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)


@app.route("/api/job/<id>")
def show_job_api(id):
    job = load_job_from_db(id)
    return jsonify(job)


@app.route("/job/<id>")
def show_job(id):
    job = load_job_from_db(id)
    if not job:
        return render_template("404.html", job=job)
    else:
        return render_template("jobpage.html", job=job)


@app.route("/form")
def form():
    return render_template("form.html", sk = sk)

@app.route("/form/data", methods = ["post"])
def data():
    if xcaptcha.verify():
        data = request.form
        # store in db
        # display an uknowledgement
        # and send an email
        add_data(data)
        return render_template("form_submitted.html", data = data)
    else:
        return render_template("toomanyattempts.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
