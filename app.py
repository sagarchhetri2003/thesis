
# import dash
# from dash import html, dcc
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import plotly.graph_objs as go
# import pickle
# shot_map_fig = pickle.load(open("shot_map_fig.pkl", "rb"))


# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.title = "Liverpool Match Dashboard"

# app.layout = dbc.Container(fluid=True, children=[
#     dbc.Row([
#         dbc.Col(html.H2("⚽ Liverpool Match Dashboard", className="text-center text-primary my-4"), width=12)
#     ]),
#     dbc.Tabs([
#         dbc.Tab(label="Shot Map", tab_id="shot-map"),
#         dbc.Tab(label="Expected Goals (xG)", tab_id="expected-goals-(xg)"),
#         dbc.Tab(label="Other", tab_id="other"),
#     ], id="tabs", active_tab="shot-map", className="mb-3"),
#     dbc.Row([dbc.Col(html.Div(id="tab-content"))])
# ])

# from dash.dependencies import Input, Output

# @app.callback(
#     Output("tab-content", "children"),
#     Input("tabs", "active_tab")
# )
# def render_content(tab):

#     if tab == "shot-map":
#         # Plots for Shot Map
#         pass

# import plotly.express as px


# stats_df = pd.read_csv("stats.csv")

# # Filter only Liverpool data
# liverpool_stats = stats_df[stats_df['team'] == 'Liverpool']

# # Select relevant columns
# liverpool_stats = liverpool_stats[['season', 'total_scoring_att', 'ontarget_scoring_att', 'goals', 'wins']]

# # Melt for plotting
# liverpool_melted = liverpool_stats.melt(id_vars='season', var_name='Metric', value_name='Value')

# # Create interactive line chart
# fig = px.line(
#     liverpool_melted,
#     x='season',
#     y='Value',
#     color='Metric',
#     markers=True,
#     title='Liverpool Performance by Season: Shots, Shots on Target, Goals, Wins',
#     labels={'Value': 'Count', 'season': 'Season'},
#     template='plotly_white'
# )

# # 🔧 Fix layout margins
# fig.update_layout(
#     title_font=dict(size=22),
#     legend_title_text='Metric',
#     margin=dict(l=60, r=60, t=80, b=60)  # Prevent cropping
# )

# # 📏 Save with larger dimensions
# fig.write_image("Liverpool Performance by Season.png", width=1000, height=600)

# # Show the chart
# fig.show()




# import pandas as pd
# import plotly.express as px

# # Load your data
# df = pd.read_csv("epl_final.csv")

# # Filter only Liverpool matches
# liverpool_df = df[(df['HomeTeam'] == 'Liverpool') | (df['AwayTeam'] == 'Liverpool')].copy()

# # Determine venue from Liverpool's perspective
# liverpool_df['Venue'] = liverpool_df['HomeTeam'].apply(lambda x: 'Home' if x == 'Liverpool' else 'Away')

# # Parse match dates and assign COVID periods
# liverpool_df['MatchDate'] = pd.to_datetime(liverpool_df['MatchDate'])

# def covid_period(date):
#     if date < pd.to_datetime('2020-03-01'):
#         return 'Pre-COVID'
#     elif date <= pd.to_datetime('2021-07-01'):
#         return 'During-COVID'
#     else:
#         return 'Post-COVID'

# liverpool_df['CovidPeriod'] = liverpool_df['MatchDate'].apply(covid_period)

# # Add match stats from Liverpool's perspective
# liverpool_df['Goals'] = liverpool_df.apply(
#     lambda row: row['FullTimeHomeGoals'] if row['Venue'] == 'Home' else row['FullTimeAwayGoals'], axis=1)

# liverpool_df['GoalsConceded'] = liverpool_df.apply(
#     lambda row: row['FullTimeAwayGoals'] if row['Venue'] == 'Home' else row['FullTimeHomeGoals'], axis=1)

# liverpool_df['Shots'] = liverpool_df.apply(
#     lambda row: row['HomeShots'] if row['Venue'] == 'Home' else row['AwayShots'], axis=1)

# liverpool_df['ShotsOnTarget'] = liverpool_df.apply(
#     lambda row: row['HomeShotsOnTarget'] if row['Venue'] == 'Home' else row['AwayShotsOnTarget'], axis=1)

# liverpool_df['Win'] = liverpool_df.apply(
#     lambda row: 1 if row['Goals'] > row['GoalsConceded'] else 0, axis=1)

# # Group and summarize
# summary = liverpool_df.groupby(['CovidPeriod', 'Venue']).agg({
#     'Goals': 'mean',
#     'GoalsConceded': 'mean',
#     'Shots': 'mean',
#     'ShotsOnTarget': 'mean',
#     'Win': 'mean'
# }).reset_index().rename(columns={'Win': 'WinRate'}).round(2)

# # Melt for visualization
# melted_summary = summary.melt(
#     id_vars=['CovidPeriod', 'Venue'],
#     value_vars=['Goals', 'GoalsConceded', 'Shots', 'ShotsOnTarget', 'WinRate'],
#     var_name='Metric',
#     value_name='Value'
# )

# # Plot
# fig = px.bar(
#     melted_summary,
#     x='CovidPeriod',
#     y='Value',
#     color='Venue',
#     barmode='group',
#     facet_col='Metric',
#     category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
#     title='📊 Liverpool Performance Breakdown by COVID Period and Venue',
#     labels={
#         'Value': 'Average per Match',
#         'CovidPeriod': 'Period',
#         'Venue': 'Venue'
#     },
#     template='plotly_white',
#     height=600
# )

# # Enhanced layout
# fig.update_layout(
#     title_font=dict(size=24),
#     font=dict(size=13),
#     legend_title_text='Venue',
#     legend=dict(orientation='h', y=1.15, x=0.3),
#     margin=dict(l=60, r=60, t=100, b=60)
# )

# # Improve annotation readability (clean up facet titles)
# fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("WinRate", "Win Rate")))

# # Save to file with clear resolution
# fig.write_image("Liverpool_COVID_Performance_FacetBar.png", width=1200, height=600)

# # Show plot
# fig.show()



# import plotly.express as px
# import plotly.graph_objects as go

# # ----- 1️⃣ Stacked Bar Chart: Goals & Win Rate Together -----
# bar_data = summary.melt(
#     id_vars=['CovidPeriod', 'Venue'],
#     value_vars=['Goals', 'WinRate'],
#     var_name='Metric',
#     value_name='Value'
# )

# fig1 = px.bar(
#     bar_data,
#     x='CovidPeriod',
#     y='Value',
#     color='Venue',
#     barmode='group',
#     facet_col='Metric',
#     category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
#     title='📊 Liverpool Goals & Win Rate by COVID Period and Venue',
#     labels={'Value': 'Metric Value', 'CovidPeriod': 'Period'},
#     template='plotly_white',
#     height=500
# )

# fig1.update_layout(
#     title_font=dict(size=22),
#     font=dict(size=12),
#     legend_title_text='Venue',
#     margin=dict(l=60, r=60, t=80, b=60)
# )
# fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("WinRate", "Win Rate")))
# fig1.write_image("Liverpool_Bar_Goals_WinRate.png", width=1100, height=500)
# fig1.show()

# # ----- 2️⃣ Line Chart: Win Rate Trend -----
# fig2 = px.line(
#     summary,
#     x='CovidPeriod',
#     y='WinRate',
#     color='Venue',
#     markers=True,
#     title='📈 Liverpool Win Rate Trend by Venue',
#     labels={'WinRate': 'Win Rate (%)', 'CovidPeriod': 'COVID Period'},
#     category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
#     template='plotly_white'
# )

# fig2.update_layout(
#     yaxis_tickformat='.0%',
#     title_font=dict(size=22),
#     font=dict(size=12),
#     legend_title_text='Venue',
#     margin=dict(l=60, r=60, t=80, b=60)
# )
# fig2.write_image("Liverpool_WinRate_Trend.png", width=800, height=500)
# fig2.show()

