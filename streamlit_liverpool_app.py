
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Liverpool Streamlit Dashboard", layout="wide")
st.title("⚽ Liverpool Full Analysis Dashboard")


import pandas as pd
import plotly.express as px
import plotly.io as pio

# 1️⃣ Load your CSV
df = pd.read_csv('Liverpool_2015_2023_Matches.csv')

# 2️⃣ Add Venue column
df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)

# 3️⃣ Add Result column
def get_result(row):
    if row['Venue'] == 'Home':
        if row['HomeGoals'] > row['AwayGoals']:
            return 'Win'
        elif row['HomeGoals'] == row['AwayGoals']:
            return 'Draw'
        else:
            return 'Loss'
    else:
        if row['AwayGoals'] > row['HomeGoals']:
            return 'Win'
        elif row['AwayGoals'] == row['HomeGoals']:
            return 'Draw'
        else:
            return 'Loss'
df['Result'] = df.apply(get_result, axis=1)

# 4️⃣ Create Summary Table
summary = df.groupby('Venue').agg(
    Total_Matches=('Result', 'count'),
    Wins=('Result', lambda x: (x == 'Win').sum())
).reset_index()

summary['Win_Percentage'] = (summary['Wins'] / summary['Total_Matches'] * 100).round(1)

# 5️⃣ SINGLE BAR CHART: Wins only
fig1 = fig1 = px.bar(
    summary,
    x='Venue',
    y='Wins',
    text='Wins',
    color='Venue',
    color_discrete_map={'Home': 'red', 'Away': 'green'},
    labels={'Wins': 'Number of Wins', 'Venue': 'Venue'},
    template='plotly_white',
    title=f"⚽ Liverpool Wins (2015–2023) — Home vs Away<br>Total Games: {summary['Total_Matches'].sum()}"
    
)

fig1.update_traces(
    textposition='outside',
    customdata=summary[['Total_Matches', 'Win_Percentage']].values,
    hovertemplate='<b>Venue:</b> %{x}<br>' +
                  '<b>Wins:</b> %{y}<br>' +
                  '<b>Total Games:</b> %{customdata[0]}<br>' +
                  '<b>Win %:</b> %{customdata[1]}%'
)
fig1.update_layout(
    title_font=dict(size=22),
    xaxis_title='Venue',
    yaxis_title='Number of Wins',
    xaxis=dict(title_font=dict(size=18)),
    yaxis=dict(title_font=dict(size=18)),
    showlegend=False
)
st.plotly_chart(fig1, use_container_width=True)


# 6️⃣ GROUPED BAR CHART: Wins vs Total
summary_melted = summary.melt(id_vars='Venue', value_vars=['Total_Matches', 'Wins'])

fig1 = fig2 = px.bar(
    summary_melted,
    x='Venue',
    y='value',
    color='variable',
    barmode='group',
    text='value',
    title='⚽ Liverpool (2015–2023): Matches Played vs Wins (Home & Away)',
    labels={'value': 'Number of Matches', 'Venue': 'Venue', 'variable': 'Metric'},
    color_discrete_map={'Total_Matches': 'royalblue', 'Wins': 'crimson'},
    template='plotly_white'
)

fig1.update_traces(textposition='outside')
fig1.update_layout(
    title_font=dict(size=22),
    xaxis=dict(title_font=dict(size=18)),
    yaxis=dict(title_font=dict(size=18)),
    legend_title_text='Metric'
)
st.plotly_chart(fig1, use_container_width=True)

import pandas as pd
import plotly.express as px
import plotly.io as pio

# 1️⃣ Load the CSV
df = pd.read_csv("Liverpool_2015_2023_Matches.csv")

# 2️⃣ Add Venue column
df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)

# 3️⃣ Add Result column
def get_result(row):
    if row['Venue'] == 'Home':
        return 'Win' if row['HomeGoals'] > row['AwayGoals'] else 'Draw' if row['HomeGoals'] == row['AwayGoals'] else 'Loss'
    else:
        return 'Win' if row['AwayGoals'] > row['HomeGoals'] else 'Draw' if row['AwayGoals'] == row['HomeGoals'] else 'Loss'
df['Result'] = df.apply(get_result, axis=1)

# 4️⃣ Add CovidPeriod column
df['Date'] = pd.to_datetime(df['Date'])
def covid_period(date):
    if date < pd.to_datetime('2020-03-01'):
        return 'Pre-COVID'
    elif date < pd.to_datetime('2021-07-01'):
        return 'During COVID'
    else:
        return 'Post-COVID'
df['CovidPeriod'] = df['Date'].apply(covid_period)

# 5️⃣ Group and summarize data
summary = df.groupby(['CovidPeriod', 'Venue', 'Result']).size().reset_index(name='Count')
summary['Result_Grouped'] = summary['Result'].apply(lambda x: 'Wins' if x == 'Win' else 'Other')
stacked = summary.groupby(['CovidPeriod', 'Venue', 'Result_Grouped'])['Count'].sum().reset_index()

# 6️⃣ Modern stacked bar chart
fig2 = px.bar(
    stacked,
    x='Venue',
    y='Count',
    color='Result_Grouped',
    barmode='stack',
    facet_col='CovidPeriod',
    color_discrete_map={'Wins': '#D7263D', 'Other': '#7F7F7F'},
    title='⚽ Liverpool Results by Venue & COVID Period (2015–2023)',
    labels={'Count': 'Matches', 'Venue': 'Venue', 'Result_Grouped': 'Outcome'},
    template='plotly_white'
)

# 7️⃣ Layout and style updates
fig2.update_layout(
    font=dict(family='Segoe UI', size=14),
    title_font=dict(size=24, color='#1f1f1f'),
    legend=dict(title='Outcome', orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
    margin=dict(t=80, b=80),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# 8️⃣ Trace styling
fig2.update_traces(
    marker_line_width=1.5,
    marker_line_color='white',
    textposition='inside',
    hovertemplate='<b>Venue:</b> %{x}<br>' +
                  '<b>Outcome:</b> %{legendgroup}<br>' +
                  '<b>Matches:</b> %{y}<extra></extra>'
)

# 9️⃣ Show and Save

# Save as PNG
st.plotly_chart(fig2, use_container_width=True)

import pandas as pd
import plotly.express as px
import plotly.io as pio

# 📂 Load dataset
df = pd.read_csv('Liverpool_Filtered_2015_onwards.csv')

# 📌 Rename columns (if needed)
rename_columns = {
    'Div': 'Division',
    'Date': 'Date',
    'HomeTeam': 'HomeTeam',
    'AwayTeam': 'AwayTeam',
    'FTHG': 'FullTimeHomeGoals',
    'FTAG': 'FullTimeAwayGoals',
    'FTR': 'FullTimeResult',
    'Season': 'Season'
}
df = df.rename(columns=rename_columns)

# 🏠 Add Venue column
df['Venue'] = df.apply(lambda row: 'Home' if row['HomeTeam'] == 'Liverpool' else 'Away', axis=1)

# 📅 Date parsing + COVID period
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
def covid_period(date):
    if pd.isnull(date): return 'Unknown'
    elif date < pd.to_datetime('2020-03-01'): return 'Pre-COVID'
    elif date < pd.to_datetime('2021-07-01'): return 'During COVID'
    else: return 'Post-COVID'
df['CovidPeriod'] = df['Date'].apply(covid_period)

# 🏁 Result column from FTR
df['Result'] = df['FullTimeResult'].map({'H': 'Win', 'D': 'Draw', 'A': 'Loss'})
df.loc[df['Venue'] == 'Away', 'Result'] = df['FullTimeResult'].map({'A': 'Win', 'D': 'Draw', 'H': 'Loss'})

# 📊 Plot 1: Wins Home vs Away
wins = df[df['Result'] == 'Win'].groupby('Venue').size().reset_index(name='Wins')
fig3 = fig1 = px.bar(
    wins, x='Venue', y='Wins', text='Wins', color='Venue',
    title='🏠 Liverpool Wins (Home vs Away)',
    color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
    template='plotly_white'
)

fig2.update_traces(marker_line_color='white', marker_line_width=1.5, textposition='outside')
fig2.update_layout(font=dict(size=14), title_font=dict(size=24))




# 📊 Plot 2: 100% Stacked Result %
outcome = df.groupby(['Venue', 'Result']).size().reset_index(name='Count')
outcome['Percent'] = outcome['Count'] / outcome.groupby('Venue')['Count'].transform('sum') * 100
fig3 = fig2 = px.bar(
    outcome, x='Venue', y='Percent', color='Result', text=outcome['Percent'].round(1),
    barmode='stack', title='⚖️ Result % Breakdown (Home vs Away)',
    color_discrete_sequence=px.colors.qualitative.Safe, template='plotly_white'
)

fig2.update_layout(font=dict(size=14), title_font=dict(size=24))
st.plotly_chart(fig2, use_container_width=True)

# 📊 Plot 3: COVID Result Breakdown
covid_outcome = df.groupby(['CovidPeriod', 'Venue', 'Result']).size().reset_index(name='Count')
fig3 = px.bar(
    covid_outcome, x='Venue', y='Count', color='Result', barmode='stack',
    facet_col='CovidPeriod', title='🦠 Result Breakdown by Venue & COVID Period',
    color_discrete_sequence=px.colors.qualitative.Bold, template='plotly_white'
)
fig3.update_layout(font=dict(size=14), title_font=dict(size=24))

# 📊 Plot 4: Wins Over Time
df['Year'] = df['Date'].dt.year
wins_time = df[df['Result'] == 'Win'].groupby(['Year', 'Venue']).size().reset_index(name='Wins')
fig3 = fig4 = px.line(
    wins_time, x='Year', y='Wins', color='Venue', markers=True,
    title='📈 Liverpool Wins Over Time (Home vs Away)',
    color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
    template='plotly_white'
)
fig3.update_layout(font=dict(size=14), title_font=dict(size=24))
st.plotly_chart(fig3, use_container_width=True)

# 📊 Plot 5: Goals Box Plot
df['GoalsFor'] = df.apply(lambda row: row['FullTimeHomeGoals'] if row['Venue'] == 'Home' else row['FullTimeAwayGoals'], axis=1)
fig3 = fig5 = px.box(
    df, x='Venue', y='GoalsFor', points='all',
    title='🎯 Goals Scored per Match (Home vs Away)',
    color='Venue',
    color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
    template='plotly_white'
)
fig3.update_layout(font=dict(size=14), title_font=dict(size=24))
st.plotly_chart(fig3, use_container_width=True)

import pandas as pd
import plotly.express as px
import plotly.io as pio

# Optional: Force plot display in Jupyter
pio.renderers.default = 'notebook'  # or 'iframe', 'svg' if needed

# 📂 Load dataset
df = pd.read_csv('EPL_result.csv')

# 🧮 Group by home team: average xG and actual goals
home_stats = df.groupby('Home').agg(
    Avg_xG_Home=('xG_Home', 'mean'),
    Avg_G_Home=('G_Home', 'mean')
).reset_index()

# 🔁 Melt for grouped bar
home_stats_melted = home_stats.melt(
    id_vars='Home',
    value_vars=['Avg_xG_Home', 'Avg_G_Home'],
    var_name='Metric',
    value_name='Goals'
)

# 🟥 Add highlighting (Liverpool bold)
home_stats_melted['Highlight'] = home_stats_melted['Home'].apply(lambda x: 'Liverpool' if x == 'Liverpool' else 'Other')

# 🖼️ Plot with enhanced design
fig44 = px.bar(
    home_stats_melted,
    x='Home',
    y='Goals',
    color='Metric',
    barmode='group',
    text='Goals',
    title='⚽ Average Home xG vs Actual Goals per Team (Highlight: Liverpool)',
    template='plotly_white',
    color_discrete_map={
        'Avg_xG_Home': '#1f77b4',  # royal blue
        'Avg_G_Home': '#d62728'   # crimson red
    }
)

# ✏️ Aesthetic improvements
fig44.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside',
    marker_line_color='white',
    marker_line_width=1.2
)
fig44.update_layout(
    xaxis_title='Club (Home Games)',
    yaxis_title='Goals (Average)',
    font=dict(size=14),
    title_font=dict(size=22),
    xaxis_tickangle=45,
    bargap=0.25
)



# 🔍 Optional: Sort by Avg_G_Home if needed
home_stats_melted.sort_values(by='Goals', ascending=False, inplace=True)

# ✅ Show plot

# 💾 Save as PNG (requires kaleido)
st.plotly_chart(fig44, use_container_width=True)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Optional: set default renderer if needed
pio.renderers.default = 'notebook'
df = pd.read_csv("EPL_result.csv")  # make sure this file is in the directory

team_abb = {
    'Everton': 'EVE', 'Aston Villa': 'AVL', 'Leicester City': 'LEI',
    'Arsenal': 'ARS', 'Liverpool': 'LIV', 'Tottenham': 'TOT',
    'Chelsea': 'CHE', 'Leeds United': 'LEE', 'Newcastle Utd': 'NEW',
    'West Ham': 'WHU', 'Southampton': 'SOU', 'Crystal Palace': 'CRY',
    'Wolves': 'WOL', 'Manchester City': 'MCI', 'Brighton': 'BHA',
    'Manchester Utd': 'MUN', 'West Brom': 'WBA', 'Burnley': 'BUR',
    'Sheffield Utd': 'SHU', 'Fulham': 'FUL'
}

df['Home'] = df['Home'].map(team_abb)
df['Away'] = df['Away'].map(team_abb)
df['GD'] = df['G_Home'] - df['G_Away']
df['Pts_Home'] = df['GD'].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)
df['Pts_Away'] = df['GD'].apply(lambda x: 0 if x > 0 else 1 if x == 0 else 3)

