
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pickle

# Load pre-processed visualizations or datasets
# Replace these with real processing or visualization logic from the notebook
# For example, load your dataframes like: df = pd.read_csv("your_dataset.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Liverpool Interactive Dashboard"

app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col(html.H2("⚽ Liverpool Interactive Dashboard", className="text-center text-primary my-4"), width=12)
    ]),
    dbc.Tabs([
        dbc.Tab(label="📍 Shot Map", tab_id="shot-map"),
        dbc.Tab(label="🎯 Expected Goals (xG)", tab_id="xg"),
        dbc.Tab(label="👥 Player Comparison", tab_id="player-comparison"),
        dbc.Tab(label="📈 Match Timeline", tab_id="timeline"),
        dbc.Tab(label="🏠 Home vs Away Stats", tab_id="home-away"),
    ], id="tabs", active_tab="shot-map", className="mb-3"),
    dbc.Row([dbc.Col(html.Div(id="tab-content"))])
])

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "shot-map":
        return html.Div([
            html.H4("Shot Map"),
            dcc.Graph(figure=px.scatter(x=[1, 2, 3], y=[4, 5, 6], title="Dummy Shot Map"))
        ])
    elif active_tab == "xg":
        return html.Div([
            html.H4("Expected Goals (xG)"),
            dcc.Graph(figure=px.line(x=[1, 2, 3], y=[0.2, 1.5, 1.7], title="xG Progression"))
        ])
    elif active_tab == "player-comparison":
        return html.Div([
            html.H4("Player Comparison"),
            dcc.Graph(figure=px.bar(x=["Salah", "Firmino"], y=[20, 13], title="Goals Scored"))
        ])
    elif active_tab == "timeline":
        return html.Div([
            html.H4("Match Timeline"),
            dcc.Graph(figure=px.line(x=[2019, 2020, 2021, 2022], y=[80, 85, 90, 95], title="Points Over Seasons"))
        ])
    elif active_tab == "home-away":
        return html.Div([
            html.H4("Home vs Away Stats"),
            dcc.Graph(figure=px.pie(names=["Home Wins", "Away Wins"], values=[25, 15], title="Win Distribution"))
        ])
    return html.Div("No content available.")

if __name__ == "__main__":
    app.run_server(debug=True)