# # ----- 3️⃣ Radar Chart: Overall Avg Comparison (Home vs Away) -----
# avg_metrics = summary.groupby('Venue')[['Goals', 'GoalsConceded', 'Shots', 'ShotsOnTarget', 'WinRate']].mean().reset_index()

# fig3 = go.Figure()

# for _, row in avg_metrics.iterrows():
#     fig3.add_trace(go.Scatterpolar(
#         r=row[1:].values,
#         theta=avg_metrics.columns[1:],
#         fill='toself',
#         name=row['Venue'],
#         line=dict(width=2)
#     ))

# fig3.update_layout(
#     polar=dict(
#         radialaxis=dict(visible=True, range=[0, max(avg_metrics.iloc[:, 1:].max()) * 1.2])
#     ),
#     title='🛡️ Overall Performance Radar: Home vs Away',
#     template='plotly_white',
#     title_font=dict(size=22),
#     font=dict(size=12),
#     margin=dict(l=60, r=60, t=80, b=60)
# )
# fig3.write_image("Liverpool_Radar_Performance_Home_Away.png", width=700, height=600)
# fig3.show()

#     if tab == "shot-map":
#     def render_shot_map():
#         # Placeholder content for the function
#         return html.Div([
#             html.P("Shot map content goes here.")
#         ])
#         pass
#         # Placeholder content for the function
#         def render_other_tab():
#             return html.Div([
#             html.P("Shot map content goes here.")
#         ])
#         return html.Div([
#             dcc.Graph(figure=shot_map_fig)
#         ])

# if active_tab == "expected-goals-(xg)":
#     # Plots for Expected Goals (xG)

#     import pandas as pd
# import plotly.express as px
# import plotly.io as pio

# # Optional: Force plot display in Jupyter
# pio.renderers.default = 'notebook'  # or 'iframe', 'svg' if needed

# # 📂 Load dataset
# df = pd.read_csv('EPL_result.csv')

# # 🧮 Group by home team: average xG and actual goals
# home_stats = df.groupby('Home').agg(
#     Avg_xG_Home=('xG_Home', 'mean'),
#     Avg_G_Home=('G_Home', 'mean')
# ).reset_index()

# # 🔁 Melt for grouped bar
# home_stats_melted = home_stats.melt(
#     id_vars='Home',
#     value_vars=['Avg_xG_Home', 'Avg_G_Home'],
#     var_name='Metric',
#     value_name='Goals'
# )

# # 🟥 Add highlighting (Liverpool bold)
# home_stats_melted['Highlight'] = home_stats_melted['Home'].apply(lambda x: 'Liverpool' if x == 'Liverpool' else 'Other')

# # 🖼️ Plot with enhanced design
# fig = px.bar(
#     home_stats_melted,
#     x='Home',
#     y='Goals',
#     color='Metric',
#     barmode='group',
#     text='Goals',
#     title='⚽ Average Home xG vs Actual Goals per Team (Highlight: Liverpool)',
#     template='plotly_white',
#     color_discrete_map={
#         'Avg_xG_Home': '#1f77b4',  # royal blue
#         'Avg_G_Home': '#d62728'   # crimson red
#     }
# )

# # ✏️ Aesthetic improvements
# fig.update_traces(
#     texttemplate='%{text:.2f}',
#     textposition='outside',
#     marker_line_color='white',
#     marker_line_width=1.2
# )
# fig.update_layout(
#     xaxis_title='Club (Home Games)',
#     yaxis_title='Goals (Average)',
#     font=dict(size=14),
#     title_font=dict(size=22),
#     xaxis_tickangle=45,
#     bargap=0.25
# )

# # 🔍 Optional: Sort by Avg_G_Home if needed
# home_stats_melted.sort_values(by='Goals', ascending=False, inplace=True)

# # ✅ Show plot
# fig.show()

# # 💾 Save as PNG (requires kaleido)
# pio.write_image(fig, "home_xg_vs_goals_liverpool_highlight.png", width=1200, height=700)


# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.io as pio

# # Optional: set default renderer if needed
# pio.renderers.default = 'notebook'

# # Sort the teams
# df_temp = df_temp.sort_values(by='xGpm', ascending=False)

# # ===============================
# # 1️⃣ Horizontal Bar Chart (xG and xGA side-by-side)
# # ===============================
# fig1 = go.Figure()

# fig1.add_trace(go.Bar(
#     x=df_temp['xGpm'],
#     y=df_temp['Team'],
#     name='xG per Match',
#     orientation='h',
#     marker=dict(color='crimson'),
#     hovertemplate='Team: %{y}<br>xG: %{x}<extra></extra>'
# ))

# fig1.add_trace(go.Bar(
#     x=df_temp['xGApm'],
#     y=df_temp['Team'],
#     name='xGA per Match',
#     orientation='h',
#     marker=dict(color='dodgerblue'),
#     hovertemplate='Team: %{y}<br>xGA: %{x}<extra></extra>'
# ))

# fig1.update_layout(
#     title='⚽ EPL 2020/21: xG vs xGA per Match (Side-by-Side)',
#     barmode='group',
#     yaxis=dict(autorange="reversed"),
#     template='plotly_white',
#     height=700
# )

# fig1.write_image("plot_xg_vs_xga_horizontal.png", scale=3)
# fig1.show()

# # ===============================
# # 2️⃣ Grouped Vertical Bar Chart
# # ===============================
# df_grouped = df_temp[['Team', 'xGpm', 'xGApm']].melt(id_vars='Team', var_name='Metric', value_name='PerMatch')

# fig2 = px.bar(
#     df_grouped,
#     x='Team',
#     y='PerMatch',
#     color='Metric',
#     barmode='group',
#     title='⚽ EPL 2020/21: xG vs xGA per Match (Grouped)',
#     template='plotly_white',
#     color_discrete_map={'xGpm': 'crimson', 'xGApm': 'dodgerblue'},
#     labels={'PerMatch': 'Per Match Value'}
# )

# fig2.update_layout(
#     xaxis_tickangle=-45,
#     height=600
# )

# fig2.write_image("plot_xg_vs_xga_grouped.png", scale=3)
# fig2.show()

# # ===============================
# # 3️⃣ Dot Plot (Lollipop Style)
# # ===============================
# fig3 = go.Figure()

# for i, row in df_temp.iterrows():
#     fig3.add_trace(go.Scatter(
#         x=[row['xGApm'], row['xGpm']],
#         y=[row['Team'], row['Team']],
#         mode='lines',
#         line=dict(color='gray', width=2),
#         hoverinfo='skip',
#         showlegend=False
#     ))
#     fig3.add_trace(go.Scatter(
#         x=[row['xGApm']],
#         y=[row['Team']],
#         mode='markers',
#         marker=dict(color='dodgerblue', size=12),
#         name='xGA' if i == 0 else None,
#         hovertemplate='Team: %{y}<br>xGA: %{x}<extra></extra>'
#     ))
#     fig3.add_trace(go.Scatter(
#         x=[row['xGpm']],
#         y=[row['Team']],
#         mode='markers',
#         marker=dict(color='crimson', size=12),
#         name='xG' if i == 0 else None,
#         hovertemplate='Team: %{y}<br>xG: %{x}<extra></extra>'
#     ))

# fig3.update_layout(
#     title="⚽ EPL 2020/21: xG vs xGA per Match (Dot Plot)",
#     template="plotly_white",
#     xaxis_title="Per Match Value",
#     height=800
# )

# fig3.write_image("plot_xg_vs_xga_dotplot.png", scale=3)
# fig3.show()



# import plotly.express as px
# import plotly.io as pio

# # Sort by delta_xGpm for ranking
# df_sorted = df_temp.sort_values(by='delta_xGpm', ascending=False)