gw_last = 7
gw_next = gw_last + 1

df_temp = pd.DataFrame({'Team': list(team_abb.values())})

# Build the full df_temp (abbreviated here for space)
df_temp['M_h'] = df_temp['Team'].apply(lambda x: df[(df['Home'] == x) & (df['GW'] < gw_next)].shape[0])
df_temp['M_a'] = df_temp['Team'].apply(lambda x: df[(df['Away'] == x) & (df['GW'] < gw_next)].shape[0])
df_temp['M'] = df_temp['M_h'] + df_temp['M_a']
df_temp['xG_h'] = df_temp['Team'].apply(lambda x: df[(df['Home'] == x) & (df['GW'] < gw_next)]['xG_Home'].sum())
df_temp['xG_a'] = df_temp['Team'].apply(lambda x: df[(df['Away'] == x) & (df['GW'] < gw_next)]['xG_Away'].sum())
df_temp['xGA_h'] = df_temp['Team'].apply(
    lambda x: df[(df['Home'] == x) & (df['GW'] < gw_next)]['xG_Away'].sum()
)

df_temp['xGA_a'] = df_temp['Team'].apply(
    lambda x: df[(df['Away'] == x) & (df['GW'] < gw_next)]['xG_Home'].sum()
)

df_temp['xGA'] = df_temp['xGA_h'] + df_temp['xGA_a']
df_temp['xGApm'] = df_temp['xGA'] / df_temp['M']



df_temp['xG'] = df_temp['xG_h'] + df_temp['xG_a']
df_temp['xGpm'] = df_temp['xG'] / df_temp['M']
df_temp['delta_xGpm'] = df_temp['xGpm'] - df_temp['xGApm']

# Sort the teams
df_temp = df_temp.sort_values(by='xGpm', ascending=False)

df_temp['delta_xG_ha'] = df_temp['xG_h'] - df_temp['xG_a']
df_temp.sort_values(by='delta_xG_ha', ascending=False)
# ===============================
# 1️⃣ Horizontal Bar Chart (xG and xGA side-by-side)
# ===============================
fig5 = fig1 = go.Figure()

fig1.add_trace(go.Bar(
    x=df_temp['xGpm'],
    y=df_temp['Team'],
    name='xG per Match',
    orientation='h',
    marker=dict(color='crimson'),
    hovertemplate='Team: %{y}<br>xG: %{x}<extra></extra>'
))


fig1.add_trace(go.Bar(
    
    x=df_temp['xGApm'],
    y=df_temp['Team'],
    name='xGA per Match',
    orientation='h',
    marker=dict(color='dodgerblue'),
    hovertemplate='Team: %{y}<br>xGA: %{x}<extra></extra>'
))

fig5.update_layout(
    title='⚽ EPL 2020/21: xG vs xGA per Match (Side-by-Side)',
    barmode='group',
    yaxis=dict(autorange="reversed"),
    template='plotly_white',
    height=700
)



# ===============================
# 2️⃣ Grouped Vertical Bar Chart
# ===============================
df_grouped = df_temp[['Team', 'xGpm', 'xGApm']].melt(id_vars='Team', var_name='Metric', value_name='PerMatch')

fig5 = fig2 = px.bar(
    df_grouped,
    x='Team',
    y='PerMatch',
    color='Metric',
    barmode='group',
    title='⚽ EPL 2020/21: xG vs xGA per Match (Grouped)',
    template='plotly_white',
    color_discrete_map={'xGpm': 'crimson', 'xGApm': 'dodgerblue'},
    labels={'PerMatch': 'Per Match Value'}
)

fig5.update_layout(
    xaxis_tickangle=-45,
    height=600
)
st.plotly_chart(fig5, use_container_width=True)


# ===============================
# 3️⃣ Dot Plot (Lollipop Style)
# ===============================
fig5 = fig3 = go.Figure()

for i, row in df_temp.iterrows():
    fig3.add_trace(go.Scatter(
        x=[row['xGApm'], row['xGpm']],
        y=[row['Team'], row['Team']],
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='skip',
        showlegend=False
    ))
    fig3.add_trace(go.Scatter(
        x=[row['xGApm']],
        y=[row['Team']],
        mode='markers',
        marker=dict(color='dodgerblue', size=12),
        name='xGA' if i == 0 else None,
        hovertemplate='Team: %{y}<br>xGA: %{x}<extra></extra>'
    ))
    fig3.add_trace(go.Scatter(
        x=[row['xGpm']],
        y=[row['Team']],
        mode='markers',
        marker=dict(color='crimson', size=12),
        name='xG' if i == 0 else None,
        hovertemplate='Team: %{y}<br>xG: %{x}<extra></extra>'
    ))

fig5.update_layout(
    title="⚽ EPL 2020/21: xG vs xGA per Match (Dot Plot)",
    template="plotly_white",
    xaxis_title="Per Match Value",
    height=800
)

st.plotly_chart(fig5, use_container_width=True)


# plt.figure(figsize=(10,6))
# plt.title("xG Scored Vs xG Conceded")
# sns.scatterplot(data=df_temp, x='xGApm', y='xGpm')
# for i in range(df_temp.shape[0]):
#     plt.text(df_temp.xGApm[i]+0.01, df_temp.xGpm[i]+0.01, 
#              df_temp.Team[i], fontdict={'fontsize':8})
# plt.xlabel("xG conceded Per match")
# plt.ylabel("xG Scored Per match")
# #plt.plot([0,3],[0,3],'r--')
# plt.xlim(df_temp.xGApm.min()-0.2,df_temp.xGApm.max()+0.2)
# plt.ylim(df_temp.xGpm.min()-0.2,df_temp.xGpm.max()+0.2)
# plt.axhline(y=df_temp.xGpm.mean(),ls='--', color='k')
# plt.axvline(x=df_temp.xGApm.mean(),ls='--', color='k')

# plt.text(x=1.6, y=2.25, s="Q1\nStrong Attack\nWeak Defence", 
#          alpha=0.7,fontsize=9, color='red')
# plt.text(x=0.9, y=2.25, s="Q2\nStrong Attack\nStrong Defence", 
#          alpha=0.7,fontsize=9, color='red')
# plt.text(x=0.9, y=0.9, s="Q3\nWeak Attack\nStrong Defence", 
#          alpha=0.7,fontsize=9, color='red')
# plt.text(x=1.6, y=0.9, s="Q3\nWeak Attack\nWeak Defence", 
#          alpha=0.7,fontsize=9, color='red')

# plt.savefig('scatter_xg_xa.png')
# st.plotly_chart(plt use_container_width=True,)


import plotly.graph_objects as go
fig = go.Figure()

# Scatter points
fig.add_trace(go.Scatter(
    x=df_temp["xGApm"],
    y=df_temp["xGpm"],
    mode='markers+text',
    text=df_temp["Team"],
    textposition="top center",
    marker=dict(size=10, color='crimson'),
    name='Teams'
))

# Mean lines
fig.add_shape(type="line",
              x0=df_temp["xGApm"].mean(), x1=df_temp["xGApm"].mean(),
              y0=df_temp["xGpm"].min()-0.2, y1=df_temp["xGpm"].max()+0.2,
              line=dict(dash='dash', color='black'))

fig.add_shape(type="line",
              x0=df_temp["xGApm"].min()-0.2, x1=df_temp["xGApm"].max()+0.2,
              y0=df_temp["xGpm"].mean(), y1=df_temp["xGpm"].mean(),
              line=dict(dash='dash', color='black'))

# Quadrant labels
fig.add_annotation(x=1.6, y=2.25, text="Q1<br>Strong Attack<br>Weak Defence", showarrow=False, font=dict(size=10, color="red"))
fig.add_annotation(x=0.9, y=2.25, text="Q2<br>Strong Attack<br>Strong Defence", showarrow=False, font=dict(size=10, color="red"))
fig.add_annotation(x=0.9, y=0.9, text="Q3<br>Weak Attack<br>Strong Defence", showarrow=False, font=dict(size=10, color="red"))
fig.add_annotation(x=1.6, y=0.9, text="Q4<br>Weak Attack<br>Weak Defence", showarrow=False, font=dict(size=10, color="red"))

# Axis settings
fig.update_layout(
    title="xG Scored vs xG Conceded per Match",
    xaxis_title="xG Conceded per Match",
    yaxis_title="xG Scored per Match",
    xaxis_range=[df_temp["xGApm"].min()-0.2, df_temp["xGApm"].max()+0.2],
    yaxis_range=[df_temp["xGpm"].min()-0.2, df_temp["xGpm"].max()+0.2],
    height=600,
    template="plotly_white"
)

