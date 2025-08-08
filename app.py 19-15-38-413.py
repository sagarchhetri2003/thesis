
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import pickle

# Load pre-saved plot
shot_map_fig = pickle.load(open("shot_map_fig.pkl", "rb"))

# Placeholder figures (replace with your actual Plotly figures from notebook)
# You must assign your other generated figures like `xg_fig`, `heatmap_fig`, etc.

# Init app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Liverpool Match Dashboard"

app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col(html.H2("⚽ Liverpool Match Dashboard", className="text-center text-primary my-4"), width=12)
    ]),
    dbc.Tabs([
        dbc.Tab(label="Shot Map", tab_id="shot-map"),
        dbc.Tab(label="Expected Goals (xG)", tab_id="expected-goals"),
        dbc.Tab(label="Other", tab_id="other")
    ], id="tabs", active_tab="shot-map", className="mb-3"),
    dbc.Row([dbc.Col(html.Div(id="tab-content"))])
])

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_content(tab):
    if tab == "shot-map":
        return html.Div([
            dcc.Graph(figure=shot_map_fig)
        ])

    elif tab == "expected-goals":
        df = pd.read_csv("EPL_result.csv")
        home_stats = df.groupby('Home').agg(
            Avg_xG_Home=('xG_Home', 'mean'),
            Avg_G_Home=('G_Home', 'mean')
        ).reset_index()
        home_stats_melted = home_stats.melt(
            id_vars='Home',
            value_vars=['Avg_xG_Home', 'Avg_G_Home'],
            var_name='Metric',
            value_name='Goals'
        )
        fig = px.bar(
            home_stats_melted,
            x='Home',
            y='Goals',
            color='Metric',
            barmode='group',
            text='Goals',
            title='⚽ Average Home xG vs Actual Goals per Team (Highlight: Liverpool)',
            template='plotly_white'
        )
        return html.Div([
            dcc.Graph(figure=fig)
        ])

    elif tab == "other":
        df = pd.read_csv('Liverpool_2015_2023_Matches.csv')
        df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)

        def get_result(row):
            if row['Venue'] == 'Home':
                return 'Win' if row['HomeGoals'] > row['AwayGoals'] else 'Draw' if row['HomeGoals'] == row['AwayGoals'] else 'Loss'
            else:
                return 'Win' if row['AwayGoals'] > row['HomeGoals'] else 'Draw' if row['AwayGoals'] == row['HomeGoals'] else 'Loss'
        df['Result'] = df.apply(get_result, axis=1)
        summary = df.groupby('Venue').agg(
            Total_Matches=('Result', 'count'),
            Wins=('Result', lambda x: (x == 'Win').sum())
        ).reset_index()
        summary['Win_Percentage'] = (summary['Wins'] / summary['Total_Matches'] * 100).round(1)
        fig = px.bar(
            summary,
            x='Venue',
            y='Wins',
            text='Wins',
            color='Venue',
            color_discrete_map={'Home': 'red', 'Away': 'green'},
            labels={'Wins': 'Number of Wins', 'Venue': 'Venue'},
            template='plotly_white',
            title="⚽ Liverpool Wins (2015–2023) — Home vs Away"
        )
        return html.Div([
            dcc.Graph(figure=fig)
        ])

    return html.P("No content available.")

if __name__ == "__main__":
    app.run_server(debug=True)
