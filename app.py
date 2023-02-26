from flask import Flask, render_template, jsonify, request, session
from database import load_jobs_from_db, load_job_from_db, add_data, get_login_info, get_recorded_info, get_record_info, remove_data_query
import os
from flask_xcaptcha import XCaptcha


app = Flask(__name__)  # instance of class Flask

try:
    # local enviroment, not synched in github ;)
    with open('local.txt') as f:
        lines = [line for line in f]
    app.config['XCAPTCHA_SITE_KEY'] = lines[2]
    app.config['XCAPTCHA_SECRET_KEY'] = lines[1]
    sk = lines[2]
    app.secret_key =lines[3]
except:
    app.config['XCAPTCHA_SITE_KEY'] = os.environ["XCAPTCHA_SITE_KEY"]
    app.config['XCAPTCHA_SECRET_KEY'] = os.environ["XCAPTCHA_SECRET_KEY"]
    sk = os.environ["XCAPTCHA_SITE_KEY"]
    app.secret_key = os.environ["secret_key"]


app.config['XCAPTCHA_VERIFY_URL'] = "https://hcaptcha.com/siteverify"
app.config['XCAPTCHA_API_URL'] = "https://hcaptcha.com/1/api.js"
app.config['XCAPTCHA_DIV_CLASS'] = "h-captcha"


xcaptcha = XCaptcha(app=app)


# any website has a route. a part of the url after the url this is going to match the empty route
@app.route("/")
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
    return render_template("form.html", sk=sk)


@app.route("/form/data", methods=["post"])
def data():
    cv = xcaptcha.verify()
    if cv:
        data = request.form
        # store in db
        # display an uknowledgement
        # and send an email
        add_data(data)
        return render_template("form_submitted.html", data=data)
    else:
        return render_template("toomanyattempts.html")


@app.route("/login", methods=["get"])
def login():
    return render_template("login.html")


@app.route("/login/data", methods=["post"])
def login_data():
    cv = xcaptcha.verify()
    if cv:
        login_data_query = get_login_info()
        login_data = request.form
        if (login_data["Name"] == login_data_query["username"]) & (login_data["password"] == login_data_query["password"]):
            session["username"] = login_data["Name"]
            session["password"] = login_data["password"]
            print(session)
            data = get_recorded_info()
            return render_template("table.html", data=data)
        else:
            return render_template("login_error.html")
    else:
        return render_template("toomanyattemptslogin.html")


@app.route("/login/data/remove", methods=["post"])
def remove_data():
    id_user = dict(request.form)
    user_data = get_record_info(id_user["id"])
    if not user_data:  # check existense of data
        return render_template("404_remove.html")
    else:
        remove_data_query(id_user["id"])
        return render_template("elimination_confirmation.html", user_data=user_data)

@app.route("/logout")
def logout():
    if "username" not in list(session.keys()):
        return render_template("logouterror.html")
    
    else:
        session.pop("username")
        session.pop("password")
        return render_template("logout.html")
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
