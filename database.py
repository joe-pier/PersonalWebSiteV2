# connect to database
from sqlalchemy import create_engine, text
import os
db_connection = os.environ["DATABASE_CREDENTIALS"] 

# how to set a secret variable:
# - set the secret variable in github secrets (settings > secrets and variables > actions > repository secrets). 
#   this can be called in the workflow via ${{  secrets.DATABASE_CREDENTIALS  }}
# - at this point we need to set the variable as a enviroment variable everytime render deploys.
#   to do this we create a workflow that sets the enviroment variable DATABASE_CREDENTIALS as ${{ secrets.DATABASE_CREDENTIALS }}
# - now each time we deploy the workflow triggers and the secret variable  secrets.DATABASE_CREDENTIALS is set as an enviroment variable and 
#   we can get it in python via db_connection = os.environ["DATABASE_CREDENTIALS"] 


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
        return jobs
