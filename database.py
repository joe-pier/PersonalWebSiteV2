# connect to database
from sqlalchemy import create_engine, text
import os
from PIL import Image
from io import BytesIO
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

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = result.mappings().all()
        new_jobs = []
        for row in jobs:
            row = dict(row)
            if row["icon"] == None:
                new_jobs.append(row)
            else:
                base64_encoded_image = base64.b64encode(row["icon"]).decode("utf-8")
                row.update({"icon": base64_encoded_image})
                new_jobs.append(row)
        return new_jobs


def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs WHERE id = :val"), val = id)
        rows = result.all()
        if len(rows)==0:
            return None
        else:
            return dict(rows[0])