# ✅ Display in Streamlit
st.plotly_chart(fig, use_container_width=True)


import plotly.express as px
import plotly.io as pio

# Sort by delta_xGpm for ranking
df_sorted = df_temp.sort_values(by='delta_xGpm', ascending=False)

# Create interactive horizontal bar chart
fig6 = px.bar(
    df_sorted,
    x='delta_xGpm',
    y='Team',
    orientation='h',
    text='delta_xGpm',
    title='⚽ EPL 2020/21: Delta xG (Scored - Conceded)',
    labels={'delta_xGpm': 'Delta xG per Match', 'Team': 'Team'},
    template='plotly_white',
    color='delta_xGpm',
    color_continuous_scale='RdYlGn'
)

# Customize layout
fig6.update_traces(
    texttemplate='%{x:.2f}',
    textposition='outside'
)
fig6.update_layout(
    xaxis_title='ΔxG per Match',
    yaxis=dict(autorange='reversed'),
    title_font=dict(size=20),
    coloraxis_showscale=False,
    margin=dict(t=60, b=40)
)

# ✅ Show interactive chart

# ✅ Save as PNG (requires kaleido)
st.plotly_chart(fig6, use_container_width=True)

import plotly.graph_objects as go
import plotly.io as pio

# Sort by home xG for consistent ordering
df_temp = df_temp.sort_values(by='xG_h', ascending=False)

# ================================
# 📊 Interactive Horizontal Bar Charts: xG Home vs Away
# ================================
fig7 = go.Figure()

# xG Home
fig7.add_trace(go.Bar(
    x=df_temp['xG_h'],
    y=df_temp['Team'],
    name='xG at Home',
    orientation='h',
    marker=dict(color='firebrick'),
    hovertemplate='Team: %{y}<br>xG at Home: %{x}<extra></extra>'
))

# xG Away
fig7.add_trace(go.Bar(
    x=df_temp['xG_a'],
    y=df_temp['Team'],
    name='xG Away',
    orientation='h',
    marker=dict(color='darkblue'),
    hovertemplate='Team: %{y}<br>xG Away: %{x}<extra></extra>'
))

fig7.update_layout(
    title='⚽ EPL 2020/21: xG Scored per Match — Home vs Away',
    barmode='group',
    yaxis=dict(autorange="reversed"),
    template='plotly_white',
    xaxis_title='xG per Match',
    height=700
)

# ✅ Show interactive chart

# ✅ Save as PNG (optional — requires kaleido)
st.plotly_chart(fig7, use_container_width=True)

import plotly.express as px
import plotly.io as pio

# Sort for visual clarity
df_sorted = df_temp.sort_values(by='delta_xG_ha', ascending=False)

# Create interactive bar chart
fig8 = px.bar(
    df_sorted,
    x='delta_xG_ha',
    y='Team',
    orientation='h',
    title='⚽ EPL 2020/21: xG Difference (Home - Away)',
    labels={'delta_xG_ha': 'ΔxG (Home - Away)', 'Team': 'Team'},
    template='plotly_white',
    text='delta_xG_ha',
    color='delta_xG_ha',
    color_continuous_scale='RdBu'
)

# Beautify the display
fig8.update_traces(
    texttemplate='%{x:.2f}',
    textposition='outside'
)
fig8.update_layout(
    xaxis_title='xG Difference (Home - Away)',
    yaxis=dict(autorange='reversed'),
    coloraxis_showscale=False,
    title_font=dict(size=20),
    margin=dict(t=60, b=40)
)

# Show plot

# Save to PNG
st.plotly_chart(fig8, use_container_width=True)

df['xG_diff'] = df['xG_Home'] - df['xG_Away']
team_xg_diff = df.groupby('Home')['xG_diff'].mean().sort_values(ascending=False).reset_index()

fig9 = px.bar(team_xg_diff, x='Home', y='xG_diff',
             title='📊 Average xG Difference (Home Teams)',
             template='plotly_white')
st.plotly_chart(fig9, use_container_width=True)

import plotly.express as px
stats_df = pd.read_csv("stats.csv")

# Filter only Liverpool data
liverpool_stats = stats_df[stats_df['team'] == 'Liverpool']

# Select relevant columns
liverpool_stats = liverpool_stats[['season', 'total_scoring_att', 'ontarget_scoring_att', 'goals', 'wins']]

# Melt for plotting
liverpool_melted = liverpool_stats.melt(id_vars='season', var_name='Metric', value_name='Value')

# Create interactive line chart
fig10 = px.line(
    liverpool_melted,
    x='season',
    y='Value',
    color='Metric',
    markers=True,
    title='Liverpool Performance by Season: Shots, Shots on Target, Goals, Wins',
    labels={'Value': 'Count', 'season': 'Season'},
    template='plotly_white'
)

# 🔧 Fix layout margins
fig10.update_layout(
    title_font=dict(size=22),
    legend_title_text='Metric',
    margin=dict(l=60, r=60, t=80, b=60)  # Prevent cropping
)

# 📏 Save with larger dimensions

# Show the chart
st.plotly_chart(fig10, use_container_width=True)

import pandas as pd
import plotly.express as px

# Load manager data
managers_df = pd.read_csv("liverpoolfc_managers.csv", sep=';')

# Convert date strings
managers_df['From'] = pd.to_datetime(managers_df['From'])
managers_df['To'] = pd.to_datetime(managers_df['To'])

# Calculate duration
managers_df['Days'] = (managers_df['To'] - managers_df['From']).dt.days
managers_df['Years'] = (managers_df['Days'] / 365).round(1)

# Sort chronologically
managers_df = managers_df.sort_values(by='From')

# Create horizontal bar chart
fig11 = px.bar(
    managers_df,
    x='Years',
    y='Name',
    color='win_perc',
    text='win_perc',
    orientation='h',
    title="🔴 Liverpool Managers: Tenure Duration vs Win %",
    labels={'Years': 'Years in Charge', 'win_perc': 'Win %'},
    color_continuous_scale='RdYlGn',
    template='plotly_white'
)

fig11.update_layout(
    xaxis_title='Years Managed',
    yaxis_title='Manager',
    coloraxis_colorbar=dict(title="Win %"),
    height=700
)

st.plotly_chart(fig11, use_container_width=True)

import pandas as pd
import plotly.express as px

# Load manager data
managers_df = pd.read_csv("liverpoolfc_managers.csv", sep=';')

# Convert date strings
managers_df['From'] = pd.to_datetime(managers_df['From'])
managers_df['To'] = pd.to_datetime(managers_df['To'])

# Calculate duration
managers_df['Days'] = (managers_df['To'] - managers_df['From']).dt.days
managers_df['Years'] = (managers_df['Days'] / 365).round(1)

# Sort by start date
managers_df = managers_df.sort_values(by='From')

# 📈 Plot 1: Win % Over Time
fig123= px.line(
    managers_df,
    x='From',
    y='win_perc',
    text='Name',
    markers=True,
    title='📈 Liverpool Managers Over Time: Win % Trend',
    labels={'From': 'Start Year', 'win_perc': 'Win Percentage'},
    template='plotly_white'
)
fig123.update_traces(textposition='top center', marker=dict(size=10, color='red'))
fig123.update_layout(
    title_font=dict(size=22),
    margin=dict(l=60, r=60, t=80, b=60),
    xaxis_tickformat='%Y',
    xaxis_title='Start Year',
    yaxis_title='Win Percentage (%)',
    hovermode='x unified'
)
st.plotly_chart(fig123, use_container_width=True)


# 🔵 Plot 2: Win % vs Games Managed (Bubble = Tenure)
fig1234 =  px.scatter(
    managers_df,
    x='P',  # Number of games played
    y='win_perc',
    size='Years',
    color='win_perc',
    text='Name',
    title='⚽ Win % vs Games Managed (Bubble = Tenure)',
    labels={'P': 'Games Managed', 'win_perc': 'Win %', 'Years': 'Tenure (Years)'},
    color_continuous_scale='Blues',
    template='plotly_white'
)
fig1234.update_traces(textposition='top center')
fig1234.update_layout(
    title_font=dict(size=22),
    margin=dict(l=60, r=60, t=80, b=60),
    xaxis_title='Games Managed',
    yaxis_title='Win Percentage (%)',
    hovermode='closest'
)
st.plotly_chart(fig1234, use_container_width=True)


# 🥧 Plot 3: Share of Total Matches Managed
fig0 = px.pie(
    managers_df,
    names='Name',
    values='P',
    title='🧩 Games Managed by Each Liverpool Manager',
    template='plotly_white',
    hole=0.3  # Donut style
)
fig0.update_traces(
    textposition='inside',
    textinfo='percent+label',
    pull=[0.05]*len(managers_df)  # Slight pull to enhance visibility
)
fig0.update_layout(
    title_font=dict(size=22),
    margin=dict(l=60, r=60, t=80, b=60)
)
st.plotly_chart(fig0, use_container_width=True)



import pandas as pd
import plotly.express as px

# Load your data
df = pd.read_csv("epl_final.csv")

# Filter only Liverpool matches
liverpool_df = df[(df['HomeTeam'] == 'Liverpool') | (df['AwayTeam'] == 'Liverpool')].copy()

# Determine venue from Liverpool's perspective
liverpool_df['Venue'] = liverpool_df['HomeTeam'].apply(lambda x: 'Home' if x == 'Liverpool' else 'Away')

# Parse match dates and assign COVID periods
liverpool_df['MatchDate'] = pd.to_datetime(liverpool_df['MatchDate'])

def covid_period(date):
    if date < pd.to_datetime('2020-03-01'):
        return 'Pre-COVID'
    elif date <= pd.to_datetime('2021-07-01'):
        return 'During-COVID'
    else:
        return 'Post-COVID'

liverpool_df['CovidPeriod'] = liverpool_df['MatchDate'].apply(covid_period)

# Add match stats from Liverpool's perspective
liverpool_df['Goals'] = liverpool_df.apply(
    lambda row: row['FullTimeHomeGoals'] if row['Venue'] == 'Home' else row['FullTimeAwayGoals'], axis=1)

liverpool_df['GoalsConceded'] = liverpool_df.apply(
    lambda row: row['FullTimeAwayGoals'] if row['Venue'] == 'Home' else row['FullTimeHomeGoals'], axis=1)

liverpool_df['Shots'] = liverpool_df.apply(
    lambda row: row['HomeShots'] if row['Venue'] == 'Home' else row['AwayShots'], axis=1)

liverpool_df['ShotsOnTarget'] = liverpool_df.apply(
    lambda row: row['HomeShotsOnTarget'] if row['Venue'] == 'Home' else row['AwayShotsOnTarget'], axis=1)

liverpool_df['Win'] = liverpool_df.apply(
    lambda row: 1 if row['Goals'] > row['GoalsConceded'] else 0, axis=1)

# Group and summarize
summary = liverpool_df.groupby(['CovidPeriod', 'Venue']).agg({
    'Goals': 'mean',
    'GoalsConceded': 'mean',
    'Shots': 'mean',
    'ShotsOnTarget': 'mean',
    'Win': 'mean'
}).reset_index().rename(columns={'Win': 'WinRate'}).round(2)