# # Create interactive horizontal bar chart
# fig = px.bar(
#     df_sorted,
#     x='delta_xGpm',
#     y='Team',
#     orientation='h',
#     text='delta_xGpm',
#     title='⚽ EPL 2020/21: Delta xG (Scored - Conceded)',
#     labels={'delta_xGpm': 'Delta xG per Match', 'Team': 'Team'},
#     template='plotly_white',
#     color='delta_xGpm',
#     color_continuous_scale='RdYlGn'
# )

# # Customize layout
# fig.update_traces(
#     texttemplate='%{x:.2f}',
#     textposition='outside'
# )
# fig.update_layout(
#     xaxis_title='ΔxG per Match',
#     yaxis=dict(autorange='reversed'),
#     title_font=dict(size=20),
#     coloraxis_showscale=False,
#     margin=dict(t=60, b=40)
# )

# # ✅ Show interactive chart
# fig.show()

# # ✅ Save as PNG (requires kaleido)
# fig.write_image("delta_xg_bar.png", scale=3)





# import plotly.graph_objects as go
# import plotly.io as pio

# # Sort by home xG for consistent ordering
# df_temp = df_temp.sort_values(by='xG_h', ascending=False)

# # ================================
# # 📊 Interactive Horizontal Bar Charts: xG Home vs Away
# # ================================
# fig = go.Figure()

# # xG Home
# fig.add_trace(go.Bar(
#     x=df_temp['xG_h'],
#     y=df_temp['Team'],
#     name='xG at Home',
#     orientation='h',
#     marker=dict(color='firebrick'),
#     hovertemplate='Team: %{y}<br>xG at Home: %{x}<extra></extra>'
# ))

# # xG Away
# fig.add_trace(go.Bar(
#     x=df_temp['xG_a'],
#     y=df_temp['Team'],
#     name='xG Away',
#     orientation='h',
#     marker=dict(color='darkblue'),
#     hovertemplate='Team: %{y}<br>xG Away: %{x}<extra></extra>'
# ))

# fig.update_layout(
#     title='⚽ EPL 2020/21: xG Scored per Match — Home vs Away',
#     barmode='group',
#     yaxis=dict(autorange="reversed"),
#     template='plotly_white',
#     xaxis_title='xG per Match',
#     height=700
# )

# # ✅ Show interactive chart
# fig.show()

# # ✅ Save as PNG (optional — requires kaleido)
# fig.write_image("xg_home_vs_away.png", scale=3)


# import plotly.express as px
# import plotly.io as pio

# # Sort for visual clarity
# df_sorted = df_temp.sort_values(by='delta_xG_ha', ascending=False)

# # Create interactive bar chart
# fig = px.bar(
#     df_sorted,
#     x='delta_xG_ha',
#     y='Team',
#     orientation='h',
#     title='⚽ EPL 2020/21: xG Difference (Home - Away)',
#     labels={'delta_xG_ha': 'ΔxG (Home - Away)', 'Team': 'Team'},
#     template='plotly_white',
#     text='delta_xG_ha',
#     color='delta_xG_ha',
#     color_continuous_scale='RdBu'
# )

# # Beautify the display
# fig.update_traces(
#     texttemplate='%{x:.2f}',
#     textposition='outside'
# )
# fig.update_layout(
#     xaxis_title='xG Difference (Home - Away)',
#     yaxis=dict(autorange='reversed'),
#     coloraxis_showscale=False,
#     title_font=dict(size=20),
#     margin=dict(t=60, b=40)
# )

# # Show plot
# fig.show()

# # Save to PNG
# fig.write_image("delta_xG_home_away_bar.png", scale=3)


# df['xG_diff'] = df['xG_Home'] - df['xG_Away']
# team_xg_diff = df.groupby('Home')['xG_diff'].mean().sort_values(ascending=False).reset_index()

# fig = px.bar(team_xg_diff, x='Home', y='xG_diff',
#              title='📊 Average xG Difference (Home Teams)',
#              template='plotly_white')
# fig.show()
#         def render_other_tab():
#             return html.Div([
#                 dcc.Graph(figure=fig)
#             ])
#         ])

#     if tab == "other":
#         # Plots for Other
# import pandas as pd
# import plotly.express as px
# import plotly.io as pio

# # 1️⃣ Load your CSV
# df = pd.read_csv('Liverpool_2015_2023_Matches.csv')

# # 2️⃣ Add Venue column
# df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)

# # 3️⃣ Add Result column
# def get_result(row):
#     if row['Venue'] == 'Home':
#         if row['HomeGoals'] > row['AwayGoals']:
#             return 'Win'
#         elif row['HomeGoals'] == row['AwayGoals']:
#             return 'Draw'
#         else:
#             return 'Loss'
#     else:
#         if row['AwayGoals'] > row['HomeGoals']:
#             return 'Win'
#         elif row['AwayGoals'] == row['HomeGoals']:
#             return 'Draw'
#         else:
#             return 'Loss'
# df['Result'] = df.apply(get_result, axis=1)

# # 4️⃣ Create Summary Table
# summary = df.groupby('Venue').agg(
#     Total_Matches=('Result', 'count'),
#     Wins=('Result', lambda x: (x == 'Win').sum())
# ).reset_index()

# summary['Win_Percentage'] = (summary['Wins'] / summary['Total_Matches'] * 100).round(1)

# # 5️⃣ SINGLE BAR CHART: Wins only
# fig1 = px.bar(
#     summary,
#     x='Venue',
#     y='Wins',
#     text='Wins',
#     color='Venue',
#     color_discrete_map={'Home': 'red', 'Away': 'green'},
#     labels={'Wins': 'Number of Wins', 'Venue': 'Venue'},
#     template='plotly_white',
#     title=f"⚽ Liverpool Wins (2015–2023) — Home vs Away<br>Total Games: {summary['Total_Matches'].sum()}"
# )

# fig1.update_traces(
#     textposition='outside',
#     customdata=summary[['Total_Matches', 'Win_Percentage']].values,
#     hovertemplate='<b>Venue:</b> %{x}<br>' +
#                   '<b>Wins:</b> %{y}<br>' +
#                   '<b>Total Games:</b> %{customdata[0]}<br>' +
#                   '<b>Win %:</b> %{customdata[1]}%'
# )
# fig1.update_layout(
#     title_font=dict(size=22),
#     xaxis_title='Venue',
#     yaxis_title='Number of Wins',
#     xaxis=dict(title_font=dict(size=18)),
#     yaxis=dict(title_font=dict(size=18)),
#     showlegend=False
# )
# fig1.show()

# # 6️⃣ GROUPED BAR CHART: Wins vs Total
# summary_melted = summary.melt(id_vars='Venue', value_vars=['Total_Matches', 'Wins'])

# fig2 = px.bar(
#     summary_melted,
#     x='Venue',
#     y='value',
#     color='variable',
#     barmode='group',
#     text='value',
#     title='⚽ Liverpool (2015–2023): Matches Played vs Wins (Home & Away)',
#     labels={'value': 'Number of Matches', 'Venue': 'Venue', 'variable': 'Metric'},
#     color_discrete_map={'Total_Matches': 'royalblue', 'Wins': 'crimson'},
#     template='plotly_white'
# )

# fig2.update_traces(textposition='outside')
# fig2.update_layout(
#     title_font=dict(size=22),
#     xaxis=dict(title_font=dict(size=18)),
#     yaxis=dict(title_font=dict(size=18)),
#     legend_title_text='Metric'
# )
# fig2.show()
# pio.write_image(fig1, "liverpool_wins_home_away.png", width=1000, height=600)
# pio.write_image(fig2, "liverpool_matches_vs_wins_grouped.png", width=1000, height=600)



# import pandas as pd
# import plotly.express as px
# import plotly.io as pio

# # 1️⃣ Load the CSV
# df = pd.read_csv("Liverpool_2015_2023_Matches.csv")

# # 2️⃣ Add Venue column
# df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)

