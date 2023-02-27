# connect to database
from sqlalchemy import create_engine, text
import os
import base64


try:
    # local enviroment
    with open('local.txt') as f:
        lines = [line for line in f]
        db_connection = lines[0]
except:
    db_connection = os.environ["DATABASE_CREDENTIALS"]


# how to set a secret variable:
# - set the secret variable in github secrets (settings > secrets and variables > actions > repository secrets). 
#   this can be called in the workflow via ${{  secrets.DATABASE_CREDENTIALS  }}
# - at this point we need to set the variable as a enviroment variable everytime render deploys.
#   to do this we create a workflow that sets the enviroment variable DATABASE_CREDENTIALS as ${{ secrets.DATABASE_CREDENTIALS }}
# - now each time we deploy the workflow triggers and the secret variable  secrets.DATABASE_CREDENTIALS is set as an enviroment variable and 
#   we can get it in python via db_connection = os.environ["DATABASE_CREDENTIALS"] 
# - last thing to do is set the enviroment variable DATABASE_CREDENTIALS also on render. 
# at the end of the process the password is not visible on github and at each deployment we can get the secret enviroment variable from github


engine = create_engine(db_connection, connect_args= 
    {
    "ssl": {
        "sll_ca": "/etc/ssl/cert.pem"
            }
    })

def encode_binary_response(response):
        """ encode the icon response from the database. remember that Json type do not natively support binary data"""
        jobs_dict = []
        for row in response:
            row_dict = dict(row)
            if row_dict["icon"] == None:
                jobs_dict.append(row_dict)
            else:
                base64_encoded_image = base64.b64encode(row_dict["icon"]).decode("utf-8")
                row_dict.update({"icon": base64_encoded_image})
                jobs_dict.append(row_dict)
        return jobs_dict

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = result.mappings().all()
        jobs_dict = encode_binary_response(jobs)
    return jobs_dict


def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from jobs WHERE id = {id}"))
        job = result.mappings().all()
        jobs_dict = encode_binary_response(job)
        if len(jobs_dict)==0:
            return None
        else:
            return dict(jobs_dict[0])
        

def add_data(data):
    with engine.connect() as conn:
        name = data["Name"]
        last_name =data["Last Name"]
        email = data["Email"]
        linkedin = data["Linkedin"]
        notes =  data["notes"]
        query = text(f"INSERT INTO `pierpersonalwebpage`.`user_data` (`name`, `last_name`, `email`,`linkedin`, `notes`) VALUES ('{name}', '{last_name}', '{email}', '{linkedin}', '{notes}')")
        conn.execute(query)


def get_login_info():
    with engine.connect() as conn:
        login_info = conn.execute(text(f"SELECT * FROM pierpersonalwebpage.login"))
        login_info_results = login_info.mappings().all()
        return dict(login_info_results[0])
    

def get_recorded_info():
    with engine.connect() as conn:
        login_info = conn.execute(text(f"SELECT * FROM pierpersonalwebpage.user_data"))
        login_info_results = login_info.mappings().all()
        return login_info_results
    

def get_record_info(id):
    with engine.connect() as conn:
        data_contact = conn.execute(text(f"SELECT * FROM pierpersonalwebpage.user_data WHERE id = {id}"))
        data_contact_results = data_contact.mappings().all()
        if not data_contact_results:
            pass
        else:
            return dict(data_contact_results[0])

def remove_data_query(id):
    with engine.connect() as conn:
        return conn.execute(text(f"DELETE FROM `pierpersonalwebpage`.`user_data` WHERE (`id` = '{id}'); "))


def load_projects_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from projects"))
        projects = result.mappings().all()
        projects_dict = encode_binary_response(projects)
    return projects_dict

def load_project_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from projects WHERE id = {id}"))
        project = result.mappings().all()
        project_dict = encode_binary_response(project)
        if len(project_dict)==0:
            return None
        else:
            return dict(project_dict[0])



def load_skills_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from skills"))
        skills = result.mappings().all()
        skills_dict = encode_binary_response(skills)
    return skills_dict