# Melt for visualization
melted_summary = summary.melt(
    id_vars=['CovidPeriod', 'Venue'],
    value_vars=['Goals', 'GoalsConceded', 'Shots', 'ShotsOnTarget', 'WinRate'],
    var_name='Metric',
    value_name='Value'
)

# Plot
fig13 = px.bar(
    melted_summary,
    x='CovidPeriod',
    y='Value',
    color='Venue',
    barmode='group',
    facet_col='Metric',
    category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
    title='📊 Liverpool Performance Breakdown by COVID Period and Venue',
    labels={
        'Value': 'Average per Match',
        'CovidPeriod': 'Period',
        'Venue': 'Venue'
    },
    template='plotly_white',
    height=600
)

# Enhanced layout
fig13.update_layout(
    title_font=dict(size=24),
    font=dict(size=13),
    legend_title_text='Venue',
    legend=dict(orientation='h', y=1.15, x=0.3),
    margin=dict(l=60, r=60, t=100, b=60)
)

# Improve annotation readability (clean up facet titles)
fig13.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("WinRate", "Win Rate")))

# Save to file with clear resolution

# Show plot
st.plotly_chart(fig13, use_container_width=True)

import plotly.express as px
import plotly.graph_objects as go

# ----- 1️⃣ Stacked Bar Chart: Goals & Win Rate Together -----
bar_data = summary.melt(
    id_vars=['CovidPeriod', 'Venue'],
    value_vars=['Goals', 'WinRate'],
    var_name='Metric',
    value_name='Value'
)

fig14 = fig1 = px.bar(
    bar_data,
    x='CovidPeriod',
    y='Value',
    color='Venue',
    barmode='group',
    facet_col='Metric',
    category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
    title='📊 Liverpool Goals & Win Rate by COVID Period and Venue',
    labels={'Value': 'Metric Value', 'CovidPeriod': 'Period'},
    template='plotly_white',
    height=500
)

fig14.update_layout(
    title_font=dict(size=22),
    font=dict(size=12),
    legend_title_text='Venue',
    margin=dict(l=60, r=60, t=80, b=60)
)
fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("WinRate", "Win Rate")))

# ----- 2️⃣ Line Chart: Win Rate Trend -----
fig14 = fig2 = px.line(
    summary,
    x='CovidPeriod',
    y='WinRate',
    color='Venue',
    markers=True,
    title='📈 Liverpool Win Rate Trend by Venue',
    labels={'WinRate': 'Win Rate (%)', 'CovidPeriod': 'COVID Period'},
    category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
    template='plotly_white'
)

fig14.update_layout(
    yaxis_tickformat='.0%',
    title_font=dict(size=22),
    font=dict(size=12),
    legend_title_text='Venue',
    margin=dict(l=60, r=60, t=80, b=60)
)

# ----- 3️⃣ Radar Chart: Overall Avg Comparison (Home vs Away) -----
avg_metrics = summary.groupby('Venue')[['Goals', 'GoalsConceded', 'Shots', 'ShotsOnTarget', 'WinRate']].mean().reset_index()

fig14 = fig3 = go.Figure()

for _, row in avg_metrics.iterrows():
    fig3.add_trace(go.Scatterpolar(
        r=row[1:].values,
        theta=avg_metrics.columns[1:],
        fill='toself',
        name=row['Venue'],
        line=dict(width=2)
    ))

fig14.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, max(avg_metrics.iloc[:, 1:].max()) * 1.2])
    ),
    title='🛡️ Overall Performance Radar: Home vs Away',
    template='plotly_white',
    title_font=dict(size=22),
    font=dict(size=12),
    margin=dict(l=60, r=60, t=80, b=60)
)
st.plotly_chart(fig14, use_container_width=True)




team_performance = pd.read_csv("team_performance.csv")
print(team_performance.columns)


df_copy = pd.read_csv("EPL_result.csv")
df_copy["FullTimeResult"] = df_copy.apply(
    lambda row: "H" if row["G_Home"] > row["G_Away"]
    else "A" if row["G_Home"] < row["G_Away"]
    else "D",
    axis=1
)

df_copy["AwayLoss"] = df_copy["FullTimeResult"] == "H"
df_copy["HomeLoss"] = df_copy["FullTimeResult"] == "A"

away_stats = df_copy.groupby("Away")[["AwayLoss"]].sum()
home_stats = df_copy.groupby("Home")[["HomeLoss"]].sum()

away_stats.columns = ["AwayLoss"]
home_stats.columns = ["HomeLoss"]

team_performance_l = pd.concat([home_stats, away_stats], axis=1).fillna(0)
team_performance_l = pd.concat([home_stats, away_stats], axis=1).fillna(0)

# ✅ Now this will work correctly
top_10_by_home_loss = team_performance_l.sort_values("HomeLoss", ascending=False).tail(10)
st.dataframe(top_10_by_home_loss[["HomeLoss", "AwayLoss"]])

# Plot
ax = top_10_by_home_loss[["HomeLoss", "AwayLoss"]].plot(
    kind="bar", colormap="seismic", figsize=(12, 6)
)

# Add labels
for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='edge', fontsize=9)

plt.title("Top 10 EPL Teams by Home Loss (with Away Loss for Comparison)")
plt.ylabel("Number of Losses")
plt.xlabel("Team")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

top_10_by_home_draws = team_performance.sort_values("HomeDraws", ascending=False).head(10)

# # Plot Away vs. Home Draws for those teams
top_10_by_home_draws[["HomeDraws", "AwayDraws"]].plot(
    kind="bar", figsize=(12, 6), colormap="seismic"
)
plt.title("Top 10 EPL Teams by Home Draws (with Away Draws for Comparison)")
plt.ylabel("Number of Draws")
plt.xlabel("Team")
plt.xticks(rotation=45)
plt.legend(["HomeDraws", "AwayDraws"])
plt.tight_layout()
st.pyplot(plt)



# Top 10 teams by Home Loss
top_10_by_home_loss = team_performance_l.sort_values("HomeLoss", ascending=False).tail(25)
# Plot Away vs. Home Loss for those teams
top_10_by_home_loss[["HomeLoss", "AwayLoss"]].plot(
    kind="bar", figsize=(12, 6), colormap="seismic"
)
plt.title("Top 10 EPL Teams by Home Loss (with Away Loss for Comparison)")
plt.ylabel("Number of Losses")
plt.xlabel("Team")
plt.xticks(rotation=45)
plt.legend(["HomeLoss", "AwayLoss"])
plt.tight_layout()
st.pyplot(plt)

team_name = "Liverpool"

df_copy["FullTimeResult"] = df_copy.apply(
    lambda row: "H" if row["G_Home"] > row["G_Away"]
    else ("A" if row["G_Home"] < row["G_Away"] else "D"),
    axis=1
)

df_copy["TeamLoss"] = (
    ((df_copy["Home"] == team_name) & (df_copy["FullTimeResult"] == "A")) |
    ((df_copy["Away"] == team_name) & (df_copy["FullTimeResult"] == "H"))
).astype(int)

team_losses_by_gw = (
    df_copy.groupby("GW")["TeamLoss"].sum().sort_values(ascending=False)
)

# Plot
team_losses_by_gw.head(10).plot(kind="bar", figsize=(12, 6), colormap="seismic")
plt.title("Top 10 Gameweeks by Losses for Liverpool")
plt.ylabel("Number of Losses")
plt.xlabel("Gameweek")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Top 10 teams by average home goals
# Calculate average home and away goals per match
teams = df_copy['Home'].unique()
avg_goals = pd.DataFrame({'Team': teams})

avg_goals['AvgHomeGoals'] = avg_goals['Team'].apply(
    lambda x: df_copy[df_copy['Home'] == x]['G_Home'].mean()
)
avg_goals['AvgAwayGoals'] = avg_goals['Team'].apply(
    lambda x: df_copy[df_copy['Away'] == x]['G_Away'].mean()
)

avg_goals.set_index('Team', inplace=True)

top_10_avg_goals = avg_goals.sort_values("AvgHomeGoals", ascending=False).head(10)

# Plot
top_10_avg_goals.plot(kind="bar", figsize=(12, 6), colormap="seismic")
plt.title("Top 10 Teams by Average Home Goals (with Away Goals for Comparison)")
plt.ylabel("Average Goals per Match")
plt.xlabel("Team")
plt.xticks(rotation=45)
plt.legend(["Home Goals", "Away Goals"])
plt.tight_layout()
st.pyplot(plt)

# Calculate halftime lead conversions for all teams
team_analysis = df[
    df["HalfTimeResult"].isin(["H", "A"])  # Only matches with a clear HT leader
].copy()

# Determine if lead was held
team_analysis["LeadHeld"] = (
    (
        (team_analysis["HalfTimeResult"] == "H") & (team_analysis["FullTimeResult"] == "H")
    ) |
    (
        (team_analysis["HalfTimeResult"] == "A") & (team_analysis["FullTimeResult"] == "A")
    )
).astype(int)

# Identify leading team (home if H, away if A)
team_analysis["LeadingTeam"] = team_analysis.apply(
    lambda row: row["HomeTeam"] if row["HalfTimeResult"] == "H" else row["AwayTeam"], axis=1
)

# Group by leading team and calculate conversion rate
team_conversion = team_analysis.groupby("LeadingTeam")["LeadHeld"].agg(["sum", "count"])
team_conversion["ConversionRate"] = (team_conversion["sum"] / team_conversion["count"]) * 100
# Top 10 teams by conversion rate
top_10 = team_conversion.sort_values("ConversionRate", ascending=False).head(10)

# Plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.bar(top_10.index, top_10["ConversionRate"], color='red')
plt.title("Top 10 Teams – Halftime Lead to Full-time Win Conversion")
plt.ylabel("Conversion Rate (%)")
plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.tight_layout()
st.pyplot(plt)


# Ensure 'ComebackWin' is created properly on team_analysis
team_analysis["ComebackWin"] = (
    (
        (team_analysis["HalfTimeResult"] == "A") & (team_analysis["FullTimeResult"] == "H")
    ) |
    (
        (team_analysis["HalfTimeResult"] == "H") & (team_analysis["FullTimeResult"] == "A")
    )
).astype(int)

# Group by team and compute remontada stats correctly
remontada_stats = team_analysis.groupby("LeadingTeam").agg(
    ComebackWins=('ComebackWin', 'sum'),
    TotalOpportunities=('ComebackWin', 'count')
).reset_index()

# Calculate comeback rate
remontada_stats["RemontadaRate"] = (remontada_stats["ComebackWins"] / remontada_stats["TotalOpportunities"]) * 100

# Sort and pick top 5
top_remontadas = remontada_stats.sort_values("RemontadaRate", ascending=False).tail(10)

# ✅ Plot Top 5 Teams by Comeback Rate
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.bar(top_remontadas["LeadingTeam"], top_remontadas["RemontadaRate"], color='green')
plt.title("Least 5 Teams by Comeback Win Rate (Remontadas)")
plt.ylabel("Comeback Win Rate (%)")
plt.xlabel("Team")
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)
# Filter Liverpool matches where they were leading at halftime (home or away)
liverpool_leads = team_analysis[
    (
        ((team_analysis["HalfTimeResult"] == "H") & (team_analysis["HomeTeam"] == "Liverpool")) |
        ((team_analysis["HalfTimeResult"] == "A") & (team_analysis["AwayTeam"] == "Liverpool"))
    )
]