# # 3️⃣ Add Result column
# def get_result(row):
#     if row['Venue'] == 'Home':
#         return 'Win' if row['HomeGoals'] > row['AwayGoals'] else 'Draw' if row['HomeGoals'] == row['AwayGoals'] else 'Loss'
#     else:
#         return 'Win' if row['AwayGoals'] > row['HomeGoals'] else 'Draw' if row['AwayGoals'] == row['HomeGoals'] else 'Loss'
# df['Result'] = df.apply(get_result, axis=1)

# # 4️⃣ Add CovidPeriod column
# df['Date'] = pd.to_datetime(df['Date'])
# def covid_period(date):
#     if date < pd.to_datetime('2020-03-01'):
#         return 'Pre-COVID'
#     elif date < pd.to_datetime('2021-07-01'):
#         return 'During COVID'
#     else:
#         return 'Post-COVID'
# df['CovidPeriod'] = df['Date'].apply(covid_period)

# # 5️⃣ Group and summarize data
# summary = df.groupby(['CovidPeriod', 'Venue', 'Result']).size().reset_index(name='Count')
# summary['Result_Grouped'] = summary['Result'].apply(lambda x: 'Wins' if x == 'Win' else 'Other')
# stacked = summary.groupby(['CovidPeriod', 'Venue', 'Result_Grouped'])['Count'].sum().reset_index()

# # 6️⃣ Modern stacked bar chart
# fig = px.bar(
#     stacked,
#     x='Venue',
#     y='Count',
#     color='Result_Grouped',
#     barmode='stack',
#     facet_col='CovidPeriod',
#     color_discrete_map={'Wins': '#D7263D', 'Other': '#7F7F7F'},
#     title='⚽ Liverpool Results by Venue & COVID Period (2015–2023)',
#     labels={'Count': 'Matches', 'Venue': 'Venue', 'Result_Grouped': 'Outcome'},
#     template='plotly_white'
# )

# # 7️⃣ Layout and style updates
# fig.update_layout(
#     font=dict(family='Segoe UI', size=14),
#     title_font=dict(size=24, color='#1f1f1f'),
#     legend=dict(title='Outcome', orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
#     margin=dict(t=80, b=80),
#     plot_bgcolor='white',
#     paper_bgcolor='white'
# )

# # 8️⃣ Trace styling
# fig.update_traces(
#     marker_line_width=1.5,
#     marker_line_color='white',
#     textposition='inside',
#     hovertemplate='<b>Venue:</b> %{x}<br>' +
#                   '<b>Outcome:</b> %{legendgroup}<br>' +
#                   '<b>Matches:</b> %{y}<extra></extra>'
# )

# # 9️⃣ Show and Save
# fig.show()

# # Save as PNG
# pio.write_image(fig, "liverpool_covid_stacked_modern.png", width=1200, height=600)


# import pandas as pd
# import plotly.express as px
# import plotly.io as pio

# # 📂 Load dataset
# df = pd.read_csv('Liverpool_Filtered_2015_onwards.csv')

# # 📌 Rename columns (if needed)
# rename_columns = {
#     'Div': 'Division',
#     'Date': 'Date',
#     'HomeTeam': 'HomeTeam',
#     'AwayTeam': 'AwayTeam',
#     'FTHG': 'FullTimeHomeGoals',
#     'FTAG': 'FullTimeAwayGoals',
#     'FTR': 'FullTimeResult',
#     'Season': 'Season'
# }
# df = df.rename(columns=rename_columns)

# # 🏠 Add Venue column
# df['Venue'] = df.apply(lambda row: 'Home' if row['HomeTeam'] == 'Liverpool' else 'Away', axis=1)

# # 📅 Date parsing + COVID period
# df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
# def covid_period(date):
#     if pd.isnull(date): return 'Unknown'
#     elif date < pd.to_datetime('2020-03-01'): return 'Pre-COVID'
#     elif date < pd.to_datetime('2021-07-01'): return 'During COVID'
#     else: return 'Post-COVID'
# df['CovidPeriod'] = df['Date'].apply(covid_period)

# # 🏁 Result column from FTR
# df['Result'] = df['FullTimeResult'].map({'H': 'Win', 'D': 'Draw', 'A': 'Loss'})
# df.loc[df['Venue'] == 'Away', 'Result'] = df['FullTimeResult'].map({'A': 'Win', 'D': 'Draw', 'H': 'Loss'})

# # 📊 Plot 1: Wins Home vs Away
# wins = df[df['Result'] == 'Win'].groupby('Venue').size().reset_index(name='Wins')
# fig1 = px.bar(
#     wins, x='Venue', y='Wins', text='Wins', color='Venue',
#     title='🏠 Liverpool Wins (Home vs Away)',
#     color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
#     template='plotly_white'
# )
# fig1.update_traces(marker_line_color='white', marker_line_width=1.5, textposition='outside')
# fig1.update_layout(font=dict(size=14), title_font=dict(size=24))
# pio.write_image(fig1, "wins_home_away.png", width=1000, height=600)
# fig1.show()



# # 📊 Plot 2: 100% Stacked Result %
# outcome = df.groupby(['Venue', 'Result']).size().reset_index(name='Count')
# outcome['Percent'] = outcome['Count'] / outcome.groupby('Venue')['Count'].transform('sum') * 100
# fig2 = px.bar(
#     outcome, x='Venue', y='Percent', color='Result', text=outcome['Percent'].round(1),
#     barmode='stack', title='⚖️ Result % Breakdown (Home vs Away)',
#     color_discrete_sequence=px.colors.qualitative.Safe, template='plotly_white'
# )
# fig2.update_layout(font=dict(size=14), title_font=dict(size=24))
# pio.write_image(fig2, "result_percent_stacked.png", width=1000, height=600)
# fig2.show()

# # 📊 Plot 3: COVID Result Breakdown
# covid_outcome = df.groupby(['CovidPeriod', 'Venue', 'Result']).size().reset_index(name='Count')
# fig3 = px.bar(
#     covid_outcome, x='Venue', y='Count', color='Result', barmode='stack',
#     facet_col='CovidPeriod', title='🦠 Result Breakdown by Venue & COVID Period',
#     color_discrete_sequence=px.colors.qualitative.Bold, template='plotly_white'
# )
# fig3.update_layout(font=dict(size=14), title_font=dict(size=24))
# pio.write_image(fig3, "result_covid_venue.png", width=1200, height=600)
# fig3.show()

# # 📊 Plot 4: Wins Over Time
# df['Year'] = df['Date'].dt.year
# wins_time = df[df['Result'] == 'Win'].groupby(['Year', 'Venue']).size().reset_index(name='Wins')
# fig4 = px.line(
#     wins_time, x='Year', y='Wins', color='Venue', markers=True,
#     title='📈 Liverpool Wins Over Time (Home vs Away)',
#     color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
#     template='plotly_white'
# )
# fig4.update_layout(font=dict(size=14), title_font=dict(size=24))
# pio.write_image(fig4, "wins_over_time.png", width=1000, height=600)
# fig4.show()

# # 📊 Plot 5: Goals Box Plot
# df['GoalsFor'] = df.apply(lambda row: row['FullTimeHomeGoals'] if row['Venue'] == 'Home' else row['FullTimeAwayGoals'], axis=1)
# fig5 = px.box(
#     df, x='Venue', y='GoalsFor', points='all',
#     title='🎯 Goals Scored per Match (Home vs Away)',
#     color='Venue',
#     color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
#     template='plotly_white'
# )
# fig5.update_layout(font=dict(size=14), title_font=dict(size=24))
# pio.write_image(fig5, "boxplot_goals.png", width=1000, height=600)
# fig5.show()







# import pandas as pd
# import plotly.express as px

# # Load manager data
# managers_df = pd.read_csv("liverpoolfc_managers.csv", sep=';')

# # Convert date strings
# managers_df['From'] = pd.to_datetime(managers_df['From'])
# managers_df['To'] = pd.to_datetime(managers_df['To'])

# # Calculate duration
# managers_df['Days'] = (managers_df['To'] - managers_df['From']).dt.days
# managers_df['Years'] = (managers_df['Days'] / 365).round(1)

# # Sort chronologically
# managers_df = managers_df.sort_values(by='From')

