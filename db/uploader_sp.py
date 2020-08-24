import sqlalchemy as sa
import pyodbc
from sqlalchemy import create_engine
import pandas as pd

server_name = 'tcp:hanson-bridge-monitor.database.windows.net'
database_name = 'Hanson-Bridge-Monitor'
Trusted_Connection = 'yes'
username = 'mcschrader'
password = 'br1dge-health'

ip = 'hanson-bridge-monitor.database.windows.net'
#%%
import urllib
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 f"SERVER={server_name};"
                                 f"DATABASE={database_name};"
                                 f"UID={username};"
                                 f"PWD={password}")
engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
conn = engine.connect()
# #%%
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()

# #%%
# from db.model import Base
# Base.metadata.create_all(engine)

#%%

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#%%
from db.model import Bridge

# bridge = Bridge(name='St. Charles Bridge', latitude=38.797440, longitude=-90.467333)
# session.add(bridge)
# session.commit()

#%%
for instance in session.query(Bridge).order_by(Bridge.id):
    print(instance.name)
#%%

obj = session.query(Bridge).filter(Bridge.name == 'St. Charles Bridge')
x  = obj.all()