# Group by Season to compute sum and total
liverpool_season_conversion = liverpool_leads.groupby("Season")["LeadHeld"].agg(["sum", "count"])
liverpool_season_conversion["ConversionRate"] = (
    liverpool_season_conversion["sum"] / liverpool_season_conversion["count"]
) * 100

# Plot
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(
    liverpool_season_conversion.index,
    liverpool_season_conversion["ConversionRate"],
    marker="o",
    color="crimson"
)

plt.title("Liverpool – Halftime Leads Converted to Wins Over Seasons")
plt.ylabel("Conversion Rate (%)")
plt.xlabel("Season")
plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# 3. Is the League Becoming More Attack-Oriented Over Time?
df_copy = df.copy() 

# Calculate match-level features
df_copy["TotalGoals"] = df_copy["FullTimeHomeGoals"] + df_copy["FullTimeAwayGoals"]
df_copy["TotalShots"] = df_copy["HomeShots"] + df_copy["AwayShots"]
df_copy["WinMargin"] = abs(df_copy["FullTimeHomeGoals"] - df_copy["FullTimeAwayGoals"])

# Step 2: Group by Season and calculate average
attack_trend = df_copy.groupby("Season")[
    ["TotalGoals", "TotalShots", "WinMargin"]
].mean()
attack_trend = attack_trend.sort_index()

plt.figure(figsize=(12, 6))

# Goals trend
plt.plot(
    attack_trend.index, attack_trend["TotalGoals"], marker="o", label="Goals per Match"
)

# Shots trend
plt.plot(
    attack_trend.index, attack_trend["TotalShots"], marker="s", label="Shots per Match"
)

# Win Margin trend
plt.plot(attack_trend.index, attack_trend["WinMargin"], marker="^", label="Win Margin")

plt.title("Is the League Becoming More Attack-Oriented Over Time?")
plt.xlabel("Season")
plt.ylabel("Average per Match")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

import matplotlib.pyplot as plt

# Step 1: Filter only Liverpool games (home or away)
liverpool_only = df[
    (df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")
].copy()

# Step 2: Calculate match-level metrics
liverpool_only["TotalGoals"] = liverpool_only["FullTimeHomeGoals"] + liverpool_only["FullTimeAwayGoals"]
liverpool_only["TotalShots"] = liverpool_only["HomeShots"] + liverpool_only["AwayShots"]
liverpool_only["WinMargin"] = abs(liverpool_only["FullTimeHomeGoals"] - liverpool_only["FullTimeAwayGoals"])

# Step 3: Group by season and calculate mean trends
liverpool_trend = liverpool_only.groupby("Season")[["TotalGoals", "TotalShots", "WinMargin"]].mean()
liverpool_trend = liverpool_trend.sort_index()

# Step 4: Plot
plt.figure(figsize=(12, 6))
plt.plot(liverpool_trend.index, liverpool_trend["TotalGoals"], marker="o", label="Goals per Match", color="red")
plt.plot(liverpool_trend.index, liverpool_trend["TotalShots"], marker="s", label="Shots per Match", color="blue")
plt.plot(liverpool_trend.index, liverpool_trend["WinMargin"], marker="^", label="Win Margin", color="green")

plt.title("Is Liverpool Becoming More Attack-Oriented Over Time?")
plt.xlabel("Season")
plt.ylabel("Average per Match")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset (update filename if needed)
df = pd.read_csv("epl_final.csv")

# Step 1: Filter only Liverpool games (home or away)
liverpool_only = df[
    (df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")
].copy()

# Step 2: Add 'Venue' column
liverpool_only["Venue"] = liverpool_only["HomeTeam"].apply(lambda x: "Home" if x == "Liverpool" else "Away")

# Step 3: Calculate match-level metrics
liverpool_only["TotalGoals"] = liverpool_only["FullTimeHomeGoals"] + liverpool_only["FullTimeAwayGoals"]
liverpool_only["TotalShots"] = liverpool_only["HomeShots"] + liverpool_only["AwayShots"]
liverpool_only["WinMargin"] = abs(liverpool_only["FullTimeHomeGoals"] - liverpool_only["FullTimeAwayGoals"])

# Step 4: Group by Season and Venue
grouped = liverpool_only.groupby(["Season", "Venue"])[["TotalGoals", "TotalShots", "WinMargin"]].mean().reset_index()

# Step 5: Pivot to prepare for plotting
pivot_goals = grouped.pivot(index="Season", columns="Venue", values="TotalGoals")
pivot_shots = grouped.pivot(index="Season", columns="Venue", values="TotalShots")
pivot_margin = grouped.pivot(index="Season", columns="Venue", values="WinMargin")

# Step 6: Plotting
fig, ax = plt.subplots(3, 1, figsize=(12, 15), sharex=True)

# Total Goals
pivot_goals.plot(ax=ax[0], marker='o')
ax[0].set_title("Liverpool - Average Total Goals per Match (Home vs Away)")
ax[0].set_ylabel("Goals per Match")
ax[0].grid(True)

# Total Shots
pivot_shots.plot(ax=ax[1], marker='s')
ax[1].set_title("Liverpool - Average Total Shots per Match (Home vs Away)")
ax[1].set_ylabel("Shots per Match")
ax[1].grid(True)

# Win Margin
pivot_margin.plot(ax=ax[2], marker='^')
ax[2].set_title("Liverpool - Average Win Margin per Match (Home vs Away)")
ax[2].set_ylabel("Win Margin")
ax[2].set_xlabel("Season")
ax[2].grid(True)

plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Calculate shot conversion rate (%)
attack_trend["ShotConversion"] = (
    attack_trend["TotalGoals"] / attack_trend["TotalShots"]
) * 100

plt.figure(figsize=(16, 6))
plt.plot(
    attack_trend.index,
    attack_trend["ShotConversion"],
    marker="o",
    color="purple",
    label="Shot Conversion Rate (%)",
)

plt.axhline(
    attack_trend["ShotConversion"].mean(), color="gray", linestyle="--", label="Average"
)

max_season = attack_trend["ShotConversion"].idxmax()
max_val = attack_trend["ShotConversion"].max()

min_season = attack_trend["ShotConversion"].idxmin()
min_val = attack_trend["ShotConversion"].min()

plt.annotate(
    f"Highest: {max_val:.1f}%",
    xy=(max_season, max_val),
    xytext=(max_season, max_val + 1.5),
    arrowprops=dict(arrowstyle="->", color="green"),
    fontsize=10,
)

plt.annotate(
    f"lowest: {min_val:.1f}%",
    xy=(min_season, min_val),
    xytext=(min_season, min_val + 1.5),
    arrowprops=dict(arrowstyle="->", color="red"),
    fontsize=10,
)

# Final plot settings
plt.title("Shot Conversion Rate Over Seasons")
plt.ylabel("Conversion Rate (%)")
plt.xlabel("Season")
plt.xticks(rotation=45)
plt.ylim(0, attack_trend["ShotConversion"].max() + 5)
plt.grid(True)
plt.legend()
plt.tight_layout()
st.pyplot(plt)
import pandas as pd
import matplotlib.pyplot as plt

# Load your data (update file name if needed)
df = pd.read_csv("epl_final.csv")

# Step 1: Filter only Liverpool matches
liverpool_df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()

# Step 2: Calculate total goals and shots per match
liverpool_df["TotalGoals"] = liverpool_df["FullTimeHomeGoals"] + liverpool_df["FullTimeAwayGoals"]
liverpool_df["TotalShots"] = liverpool_df["HomeShots"] + liverpool_df["AwayShots"]

# Step 3: Group by Season and calculate averages
attack_trend = liverpool_df.groupby("Season")[["TotalGoals", "TotalShots"]].mean()

# Step 4: Calculate shot conversion rate (%)
attack_trend["ShotConversion"] = (attack_trend["TotalGoals"] / attack_trend["TotalShots"]) * 100

# Step 5: Plot
plt.figure(figsize=(16, 6))
plt.plot(
    attack_trend.index,
    attack_trend["ShotConversion"],
    marker="o",
    color="purple",
    label="Shot Conversion Rate (%)",
)

# Add average line
plt.axhline(
    attack_trend["ShotConversion"].mean(), color="gray", linestyle="--", label="Average"
)

# Highlight best and worst seasons
max_season = attack_trend["ShotConversion"].idxmax()
max_val = attack_trend["ShotConversion"].max()

min_season = attack_trend["ShotConversion"].idxmin()
min_val = attack_trend["ShotConversion"].min()

plt.annotate(
    f"Highest: {max_val:.1f}%",
    xy=(max_season, max_val),
    xytext=(max_season, max_val + 1.5),
    arrowprops=dict(arrowstyle="->", color="green"),
    fontsize=10,
)

plt.annotate(
    f"Lowest: {min_val:.1f}%",
    xy=(min_season, min_val),
    xytext=(min_season, min_val + 1.5),
    arrowprops=dict(arrowstyle="->", color="red"),
    fontsize=10,
)

# Final plot settings
plt.title("Liverpool Shot Conversion Rate Over Seasons")
plt.ylabel("Conversion Rate (%)")
plt.xlabel("Season")
plt.xticks(rotation=45)
plt.ylim(0, attack_trend["ShotConversion"].max() + 5)
plt.grid(True)
plt.legend()
plt.tight_layout()
st.pyplot(plt)

# 4. Are matches becoming more physical, as measured by fouls and cards?
df_copy = df.copy()

df_copy["TotalFouls"] = df_copy["HomeFouls"] + df_copy["AwayFouls"]
df_copy["TotalYellowCards"] = df_copy["HomeYellowCards"] + df_copy["AwayYellowCards"]
df_copy["TotalRedCards"] = df_copy["HomeRedCards"] + df_copy["AwayRedCards"]

physical_trends = df_copy.groupby("Season")[
    ["TotalFouls", "TotalYellowCards", "TotalRedCards"]
].mean()

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True)

metrics = ["TotalFouls", "TotalYellowCards", "TotalRedCards"]
colors = ["#1f77b4", "#ff7f0e", "#d62728"]
titles = ["Fouls per Match", "Yellow Cards per Match", "Red Cards per Match"]

for i, ax in enumerate(axes):
    ax.plot(
        physical_trends.index, physical_trends[metrics[i]], marker="o", color=colors[i]
    )
    ax.set_title(titles[i], fontsize=12)
    ax.set_ylabel("Average per Match")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_xticks(range(len(physical_trends.index)))
    ax.set_xticklabels(physical_trends.index, rotation=45, ha="right", fontsize=9)

fig.suptitle("Physicality in the League Over Time", fontsize=16, fontweight="bold")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv("epl_final.csv")

# Step 1: Filter Liverpool matches
liverpool_df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()

# Step 2: Create physicality-related columns
liverpool_df["TotalFouls"] = liverpool_df["HomeFouls"] + liverpool_df["AwayFouls"]
liverpool_df["TotalYellowCards"] = liverpool_df["HomeYellowCards"] + liverpool_df["AwayYellowCards"]
liverpool_df["TotalRedCards"] = liverpool_df["HomeRedCards"] + liverpool_df["AwayRedCards"]

# Step 3: Group by season and calculate average per match
physical_trends = liverpool_df.groupby("Season")[["TotalFouls", "TotalYellowCards", "TotalRedCards"]].mean()

# Step 4: Plot
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True)

