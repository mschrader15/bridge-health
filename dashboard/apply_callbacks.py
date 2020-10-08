from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_html_components as html
from index import app
from dashboard.plots import geo_located_bridges, individual_trace, get_bridges_status_plot, geo_located_bridge_sensor, \
    individual_weather, geo_located_bridges_excel, geo_located_bridge_sensor_excel, individual_trace_excel, \
    individual_weather_excel, get_bridges_status_plot_excel


class ClickMonitor():
    def __init__(self):
        self.reset_clicks = 0
        self.click_data = ''


click_monitor = ClickMonitor()
click_monitor_2 = ClickMonitor()
# click_monitor_3 = ClickMonitor()


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


def interpret_user_inputs(click_data, reset_button):
    bridge_name = ''
    n_clicks = 0
    if click_data:
        try:
            bridge_name = click_data['points'][0]['text']
        except KeyError:
            bridge_name = ''
    if reset_button:
        n_clicks = reset_button
    return bridge_name, n_clicks


def apply_callback(session):
    # Create callbacks
    app.clientside_callback(
        ClientsideFunction(namespace="clientside", function_name="resize"),
        Output("output-clientside", "children"),
        [Input("main_graph", "figure")],
    )

    @app.callback(
        [Output("main_graph", "figure"),
         Output('call-back-1-store', 'children')],
        [Input("url", "pathname"),
         Input("main_graph", "clickData"),
         Input('reset_button', 'n_clicks')],
        [State('call-back-1-store', 'children')]
    )
    def display_main(url, click_data, reset_button, stored_states):
        bridge_name, n_clicks = interpret_user_inputs(click_data=click_data, reset_button=reset_button)
        try:
            data = stored_states['props']['children'].split('-')
        except (AttributeError, TypeError):
            data = ["", 0]
        last_bridge_name = data[0]
        last_n_clicks = int(data[1])
        if click_data:
            if bridge_name != last_bridge_name:
                return geo_located_bridge_sensor_excel(session, bridge_name=bridge_name), html.P("-".join([bridge_name, str(n_clicks)]))
        if reset_button:
            if reset_button > click_monitor.reset_clicks:
                click_monitor.reset_clicks = reset_button
                return geo_located_bridges_excel(session), html.P("-".join([last_bridge_name, str(n_clicks)]))
        return geo_located_bridges_excel(session), html.P("-".join([last_bridge_name, str(last_n_clicks)]))

    @app.callback(
        [Output("water_services", "figure"),
         Output('call-back-2-store', 'children')],
        [Input("main_graph", "clickData"),
         Input('reset_button', 'n_clicks')],
        [State('call-back-2-store', 'children')]
    )
    def get_individual_figure(click_data, reset_button, stored_states):
        bridge_name, n_clicks = interpret_user_inputs(click_data=click_data, reset_button=reset_button)
        try:
            data = stored_states['props']['children'].split('-')
        except (AttributeError, TypeError):
            data = ["", 0]
        last_bridge_name = data[0]
        last_n_clicks = int(data[1])
        if click_data:
            try:
                bridge_name = click_data['points'][0]['text']
            except KeyError:
                return EMPTY_PLOT, html.P("-".join([last_bridge_name, str(last_n_clicks)]))
            if bridge_name != last_bridge_name:
                fig = individual_trace_excel(session, bridge_name=bridge_name, measurement=['Gage height, ft'])
                output_dict = fig.to_dict()
                return dict(data=output_dict['data'], layout=output_dict['layout']), html.P(
                    "-".join([bridge_name, str(n_clicks)]))
        if reset_button:
            if n_clicks > last_n_clicks:
                return EMPTY_PLOT, html.P("-".join([last_bridge_name, str(reset_button)]))
        else:
            return EMPTY_PLOT, html.P("-".join([last_bridge_name, str(last_n_clicks)]))

    @app.callback([Output("precipitation_forecast", "figure"),
                   Output('call-back-3-store', 'children')],
                  [Input("main_graph", "clickData"),
                   Input('reset_button', 'n_clicks'), ],
                  [State('call-back-3-store', 'children')]
                  )
    def update_weather(click_data, reset_button, stored_states):
        bridge_name, n_clicks = interpret_user_inputs(click_data=click_data, reset_button=reset_button)
        try:
            data = stored_states['props']['children'].split('-')
        except (AttributeError, TypeError):
            data = ["", 0]
        last_bridge_name = data[0]
        last_n_clicks = int(data[1])
        if click_data:
            try:
                bridge_name = click_data['points'][0]['text']
            except KeyError:
                return EMPTY_PLOT, html.P("-".join([last_bridge_name, str(last_n_clicks)]))
            if bridge_name != last_bridge_name:
                return individual_weather_excel(session, bridge_name=bridge_name), html.P(
                    "-".join([bridge_name, str(n_clicks)]))
        if reset_button:
            if n_clicks > last_n_clicks:
                return EMPTY_PLOT, html.P("-".join([last_bridge_name, str(reset_button)]))
        else:
            return EMPTY_PLOT, html.P("-".join([last_bridge_name, str(last_n_clicks)]))

    @app.callback(
        Output("bridge-status", "figure"),
        [Input("url", "pathname"), ]
    )
    def update_status(url):
        if url:
            return get_bridges_status_plot_excel(session)
