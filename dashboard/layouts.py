from dash import dcc, html

def create_layout():
    return html.Div([

        # ── Header ────────────────────────────────────
        html.Div([
            html.H1("Network Packet Analyzer",
                    style={"color": "#00FF41", "fontFamily": "monospace"}),
            html.P("Live traffic monitor & threat detection",
                   style={"color": "#888", "fontFamily": "monospace"}),
        ], style={"background": "#0d0d0d", "padding": "20px 30px",
                  "borderBottom": "1px solid #00FF41"}),

        # ── Auto refresh every 2 seconds ──────────────
        dcc.Interval(id="tick", interval=2000, n_intervals=0),

        # ── Stats row ─────────────────────────────────
        html.Div([
            stat_card("total-packets",  "Total Packets"),
            stat_card("total-alerts",   "Total Alerts"),
            stat_card("top-talker",     "Top Talker"),
            stat_card("active-proto",   "Top Protocol"),
        ], style={"display": "grid",
                  "gridTemplateColumns": "repeat(4, 1fr)",
                  "gap": "16px", "padding": "20px 30px",
                  "background": "#111"}),

        # ── Charts row ────────────────────────────────
        html.Div([
            html.Div([
                html.H3("Live Traffic",
                        style={"color":"#00FF41","fontFamily":"monospace",
                               "marginBottom":"10px"}),
                dcc.Graph(id="traffic-graph",
                          style={"height":"280px"},
                          config={"displayModeBar": False}),
            ], style=card_style()),

            html.Div([
                html.H3("Protocol Breakdown",
                        style={"color":"#00FF41","fontFamily":"monospace",
                               "marginBottom":"10px"}),
                dcc.Graph(id="proto-pie",
                          style={"height":"280px"},
                          config={"displayModeBar": False}),
            ], style=card_style()),

        ], style={"display": "grid",
                  "gridTemplateColumns": "2fr 1fr",
                  "gap": "16px", "padding": "0 30px 20px"}),

        # ── Top talkers + Alert feed ──────────────────
        html.Div([
            html.Div([
                html.H3("Top Talkers",
                        style={"color":"#00FF41","fontFamily":"monospace",
                               "marginBottom":"10px"}),
                dcc.Graph(id="top-talkers",
                          style={"height":"250px"},
                          config={"displayModeBar": False}),
            ], style=card_style()),

            html.Div([
                html.H3("Alert Feed",
                        style={"color":"#FF4444","fontFamily":"monospace",
                               "marginBottom":"10px"}),
                html.Div(id="alert-feed",
                         style={"height":"250px","overflowY":"auto"}),
            ], style=card_style()),

        ], style={"display": "grid",
                  "gridTemplateColumns": "1fr 1fr",
                  "gap": "16px", "padding": "0 30px 30px"}),

    ], style={"background": "#111", "minHeight": "100vh"})


def stat_card(elem_id, label):
    return html.Div([
        html.P(label, style={"color":"#888","fontFamily":"monospace",
                             "fontSize":"12px","margin":"0"}),
        html.H2(id=elem_id, children="0",
                style={"color":"#00FF41","fontFamily":"monospace","margin":"4px 0 0"}),
    ], style={"background":"#1a1a1a","border":"1px solid #333",
              "borderRadius":"8px","padding":"16px"})


def card_style():
    return {"background":"#1a1a1a","border":"1px solid #333",
            "borderRadius":"8px","padding":"16px"}