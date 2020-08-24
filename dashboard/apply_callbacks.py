import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from index import app
from dashboard.plots import geo_located_bridges, individual_trace, get_bridges_status_plot, geo_located_bridge_sensor,\
    individual_weather
import time


class ClickMonitor():
    def __init__(self):
        self.reset_clicks = 0


click_monitor = ClickMonitor()
click_monitor_2 = ClickMonitor()
click_monitor_3 = ClickMonitor()


EMPTY_PLOT = {
                "layout": {
                    "xaxis": {
                        "visible": False
                    },
                    "yaxis": {
                        "visible": False
                    },
                    "annotations": [
                        {
                            "text": "Select a bridge on the bridge overview plot",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {
                                "size": 20
                            }
                        }
                    ]
                }
            }

LOADING_PLOT = {
                "layout": {
                    "xaxis": {
                        "visible": False
                    },
                    "yaxis": {
                        "visible": False
                    },
                    "annotations": [
                        {
                            "text": "Plot is loading ...",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {
                                "size": 20
                            }
                        }
                    ]
                }
            }



def apply_callback(session):
    # Create callbacks
    app.clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="resize"),
        Output("output-clientside", "children"),
        [Input("main_graph", "figure")],
    )

    @app.callback(
        Output("main_graph", "figure"),
        [Input("url", "pathname"),
         Input("main_graph", "clickData"),
         Input('reset_button', 'n_clicks')],
        #[State("lock_selector", "value"), State("main_graph", "relayoutData")],
    )
    def display_main(url, click_data, reset_button):
        reset_pressed = False
        if reset_button:
            if reset_button > click_monitor.reset_clicks:
                reset_pressed = True
                click_monitor.reset_clicks = reset_button
                return geo_located_bridges(session)
        if click_data:
            bridge_name = click_data['points'][0]['text']
            return geo_located_bridge_sensor(session, bridge_name=bridge_name)
        else:
            return geo_located_bridges(session)

    @app.callback(
        Output("water_services", "figure"),
        [Input("main_graph", "clickData"),
         Input('reset_button', 'n_clicks')
         ],
    )
    def get_individual_figure(click_data, reset_button):
        #ctx = dash.callback_context
        if reset_button:
            if reset_button > click_monitor_2.reset_clicks:
                click_monitor_2.reset_clicks = reset_button
                return EMPTY_PLOT
        if click_data:
            bridge_name = click_data['points'][0]['text']
            #time.sleep(2)
            fig = individual_trace(session, bridge_name=bridge_name, measurement=['Gage height, ft'])
            output_dict = fig.to_dict()
            return dict(data=output_dict['data'], layout=output_dict['layout'])
        else:
            return EMPTY_PLOT

    @app.callback(
        Output("precipitation_forecast", "figure"),
        [Input("main_graph", "clickData"),
         Input('reset_button', 'n_clicks')
         ],
    )
    def update_weather(click_data, reset_button):
        #ctx = dash.callback_context
        if reset_button:
            if reset_button > click_monitor_3.reset_clicks:
                click_monitor_3.reset_clicks = reset_button
                return EMPTY_PLOT
        if click_data:
            bridge_name = click_data['points'][0]['text']
            #time.sleep(2)
            return individual_weather(session, bridge_name=bridge_name)

        else:
            return EMPTY_PLOT

    @app.callback(
        Output("bridge-status", "figure"),
        [Input("url", "pathname"),]
    )
    def update_status(url):
        if url:
            return get_bridges_status_plot(session)
