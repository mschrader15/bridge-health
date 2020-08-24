from index import config, app
from db.model import get_session
from dashboard.layout import LAYOUT
from dashboard.apply_callbacks import apply_callback

SESSION = None
#
# if
if not SESSION:
    SESSION = get_session(config, update_structure=False)
apply_callback(SESSION)
app.layout = LAYOUT
server = app.server

if __name__ == "__main__":

    # if not SESSION:
    #     SESSION = get_session(config, update_structure=False)
    # apply_callback(SESSION)
    # app.layout = LAYOUT
    app.run_server(debug=True)

