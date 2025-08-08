import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# 🚨 Import or load your pre-created Plotly figures here
# Example: from your_notebook_figures import all_figures
# all_figures = {
#     'vs Arsenal': {
#         'shot_map': ...,
#         'xg': ...,
#         'heatmap': ...,
#         'player_stats': ...,
#         'tactical': ...
#     }, ...
# }

# Dummy placeholder for structure
all_figures = {}  # <-- REPLACE THIS with your actual dictionary of Plotly figure objects

# Match options from the keys of your dictionary
match_options = [{'label': match, 'value': match} for match in all_figures.keys()]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Liverpool Match Dashboard"

# ------------- Layout ------------- #
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col(html.H2("⚽ Liverpool Match Dashboard", className="text-center text-primary my-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Select Match:", className="fw-bold"),
            dcc.Dropdown(
                id="match-dropdown",
                options=match_options,
                value=match_options[0]['value'] if match_options else None,
                clearable=False
            ),
        ], md=3)
    ]),

    dbc.Tabs([
        dbc.Tab(label="Shot Map", tab_id="tab-shot"),
        dbc.Tab(label="Expected Goals (xG)", tab_id="tab-xg"),
        dbc.Tab(label="Heatmap", tab_id="tab-heatmap"),
        dbc.Tab(label="Player Statistics", tab_id="tab-player"),
        dbc.Tab(label="Tactical Insights", tab_id="tab-tactical")
    ], id="tabs", active_tab="tab-shot", className="my-3"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="main-figure"), width=12)
    ]),

    html.Div(id="store-wrapper", style={"display": "none"}, children=[
        dcc.Store(id="selected-player"),
        dcc.Store(id="hovered-region")
    ])
])

# ------------- Callbacks ------------- #

# Main view update based on tab + match + selected player
@app.callback(
    Output("main-figure", "figure"),
    Input("tabs", "active_tab"),
    Input("match-dropdown", "value"),
    Input("selected-player", "data"),
    Input("hovered-region", "data")
)
def update_view(tab, match, selected_player, hovered_region):
    if match not in all_figures:
        return go.Figure()

    figs = all_figures[match]

    if tab == "tab-shot":
        fig = figs["shot_map"]
        if selected_player:
            # Optionally highlight selected player's shots
            fig.update_traces(
                selector=dict(name=selected_player),
                marker=dict(size=12, color="gold", symbol="star")
            )
        return fig

    elif tab == "tab-xg":
        fig = figs["xg"]
        if selected_player:
            fig.update_layout(title=f"xG Contribution: {selected_player}")
        if hovered_region:
            # Optional: Filter xG by region (not implemented here)
            pass
        return fig

    elif tab == "tab-heatmap":
        return figs["heatmap"]

    elif tab == "tab-player":
        return figs["player_stats"]

    elif tab == "tab-tactical":
        return figs["tactical"]

    return go.Figure()

# Capture selected player from Player Stats figure
@app.callback(
    Output("selected-player", "data"),
    Input("main-figure", "clickData"),
    State("tabs", "active_tab")
)
def capture_player_selection(clickData, tab):
    if tab == "tab-player" and clickData:
        try:
            return clickData["points"][0]["customdata"][0]
        except (KeyError, IndexError):
            pass
    return None

# Capture hover region on Heatmap (optional)
@app.callback(
    Output("hovered-region", "data"),
    Input("main-figure", "hoverData"),
    State("tabs", "active_tab")
)
def capture_hover_region(hoverData, tab):
    if tab == "tab-heatmap" and hoverData:
        return hoverData["points"][0]
    return None

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