metrics = ["TotalFouls", "TotalYellowCards", "TotalRedCards"]
colors = ["#1f77b4", "#ff7f0e", "#d62728"]
titles = ["Fouls per Match", "Yellow Cards per Match", "Red Cards per Match"]

for i, ax in enumerate(axes):
    ax.plot(
        physical_trends.index, physical_trends[metrics[i]], marker="o", color=colors[i]
    )
    ax.set_title(titles[i], fontsize=12)
    ax.set_ylabel("Average per Match")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_xticks(range(len(physical_trends.index)))
    ax.set_xticklabels(physical_trends.index, rotation=45, ha="right", fontsize=9)

fig.suptitle("Liverpool Physicality Trends Over Time", fontsize=16, fontweight="bold")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
st.pyplot(plt)

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv("epl_final.csv")

# Filter Liverpool games
liverpool_df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()

# Define Venue
liverpool_df["Venue"] = liverpool_df["HomeTeam"].apply(lambda x: "Home" if x == "Liverpool" else "Away")

# Goals For/Against and Match Result
liverpool_df["GoalsFor"] = liverpool_df.apply(
    lambda row: row["FullTimeHomeGoals"] if row["Venue"] == "Home" else row["FullTimeAwayGoals"], axis=1)
liverpool_df["GoalsAgainst"] = liverpool_df.apply(
    lambda row: row["FullTimeAwayGoals"] if row["Venue"] == "Home" else row["FullTimeHomeGoals"], axis=1)
liverpool_df["Result"] = liverpool_df.apply(
    lambda row: "Win" if row["GoalsFor"] > row["GoalsAgainst"] else
    ("Loss" if row["GoalsFor"] < row["GoalsAgainst"] else "Draw"), axis=1
)

# Physical stats
liverpool_df["Fouls"] = liverpool_df["HomeFouls"] + liverpool_df["AwayFouls"]
liverpool_df["YellowCards"] = liverpool_df["HomeYellowCards"] + liverpool_df["AwayYellowCards"]
liverpool_df["RedCards"] = liverpool_df["HomeRedCards"] + liverpool_df["AwayRedCards"]

# Melt for comparison
melt_df = liverpool_df.melt(
    id_vars=["Season", "Venue", "Result"],
    value_vars=["Fouls", "YellowCards", "RedCards"],
    var_name="Metric",
    value_name="Value"
)

# === Individual detailed plot for each metric ===
for metric in ["Fouls", "YellowCards", "RedCards"]:
    g = sns.catplot(
        data=melt_df[melt_df["Metric"] == metric],
        x="Season", y="Value", hue="Result", col="Venue",
        kind="bar", height=5, aspect=1.4, palette="muted", errorbar=None
    )
    g.set_titles("{col_name} Venue")
    g.set_axis_labels("Season", f"{metric} per Match")
    g.set_xticklabels(rotation=45)
    g.fig.subplots_adjust(top=0.85)
    g.fig.suptitle(f"Liverpool: {metric} by Result (Home vs Away)", fontsize=16)
    st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data (replace with your actual DataFrame if already loaded)
df_copy = pd.read_csv("epl_final.csv")

# Home discipline
home_cards = df_copy.groupby("HomeTeam").agg(
    HomeYellows=("HomeYellowCards", "sum"),
    HomeReds=("HomeRedCards", "sum"),
    HomeFouls=("HomeFouls", "sum"),
    HomeGames=("HomeTeam", "count")
)

# Away discipline
away_cards = df_copy.groupby("AwayTeam").agg(
    AwayYellows=("AwayYellowCards", "sum"),
    AwayReds=("AwayRedCards", "sum"),
    AwayFouls=("AwayFouls", "sum"),
    AwayGames=("AwayTeam", "count")
)

# Combine home and away stats
discipline = home_cards.join(away_cards, how="inner")
discipline.index.name = "Team"

# Total cards
discipline["Cards_Home"] = discipline["HomeYellows"] + discipline["HomeReds"]
discipline["Cards_Away"] = discipline["AwayYellows"] + discipline["AwayReds"]

# Per game card rate
discipline["CardsPerGame_Home"] = discipline["Cards_Home"] / discipline["HomeGames"]
discipline["CardsPerGame_Away"] = discipline["Cards_Away"] / discipline["AwayGames"]

# Aggression delta
discipline["AggressionDelta"] = discipline["CardsPerGame_Away"] - discipline["CardsPerGame_Home"]

# Sort
delta_sorted = discipline.sort_values("AggressionDelta", ascending=False)

# Plot
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")
colors = ["red" if x > 0 else "blue" for x in delta_sorted["AggressionDelta"]]

sns.barplot(
    x=delta_sorted["AggressionDelta"],
    y=delta_sorted.index,
    palette=colors
)

plt.axvline(0, color="black", linestyle="--")
plt.title("↕️ Aggression Delta: Away - Home Cards per Game", fontsize=16)
plt.xlabel("Difference (Away - Home)")
plt.ylabel("Team")
plt.tight_layout()
st.pyplot(plt)

df_reds = df.copy()

# Flags
df_reds["HomeRed"] = df_reds["HomeRedCards"] > 0
df_reds["AwayRed"] = df_reds["AwayRedCards"] > 0

# Who got the red card
df_reds["RedCardTeam"] = df_reds.apply(
    lambda row: (
        "Home Team" if row["HomeRed"] else "Away Team" if row["AwayRed"] else "No Red"
    ),
    axis=1,
)


# Final outcome for the red card team
def red_card_outcome(row):
    if row["RedCardTeam"] == "Home Team":
        if row["FullTimeResult"] == "H":
            return "Win"
        elif row["FullTimeResult"] == "D":
            return "Draw"
        else:
            return "Loss"
    elif row["RedCardTeam"] == "Away Team":
        if row["FullTimeResult"] == "A":
            return "Win"
        elif row["FullTimeResult"] == "D":
            return "Draw"
        else:
            return "Loss"
    else:
        return None


df_reds["RedCardOutcome"] = df_reds.apply(red_card_outcome, axis=1)

# Filter only matches with red cards
df_with_red = df_reds[df_reds["RedCardTeam"] != "No Red"]
 #Add percent for each red card team category
summary = (
    df_with_red.groupby(["RedCardTeam", "RedCardOutcome"])
    .size()
    .reset_index(name="MatchCount")
)

summary["Percentage"] = (
    summary["MatchCount"]
    / summary.groupby("RedCardTeam")["MatchCount"].transform("sum")
    * 100
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=summary,
    x="RedCardOutcome",
    y="Percentage",
    hue="RedCardTeam",
    palette=["#5B47EF", "#118AB2"],
)

plt.title("Match Outcomes After a Red Card", fontsize=14)
plt.ylabel("Percentage of Matches")
plt.xlabel("Outcome for the Team That Got the Red Card")
plt.ylim(0, 100)
plt.legend(title="Team That Got the Red Card")
plt.grid(axis="y", linestyle="--", alpha=0.3)
st.pyplot(plt)

# Annotate bars
for i in range(len(summary)):
    row = summary.iloc[i]
    plt.text(
        x=i % 3 - 0.15 + (0.3 if row["RedCardTeam"] == "Away Team" else 0),
        y=row["Percentage"] + 1,
        s=f"{row['Percentage']:.1f}%",
        fontsize=9,
    )

plt.tight_layout()
st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("epl_final.csv")

# Filter Liverpool matches
df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()

# Flag red cards
df["HomeRed"] = df["HomeRedCards"] > 0
df["AwayRed"] = df["AwayRedCards"] > 0

# Who got the red card
df["RedCardTo"] = df.apply(
    lambda row: (
        "Liverpool" if (row["HomeTeam"] == "Liverpool" and row["HomeRed"]) or 
                      (row["AwayTeam"] == "Liverpool" and row["AwayRed"])
        else "Opponent" if row["HomeRed"] or row["AwayRed"] else "No Red"
    ),
    axis=1,
)

# Determine if Liverpool won
def lfc_result(row):
    if row["HomeTeam"] == "Liverpool":
        return "Win" if row["FullTimeResult"] == "H" else "Loss" if row["FullTimeResult"] == "A" else "Draw"
    else:
        return "Win" if row["FullTimeResult"] == "A" else "Loss" if row["FullTimeResult"] == "H" else "Draw"

df["LiverpoolResult"] = df.apply(lfc_result, axis=1)

# Only games with red cards
df_red_only = df[df["RedCardTo"] != "No Red"]

# Aggregate
summary = df_red_only.groupby(["RedCardTo", "LiverpoolResult"]).size().reset_index(name="MatchCount")

# Percentage
summary["Percentage"] = (
    summary["MatchCount"] /
    summary.groupby("RedCardTo")["MatchCount"].transform("sum")
) * 100

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=summary, x="LiverpoolResult", y="Percentage", hue="RedCardTo", palette=["#EF476F", "#06D6A0"])
plt.title("Who Wins When a Red Card is Given? (Liverpool Matches)", fontsize=14)
plt.ylabel("Percentage of Matches")
plt.xlabel("Liverpool Match Outcome")
plt.ylim(0, 100)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.legend(title="Red Card Given To")
st.pyplot(plt)

# Annotate
for i in range(len(summary)):
    row = summary.iloc[i]
    x = i % 3 + (-0.2 if row["RedCardTo"] == "Liverpool" else 0.1)
    plt.text(x, row["Percentage"] + 1, f"{row['Percentage']:.1f}%", fontsize=9)

plt.tight_layout()

# Values for away red card outcome
labels = ["Loss", "Draw", "Win"]
sizes = [62.3, 26.6, 11.1]
colors = ["#930828", "#FFD166", "#06D65D"]

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
plt.title("Away Team Outcomes After Receiving a Red Card")
plt.tight_layout()
st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("epl_final.csv")

# Filter only Liverpool matches
df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()

# Flags for red cards
df["HomeRed"] = df["HomeRedCards"] > 0
df["AwayRed"] = df["AwayRedCards"] > 0

# Did Liverpool get the red?
df["RedToLFC"] = df.apply(
    lambda row: (
        (row["HomeTeam"] == "Liverpool" and row["HomeRed"]) or
        (row["AwayTeam"] == "Liverpool" and row["AwayRed"])
    ),
    axis=1
)

# Only matches where Liverpool got a red
lfc_red = df[df["RedToLFC"]]

# Determine Liverpool result
def get_result(row):
    if row["HomeTeam"] == "Liverpool":
        return "Win" if row["FullTimeResult"] == "H" else "Loss" if row["FullTimeResult"] == "A" else "Draw"
    else:
        return "Win" if row["FullTimeResult"] == "A" else "Loss" if row["FullTimeResult"] == "H" else "Draw"

lfc_red["LiverpoolResult"] = lfc_red.apply(get_result, axis=1)

