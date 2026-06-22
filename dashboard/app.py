import dash
from dashboard.layouts import create_layout
from dashboard.callbacks import register_callbacks

def create_app(logger):
    app = dash.Dash(
        __name__,
        title="Network Packet Analyzer",
        update_title=None,
    )
    app.layout = create_layout()
    register_callbacks(app, logger)
    return app