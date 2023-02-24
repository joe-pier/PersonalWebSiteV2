# connect to database
from sqlalchemy import create_engine, text
import os
db_connection = os.environ["DATABASE_CREDENTIALS"] 
print(db_connection)
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