# Count results
result_counts = lfc_red["LiverpoolResult"].value_counts().reindex(["Loss", "Draw", "Win"]).fillna(0)
labels = result_counts.index.tolist()
sizes = result_counts.values
colors = ["#930828", "#FFD166", "#06D65D"]

# Pie chart
plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
plt.title("Liverpool Outcomes After Receiving a Red Card")
plt.tight_layout()
st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("epl_final.csv")

# Filter Liverpool matches
df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()

# Flag red cards for Liverpool at Home and Away
df["LFC_HomeRed"] = (df["HomeTeam"] == "Liverpool") & (df["HomeRedCards"] > 0)
df["LFC_AwayRed"] = (df["AwayTeam"] == "Liverpool") & (df["AwayRedCards"] > 0)

# Combine for unified flag
df["LFC_RedCardVenue"] = df.apply(
    lambda row: "Home" if row["LFC_HomeRed"]
    else "Away" if row["LFC_AwayRed"]
    else None,
    axis=1
)

# Filter only red-card matches for Liverpool
lfc_reds = df[df["LFC_RedCardVenue"].notnull()].copy()

# Define match outcome for Liverpool
def get_result(row):
    if row["HomeTeam"] == "Liverpool":
        return "Win" if row["FullTimeResult"] == "H" else "Loss" if row["FullTimeResult"] == "A" else "Draw"
    else:
        return "Win" if row["FullTimeResult"] == "A" else "Loss" if row["FullTimeResult"] == "H" else "Draw"

lfc_reds["LiverpoolResult"] = lfc_reds.apply(get_result, axis=1)

# Set up plots
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

colors = ["#930828", "#FFD166", "#06D65D"]
labels = ["Loss", "Draw", "Win"]

for i, venue in enumerate(["Home", "Away"]):
    subset = lfc_reds[lfc_reds["LFC_RedCardVenue"] == venue]
    counts = subset["LiverpoolResult"].value_counts().reindex(labels).fillna(0)
    axes[i].pie(
        counts,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140
    )
    axes[i].set_title(f"Liverpool Outcomes After Red Card ({venue})")

plt.suptitle(" Liverpool Match Outcomes After Receiving a Red Card — Home vs Away", fontsize=14)
plt.tight_layout()
st.pyplot(plt)
# Export red card match outcomes to CSV
lfc_reds[["Season", "LFC_RedCardVenue", "LiverpoolResult"]].to_csv("liverpool_red_card_outcomes.csv", index=False)
# ✅ Load the dataset
# df_copy = pd.read_csv("EPL_result.csv")

# # 🔍 Inspect the columns
# print(df_copy.columns.tolist())

# # Now continue with your logic
# # Example:
# home_def = df_copy.groupby("Home")[["G_Away"]].sum()
# away_def = df_copy.groupby("Away")[["G_Home"]].sum()
# Which teams are the most defensively efficient (conceding few goals per shot faced)?
# Calculate shots faced and goals conceded per team
# Use actual column names that exist

# home_def = df_copy.groupby("HomeTeam")[["G_Away"]].sum().rename(columns={"G_Away": "GoalsConceded_Home"})
# away_def = df_copy.groupby("AwayTeam")[["G_Home"]].sum().rename(columns={"G_Home": "GoalsConceded_Away"})

# # Total goals conceded = goals conceded at home + away
# team_def = home_def.join(away_def, how="outer").fillna(0)
# team_def["TotalGoalsConceded"] = team_def["GoalsConceded_Home"] + team_def["GoalsConceded_Away"]

# # Estimate total shots faced per team
# home_shots_faced = df_copy.groupby("Home")[["xG_Away"]].count().rename(columns={"xG_Away": "ShotsFaced_Home"})
# away_shots_faced = df_copy.groupby("Away")[["xG_Home"]].count().rename(columns={"xG_Home": "ShotsFaced_Away"})

# team_def = team_def.join(home_shots_faced).join(away_shots_faced)
# team_def["TotalShotsFaced"] = team_def["ShotsFaced_Home"] + team_def["ShotsFaced_Away"]

# # Defensive efficiency: goals conceded per shot faced
# team_def["ConcededPerShot"] = team_def["TotalGoalsConceded"] / team_def["TotalShotsFaced"]

# defensive_ranking = team_def.sort_values("ConcededPerShot",ascending=False)
# Defensive stats calculation using correct column names
# Load the dataset
df_copy = pd.read_csv("EPL_result.csv")

# Optional: View the columns to verify
print(df_copy.columns.tolist())

# Group and sum goals conceded
home_def = df_copy.groupby("Home")[["G_Away"]].sum().rename(columns={"G_Away": "GoalsConceded_Home"})
away_def = df_copy.groupby("Away")[["G_Home"]].sum().rename(columns={"G_Home": "GoalsConceded_Away"})

# Merge both into one DataFrame
team_def = pd.concat([home_def, away_def], axis=1)

# Calculate shots faced
home_shots_faced = df_copy.groupby("Home")[["xG_Away"]].sum()
away_shots_faced = df_copy.groupby("Away")[["xG_Home"]].sum()

team_def["ShotsFaced"] = (home_shots_faced["xG_Away"] + away_shots_faced["xG_Home"])
team_def["GoalsConceded"] = team_def["GoalsConceded_Home"] + team_def["GoalsConceded_Away"]
team_def["ConcededPerShot"] = team_def["GoalsConceded"] / team_def["ShotsFaced"]

# Sort defensively weakest
defensive_ranking = team_def.sort_values("ConcededPerShot", ascending=False)

# Print or plot
st.subheader("Defensive Efficiency (Goals Conceded per xG Faced)")
st.dataframe(defensive_ranking)
# Plot
st.subheader("🔴 Worst Defensive Teams by Goals Conceded per xG Faced")
plt.figure(figsize=(12, 6))
plt.bar(defensive_ranking.index, defensive_ranking["ConcededPerShot"], color='darkred')
plt.xticks(rotation=45)
plt.ylabel("Goals Conceded per xG Faced")
plt.title("Worst Defensive Teams in EPL")
plt.tight_layout()

st.pyplot(plt)

# plt.figure(figsize=(14, 6))
# sns.barplot(
#     x=defensive_ranking["ConcededPerShot"].head(30),
#     y=defensive_ranking.head(30).index,
#     palette="crest",
# )
# plt.title("Best Defensive Teams (Goals Conceded per Shot Faced)")
# plt.xlabel("Goals Conceded per Shot Faced")
# plt.ylabel("Team")
# plt.grid(axis="x", linestyle="--", alpha=0.4)
# plt.tight_layout()

# Which teams draw the most matches? Are there consistent "draw kings"?

# Count draws at home and away
def get_result(row):
    if row["G_Home"] > row["G_Away"]:
        return "H"
    elif row["G_Home"] < row["G_Away"]:
        return "A"
    else:
        return "D"

df_copy["FullTimeResult"] = df_copy.apply(get_result, axis=1)



df_copy["IsDraw"] = df_copy["FullTimeResult"] == "D"
draws = (
    df_copy.groupby("Home")["IsDraw"].sum()
    + df_copy.groupby("Away")["IsDraw"].sum()
)
draws = draws.sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=draws.head(10).values, y=draws.head(10).index, palette="Blues_d")
plt.title("Top 10 Teams with Most Draws")
plt.xlabel("Number of Draws")
plt.ylabel("Team")
plt.tight_layout()
st.pyplot(plt)

# Teams Analysis
df_copy = df.copy()

# 1. Define wins
df_copy["HomeWin"] = (df_copy["FullTimeResult"] == "H").astype(int)
df_copy["AwayWin"] = (df_copy["FullTimeResult"] == "A").astype(int)

# 2. Group home stats
home_stats = df_copy.groupby("HomeTeam").agg(
    Goals_Home=("FullTimeHomeGoals", "sum"),
    Shots_Home=("HomeShots", "sum"),
    ShotsOnTarget_Home=("HomeShotsOnTarget", "sum"),
    Fouls_Home=("HomeFouls", "sum"),
    Yellow_Home=("HomeYellowCards", "sum"),
    Red_Home=("HomeRedCards", "sum"),
    Wins_Home=("HomeWin", "sum"),
    Games_Home=("HomeWin", "count"),
)

# 3. Group away stats
away_stats = df_copy.groupby("AwayTeam").agg(
    Goals_Away=("FullTimeAwayGoals", "sum"),
    Shots_Away=("AwayShots", "sum"),
    ShotsOnTarget_Away=("AwayShotsOnTarget", "sum"),
    Fouls_Away=("AwayFouls", "sum"),
    Yellow_Away=("AwayYellowCards", "sum"),
    Red_Away=("AwayRedCards", "sum"),
    Wins_Away=("AwayWin", "sum"),
    Games_Away=("AwayWin", "count"),
)

# 4. Merge and calculate totals
teamStatistics = home_stats.add(away_stats, fill_value=0)
teamStatistics.index.name = "Team"

# 5. Derived columns
teamStatistics["Goals"] = teamStatistics["Goals_Home"] + teamStatistics["Goals_Away"]
teamStatistics["Shots"] = teamStatistics["Shots_Home"] + teamStatistics["Shots_Away"]
teamStatistics["ShotsOnTarget"] = (
    teamStatistics["ShotsOnTarget_Home"] + teamStatistics["ShotsOnTarget_Away"]
)
teamStatistics["Fouls"] = teamStatistics["Fouls_Home"] + teamStatistics["Fouls_Away"]
teamStatistics["Cards"] = (
    teamStatistics["Yellow_Home"]
    + teamStatistics["Red_Home"]
    + teamStatistics["Yellow_Away"]
    + teamStatistics["Red_Away"]
)
teamStatistics["Wins"] = teamStatistics["Wins_Home"] + teamStatistics["Wins_Away"]
teamStatistics["Games"] = teamStatistics["Games_Home"] + teamStatistics["Games_Away"]

# 6. Efficiency & Accuracy ratios
teamStatistics["Goal/ST"] = teamStatistics["Goals"] / teamStatistics["ShotsOnTarget"]
teamStatistics["Wins/Games"] = teamStatistics["Wins"] / teamStatistics["Games"]
teamStatistics["Cards/Fouls"] = teamStatistics["Cards"] / teamStatistics["Fouls"]

# 7. Clean up
teamStatistics = teamStatistics.reset_index()[
    ["Team", "Goal/ST", "Wins/Games", "Cards/Fouls"] + list(teamStatistics.columns)
    ]
teamStatistics = teamStatistics.loc[:, ~teamStatistics.columns.duplicated()]


# Sort by accuracy
goal_on_shots = teamStatistics.sort_values(by="Goal/ST", ascending=False)

plt.figure(figsize=(14, 10))
sns.barplot(data=goal_on_shots, x="Goal/ST", y="Team", palette="Blues_r")

plt.title("Most Accurate Teams (Goals per Shot on Target)")
plt.xlabel("Conversion Rate")
plt.ylabel("Team")
plt.xlim(0, goal_on_shots["Goal/ST"].max() * 1.1)
plt.gca().xaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f"{x:.1%}")
)  # Percent format
plt.tight_layout()
st.pyplot(plt)

