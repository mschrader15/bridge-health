import plotly.graph_objects as go
from index import config
from db.model import get_bridges_to_plot, get_matching_bridge
from functions.waterservices_api import get_data


def get_bridges_status_plot(session):
    statuses = ['Ok', 'Monitor', 'Alert']
    fig = go.Figure()

    bridges = get_bridges_to_plot(session)

    ok = 0
    monitor = 0
    alert = 0
    for status in bridges[-1]:
        if status == statuses[0]:
            ok += 1
        elif status == statuses[1]:
            monitor += 1
        elif status == statuses[2]:
            alert += 1


    fig.add_trace(go.Pie(labels=statuses, values=[ok, monitor, alert], hole=.5))
    fig.update_traces(marker=dict(colors=[config.STATUS_COLOR_DICT[status] for status in statuses],),
                      textinfo='value')

    # fig.add_trace(go.Bar(x=statuses,
    #                      y=[ok, monitor, alert],
    #                      marker_color=[config.STATUS_COLOR_DICT[status] for status in statuses]))
    #
    # fig.update_layout(yaxis=dict(dtick=1))

    fig.update_layout(
                      title=dict(text="Bridge Statuses",
                                 x=0.5)
                      )

    return fig


def get_bridges_status_plot_excel(session):
    statuses = ['Ok', 'Monitor', 'Alert']
    fig = go.Figure()
    bridges = session.get_bridges_to_plot()
    ok = 0
    monitor = 0
    alert = 0
    for status in bridges[-1]:
        if status == statuses[0]:
            ok += 1
        elif status == statuses[1]:
            monitor += 1
        elif status == statuses[2]:
            alert += 1

    fig.add_trace(go.Pie(labels=statuses, values=[ok, monitor, alert], hole=.5))
    fig.update_traces(marker=dict(colors=[config.STATUS_COLOR_DICT[status] for status in statuses],),
                      textinfo='value')

    # fig.add_trace(go.Bar(x=statuses,
    #                      y=[ok, monitor, alert],
    #                      marker_color=[config.STATUS_COLOR_DICT[status] for status in statuses]))
    #
    # fig.update_layout(yaxis=dict(dtick=1))

    fig.update_layout(
                      title=dict(text="Bridge Statuses",
                                 x=0.5)
                      )

    return fig