# # Create horizontal bar chart
# fig = px.bar(
#     managers_df,
#     x='Years',
#     y='Name',
#     color='win_perc',
#     text='win_perc',
#     orientation='h',
#     title="🔴 Liverpool Managers: Tenure Duration vs Win %",
#     labels={'Years': 'Years in Charge', 'win_perc': 'Win %'},
#     color_continuous_scale='RdYlGn',
#     template='plotly_white'
# )

# fig.update_layout(
#     xaxis_title='Years Managed',
#     yaxis_title='Manager',
#     coloraxis_colorbar=dict(title="Win %"),
#     height=700
# )

# fig.show()
# fig.write_image("manager.png")


# import pandas as pd
# import plotly.express as px

# # Load manager data
# managers_df = pd.read_csv("liverpoolfc_managers.csv", sep=';')

# # Convert date strings
# managers_df['From'] = pd.to_datetime(managers_df['From'])
# managers_df['To'] = pd.to_datetime(managers_df['To'])

# # Calculate duration
# managers_df['Days'] = (managers_df['To'] - managers_df['From']).dt.days
# managers_df['Years'] = (managers_df['Days'] / 365).round(1)

# # Sort by start date
# managers_df = managers_df.sort_values(by='From')

# # 📈 Plot 1: Win % Over Time
# fig1 = px.line(
#     managers_df,
#     x='From',
#     y='win_perc',
#     text='Name',
#     markers=True,
#     title='📈 Liverpool Managers Over Time: Win % Trend',
#     labels={'From': 'Start Year', 'win_perc': 'Win Percentage'},
#     template='plotly_white'
# )
# fig1.update_traces(textposition='top center', marker=dict(size=10, color='red'))
# fig1.update_layout(
#     title_font=dict(size=22),
#     margin=dict(l=60, r=60, t=80, b=60),
#     xaxis_tickformat='%Y',
#     xaxis_title='Start Year',
#     yaxis_title='Win Percentage (%)',
#     hovermode='x unified'
# )
# fig1.write_image("liverpool_managers_win_trend.png", width=1000, height=600)
# fig1.show()

# # 🔵 Plot 2: Win % vs Games Managed (Bubble = Tenure)
# fig2 = px.scatter(
#     managers_df,
#     x='P',  # Number of games played
#     y='win_perc',
#     size='Years',
#     color='win_perc',
#     text='Name',
#     title='⚽ Win % vs Games Managed (Bubble = Tenure)',
#     labels={'P': 'Games Managed', 'win_perc': 'Win %', 'Years': 'Tenure (Years)'},
#     color_continuous_scale='Blues',
#     template='plotly_white'
# )
# fig2.update_traces(textposition='top center')
# fig2.update_layout(
#     title_font=dict(size=22),
#     margin=dict(l=60, r=60, t=80, b=60),
#     xaxis_title='Games Managed',
#     yaxis_title='Win Percentage (%)',
#     hovermode='closest'
# )
# fig2.write_image("liverpool_managers_bubble.png", width=1000, height=600)
# fig2.show()

# # 🥧 Plot 3: Share of Total Matches Managed
# fig3 = px.pie(
#     managers_df,
#     names='Name',
#     values='P',
#     title='🧩 Games Managed by Each Liverpool Manager',
#     template='plotly_white',
#     hole=0.3  # Donut style
# )
# fig3.update_traces(
#     textposition='inside',
#     textinfo='percent+label',
#     pull=[0.05]*len(managers_df)  # Slight pull to enhance visibility
# )
# fig3.update_layout(
#     title_font=dict(size=22),
#     margin=dict(l=60, r=60, t=80, b=60)
# )
# fig3.write_image("liverpool_managers_pie.png", width=800, height=600)
# fig3.show()

#         return html.Div([
#             dcc.Graph(figure=fig)
#         ])

#     return html.P("No content available.")

# if __name__ == "__main__":
#     app.run(debug=True)







# # import dash
# # from dash import html, dcc
# # from dash.dependencies import Input, Output
# # import dash_bootstrap_components as dbc
# # import plotly.express as px
# # import plotly.graph_objs as go
# # import pandas as pd
# # import pickle
# # import os

# # # Initialize the Dash app
# # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# # app.title = "Liverpool Match Dashboard"

# # # Load the shot map figure if it exists
# # try:
# #     shot_map_fig = pickle.load(open("shot_map_fig.pkl", "rb"))
# # except FileNotFoundError:
# #     # Create a placeholder figure if file doesn't exist
# #     shot_map_fig = px.scatter(x=[0, 1], y=[0, 1], title="Shot Map - Data not available")

# # # App layout
# # app.layout = dbc.Container(fluid=True, children=[
# #     dbc.Row([
# #         dbc.Col(html.H2("⚽ Liverpool Match Dashboard", className="text-center text-primary my-4"), width=12)
# #     ]),
# #     dbc.Tabs([
# #         dbc.Tab(label="Shot Map", tab_id="shot-map"),
# #         dbc.Tab(label="Expected Goals (xG)", tab_id="expected-goals-(xg)"),
# #         dbc.Tab(label="Other", tab_id="other"),
# #     ], id="tabs", active_tab="shot-map", className="mb-3"),
# #     dbc.Row([dbc.Col(html.Div(id="tab-content"))])
# # ])

# # # Helper functions for Shot Map tab
# # def create_liverpool_performance_stats():
# #     """Create Liverpool performance stats figure"""
# #     try:
# #         stats_df = pd.read_csv("stats.csv")
# #         # Filter only Liverpool data
# #         liverpool_stats = stats_df[stats_df['team'] == 'Liverpool']
# #         # Select relevant columns
# #         liverpool_stats = liverpool_stats[['season', 'total_scoring_att', 'ontarget_scoring_att', 'goals', 'wins']]
# #         # Melt for plotting
# #         liverpool_melted = liverpool_stats.melt(id_vars='season', var_name='Metric', value_name='Value')
        
# #         # Create interactive line chart
# #         fig = px.line(
# #             liverpool_melted,
# #             x='season',
# #             y='Value',
# #             color='Metric',
# #             markers=True,
# #             title='Liverpool Performance by Season: Shots, Shots on Target, Goals, Wins',
# #             labels={'Value': 'Count', 'season': 'Season'},
# #             template='plotly_white'
# #         )
        
# #         # Fix layout margins
# #         fig.update_layout(
# #             title_font=dict(size=22),
# #             legend_title_text='Metric',
# #             margin=dict(l=60, r=60, t=80, b=60)
# #         )
        
# #         return fig
# #     except FileNotFoundError:
# #         return px.line(title="Liverpool Performance Stats - Data not available")

# # def create_covid_performance_breakdown():
# #     """Create COVID performance breakdown figure"""
# #     try:
# #         df = pd.read_csv("epl_final.csv")
# #         # Filter only Liverpool matches
# #         liverpool_df = df[(df['HomeTeam'] == 'Liverpool') | (df['AwayTeam'] == 'Liverpool')].copy()
        
# #         # Determine venue from Liverpool's perspective
# #         liverpool_df['Venue'] = liverpool_df['HomeTeam'].apply(lambda x: 'Home' if x == 'Liverpool' else 'Away')
        
# #         # Parse match dates and assign COVID periods
# #         liverpool_df['MatchDate'] = pd.to_datetime(liverpool_df['MatchDate'])
        
# #         def covid_period(date):
# #             if date < pd.to_datetime('2020-03-01'):
# #                 return 'Pre-COVID'
# #             elif date <= pd.to_datetime('2021-07-01'):
# #                 return 'During-COVID'
# #             else:
# #                 return 'Post-COVID'
        
# #         liverpool_df['CovidPeriod'] = liverpool_df['MatchDate'].apply(covid_period)
        
# #         # Add match stats from Liverpool's perspective
# #         liverpool_df['Goals'] = liverpool_df.apply(
# #             lambda row: row['FullTimeHomeGoals'] if row['Venue'] == 'Home' else row['FullTimeAwayGoals'], axis=1)
        
