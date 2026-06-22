from dash import Input, Output
import plotly.graph_objs as go

DARK = "#111111"
GREEN = "#00FF41"
RED = "#FF4444"

def register_callbacks(app, logger):

    @app.callback(
        Output("traffic-graph", "figure"),
        Input("tick", "n_intervals")
    )
    def update_traffic(_):
        rows = logger.get_traffic_timeseries(seconds=60)
        if not rows:
            return empty_fig("No traffic yet")
        times  = [r[0] for r in rows]
        counts = [r[1] for r in rows]
        fig = go.Figure(go.Scatter(
            x=times, y=counts, mode="lines",
            line=dict(color=GREEN, width=2),
            fill="tozeroy",
            fillcolor="rgba(0,255,65,0.1)"
        ))
        fig.update_layout(**dark_layout())
        return fig

    @app.callback(
        Output("proto-pie", "figure"),
        Input("tick", "n_intervals")
    )
    def update_proto(_):
        rows = logger.get_protocol_counts()
        if not rows:
            return empty_fig("No data yet")
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
        fig = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.4,
            marker=dict(colors=["#00FF41","#00BFFF",
                                 "#FF4444","#FFD700","#888"])
        ))
        fig.update_layout(**dark_layout())
        return fig

    @app.callback(
        Output("top-talkers", "figure"),
        Input("tick", "n_intervals")
    )
    def update_talkers(_):
        rows = logger.get_top_talkers(limit=8)
        if not rows:
            return empty_fig("No data yet")
        ips    = [r[0] for r in rows]
        counts = [r[1] for r in rows]
        fig = go.Figure(go.Bar(
            x=counts, y=ips,
            orientation="h",
            marker=dict(color=GREEN)
        ))
        fig.update_layout(**dark_layout())
        return fig

    @app.callback(
        Output("alert-feed", "children"),
        Input("tick", "n_intervals")
    )
    def update_alerts(_):
        from dash import html
        rows = logger.get_recent_alerts(limit=20)
        if not rows:
            return [html.P("No alerts yet",
                           style={"color":"#555","fontFamily":"monospace",
                                  "fontSize":"13px"})]
        items = []
        for row in rows:
            _, ts, src, atype, sev, detail = row
            color = RED if sev == "HIGH" else "#FFD700"
            items.append(html.Div([
                html.Span(f"[{sev}] ",
                          style={"color":color,"fontWeight":"bold"}),
                html.Span(f"{atype} — {src}",
                          style={"color":"#fff"}),
                html.P(detail,
                       style={"color":"#888","fontSize":"11px","margin":"2px 0 8px"}),
            ], style={"fontFamily":"monospace","fontSize":"12px",
                      "borderBottom":"1px solid #222","paddingBottom":"6px"}))
        return items

    @app.callback(
        [Output("total-packets", "children"),
         Output("total-alerts",  "children"),
         Output("top-talker",    "children"),
         Output("active-proto",  "children")],
        Input("tick", "n_intervals")
    )
    def update_stats(_):
        pkts    = logger.get_recent_packets(limit=999999)
        alerts  = logger.get_recent_alerts(limit=999999)
        talkers = logger.get_top_talkers(limit=1)
        protos  = logger.get_protocol_counts()

        total_p = len(pkts)
        total_a = len(alerts)
        top_ip  = talkers[0][0] if talkers else "—"
        top_pr  = max(protos, key=lambda x: x[1])[0] if protos else "—"

        return str(total_p), str(total_a), top_ip, top_pr


def dark_layout():
    return dict(
        paper_bgcolor=DARK,
        plot_bgcolor=DARK,
        font=dict(color="#888", family="monospace"),
        margin=dict(l=10, r=10, t=10, b=10),
    )

def empty_fig(msg):
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False,
                       font=dict(color="#555", size=14))
    fig.update_layout(**dark_layout())
    return fig