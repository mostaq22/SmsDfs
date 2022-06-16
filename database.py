import os
from settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine(Settings().database_url)

Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)  # exporting