wins_on_games = teamStatistics.sort_values(by="Wins/Games", ascending=False)

plt.figure(figsize=(14, 10))
sns.barplot(data=wins_on_games, x="Wins/Games", y="Team", palette="Greens_r")

plt.title("Most Efficient Teams (Win Ratio)")
plt.xlabel("Win Ratio")
plt.ylabel("Team")
plt.xlim(0, wins_on_games["Wins/Games"].max() * 1.1)
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
plt.tight_layout()
st.pyplot(plt)



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("epl_final.csv")
print(df_copy.columns.tolist())
print(df.head())              # See sample data
   # See actual column names



# Filter Liverpool matches
lfc_df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()

# Add Venue column
lfc_df["Venue"] = lfc_df["HomeTeam"].apply(lambda x: "Home" if x == "Liverpool" else "Away")

# Determine match result from Liverpool's perspective
def get_result(row):
    if row["HomeTeam"] == "Liverpool":
        return "Win" if row["FullTimeResult"] == "H" else "Draw" if row["FullTimeResult"] == "D" else "Loss"
    else:
        return "Win" if row["FullTimeResult"] == "A" else "Draw" if row["FullTimeResult"] == "D" else "Loss"

lfc_df["Result"] = lfc_df.apply(get_result, axis=1)

# Calculate win ratios for each venue
venue_stats = lfc_df.groupby("Venue")["Result"].value_counts().unstack().fillna(0)
venue_stats["Total"] = venue_stats.sum(axis=1)
venue_stats["Win Ratio"] = venue_stats["Win"] / venue_stats["Total"]

# Prepare for plot
venue_stats_reset = venue_stats.reset_index()

# Plot
plt.figure(figsize=(8, 5))
sns.barplot(data=venue_stats_reset, x="Win Ratio", y="Venue", palette="Greens_r")

plt.title("Liverpool Win Ratio by Venue (Home vs Away)")
plt.xlabel("Win Ratio")
plt.ylabel("Venue")
plt.xlim(0, 1)
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
plt.tight_layout()
st.pyplot(plt)

cards_on_fouls = teamStatistics.sort_values(by="Cards/Fouls", ascending=False)

plt.figure(figsize=(14,10))
sns.barplot(data=cards_on_fouls, x="Cards/Fouls", y="Team", palette="Reds_r")

plt.title("Most Aggressive Teams (Cards per Foul)")
plt.xlabel("Aggression Ratio")
plt.ylabel("Team")
plt.xlim(0, cards_on_fouls["Cards/Fouls"].max() * 1.1)
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.1%}"))
plt.tight_layout()
st.pyplot(plt)



#import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Filter Liverpool matches (home or away)
liverpool_matches = df_copy[
    (df_copy["HomeTeam"] == "Liverpool") | (df_copy["AwayTeam"] == "Liverpool")
].copy()

# Parse dates safely
liverpool_matches["MatchDate"] = pd.to_datetime(liverpool_matches["MatchDate"], errors="coerce")

# Keep only 2019 and 2020 matches
liverpool_matches = liverpool_matches[
    liverpool_matches["MatchDate"].dt.year.isin([2019, 2020])
].sort_values("MatchDate")

# Compute Liverpool and Opponent goals
liverpool_matches["Liverpool Goals"] = liverpool_matches.apply(
    lambda row: row["FullTimeHomeGoals"] if row["HomeTeam"] == "Liverpool" else row["FullTimeAwayGoals"],
    axis=1
)

liverpool_matches["Opponent Goals"] = liverpool_matches.apply(
    lambda row: row["FullTimeAwayGoals"] if row["HomeTeam"] == "Liverpool" else row["FullTimeHomeGoals"],
    axis=1
)

# Plot
plt.figure(figsize=(14, 5))
plt.plot(
    liverpool_matches["MatchDate"], liverpool_matches["Liverpool Goals"],
    label="Liverpool Goals", marker="o", linestyle="-"
)
plt.plot(
    liverpool_matches["MatchDate"], liverpool_matches["Opponent Goals"],
    label="Opponent Goals", marker="x", linestyle="--"
)
plt.title("Liverpool Goals vs Opponent Goals (2019–2020)")
plt.xlabel("Match Date")
plt.ylabel("Goals")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)





# Filter Liverpool shots
liverpool_shots = pd.read_csv("shots_EPL_1920.csv")

# Filter only Liverpool shots (home team = Liverpool)
liverpool_shots = liverpool_shots[liverpool_shots["h_team"] == "Liverpool"]

# Filter only goals
liverpool_goals = liverpool_shots[liverpool_shots["result"] == "Goal"]

# Top 10 scorers
top_scorers = liverpool_goals.groupby("player")["result"].count().sort_values(ascending=False).head(10)

# Top 10 assist providers
top_assists = liverpool_shots[liverpool_shots["player_assisted"].notna()]\
    .groupby("player_assisted")["id"].count().sort_values(ascending=False).head(10)


fig, axs = plt.subplots(1, 2, figsize=(16, 5))
sns.barplot(x=top_scorers.values, y=top_scorers.index, ax=axs[0])
axs[0].set_title("Top Liverpool Scorers")
axs[0].set_xlabel("Goals")

sns.barplot(x=top_assists.values, y=top_assists.index, ax=axs[1])
axs[1].set_title("Top Liverpool Assist Providers")
axs[1].set_xlabel("Assists")

plt.tight_layout()
st.pyplot(plt)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data and filter by year
liverpool_shots = pd.read_csv("shots_EPL_1920.csv")
liverpool_shots["date"] = pd.to_datetime(liverpool_shots["date"], errors="coerce")
liverpool_shots = liverpool_shots[liverpool_shots["date"].dt.year.isin([2019, 2020])]

# ✅ Filter: Only shots taken by Liverpool
# Check if Liverpool is either home or away AND that the shot was taken by that side
liverpool_shots = liverpool_shots[
    ((liverpool_shots["h_team"] == "Liverpool") & (liverpool_shots["h_a"] == "h")) |
    ((liverpool_shots["a_team"] == "Liverpool") & (liverpool_shots["h_a"] == "a"))
].copy()

# ✅ Add Venue column
liverpool_shots["Venue"] = liverpool_shots["h_a"].apply(lambda x: "Home" if x == "h" else "Away")

# ✅ Add isGoal column
liverpool_shots["isGoal"] = liverpool_shots["result"] == "Goal"

# ✅ Plot
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
for ax, title in zip(axes, ["Home", "Away"]):
    subset = liverpool_shots[liverpool_shots["Venue"] == title]
    sns.scatterplot(data=subset, x="X", y="Y", hue="isGoal", palette={True: "green", False: "red"}, ax=ax, s=30)
    ax.set_title(f"Liverpool Shot Map ({title})")
    ax.set_xlim(0.7, 1.05)
    ax.set_ylim(0.2, 0.9)
    ax.set_xlabel("Normalized X (Goal Right)")
    ax.set_ylabel("Normalized Y (Pitch Height)")
    ax.set_aspect('equal')
    ax.invert_yaxis()

plt.tight_layout()
st.pyplot(fig)


# ==== 2. Shot Type Bar Chart ====
plt.figure(figsize=(12, 6))
shot_types = liverpool_shots.groupby(["Venue", "shotType"])["id"].count().unstack().fillna(0)
shot_types.T.plot(kind='bar')
plt.title("Liverpool Shot Types: Home vs Away")
plt.ylabel("Number of Shots")
plt.tight_layout()
st.pyplot(plt)

# ==== 3. Shot Situations Bar Chart ====
plt.figure(figsize=(12, 6))
situations = liverpool_shots.groupby(["Venue", "situation"])["id"].count().unstack().fillna(0)
situations.T.plot(kind='bar')
plt.title("Shot Situations: Home vs Away")
plt.ylabel("Number of Shots")
plt.tight_layout()
st.pyplot(plt)

home_xg = liverpool_shots[liverpool_shots["Venue"] == "Home"].groupby("player")["xG"].sum().sort_values(ascending=False).head(5)
away_xg = liverpool_shots[liverpool_shots["Venue"] == "Away"].groupby("player")["xG"].sum().sort_values(ascending=False).head(5)

fig, axs = plt.subplots(1, 2, figsize=(16, 5))
sns.barplot(x=home_xg.values, y=home_xg.index, ax=axs[0])
axs[0].set_title("Top xG Contributors (Home)")
axs[0].set_xlabel("xG")

sns.barplot(x=away_xg.values, y=away_xg.index, ax=axs[1])
axs[1].set_title("Top xG Contributors (Away)")
axs[1].set_xlabel("xG")

plt.tight_layout()
st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
shots = pd.read_csv("shots_EPL_1920.csv")

# Filter Liverpool shots
liverpool_shots = shots[(shots["h_team"] == "Liverpool") | (shots["a_team"] == "Liverpool")].copy()

# Add Venue column
liverpool_shots["Venue"] = liverpool_shots.apply(
    lambda row: "Home" if row["h_team"] == "Liverpool" else "Away", axis=1
)

# Plotting heatmaps
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

for ax, venue in zip(axes, ["Home", "Away"]):
    subset = liverpool_shots[liverpool_shots["Venue"] == venue]
    sns.kdeplot(
        data=subset,
        x="X",
        y="Y",
        fill=True,
        thresh=0,
        levels=100,
        cmap="Reds",
        ax=ax
    )
    ax.set_title(f"Liverpool Shot Density – {venue} Matches")
    ax.set_xlim(0.7, 1.05)
    ax.set_ylim(0.2, 0.9)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_xlabel("Normalized X (Goal on the Right)")
    ax.set_ylabel("Normalized Y (Pitch Height)")

plt.tight_layout()
st.pyplot(plt)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load shot data
shots = pd.read_csv("shots_EPL_1920.csv")

# Filter Liverpool shots
liverpool_shots = shots[(shots["h_team"] == "Liverpool") | (shots["a_team"] == "Liverpool")].copy()

# Add 'Venue' column
liverpool_shots["Venue"] = liverpool_shots.apply(
    lambda row: "Home" if row["h_team"] == "Liverpool" else "Away", axis=1
)

# Filter for Salah and Firmino
key_players = ["Mohamed Salah", "Roberto Firmino"]
player_shots = liverpool_shots[liverpool_shots["player"].isin(key_players)]

# Plot: 2x2 grid (Home vs Away for each player)
fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharex=True, sharey=True)

for i, player in enumerate(key_players):
    for j, venue in enumerate(["Home", "Away"]):
        subset = player_shots[(player_shots["player"] == player) & (player_shots["Venue"] == venue)]
        ax = axes[i][j]
        sns.kdeplot(
            data=subset,
            x="X",
            y="Y",
            fill=True,
            thresh=0,
            levels=100,
            cmap="Reds",
            ax=ax
        )
        ax.set_title(f"{player} – {venue} Matches", fontsize=12)
        ax.set_xlim(0.7, 1.05)
        ax.set_ylim(0.2, 0.9)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.set_xlabel("Normalized X")
        ax.set_ylabel("Normalized Y")

plt.suptitle("Shot Density Heatmap: Mohamed Salah vs Roberto Firmino (Home & Away)", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(plt)


