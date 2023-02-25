from flask import Flask, render_template, jsonify
from database import load_jobs_from_db, load_job_from_db

app = Flask(__name__) # instance of class Flask

UPLOAD_FOLDER = './uploads'

@app.route("/") # any website has a route. a part of the url after the url
# this is going to match the empty route
def home():
    jobs = load_jobs_from_db()
    return render_template('home.html', jobs= jobs ,name = "Pier")

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
        return render_template("404.html", job = job) 
    else:
        return render_template("jobpage.html", job = job)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)