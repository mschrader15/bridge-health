import plotly.graph_objects as go
# import numpy as np
# from main import SESSION, get_bridges_to_plot
from index import config
from db.model import get_bridges_to_plot, get_matching_bridge
import math


def _get_central_location(lat, lon):
    x = 0.0
    y = 0.0
    z = 0.0
    for coords in zip(lat, lon):
        latitude = math.radians(float(coords[0]))
        longitude = math.radians(float(coords[1]))
        x += math.cos(latitude) * math.cos(longitude)
        y += math.cos(latitude) * math.sin(longitude)
        z += math.sin(latitude)
    total = len(lat)
    x = x / total
    y = y / total
    z = z / total
    central_longitude = math.atan2(y, x)
    central_square_root = math.sqrt(x * x + y * y)
    central_latitude = math.atan2(z, central_square_root)
    return math.degrees(central_latitude), math.degrees(central_longitude)


def geo_located_bridges_excel(session):
    bridges = session.get_bridges_to_plot()
    lat_mid, lon_mid = _get_central_location(bridges[0], bridges[1])

    fig = go.Figure()

    for i, _ in enumerate(bridges[0]):
        fig.add_trace(
            go.Scattermapbox(lat=[bridges[0][i]],
                             lon=[bridges[1][i]],
                             text=[bridges[2][i]],
                             #fillcolor=[config.STATUS_COLOR_DICT[status] for status in bridges[3]],
                             marker=go.scattermapbox.Marker(#symbol='Bridge',
                                                            size=15,
                                                            color=config.STATUS_COLOR_DICT[bridges[3][i]],
                                                            opacity=0.7
                                                            )))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=config.MAPBOX_KEY,
            bearing=0,
            center=dict(
                lat=lat_mid,
                lon=lon_mid
            ),
            pitch=0,
            zoom=5
        ),
    )
    fig.update_layout(config.PLOT_LAYOUT,
                      title=dict(text="Bridge Overview",
                                 x=0.5)
                      )

    return fig


def geo_located_bridges(session):
    bridges = get_bridges_to_plot(session)
    lat_mid, lon_mid = _get_central_location(bridges[0], bridges[1])

    fig = go.Figure()

    for i, _ in enumerate(bridges[0]):
        fig.add_trace(
            go.Scattermapbox(lat=[bridges[0][i]],
                             lon=[bridges[1][i]],
                             text=[bridges[2][i]],
                             #fillcolor=[config.STATUS_COLOR_DICT[status] for status in bridges[3]],
                             marker=go.scattermapbox.Marker(#symbol='Bridge',
                                                            size=15,
                                                            color=config.STATUS_COLOR_DICT[bridges[3][i]],
                                                            opacity=0.7
                                                            )))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=dict(
            accesstoken=config.MAPBOX_KEY,
            bearing=0,
            center=dict(
                lat=lat_mid,
                lon=lon_mid
            ),
            pitch=0,
            zoom=5
        ),
    )
    fig.update_layout(config.PLOT_LAYOUT,
                      title=dict(text="Bridge Overview",
                                 x=0.5)
                      )

    return fig


def geo_located_bridge_sensor(session, bridge_name):
    bridge = get_matching_bridge(session, bridge_name)

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(lat=[str(float(bridge.latitude))],
                                   lon=[str(float(bridge.longitude))],
                                   text=bridge.name,
                                   marker=go.scattermapbox.Marker(size=30,
                                                                  color=config.STATUS_COLOR_DICT[
                                                                      bridge.assesed_prognosis],
                                                                  ),
                                   name='Bridge'
                                   ),
                  )

    for i, hydro in enumerate(bridge.hydro_locations):
        fig.add_trace(go.Scattermapbox(lat=[str(float(hydro.latitude))],
                                       lon=[str(float(hydro.longitude))],
                                       text=hydro.code,
                                       marker=go.scattermapbox.Marker(size=20,
                                                                      color=config.PLOT_COLORS[i],
                                                                      ),
                                       name='USGS Monitoring Location ' + hydro.code
                                       )
                      )

    lat = [bridge.latitude] + [hydro.latitude for hydro in bridge.hydro_locations]
    lon = [bridge.longitude] + [hydro.longitude for hydro in bridge.hydro_locations]
    lat_mid, lon_mid = _get_central_location(lat, lon)

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=dict(
            accesstoken=config.MAPBOX_KEY,
            bearing=0,
            center=dict(
                lat=lat_mid,
                lon=lon_mid
            ),
            style='basic',
            pitch=0,
            zoom=8
        ),
    )

    fig.update_layout(config.PLOT_LAYOUT,
                      title=dict(text=bridge_name + " and corresponding USGS Monitoring Sites",
                                 x=0.5)
                      )

    return fig

def geo_located_bridge_sensor_excel(session, bridge_name):
    bridge = session.get_matching_bridge(bridge_name)

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(lat=[str(float(bridge.latitude))],
                                   lon=[str(float(bridge.longitude))],
                                   text=bridge.name,
                                   marker=go.scattermapbox.Marker(size=30,
                                                                  color=config.STATUS_COLOR_DICT[
                                                                      bridge.assesed_prognosis],
                                                                  ),
                                   name='Bridge'
                                   ),
                  )

    for i, hydro in enumerate(bridge.hydro_locations):
        fig.add_trace(go.Scattermapbox(lat=[str(float(hydro.latitude))],
                                       lon=[str(float(hydro.longitude))],
                                       text=hydro.code,
                                       marker=go.scattermapbox.Marker(size=20,
                                                                      color=config.PLOT_COLORS[i],
                                                                      ),
                                       name='USGS Monitoring Location ' + hydro.code
                                       )
                      )

    lat = [bridge.latitude] + [hydro.latitude for hydro in bridge.hydro_locations]
    lon = [bridge.longitude] + [hydro.longitude for hydro in bridge.hydro_locations]
    lat_mid, lon_mid = _get_central_location(lat, lon)

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=dict(
            accesstoken=config.MAPBOX_KEY,
            bearing=0,
            center=dict(
                lat=lat_mid,
                lon=lon_mid
            ),
            style='basic',
            pitch=0,
            zoom=8
        ),
    )

    fig.update_layout(config.PLOT_LAYOUT,
                      title=dict(text=bridge_name + " and corresponding USGS Monitoring Sites",
                                 x=0.5)
                      )

    return fig