# #         liverpool_df['GoalsConceded'] = liverpool_df.apply(
# #             lambda row: row['FullTimeAwayGoals'] if row['Venue'] == 'Home' else row['FullTimeHomeGoals'], axis=1)
        
# #         liverpool_df['Shots'] = liverpool_df.apply(
# #             lambda row: row['HomeShots'] if row['Venue'] == 'Home' else row['AwayShots'], axis=1)
        
# #         liverpool_df['ShotsOnTarget'] = liverpool_df.apply(
# #             lambda row: row['HomeShotsOnTarget'] if row['Venue'] == 'Home' else row['AwayShotsOnTarget'], axis=1)
        
# #         liverpool_df['Win'] = liverpool_df.apply(
# #             lambda row: 1 if row['Goals'] > row['GoalsConceded'] else 0, axis=1)
        
# #         # Group and summarize
# #         summary = liverpool_df.groupby(['CovidPeriod', 'Venue']).agg({
# #             'Goals': 'mean',
# #             'GoalsConceded': 'mean',
# #             'Shots': 'mean',
# #             'ShotsOnTarget': 'mean',
# #             'Win': 'mean'
# #         }).reset_index().rename(columns={'Win': 'WinRate'}).round(2)
        
# #         # Melt for visualization
# #         melted_summary = summary.melt(
# #             id_vars=['CovidPeriod', 'Venue'],
# #             value_vars=['Goals', 'GoalsConceded', 'Shots', 'ShotsOnTarget', 'WinRate'],
# #             var_name='Metric',
# #             value_name='Value'
# #         )
        
# #         # Plot
# #         fig = px.bar(
# #             melted_summary,
# #             x='CovidPeriod',
# #             y='Value',
# #             color='Venue',
# #             barmode='group',
# #             facet_col='Metric',
# #             category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
# #             title='📊 Liverpool Performance Breakdown by COVID Period and Venue',
# #             labels={
# #                 'Value': 'Average per Match',
# #                 'CovidPeriod': 'Period',
# #                 'Venue': 'Venue'
# #             },
# #             template='plotly_white',
# #             height=600
# #         )
        
# #         # Enhanced layout
# #         fig.update_layout(
# #             title_font=dict(size=24),
# #             font=dict(size=13),
# #             legend_title_text='Venue',
# #             legend=dict(orientation='h', y=1.15, x=0.3),
# #             margin=dict(l=60, r=60, t=100, b=60)
# #         )
        
# #         # Improve annotation readability
# #         fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("WinRate", "Win Rate")))
        
# #         return fig
# #     except FileNotFoundError:
# #         return px.bar(title="COVID Performance Breakdown - Data not available")

# # def create_goals_winrate_chart():
# #     """Create Goals & Win Rate chart"""
# #     try:
# #         # This would use the summary from create_covid_performance_breakdown
# #         # For now, create sample data
# #         sample_data = pd.DataFrame({
# #             'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID'] * 4,
# #             'Venue': ['Home', 'Away'] * 6,
# #             'Goals': [2.1, 1.8, 1.9, 1.6, 2.2, 1.9],
# #             'WinRate': [0.65, 0.45, 0.58, 0.42, 0.72, 0.48]
# #         })
        
# #         bar_data = sample_data.melt(
# #             id_vars=['CovidPeriod', 'Venue'],
# #             value_vars=['Goals', 'WinRate'],
# #             var_name='Metric',
# #             value_name='Value'
# #         )
        
# #         fig = px.bar(
# #             bar_data,
# #             x='CovidPeriod',
# #             y='Value',
# #             color='Venue',
# #             barmode='group',
# #             facet_col='Metric',
# #             category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
# #             title='📊 Liverpool Goals & Win Rate by COVID Period and Venue',
# #             labels={'Value': 'Metric Value', 'CovidPeriod': 'Period'},
# #             template='plotly_white',
# #             height=500
# #         )
        
# #         fig.update_layout(
# #             title_font=dict(size=22),
# #             font=dict(size=12),
# #             legend_title_text='Venue',
# #             margin=dict(l=60, r=60, t=80, b=60)
# #         )
# #         fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("WinRate", "Win Rate")))
        
# #         return fig
# #     except Exception:
# #         return px.bar(title="Goals & Win Rate - Data not available")

# # def create_winrate_trend():
# #     """Create Win Rate Trend chart"""
# #     try:
# #         sample_data = pd.DataFrame({
# #             'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID', 'Pre-COVID', 'During-COVID', 'Post-COVID'],
# #             'Venue': ['Home', 'Home', 'Home', 'Away', 'Away', 'Away'],
# #             'WinRate': [0.65, 0.58, 0.72, 0.45, 0.42, 0.48]
# #         })
        
# #         fig = px.line(
# #             sample_data,
# #             x='CovidPeriod',
# #             y='WinRate',
# #             color='Venue',
# #             markers=True,
# #             title='📈 Liverpool Win Rate Trend by Venue',
# #             labels={'WinRate': 'Win Rate (%)', 'CovidPeriod': 'COVID Period'},
# #             category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
# #             template='plotly_white'
# #         )
        
# #         fig.update_layout(
# #             yaxis_tickformat='.0%',
# #             title_font=dict(size=22),
# #             font=dict(size=12),
# #             legend_title_text='Venue',
# #             margin=dict(l=60, r=60, t=80, b=60)
# #         )
        
# #         return fig
# #     except Exception:
# #         return px.line(title="Win Rate Trend - Data not available")

# # def create_radar_chart():
# #     """Create Radar Chart for Home vs Away performance"""
# #     try:
# #         # Sample data for radar chart
# #         avg_metrics = pd.DataFrame({
# #             'Venue': ['Home', 'Away'],
# #             'Goals': [2.1, 1.7],
# #             'GoalsConceded': [1.0, 1.3],
# #             'Shots': [15.2, 13.8],
# #             'ShotsOnTarget': [6.1, 5.4],
# #             'WinRate': [0.65, 0.45]
# #         })
        
# #         fig = go.Figure()
        
# #         for _, row in avg_metrics.iterrows():
# #             fig.add_trace(go.Scatterpolar(
# #                 r=row[1:].values,
# #                 theta=avg_metrics.columns[1:],
# #                 fill='toself',
# #                 name=row['Venue'],
# #                 line=dict(width=2)
# #             ))
        
# #         fig.update_layout(
# #             polar=dict(
# #                 radialaxis=dict(visible=True, range=[0, max(avg_metrics.iloc[:, 1:].max()) * 1.2])
# #             ),
# #             title='🛡️ Overall Performance Radar: Home vs Away',
# #             template='plotly_white',
# #             title_font=dict(size=22),
# #             font=dict(size=12),
# #             margin=dict(l=60, r=60, t=80, b=60)
# #         )
        
# #         return fig
# #     except Exception:
# #         return go.Figure().add_annotation(text="Radar Chart - Data not available")

# # # Helper functions for Expected Goals tab
# # def create_home_xg_vs_goals():
# #     """Create Home xG vs Goals chart"""
# #     try:
# #         df = pd.read_csv('EPL_result.csv')
        
# #         # Group by home team: average xG and actual goals
# #         home_stats = df.groupby('Home').agg(
# #             Avg_xG_Home=('xG_Home', 'mean'),
# #             Avg_G_Home=('G_Home', 'mean')
# #         ).reset_index()
        
# #         # Melt for grouped bar
# #         home_stats_melted = home_stats.melt(
# #             id_vars='Home',
# #             value_vars=['Avg_xG_Home', 'Avg_G_Home'],
# #             var_name='Metric',
# #             value_name='Goals'
# #         )
        
# #         # Add highlighting (Liverpool bold)
# #         home_stats_melted['Highlight'] = home_stats_melted['Home'].apply(lambda x: 'Liverpool' if x == 'Liverpool' else 'Other')
        
