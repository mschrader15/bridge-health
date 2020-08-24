import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import pyodbc
import pandas as pd
from sqlalchemy_utils.functions import database_exists
from index import config, paths
import urllib
from db.model import Base, Bridge, Hydro, get_session
from functions.waterservices_api import get_lat_lon


def generate_engine():

    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                     f"SERVER={config.SERVER_NAME};"
                                     f"DATABASE={config.DATABASE_NAME};"
                                     f"UID={config.DATABASE_USERNAME};"
                                     f"PWD={config.DATABASE_PASSWORD}")

    return sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))


def validate_database(update_structure):
    engine = generate_engine()
    if not database_exists(engine.url):  # Checks for the first time
        Base.metadata.create_all(engine) # Create new DB
        print("New Database Created" + str(database_exists(engine.url)))  # Verifies if database is there or not.
    elif update_structure:
        Base.metadata.create_all(engine)
        print("Database Structure Updated" + str(database_exists(engine.url)))  # Verifies if database is there or not
    else:
        print("Database Already Exists")
    return engine


def create_session(engine):
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()



def add_bridges(bridge_df, session):

    # SHOULDN'T ITERATE DOWN A PANDAS DF BUT I DON'T THINK IT WILL BE THAT LONG
    current_bridge_names = [bridge.name for bridge in session.query(Bridge).all()]
    for i, bridge_name in enumerate(list(bridge_df['Bridge_Name'])):
        if bridge_name not in current_bridge_names:
            new_bridge = Bridge(name=bridge_name, latitude=bridge_df['Lat'].iloc[i],
                                longitude=bridge_df['Lon'].iloc[i])
            session.add(new_bridge)
        else:
            local_bridge = session.query(Bridge).filter(Bridge.name == bridge_name).all()[0]
            write = False
            if bridge_df['Lat'].iloc[i] != float(local_bridge.latitude):
                local_bridge.latitude = bridge_df['Lat'].iloc[i]
                write = True
            if bridge_df['Lon'].iloc[i] != float(local_bridge.longitude):
                local_bridge.longitude = bridge_df['Lon'].iloc[i]
                write = True
            if write:
                session.add(local_bridge)
    session.commit()


def add_hydro_locations(bridge_df, session):

    local_df = bridge_df.set_index('Bridge_Name')

    for bridge in session.query(Bridge).all():
        hydro_locations = [location.code for location in bridge.hydro_locations]
        hydro_sensors = local_df.loc[bridge.name, 'Water_Site_Number'].split(',')
        hydro_sensors = [sensor.strip() for sensor in hydro_sensors]
        for sensor in hydro_sensors:
            if sensor not in hydro_locations:
                hydro = Hydro(code=sensor)
                bridge.hydro_locations.append(hydro)
                session.add(bridge)
            else:
                hydro = session.query(Hydro).filter(Hydro.code == sensor).first()
                hydro.latitude, hydro.longitude = get_lat_lon(sensor)
                session.add(hydro)
    session.commit()


# def add_weather_locations(bridge_df, session):
#
#     local_df = bridge_df.set_index('Bridge_Name')
#     for bridge in session.query(Bridge).all():


if __name__ == "__main__":

    update_structure = False

    bridge_file = paths.BRIDGE_EXCEL
    bridge_df = pd.read_excel(bridge_file, dtype={'Water_Site_Number': str})

    session = get_session(config, update_structure)

    add_bridges(bridge_df, session)
    add_hydro_locations(bridge_df, session)


