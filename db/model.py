import urllib
from sqlalchemy_utils import database_exists
from sqlalchemy import Column, Integer, String, DECIMAL, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import ForeignKey, create_engine
from contextlib import contextmanager

Base = declarative_base()


class Bridge(Base):
    __tablename__ = 'bridges'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    longitude = Column(DECIMAL(9, 6))  # per https://stackoverflow.com/questions/1196415/what-datatype-to-use-when-storing-latitude-and-longitude-data-in-sql-databases
    latitude = Column(DECIMAL(8, 6))
    assesed_prognosis = Column(String, default='Ok')
    water_level_threshold_monitor = Column(Float, default=0)
    water_level_threshold_alert = Column(Float, default=0)

    # relationships
    hydro_locations = relationship("Hydro", order_by='Hydro.id', back_populates='bridge')
    weather_locations = relationship("WeatherStation", order_by='WeatherStation.id', back_populates='bridge')


class Hydro(Base):
    __tablename__ = 'hydro_sensors'

    id = Column(Integer, primary_key=True)
    code = Column(String)
    position = Column(String)
    longitude = Column(DECIMAL(9, 6))
    latitude = Column(DECIMAL(8, 6))

    # relationships
    bridge_id = Column(Integer, ForeignKey('bridges.id'))
    bridge = relationship("Bridge", back_populates="hydro_locations")
    hydro_data = relationship("HydroData", back_populates="hydro_sensor")


class HydroData(Base):
    __tablename__ = 'hydro_data'

    id = Column(Integer, primary_key=True)
    data = Column(Float)
    time = Column(DateTime)
    hydro_id = Column(Integer, ForeignKey('hydro_sensors.id'))

    # relationship
    hydro_sensor = relationship("Hydro", back_populates="hydro_data", uselist=False)


class WeatherStation(Base):
    __tablename__ = 'weather_stations'

    id = Column(Integer, primary_key=True)
    grid_x = Column(String)
    grid_y = Column(String)

    # relationships
    bridge_id = Column(Integer, ForeignKey('bridges.id'))
    bridge = relationship("Bridge", back_populates="weather_locations")
    weather_data = relationship("WeatherData", back_populates="weather_station")


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    one_day_forecast = Column(String)
    weather_id = Column(Integer, ForeignKey('weather_stations.id'))
    # relationships
    weather_station = relationship("WeatherStation", back_populates='weather_data', uselist=False)


def _generate_engine(config):

    params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                     f"SERVER={config.SERVER_NAME};"
                                     f"DATABASE={config.DATABASE_NAME};"
                                     f"UID={config.DATABASE_USERNAME};"
                                     f"PWD={config.DATABASE_PASSWORD};"
                                     "MARS_Connection=Yes")

    return create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))


def _get_engine(config, update_structure):
    engine = _generate_engine(config)

    if not database_exists(engine.url):  # Checks for the first time
        Base.metadata.create_all(engine)  # Create new DB
        print("New Database Created" + str(database_exists(engine.url)))  # Verifies if database is there or not.
    elif update_structure:
        Base.metadata.create_all(engine)
        print("Database Structure Updated" + str(database_exists(engine.url)))  # Verifies if database is there or not
    else:
        print("Database Already Exists")
    return engine


def _create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session


def get_session(config, update_structure):
    return _create_session(_get_engine(config, update_structure))

@contextmanager
def session_scope(config, update_structure):
    """Provide a transactional scope around a series of operations."""
    Session = scoped_session(get_session(config, update_structure))
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_bridges_to_plot(session):
    lat = []
    lon = []
    text = []
    status = []
    for bridge in session.query(Bridge).all():
        lat.append(str(float(bridge.latitude)))
        lon.append(str(float(bridge.longitude)))
        text.append(bridge.name)
        status.append(bridge.assesed_prognosis)
    return lat, lon, text, status


def get_matching_bridge(session, bridge_name):
    return session.query(Bridge).filter(Bridge.name == bridge_name).first()


def get_simplified_data(excel_file):
    import pandas as pd
    df = pd.read_excel(excel_file)
    return df


class PsuedoHydroLocation:
    def __init__(self, lat, lon, code):
        self.latitude = lat
        self.longitude = lon
        self.code = code



class PsuedoBridge:
    def __init__(self, lat, lon, prognosis, name, hydro_lats, hydro_lons, hydro_codes):
        self.latitude = lat
        self.longitude = lon
        self.assesed_prognosis = prognosis
        self.name = name
        self.hydro_locations = [PsuedoHydroLocation(item[0], item[1], item[2]) for item in zip(hydro_lats,
                                                                                               hydro_lons,
                                                                                               hydro_codes)]


class BridgeOverride:

    def __init__(self, excel_file):
        import pandas as pd
        self.df = pd.read_excel(excel_file)

    def get_bridges_to_plot(self,):
        lat = []
        lon = []
        text = []
        status = []
        for bridge in self.df.iterrows():
            lat.append(str(float(bridge[1].Lat)))
            lon.append(str(float(bridge[1].Lon)))
            text.append(bridge[1].Bridge_Name)
            status.append(bridge[1].Assessed_Prognosis)
        return lat, lon, text, status

    def get_matching_bridge(self, bridge_name):
        local_df = self.df.loc[self.df.Bridge_Name == bridge_name]
        lat = str(float(local_df.Lat.values[0]))
        lon = str(float(local_df.Lon.values[0]))
        name = local_df.Bridge_Name
        status = local_df.Assessed_Prognosis.values[0]
        hydro_code = local_df.Water_Site_Number.values[0].split(',')
        hydro_lat = local_df.Water_Site_Lat.values[0].split(',')
        hydro_lon = local_df.Water_Site_Lon.values[0].split(',')
        hydro_code = [code.strip() for code in hydro_code]
        hydro_lat = [_lat.strip() for _lat in hydro_lat]
        hydro_lon = [_lon.strip() for _lon in hydro_lon]
        return PsuedoBridge(lat, lon, status, name, hydro_lat, hydro_lon, hydro_code)