# #         # Plot with enhanced design
# #         fig = px.bar(
# #             home_stats_melted,
# #             x='Home',
# #             y='Goals',
# #             color='Metric',
# #             barmode='group',
# #             text='Goals',
# #             title='⚽ Average Home xG vs Actual Goals per Team (Highlight: Liverpool)',
# #             template='plotly_white',
# #             color_discrete_map={
# #                 'Avg_xG_Home': '#1f77b4',
# #                 'Avg_G_Home': '#d62728'
# #             }
# #         )
        
# #         # Aesthetic improvements
# #         fig.update_traces(
# #             texttemplate='%{text:.2f}',
# #             textposition='outside',
# #             marker_line_color='white',
# #             marker_line_width=1.2
# #         )
# #         fig.update_layout(
# #             xaxis_title='Club (Home Games)',
# #             yaxis_title='Goals (Average)',
# #             font=dict(size=14),
# #             title_font=dict(size=22),
# #             xaxis_tickangle=45,
# #             bargap=0.25
# #         )
        
# #         return fig
# #     except FileNotFoundError:
# #         return px.bar(title="Home xG vs Goals - Data not available")

# # def create_xg_vs_xga_charts():
# #     """Create xG vs xGA charts"""
# #     try:
# #         # Sample data for xG analysis
# #         sample_teams = ['Liverpool', 'Manchester City', 'Arsenal', 'Chelsea', 'Tottenham', 'Manchester United']
# #         sample_data = pd.DataFrame({
# #             'Team': sample_teams,
# #             'xGpm': [2.1, 2.3, 1.8, 1.9, 1.7, 1.6],
# #             'xGApm': [1.0, 0.9, 1.2, 1.1, 1.3, 1.4]
# #         })
        
# #         # Sort by xG
# #         sample_data = sample_data.sort_values(by='xGpm', ascending=False)
        
# #         # Horizontal Bar Chart
# #         fig = go.Figure()
        
# #         fig.add_trace(go.Bar(
# #             x=sample_data['xGpm'],
# #             y=sample_data['Team'],
# #             name='xG per Match',
# #             orientation='h',
# #             marker=dict(color='crimson'),
# #             hovertemplate='Team: %{y}<br>xG: %{x}<extra></extra>'
# #         ))
        
# #         fig.add_trace(go.Bar(
# #             x=sample_data['xGApm'],
# #             y=sample_data['Team'],
# #             name='xGA per Match',
# #             orientation='h',
# #             marker=dict(color='dodgerblue'),
# #             hovertemplate='Team: %{y}<br>xGA: %{x}<extra></extra>'
# #         ))
        
# #         fig.update_layout(
# #             title='⚽ EPL: xG vs xGA per Match (Side-by-Side)',
# #             barmode='group',
# #             yaxis=dict(autorange="reversed"),
# #             template='plotly_white',
# #             height=700
# #         )
        
# #         return fig
# #     except Exception:
# #         return go.Figure().add_annotation(text="xG vs xGA - Data not available")

# # def create_delta_xg_chart():
# #     """Create Delta xG chart"""
# #     try:
# #         # Sample data
# #         sample_teams = ['Liverpool', 'Manchester City', 'Arsenal', 'Chelsea', 'Tottenham', 'Manchester United']
# #         sample_data = pd.DataFrame({
# #             'Team': sample_teams,
# #             'delta_xGpm': [1.1, 1.4, 0.6, 0.8, 0.4, 0.2]
# #         })
        
# #         # Sort by delta
# #         sample_data = sample_data.sort_values(by='delta_xGpm', ascending=False)
        
# #         fig = px.bar(
# #             sample_data,
# #             x='delta_xGpm',
# #             y='Team',
# #             orientation='h',
# #             text='delta_xGpm',
# #             title='⚽ EPL: Delta xG (Scored - Conceded)',
# #             labels={'delta_xGpm': 'Delta xG per Match', 'Team': 'Team'},
# #             template='plotly_white',
# #             color='delta_xGpm',
# #             color_continuous_scale='RdYlGn'
# #         )
        
# #         fig.update_traces(
# #             texttemplate='%{x:.2f}',
# #             textposition='outside'
# #         )
# #         fig.update_layout(
# #             xaxis_title='ΔxG per Match',
# #             yaxis=dict(autorange='reversed'),
# #             title_font=dict(size=20),
# #             coloraxis_showscale=False,
# #             margin=dict(t=60, b=40)
# #         )
        
# #         return fig
# #     except Exception:
# #         return px.bar(title="Delta xG - Data not available")

# # def create_xg_home_away():
# #     """Create xG Home vs Away chart"""
# #     try:
# #         # Sample data
# #         sample_teams = ['Liverpool', 'Manchester City', 'Arsenal', 'Chelsea', 'Tottenham', 'Manchester United']
# #         sample_data = pd.DataFrame({
# #             'Team': sample_teams,
# #             'xG_h': [2.3, 2.5, 2.0, 2.1, 1.9, 1.8],
# #             'xG_a': [1.9, 2.1, 1.6, 1.7, 1.5, 1.4]
# #         })
        
# #         # Sort by home xG
# #         sample_data = sample_data.sort_values(by='xG_h', ascending=False)
        
# #         fig = go.Figure()
        
# #         # xG Home
# #         fig.add_trace(go.Bar(
# #             x=sample_data['xG_h'],
# #             y=sample_data['Team'],
# #             name='xG at Home',
# #             orientation='h',
# #             marker=dict(color='firebrick'),
# #             hovertemplate='Team: %{y}<br>xG at Home: %{x}<extra></extra>'
# #         ))
        
# #         # xG Away
# #         fig.add_trace(go.Bar(
# #             x=sample_data['xG_a'],
# #             y=sample_data['Team'],
# #             name='xG Away',
# #             orientation='h',
# #             marker=dict(color='darkblue'),
# #             hovertemplate='Team: %{y}<br>xG Away: %{x}<extra></extra>'
# #         ))
        
# #         fig.update_layout(
# #             title='⚽ EPL: xG Scored per Match — Home vs Away',
# #             barmode='group',
# #             yaxis=dict(autorange="reversed"),
# #             template='plotly_white',
# #             xaxis_title='xG per Match',
# #             height=700
# #         )
        
# #         return fig
# #     except Exception:
# #         return go.Figure().add_annotation(text="xG Home vs Away - Data not available")

# # def create_xg_difference_chart():
# #     """Create xG Difference chart"""
# #     try:
# #         # Sample data
# #         sample_teams = ['Liverpool', 'Manchester City', 'Arsenal', 'Chelsea', 'Tottenham', 'Manchester United']
# #         sample_data = pd.DataFrame({
# #             'Team': sample_teams,
# #             'delta_xG_ha': [0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
# #         })
        
# #         # Sort for visual clarity
# #         sample_data = sample_data.sort_values(by='delta_xG_ha', ascending=False)
        
# #         fig = px.bar(
# #             sample_data,
# #             x='delta_xG_ha',
# #             y='Team',
# #             orientation='h',
# #             title='⚽ EPL: xG Difference (Home - Away)',
# #             labels={'delta_xG_ha': 'ΔxG (Home - Away)', 'Team': 'Team'},
# #             template='plotly_white',
# #             text='delta_xG_ha',
# #             color='delta_xG_ha',
# #             color_continuous_scale='RdBu'
# #         )
        
# #         fig.update_traces(
# #             texttemplate='%{x:.2f}',
# #             textposition='outside'
# #         )
# #         fig.update_layout(
# #             xaxis_title='xG Difference (Home - Away)',
# #             yaxis=dict(autorange='reversed'),
# #             coloraxis_showscale=False,
# #             title_font=dict(size=20),
# #             margin=dict(t=60, b=40)
# #         )
        
# #         return fig
# #     except Exception:
# #         return px.bar(title="xG Difference - Data not available")

# # # Helper functions for Other tab
# # def create_wins_home_away():
# #     """Create Wins Home vs Away chart"""
# #     try:
# #         df = pd.read_csv('Liverpool_2015_2023_Matches.csv')
        
