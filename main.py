from index import config, app, Paths
from db.model import session_scope, BridgeOverride
from dashboard.layout import LAYOUT
from dashboard.apply_callbacks import apply_callback

# if
# if not SESSION:
#     SESSION = get_session(config, update_structure=False)

# with session_scope(config=config, update_structure=False) as SESSION:
SESSION = BridgeOverride(Paths.BRIDGE_EXCEL)
apply_callback(SESSION)
app.layout = LAYOUT
server = app.server


if __name__ == "__main__":

    # if not SESSION:
    #     SESSION = get_session(config, update_structure=False)
    # apply_callback(SESSION)
    # app.layout = LAYOUT
    app.run_server(debug=True)

