from flask import Flask, render_template, jsonify, request, session
from database import load_jobs_from_db, load_job_from_db, add_data, get_login_info, get_recorded_info, get_record_info, remove_data_query, load_projects_from_db,load_project_from_db
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
    app.secret_key = lines[3]
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
    projects = load_projects_from_db()
    return render_template('home.html', jobs=jobs,projects = projects, name="Pier")



@app.route("/job/<id>")
def show_job(id):
    job = load_job_from_db(id)
    if not job:
        return render_template("404.html", job=job)
    else:
        return render_template("jobpage.html", job=job)

@app.route("/project/<id>")
def show_projects(id):
    project = load_project_from_db(id)
    if not project:
        return render_template("404.html", project=project)
    else:
        return render_template("projectpage.html", project=project)

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
    return render_template("login.html", session=list(session.keys()))


@app.route("/login/data", methods=["post"])
def login_data():
    if "captcha" not in list(session.keys()):
        cv = xcaptcha.verify()
        if cv:
            login_data_query = get_login_info()
            login_data = request.form
            # to retain the access i have to put here a condition to check the presence of user and password in the sessions cookies
            if (login_data["Name"] == login_data_query["username"]) & (login_data["password"] == login_data_query["password"]):
                session["username"] = login_data["Name"]
                session["password"] = login_data["password"]
                session["captcha"] = True
                data = get_recorded_info()
                return render_template("table.html", data=data)
            else:
                return render_template("login_error.html")
        else:
            return render_template("toomanyattemptslogin.html")
    else:
        login_data_query = get_login_info()
        login_data = request.form
        if (login_data["Name"] == login_data_query["username"]) & (login_data["password"] == login_data_query["password"]):
            session["username"] = login_data["Name"]
            session["password"] = login_data["password"]
            session["captcha"] = True
            data = get_recorded_info()
            return render_template("table.html", data=data)
        else:
            return render_template("login_error.html")


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
    if len(list(session.keys())) == 0:
        return render_template("logouterror.html")

    else:
        try:
            session.pop("username")
        except:
            pass
        try:
            session.pop("password")
        except:
            pass
        try:
            session.pop("captcha")
        except:
            pass
    return render_template("logout.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
