import plotly.graph_objects as go
from db.model import get_bridges_to_plot, get_matching_bridge
from functions.waterservices_api import get_data
from functions.weather_api import get_future_precipitation
from index import config


class HistoricalMonitor:
    """
    This class is to monitor the last plot, though I don't know that it is necessary
    """

    def __init__(self):
        self.bridge_name = None
        self.measurement_type = None

    def check_last(self, bridge, measurements):
        new = [False, False]
        if self.bridge_name != bridge:
            new[0] = True
            self.bridge_name = bridge
        if self.measurement_type != measurements:
            new[1] = True
            self.measurement_type = measurements
        return new


historical_monitor = HistoricalMonitor()


def individual_trace(session, bridge_name, measurement):
    bridge = get_matching_bridge(session, bridge_name)
    locations = bridge.hydro_locations
    plot_data = []
    site_codes = [location.code for location in locations]
    data = get_data(sites=site_codes, parameters=measurement, delta_days=5)

    fig = go.Figure()

    for i, site in enumerate(site_codes):
        for param in measurement:
            fig.add_trace(go.Scatter(
                x=data[i][param]['time'],
                y=data[i][param]['measurement'],
                name=data[i][param]['name'],
                line=dict(shape="spline", smoothing=1, width=3, color=config.PLOT_COLORS[i]),
                marker=dict(symbol="diamond-open"),
            ))

    if len(measurement) <= 1:
        fig.update_layout(yaxis=dict(title=measurement[0]),
                          title=dict(text=bridge_name + " USGS Data",
                                     x=0.5), )

    fig.update_layout(config.PLOT_LAYOUT)

    return fig


def individual_weather(session, bridge_name):
    bridge = get_matching_bridge(session, bridge_name)
    hour_time, day_time, hour_rain, day_rain = get_future_precipitation(latitude=bridge.latitude, longitude=bridge.longitude)

    summed_data = [0]
    for i, rain in enumerate(day_rain):
        if i > 0:
            summed_data.append(summed_data[i - 1] + rain)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=hour_time + day_time,
                         y=hour_rain + day_rain,
                         #marker=dict(line=dict(width=20)),
                         name="Daily Precipitation"
                         ))

    fig.add_trace(go.Scatter(x=day_time,
                             y=summed_data,
                             line=dict(width=3),
                             name="Cumulative Precipitation"))

    fig.update_layout(yaxis=dict(title="Precipitation [mm]"),
                      title=dict(text="Precipitation Forecast for " + bridge_name,
                                 x=0.5), )

    fig.update_layout(config.PLOT_LAYOUT)
    return fig
