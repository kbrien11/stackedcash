from app import run
from app import user
from app import Job

User.dbpath = 'data/stacked.db'
Job.dbpath = 'data/stacked.db'

run()