# #         # Add Venue column
# #         df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)
        
# #         # Add Result column
# #         def get_result(row):
# #             if row['Venue'] == 'Home':
# #                 if row['HomeGoals'] > row['AwayGoals']:
# #                     return 'Win'
# #                 elif row['HomeGoals'] == row['AwayGoals']:
# #                     return 'Draw'
# #                 else:
# #                     return 'Loss'
# #             else:
# #                 if row['AwayGoals'] > row['HomeGoals']:
# #                     return 'Win'
# #                 elif row['AwayGoals'] == row['HomeGoals']:
# #                     return 'Draw'
# #                 else:
# #                     return 'Loss'
        
# #         df['Result'] = df.apply(get_result, axis=1)
        
# #         # Create Summary Table
# #         summary = df.groupby('Venue').agg(
# #             Total_Matches=('Result', 'count'),
# #             Wins=('Result', lambda x: (x == 'Win').sum())
# #         ).reset_index()
        
# #         summary['Win_Percentage'] = (summary['Wins'] / summary['Total_Matches'] * 100).round(1)
        
# #         fig = px.bar(
# #             summary,
# #             x='Venue',
# #             y='Wins',
# #             text='Wins',
# #             color='Venue',
# #             color_discrete_map={'Home': 'red', 'Away': 'green'},
# #             labels={'Wins': 'Number of Wins', 'Venue': 'Venue'},
# #             template='plotly_white',
# #             title=f"⚽ Liverpool Wins (2015–2023) — Home vs Away<br>Total Games: {summary['Total_Matches'].sum()}"
# #         )
        
# #         fig.update_traces(
# #             textposition='outside',
# #             customdata=summary[['Total_Matches', 'Win_Percentage']].values,
# #             hovertemplate='<b>Venue:</b> %{x}<br>' +
# #                           '<b>Wins:</b> %{y}<br>' +
# #                           '<b>Total Games:</b> %{customdata[0]}<br>' +
# #                           '<b>Win %:</b> %{customdata[1]}%'
# #         )
# #         fig.update_layout(
# #             title_font=dict(size=22),
# #             xaxis_title='Venue',
# #             yaxis_title='Number of Wins',
# #             xaxis=dict(title_font=dict(size=18)),
# #             yaxis=dict(title_font=dict(size=18)),
# #             showlegend=False
# #         )
        
# #         return fig
# #     except FileNotFoundError:
# #         # Create sample data
# #         sample_data = pd.DataFrame({
# #             'Venue': ['Home', 'Away'],
# #             'Wins': [85, 65],
# #             'Total_Matches': [120, 118],
# #             'Win_Percentage': [70.8, 55.1]
# #         })
        
# #         fig = px.bar(
# #             sample_data,
# #             x='Venue',
# #             y='Wins',
# #             text='Wins',
# #             color='Venue',
# #             color_discrete_map={'Home': 'red', 'Away': 'green'},
# #             title="⚽ Liverpool Wins — Home vs Away (Sample Data)",
# #             template='plotly_white'
# #         )
        
# #         return fig

# # def create_covid_results_breakdown():
# #     """Create COVID results breakdown"""
# #     try:
# #         df = pd.read_csv("Liverpool_2015_2023_Matches.csv")
        
# #         # Add Venue column
# #         df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)
        
# #         # Add Result column
# #         def get_result(row):
# #             if row['Venue'] == 'Home':
# #                 return 'Win' if row['HomeGoals'] > row['AwayGoals'] else 'Draw' if row['HomeGoals'] == row['AwayGoals'] else 'Loss'
# #             else:
# #                 return 'Win' if row['AwayGoals'] > row['HomeGoals'] else 'Draw' if row['AwayGoals'] == row['HomeGoals'] else 'Loss'
        
# #         df['Result'] = df.apply(get_result, axis=1)
        
# #         # Add CovidPeriod column
# #         df['Date'] = pd.to_datetime(df['Date'])
# #         def covid_period(date):
# #             if date < pd.to_datetime('2020-03-01'):
# #                 return 'Pre-COVID'
# #             elif date < pd.to_datetime('2021-07-01'):
# #                 return 'During COVID'
# #             else:
# #                 return 'Post-COVID'
        
# #         df['CovidPeriod'] = df['Date'].apply(covid_period)
        
# #         # Group and summarize data
# #         summary = df.groupby(['CovidPeriod', 'Venue', 'Result']).size().reset_index(name='Count')
# #         summary['Result_Grouped'] = summary['Result'].apply(lambda x: 'Wins' if x == 'Win' else 'Other')
# #         stacked = summary.groupby(['CovidPeriod', 'Venue', 'Result_Grouped'])['Count'].sum().reset_index()
        
# #         fig = px.bar(
# #             stacked,
# #             x='Venue',
# #             y='Count',
# #             color='Result_Grouped',
# #             barmode='stack',
# #             facet_col='CovidPeriod',
# #             color_discrete_map={'Wins': '#D7263D', 'Other': '#7F7F7F'},
# #             title='⚽ Liverpool Results by Venue & COVID Period (2015–2023)',
# #             labels={'Count': 'Matches', 'Venue': 'Venue', 'Result_Grouped': 'Outcome'},
# #             template='plotly_white'
# #         )
        
# #         fig.update_layout(
# #             font=dict(family='Segoe UI', size=14),
# #             title_font=dict(size=24, color='#1f1f1f'),
# #             legend=dict(title='Outcome', orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
# #             margin=dict(t=80, b=80),
# #             plot_bgcolor='white',
# #             paper_bgcolor='white'
# #         )
        
# #         fig.update_traces(
# #             marker_line_width=1.5,
# #             marker_line_color='white',
# #             textposition='inside',
# #             hovertemplate='<b>Venue:</b> %{x}<br>' +
# #                           '<b>Outcome:</b> %{legendgroup}<br>' +
# #                           '<b>Matches:</b> %{y}<extra></extra>'
# #         )
        
# #         return fig
# #     except FileNotFoundError:
# #         return px.bar(title="COVID Results Breakdown - Data not available")

# # def create_wins_over_time():
# #     """Create Wins Over Time chart"""
# #     try:
# #         df = pd.read_csv('Liverpool_Filtered_2015_onwards.csv')
        
# #         # Process data
# #         df['Venue'] = df.apply(lambda row: 'Home' if row['HomeTeam'] == 'Liverpool' else 'Away', axis=1)
# #         df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
# #         df['Result'] = df['FullTimeResult'].map({'H': 'Win', 'D': 'Draw', 'A': 'Loss'})
# #         df.loc[df['Venue'] == 'Away', 'Result'] = df['FullTimeResult'].map({'A': 'Win', 'D': 'Draw', 'H': 'Loss'})
        
# #         df['Year'] = df['Date'].dt.year
# #         wins_time = df[df['Result'] == 'Win'].groupby(['Year', 'Venue']).size().reset_index(name='Wins')
        
# #         fig = px.line(
# #             wins_time, x='Year', y='Wins', color='Venue', markers=True,
# #             title='📈 Liverpool Wins Over Time (Home vs Away)',
# #             color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
# #             template='plotly_white'
# #         )
# #         fig.update_layout(font=dict(size=14), title_font=dict(size=24))
        
# #         return fig
# #     except FileNotFoundError:
# #         return px.line(title="Wins Over Time - Data not available")

# # def create_manager_performance():
# #     """Create Manager Performance chart"""
# #     try:
# #         managers_df = pd.read_csv("liverpoolfc_managers.csv", sep=';')
        
# #         # Convert date strings
# #         managers_df['From'] = pd.to_datetime(managers_df['From'])
# #         managers_df['To'] = pd.to_datetime(managers_df['To'])
        
# #         # Calculate duration
# #         managers_df['Days'] = (managers_df['To'] - managers_df['From']).dt.days
# #         managers_df['Years'] = (managers_df['Days'] / 365).round(1)
        
# #         # Sort chronologically
# #         managers_df