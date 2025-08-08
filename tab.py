import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- PAGE CONFIG & LOGO ----------
st.set_page_config(page_title="Liverpool FC Dashboard", layout="wide")
# logo = Image.open("liverpool_logo.png")
# st.sidebar.image(logo, width=100)
st.sidebar.title("Liverpool FC Dashboard")
st.sidebar.markdown("Interactive Match Analysis (2015–2023)")

# ---------- THEME TOGGLE ----------
theme = st.sidebar.radio("🎨 Select Theme", ["Light", "Dark"], index=0)
plotly_template = "seaborn" if theme == "Light" else "plotly_dark"

# ---------- DATA PREPARATION ----------
df = pd.read_csv('Liverpool_2015_2023_Matches.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)

def get_result(row):
    if row['Venue'] == 'Home':
        return 'Win' if row['HomeGoals'] > row['AwayGoals'] else 'Draw' if row['HomeGoals'] == row['AwayGoals'] else 'Loss'
    else:
        return 'Win' if row['AwayGoals'] > row['HomeGoals'] else 'Draw' if row['AwayGoals'] == row['HomeGoals'] else 'Loss'
df['Result'] = df.apply(get_result, axis=1)

def covid_period(date):
    if date < pd.to_datetime('2020-03-01'):
        return 'Pre-COVID'
    elif date < pd.to_datetime('2021-07-01'):
        return 'During COVID'
    else:
        return 'Post-COVID'
df['CovidPeriod'] = df['Date'].apply(covid_period)

# ---------- TABS ----------
tab1, tab2, tab3, tab4,tab5,tab6,tab7,tab8,tab9= st.tabs(["📊 Venue Win Stats", "🦠 COVID Period Breakdown", "📈 Timeline & Goals", "📊 EPL xG Comparison,","🕰️ Club Trends & Manager Era","📊 Team Momentum & Conversion","🔥 Attacking Trends","🛡️ Physicality & Discipline","🏆 Liverpool's 2019 & 2020 Title-Winning Performance"])

# ================= TAB 1 =================
with tab1:
    st.subheader("🏠 Liverpool Venue Win Summary (2015–2023)")
    summary = df.groupby('Venue').agg(
        Total_Matches=('Result', 'count'),
        Wins=('Result', lambda x: (x == 'Win').sum())
    ).reset_index()
    summary['Win_Percentage'] = (summary['Wins'] / summary['Total_Matches'] * 100).round(1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔴 Wins by Venue")
        fig1 = px.bar(summary, x='Venue', y='Wins', text='Wins', color='Venue',
                      color_discrete_map={'Home': 'red', 'Away': 'green'},
                      template=plotly_template)
        fig1.update_traces(textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("#### 🔵 Matches vs Wins (Grouped)")
        summary_melted = summary.melt(id_vars='Venue', value_vars=['Total_Matches', 'Wins'])
        fig2 = px.bar(summary_melted, x='Venue', y='value', color='variable',
                      barmode='group', text='value', template=plotly_template,
                      color_discrete_map={'Total_Matches': 'royalblue', 'Wins': 'crimson'})
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

# ================= TAB 2 =================
with tab2:
    st.subheader("🦠 COVID Period Match Outcomes")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Result Stack by COVID Period")
        summary = df.groupby(['CovidPeriod', 'Venue', 'Result']).size().reset_index(name='Count')
        summary['Result_Grouped'] = summary['Result'].apply(lambda x: 'Wins' if x == 'Win' else 'Other')
        stacked = summary.groupby(['CovidPeriod', 'Venue', 'Result_Grouped'])['Count'].sum().reset_index()

        fig3 = px.bar(stacked, x='Venue', y='Count', color='Result_Grouped',
                      facet_col='CovidPeriod', barmode='stack',
                      color_discrete_map={'Wins': '#D7263D', 'Other': '#7F7F7F'},
                      template=plotly_template)
        fig3.update_traces(marker_line_width=1.5, marker_line_color='white', textposition='inside')
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown("#### ⚖️ Result % Breakdown")
        outcome = df.groupby(['Venue', 'Result']).size().reset_index(name='Count')
        outcome['Percent'] = outcome['Count'] / outcome.groupby('Venue')['Count'].transform('sum') * 100

        fig4 = px.bar(outcome, x='Venue', y='Percent', color='Result', text=outcome['Percent'].round(1),
                      barmode='stack', template=plotly_template)
        st.plotly_chart(fig4, use_container_width=True)

# ================= TAB 3 =================
with tab3:
    st.subheader("📈 Timeline & Goal Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ⏳ Wins Over Time")
        df['Year'] = df['Date'].dt.year
        wins_time = df[df['Result'] == 'Win'].groupby(['Year', 'Venue']).size().reset_index(name='Wins')
        fig5 = px.line(wins_time, x='Year', y='Wins', color='Venue', markers=True,
                       color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
                       template=plotly_template)
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        st.markdown("#### 🎯 Goals per Match")
        df['GoalsFor'] = df.apply(lambda row: row['HomeGoals'] if row['Venue'] == 'Home' else row['AwayGoals'], axis=1)
        fig6 = px.box(df, x='Venue', y='GoalsFor', points='all',
                      color='Venue',
                      color_discrete_map={'Home': '#FF4136', 'Away': '#2ECC40'},
                      template=plotly_template)
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("#### 🧬 COVID Period Result Breakdown")
    covid_outcome = df.groupby(['CovidPeriod', 'Venue', 'Result']).size().reset_index(name='Count')
    fig7 = px.bar(covid_outcome, x='Venue', y='Count', color='Result', barmode='stack',
                  facet_col='CovidPeriod',
                  color_discrete_sequence=px.colors.qualitative.Bold,
                  template=plotly_template)
    st.plotly_chart(fig7, use_container_width=True)
# ✅ Liverpool Dashboard with Light/Dark Theme + EPL xG Comparison Tab



# ================= TAB 4 =================
# ✅ Liverpool Dashboard with Light/Dark Theme + EPL xG Comparison Tab

# ================= TAB 4 =================
with tab4:
    st.subheader("📊 EPL 2020/21 xG Comparison")
    df_raw = pd.read_csv("EPL_result.csv")
    home_stats = df_raw.groupby('Home').agg(
        Avg_xG_Home=('xG_Home', 'mean'),
        Avg_G_Home=('G_Home', 'mean')
    ).reset_index()
    home_stats_melted = home_stats.melt(
        id_vars='Home',
        value_vars=['Avg_xG_Home', 'Avg_G_Home'],
        var_name='Metric',
        value_name='Goals'
    )
    home_stats_melted['Highlight'] = home_stats_melted['Home'].apply(lambda x: 'Liverpool' if x == 'Liverpool' else 'Other')
    fig44 = px.bar(
        home_stats_melted,
        x='Home',
        y='Goals',
        color='Metric',
        barmode='group',
        text='Goals',
        title='⚽ Average Home xG vs Actual Goals per Team (Highlight: Liverpool)',
        template=plotly_template,
        color_discrete_map={
            'Avg_xG_Home': '#1f77b4',
            'Avg_G_Home': '#d62728'
        }
    )
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
    home_stats_melted.sort_values(by='Goals', ascending=False, inplace=True)
    st.plotly_chart(fig44, use_container_width=True)
    df = pd.read_csv("EPL_result.csv")
    team_abb = { 'Everton': 'EVE', 'Aston Villa': 'AVL', 'Leicester City': 'LEI', 'Arsenal': 'ARS', 'Liverpool': 'LIV', 'Tottenham': 'TOT',
        'Chelsea': 'CHE', 'Leeds United': 'LEE', 'Newcastle Utd': 'NEW', 'West Ham': 'WHU', 'Southampton': 'SOU', 'Crystal Palace': 'CRY',
        'Wolves': 'WOL', 'Manchester City': 'MCI', 'Brighton': 'BHA', 'Manchester Utd': 'MUN', 'West Brom': 'WBA', 'Burnley': 'BUR',
        'Sheffield Utd': 'SHU', 'Fulham': 'FUL' }

    df['Home'] = df['Home'].map(team_abb)
    df['Away'] = df['Away'].map(team_abb)
    df['GD'] = df['G_Home'] - df['G_Away']
    df['Pts_Home'] = df['GD'].apply(lambda x: 3 if x > 0 else 1 if x == 0 else 0)
    df['Pts_Away'] = df['GD'].apply(lambda x: 0 if x > 0 else 1 if x == 0 else 3)

    gw_last = 7
    gw_next = gw_last + 1
    df_temp = pd.DataFrame({'Team': list(team_abb.values())})
    df_temp['M_h'] = df_temp['Team'].apply(lambda x: df[(df['Home'] == x) & (df['GW'] < gw_next)].shape[0])
    df_temp['M_a'] = df_temp['Team'].apply(lambda x: df[(df['Away'] == x) & (df['GW'] < gw_next)].shape[0])
    df_temp['M'] = df_temp['M_h'] + df_temp['M_a']
    df_temp['xG_h'] = df_temp['Team'].apply(lambda x: df[(df['Home'] == x) & (df['GW'] < gw_next)]['xG_Home'].sum())
    df_temp['xG_a'] = df_temp['Team'].apply(lambda x: df[(df['Away'] == x) & (df['GW'] < gw_next)]['xG_Away'].sum())
    df_temp['xGA_h'] = df_temp['Team'].apply(lambda x: df[(df['Home'] == x) & (df['GW'] < gw_next)]['xG_Away'].sum())
    df_temp['xGA_a'] = df_temp['Team'].apply(lambda x: df[(df['Away'] == x) & (df['GW'] < gw_next)]['xG_Home'].sum())

    df_temp['xGA'] = df_temp['xGA_h'] + df_temp['xGA_a']
    df_temp['xGApm'] = df_temp['xGA'] / df_temp['M']
    df_temp['xG'] = df_temp['xG_h'] + df_temp['xG_a']
    df_temp['xGpm'] = df_temp['xG'] / df_temp['M']
    df_temp['delta_xGpm'] = df_temp['xGpm'] - df_temp['xGApm']
    df_temp['delta_xG_ha'] = df_temp['xG_h'] - df_temp['xG_a']
    df_temp = df_temp.sort_values(by='xGpm', ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔼 xG vs xGA per Match")
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=df_temp['xGpm'], y=df_temp['Team'], name='xG per Match', orientation='h', marker=dict(color='crimson')))
        fig1.add_trace(go.Bar(x=df_temp['xGApm'], y=df_temp['Team'], name='xGA per Match', orientation='h', marker=dict(color='dodgerblue')))
        fig1.update_layout(template=plotly_template, barmode='group', yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("#### 🔹 Grouped Vertical Chart")
        df_grouped = df_temp[['Team', 'xGpm', 'xGApm']].melt(id_vars='Team', var_name='Metric', value_name='PerMatch')
        fig2 = px.bar(df_grouped, x='Team', y='PerMatch', color='Metric', barmode='group',
                      color_discrete_map={'xGpm': 'crimson', 'xGApm': 'dodgerblue'},
                      template=plotly_template)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 🔺 Dot Plot")
        fig3 = go.Figure()
        for i, row in df_temp.iterrows():
            fig3.add_trace(go.Scatter(x=[row['xGApm'], row['xGpm']], y=[row['Team'], row['Team']], mode='lines', line=dict(color='gray')))
            fig3.add_trace(go.Scatter(x=[row['xGApm']], y=[row['Team']], mode='markers', marker=dict(color='dodgerblue', size=12)))
            fig3.add_trace(go.Scatter(x=[row['xGpm']], y=[row['Team']], mode='markers', marker=dict(color='crimson', size=12)))
        fig3.update_layout(template=plotly_template)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### 🔢 Quadrant Scatter")
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=df_temp["xGApm"], y=df_temp["xGpm"], mode='markers+text', text=df_temp["Team"], textposition="top center", marker=dict(size=10, color='crimson')))
        fig4.add_shape(type="line", x0=df_temp["xGApm"].mean(), x1=df_temp["xGApm"].mean(), y0=df_temp["xGpm"].min()-0.2, y1=df_temp["xGpm"].max()+0.2, line=dict(dash='dash'))
        fig4.add_shape(type="line", x0=df_temp["xGApm"].min()-0.2, x1=df_temp["xGApm"].max()+0.2, y0=df_temp["xGpm"].mean(), y1=df_temp["xGpm"].mean(), line=dict(dash='dash'))
        fig4.update_layout(template=plotly_template)
        st.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("#### 🔢 Delta xG per Match")
        df_sorted = df_temp.sort_values(by='delta_xGpm', ascending=False)
        fig5 = px.bar(df_sorted, x='delta_xGpm', y='Team', orientation='h', template=plotly_template, color='delta_xGpm', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown("#### 🏡 xG Home vs Away")
        df_temp = df_temp.sort_values(by='xG_h', ascending=False)
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(x=df_temp['xG_h'], y=df_temp['Team'], name='xG at Home', orientation='h', marker=dict(color='firebrick')))
        fig6.add_trace(go.Bar(x=df_temp['xG_a'], y=df_temp['Team'], name='xG Away', orientation='h', marker=dict(color='darkblue')))
        fig6.update_layout(template=plotly_template, barmode='group', yaxis=dict(autorange='reversed'))
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("#### 🌐 xG Difference (Home - Away)")
    df_sorted = df_temp.sort_values(by='delta_xG_ha', ascending=False)
    fig7 = px.bar(df_sorted, x='delta_xG_ha', y='Team', orientation='h', template=plotly_template, color='delta_xG_ha', color_continuous_scale='RdBu')
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("#### 🔢 Avg xG Diff by Home Team")
    df['xG_diff'] = df['xG_Home'] - df['xG_Away']
    team_xg_diff = df.groupby('Home')['xG_diff'].mean().sort_values(ascending=False).reset_index()
    fig8 = px.bar(team_xg_diff, x='Home', y='xG_diff', template=plotly_template)
    st.plotly_chart(fig8, use_container_width=True)
with tab5:
    st.subheader("🕰️ Club Trends & Manager Era")

    col1, col2 = st.columns(2)
    with col1:
        stats_df = pd.read_csv("stats.csv")
        liverpool_stats = stats_df[stats_df['team'] == 'Liverpool']
        liverpool_stats = liverpool_stats[['season', 'total_scoring_att', 'ontarget_scoring_att', 'goals', 'wins']]
        liverpool_melted = liverpool_stats.melt(id_vars='season', var_name='Metric', value_name='Value')
        fig10 = px.line(
            liverpool_melted,
            x='season',
            y='Value',
            color='Metric',
            markers=True,
            title='Liverpool Performance by Season: Shots, Shots on Target, Goals, Wins',
            labels={'Value': 'Count', 'season': 'Season'},
            template=plotly_template
        )
        fig10.update_layout(title_font=dict(size=22), legend_title_text='Metric', margin=dict(l=60, r=60, t=80, b=60))
        st.plotly_chart(fig10, use_container_width=True)

    with col2:
        managers_df = pd.read_csv("liverpoolfc_managers.csv", sep=';')
        managers_df['From'] = pd.to_datetime(managers_df['From'])
        managers_df['To'] = pd.to_datetime(managers_df['To'])
        managers_df['Days'] = (managers_df['To'] - managers_df['From']).dt.days
        managers_df['Years'] = (managers_df['Days'] / 365).round(1)
        managers_df = managers_df.sort_values(by='From')

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
            template=plotly_template
        )
        fig11.update_layout(
            xaxis_title='Years Managed',
            yaxis_title='Manager',
            coloraxis_colorbar=dict(title="Win %"),
            height=700
        )
        st.plotly_chart(fig11, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig123 = px.line(
            managers_df,
            x='From',
            y='win_perc',
            text='Name',
            markers=True,
            title='📈 Liverpool Managers Over Time: Win % Trend',
            labels={'From': 'Start Year', 'win_perc': 'Win Percentage'},
            template=plotly_template
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

    with col4:
        fig1234 = px.scatter(
            managers_df,
            x='P',
            y='win_perc',
            size='Years',
            color='win_perc',
            text='Name',
            title='⚽ Win % vs Games Managed (Bubble = Tenure)',
            labels={'P': 'Games Managed', 'win_perc': 'Win %', 'Years': 'Tenure (Years)'},
            color_continuous_scale='Blues',
            template=plotly_template
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

    fig0 = px.pie(
        managers_df,
        names='Name',
        values='P',
        title='🧩 Games Managed by Each Liverpool Manager',
        template=plotly_template,
        hole=0.3
    )
    fig0.update_traces(
        textposition='inside',
        textinfo='percent+label',
        pull=[0.05]*len(managers_df)
    )
    fig0.update_layout(
        title_font=dict(size=22),
        margin=dict(l=60, r=60, t=80, b=60)
    )
    st.plotly_chart(fig0, use_container_width=True)

    # ----- COVID Period Analysis & Radar Chart -----
    df = pd.read_csv("epl_final.csv")
    liverpool_df = df[(df['HomeTeam'] == 'Liverpool') | (df['AwayTeam'] == 'Liverpool')].copy()
    liverpool_df['Venue'] = liverpool_df['HomeTeam'].apply(lambda x: 'Home' if x == 'Liverpool' else 'Away')
    liverpool_df['MatchDate'] = pd.to_datetime(liverpool_df['MatchDate'])

    def covid_period(date):
        if date < pd.to_datetime('2020-03-01'):
            return 'Pre-COVID'
        elif date <= pd.to_datetime('2021-07-01'):
            return 'During-COVID'
        else:
            return 'Post-COVID'

    liverpool_df['CovidPeriod'] = liverpool_df['MatchDate'].apply(covid_period)
    liverpool_df['Goals'] = liverpool_df.apply(lambda row: row['FullTimeHomeGoals'] if row['Venue'] == 'Home' else row['FullTimeAwayGoals'], axis=1)
    liverpool_df['GoalsConceded'] = liverpool_df.apply(lambda row: row['FullTimeAwayGoals'] if row['Venue'] == 'Home' else row['FullTimeHomeGoals'], axis=1)
    liverpool_df['Shots'] = liverpool_df.apply(lambda row: row['HomeShots'] if row['Venue'] == 'Home' else row['AwayShots'], axis=1)
    liverpool_df['ShotsOnTarget'] = liverpool_df.apply(lambda row: row['HomeShotsOnTarget'] if row['Venue'] == 'Home' else row['AwayShotsOnTarget'], axis=1)
    liverpool_df['Win'] = liverpool_df.apply(lambda row: 1 if row['Goals'] > row['GoalsConceded'] else 0, axis=1)

    summary = liverpool_df.groupby(['CovidPeriod', 'Venue']).agg({
        'Goals': 'mean',
        'GoalsConceded': 'mean',
        'Shots': 'mean',
        'ShotsOnTarget': 'mean',
        'Win': 'mean'
    }).reset_index().rename(columns={'Win': 'WinRate'}).round(2)

    melted_summary = summary.melt(
        id_vars=['CovidPeriod', 'Venue'],
        value_vars=['Goals', 'GoalsConceded', 'Shots', 'ShotsOnTarget', 'WinRate'],
        var_name='Metric',
        value_name='Value'
    )

    col5, col6 = st.columns(2)
    with col5:
        fig13 = px.bar(
            melted_summary,
            x='CovidPeriod',
            y='Value',
            color='Venue',
            barmode='group',
            facet_col='Metric',
            category_orders={'CovidPeriod': ['Pre-COVID', 'During-COVID', 'Post-COVID']},
            title='📊 Performance Breakdown by COVID Period',
            labels={'Value': 'Avg per Match', 'CovidPeriod': 'Period', 'Venue': 'Venue'},
            template=plotly_template,
            height=600
        )
        fig13.update_layout(
            title_font=dict(size=24),
            font=dict(size=13),
            legend_title_text='Venue',
            legend=dict(orientation='h', y=1.15, x=0.3),
            margin=dict(l=60, r=60, t=100, b=60)
        )
        fig13.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("WinRate", "Win Rate")))
        st.plotly_chart(fig13, use_container_width=True)

    with col6:
        avg_metrics = summary.groupby('Venue')[['Goals', 'GoalsConceded', 'Shots', 'ShotsOnTarget', 'WinRate']].mean().reset_index()
        fig14 = go.Figure()
        for _, row in avg_metrics.iterrows():
            fig14.add_trace(go.Scatterpolar(
                r=row[1:].values,
                theta=avg_metrics.columns[1:],
                fill='toself',
                name=row['Venue'],
                line=dict(width=2)
            ))
        fig14.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max(avg_metrics.iloc[:, 1:].max()) * 1.2])),
            title='🛡️ Radar Chart: Avg Metrics Home vs Away',
            template=plotly_template,
            title_font=dict(size=22),
            margin=dict(l=60, r=60, t=80, b=60)
        )
        st.plotly_chart(fig14, use_container_width=True)



with tab6:
    st.subheader("📊 Team Momentum & Conversion")

    df_copy = pd.read_csv("EPL_result.csv")
    df_copy["FullTimeResult"] = df_copy.apply(
        lambda row: "H" if row["G_Home"] > row["G_Away"]
        else "A" if row["G_Home"] < row["G_Away"]
        else "D",
        axis=1
    )
    df_copy["AwayLoss"] = df_copy["FullTimeResult"] == "H"
    df_copy["HomeLoss"] = df_copy["FullTimeResult"] == "A"

    away_stats = df_copy.groupby("Away")["AwayLoss"].sum()
    home_stats = df_copy.groupby("Home")["HomeLoss"].sum()
    team_performance_l = pd.concat([home_stats, away_stats], axis=1).fillna(0)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚽ Top 10 Teams by Average Home Goals")
        teams = df_copy['Home'].unique()
        avg_goals = pd.DataFrame({'Team': teams})
        avg_goals['AvgHomeGoals'] = avg_goals['Team'].apply(lambda x: df_copy[df_copy['Home'] == x]['G_Home'].mean())
        avg_goals['AvgAwayGoals'] = avg_goals['Team'].apply(lambda x: df_copy[df_copy['Away'] == x]['G_Away'].mean())
        avg_goals.set_index('Team', inplace=True)
        top_10_avg_goals = avg_goals.sort_values("AvgHomeGoals", ascending=False).head(10)
        fig_goal, ax_goal = plt.subplots(figsize=(6, 4))
        top_10_avg_goals.plot(kind="bar", colormap="seismic", ax=ax_goal)
        ax_goal.set_title("Avg Home Goals (Top 10)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig_goal)

    with col2:
        st.markdown("### 📉 Halftime Conversion Rate")
        team_analysis = df[df["HalfTimeResult"].isin(["H", "A"])].copy()
        team_analysis["LeadHeld"] = (
            ((team_analysis["HalfTimeResult"] == "H") & (team_analysis["FullTimeResult"] == "H")) |
            ((team_analysis["HalfTimeResult"] == "A") & (team_analysis["FullTimeResult"] == "A"))
        ).astype(int)
        team_analysis["LeadingTeam"] = team_analysis.apply(lambda row: row["HomeTeam"] if row["HalfTimeResult"] == "H" else row["AwayTeam"], axis=1)
        team_conversion = team_analysis.groupby("LeadingTeam")["LeadHeld"].agg(["sum", "count"])
        team_conversion["ConversionRate"] = (team_conversion["sum"] / team_conversion["count"]) * 100
        top_10 = team_conversion.sort_values("ConversionRate", ascending=False).head(10)
        fig8, ax8 = plt.subplots(figsize=(6, 4))
        ax8.bar(top_10.index, top_10["ConversionRate"], color='red')
        ax8.set_title("Top 10 Halftime to FT Win")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig8)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 🔁 Comeback Rates")
        team_analysis["ComebackWin"] = (
            ((team_analysis["HalfTimeResult"] == "A") & (team_analysis["FullTimeResult"] == "H")) |
            ((team_analysis["HalfTimeResult"] == "H") & (team_analysis["FullTimeResult"] == "A"))
        ).astype(int)
        remontada_stats = team_analysis.groupby("LeadingTeam").agg(ComebackWins=('ComebackWin', 'sum'), TotalOpportunities=('ComebackWin', 'count')).reset_index()
        remontada_stats["RemontadaRate"] = (remontada_stats["ComebackWins"] / remontada_stats["TotalOpportunities"]) * 100
        top_remontadas = remontada_stats.sort_values("RemontadaRate", ascending=False).tail(10)
        fig9, ax9 = plt.subplots(figsize=(6, 4))
        ax9.bar(top_remontadas["LeadingTeam"], top_remontadas["RemontadaRate"], color='green')
        ax9.set_title("Lowest 5 Comeback Rates")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig9)

    with col4:
        st.markdown("### 🔴 Liverpool Halftime Conversion")
        liverpool_leads = team_analysis[
            (((team_analysis["HalfTimeResult"] == "H") & (team_analysis["HomeTeam"] == "Liverpool")) |
             ((team_analysis["HalfTimeResult"] == "A") & (team_analysis["AwayTeam"] == "Liverpool")))
        ]
        liverpool_season_conversion = liverpool_leads.groupby("Season")["LeadHeld"].agg(["sum", "count"])
        liverpool_season_conversion["ConversionRate"] = (
            liverpool_season_conversion["sum"] / liverpool_season_conversion["count"]
        ) * 100
        fig10, ax10 = plt.subplots(figsize=(6, 4))
        ax10.plot(liverpool_season_conversion.index, liverpool_season_conversion["ConversionRate"], marker="o", color="crimson")
        ax10.set_title("Liverpool – HT Leads to Wins")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig10)
with tab7:
    st.subheader("🔥 Attacking Trends: League & Liverpool")

    df_full = pd.read_csv("epl_final.csv")
    df_copy = df_full.copy()

    df_copy["TotalGoals"] = df_copy["FullTimeHomeGoals"] + df_copy["FullTimeAwayGoals"]
    df_copy["TotalShots"] = df_copy["HomeShots"] + df_copy["AwayShots"]
    df_copy["WinMargin"] = abs(df_copy["FullTimeHomeGoals"] - df_copy["FullTimeAwayGoals"])
    attack_trend = df_copy.groupby("Season")[["TotalGoals", "TotalShots", "WinMargin"]].mean().sort_index()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ⚽ League Attack Trend")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.plot(attack_trend.index, attack_trend["TotalGoals"], marker="o", label="Goals")
        ax1.plot(attack_trend.index, attack_trend["TotalShots"], marker="s", label="Shots")
        ax1.plot(attack_trend.index, attack_trend["WinMargin"], marker="^", label="Win Margin")
        ax1.set_title("League Attacking Trend Over Time")
        ax1.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)

    with col2:
        st.markdown("### 🔴 Liverpool Attack Trend")
        lfc_only = df_full[(df_full["HomeTeam"] == "Liverpool") | (df_full["AwayTeam"] == "Liverpool")].copy()
        lfc_only["TotalGoals"] = lfc_only["FullTimeHomeGoals"] + lfc_only["FullTimeAwayGoals"]
        lfc_only["TotalShots"] = lfc_only["HomeShots"] + lfc_only["AwayShots"]
        lfc_only["WinMargin"] = abs(lfc_only["FullTimeHomeGoals"] - lfc_only["FullTimeAwayGoals"])
        lfc_trend = lfc_only.groupby("Season")[["TotalGoals", "TotalShots", "WinMargin"]].mean().sort_index()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.plot(lfc_trend.index, lfc_trend["TotalGoals"], marker="o", color="red", label="Goals")
        ax2.plot(lfc_trend.index, lfc_trend["TotalShots"], marker="s", color="blue", label="Shots")
        ax2.plot(lfc_trend.index, lfc_trend["WinMargin"], marker="^", color="green", label="Win Margin")
        ax2.set_title("Liverpool Attacking Trend")
        ax2.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("### 🏠 Home vs Away Breakdown for Liverpool")
    lfc_only["Venue"] = lfc_only["HomeTeam"].apply(lambda x: "Home" if x == "Liverpool" else "Away")
    grouped = lfc_only.groupby(["Season", "Venue"])[["TotalGoals", "TotalShots", "WinMargin"]].mean().reset_index()

    pivot_goals = grouped.pivot(index="Season", columns="Venue", values="TotalGoals")
    pivot_shots = grouped.pivot(index="Season", columns="Venue", values="TotalShots")
    pivot_margin = grouped.pivot(index="Season", columns="Venue", values="WinMargin")

    fig3, axs = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
    pivot_goals.plot(ax=axs[0], marker='o'); axs[0].set_title("Avg Total Goals per Match")
    pivot_shots.plot(ax=axs[1], marker='s'); axs[1].set_title("Avg Total Shots per Match")
    pivot_margin.plot(ax=axs[2], marker='^'); axs[2].set_title("Avg Win Margin per Match")
    for ax in axs: ax.grid(True); ax.set_ylabel("Avg per Match")
    axs[2].set_xlabel("Season")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig3)

    st.markdown("### 🎯 Shot Conversion Rate (League vs Liverpool)")
    attack_trend["ShotConversion"] = (attack_trend["TotalGoals"] / attack_trend["TotalShots"])*100
    fig4, ax4 = plt.subplots(figsize=(12, 4))
    ax4.plot(attack_trend.index, attack_trend["ShotConversion"], marker="o", color="purple", label="League")
    ax4.axhline(attack_trend["ShotConversion"].mean(), color="gray", linestyle="--", label="Avg")
    ax4.set_title("League Shot Conversion Rate")
    ax4.legend(); plt.xticks(rotation=45); plt.tight_layout()
    st.pyplot(fig4)

    lfc_trend["ShotConversion"] = (lfc_trend["TotalGoals"] / lfc_trend["TotalShots"])*100
    fig5, ax5 = plt.subplots(figsize=(12, 4))
    ax5.plot(lfc_trend.index, lfc_trend["ShotConversion"], marker="o", color="purple", label="Liverpool")
    ax5.axhline(lfc_trend["ShotConversion"].mean(), color="gray", linestyle="--", label="Avg")
    ax5.set_title("Liverpool Shot Conversion Rate")
    ax5.legend(); plt.xticks(rotation=45); plt.tight_layout()
    st.pyplot(fig5)

with tab8:
    st.header("⚔️ Physicality & Discipline Analysis")

    col1, col2 = st.columns(2)


   
    with col1:
        st.subheader("Fouls, Yellow & Red Cards Per Season (League)")
        df_copy = df.copy()
        df_copy["TotalFouls"] = df_copy["HomeFouls"] + df_copy["AwayFouls"]
        df_copy["TotalYellowCards"] = df_copy["HomeYellowCards"] + df_copy["AwayYellowCards"]
        df_copy["TotalRedCards"] = df_copy["HomeRedCards"] + df_copy["AwayRedCards"]
        physical_trends = df_copy.groupby("Season")[["TotalFouls", "TotalYellowCards", "TotalRedCards"]].mean()

        fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=True)
        metrics = ["TotalFouls", "TotalYellowCards", "TotalRedCards"]
        colors = ["#1f77b4", "#ff7f0e", "#d62728"]
        titles = ["Fouls per Match", "Yellow Cards per Match", "Red Cards per Match"]

        for i, ax in enumerate(axes):
            ax.plot(physical_trends.index, physical_trends[metrics[i]], marker="o", color=colors[i])
            ax.set_title(titles[i])
            ax.set_ylabel("Average per Match")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.set_xticks(range(len(physical_trends.index)))
            ax.set_xticklabels(physical_trends.index, rotation=45)

        fig.suptitle("Physicality in EPL Over Time", fontsize=16, fontweight="bold")
        st.pyplot(fig)

        # 🔴 Liverpool-specific plot just below
        st.markdown("#### 🟥 Liverpool Physicality Trends")
        liverpool_df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()
        liverpool_df["TotalFouls"] = liverpool_df["HomeFouls"] + liverpool_df["AwayFouls"]
        liverpool_df["TotalYellowCards"] = liverpool_df["HomeYellowCards"] + liverpool_df["AwayYellowCards"]
        liverpool_df["TotalRedCards"] = liverpool_df["HomeRedCards"] + liverpool_df["AwayRedCards"]
        physical_trends_lfc = liverpool_df.groupby("Season")[["TotalFouls", "TotalYellowCards", "TotalRedCards"]].mean()

        fig_lfc, axes_lfc = plt.subplots(1, 3, figsize=(18, 6), sharex=True)
        for i, ax in enumerate(axes_lfc):
            ax.plot(physical_trends_lfc.index, physical_trends_lfc[metrics[i]], marker="o", color=colors[i])
            ax.set_title(titles[i], fontsize=12)
            ax.set_ylabel("Average per Match")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.tick_params(axis="x", rotation=45)

        fig_lfc.suptitle("Liverpool Physicality Trends Over Time", fontsize=16, fontweight="bold")
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        st.pyplot(fig_lfc)

        # 🔴 Liverpool-specific line plots
    st.markdown("#### 🟥 Liverpool Physicality Trends")
    liverpool_df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()
    liverpool_df["TotalFouls"] = liverpool_df["HomeFouls"] + liverpool_df["AwayFouls"]
    liverpool_df["TotalYellowCards"] = liverpool_df["HomeYellowCards"] + liverpool_df["AwayYellowCards"]
    liverpool_df["TotalRedCards"] = liverpool_df["HomeRedCards"] + liverpool_df["AwayRedCards"]
    physical_trends_lfc = liverpool_df.groupby("Season")[["TotalFouls", "TotalYellowCards", "TotalRedCards"]].mean()

    fig_lfc, axes_lfc = plt.subplots(1, 3, figsize=(18, 6), sharex=True)
    for i, ax in enumerate(axes_lfc):
        ax.plot(physical_trends_lfc.index, physical_trends_lfc[metrics[i]], marker="o", color=colors[i])
        ax.set_title(titles[i], fontsize=12)
        ax.set_ylabel("Average per Match")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.tick_params(axis="x", rotation=45)

    fig_lfc.suptitle("Liverpool Physicality Trends Over Time", fontsize=16, fontweight="bold")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    st.pyplot(fig_lfc)

    # 📊 Seaborn catplots: Liverpool Physicality by Venue & Result
    st.markdown("#### ⚖️ Liverpool Physicality Split by Venue & Result")
    liverpool_df["Venue"] = liverpool_df["HomeTeam"].apply(lambda x: "Home" if x == "Liverpool" else "Away")
    liverpool_df["GoalsFor"] = liverpool_df.apply(
        lambda row: row["FullTimeHomeGoals"] if row["Venue"] == "Home" else row["FullTimeAwayGoals"], axis=1)
    liverpool_df["GoalsAgainst"] = liverpool_df.apply(
        lambda row: row["FullTimeAwayGoals"] if row["Venue"] == "Home" else row["FullTimeHomeGoals"], axis=1)
    liverpool_df["Result"] = liverpool_df.apply(
        lambda row: "Win" if row["GoalsFor"] > row["GoalsAgainst"] else
        ("Loss" if row["GoalsFor"] < row["GoalsAgainst"] else "Draw"), axis=1)

    liverpool_df["Fouls"] = liverpool_df["HomeFouls"] + liverpool_df["AwayFouls"]
    liverpool_df["YellowCards"] = liverpool_df["HomeYellowCards"] + liverpool_df["AwayYellowCards"]
    liverpool_df["RedCards"] = liverpool_df["HomeRedCards"] + liverpool_df["AwayRedCards"]

    melt_df = liverpool_df.melt(
        id_vars=["Season", "Venue", "Result"],
        value_vars=["Fouls", "YellowCards", "RedCards"],
        var_name="Metric",
        value_name="Value"
    )

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
        st.pyplot(g.fig)


    with col2:
        st.subheader("Discipline: Away vs Home (Aggression Delta)")
        home_cards = df.groupby("HomeTeam").agg(HomeYellows=("HomeYellowCards", "sum"), HomeReds=("HomeRedCards", "sum"), HomeGames=("HomeTeam", "count"))
        away_cards = df.groupby("AwayTeam").agg(AwayYellows=("AwayYellowCards", "sum"), AwayReds=("AwayRedCards", "sum"), AwayGames=("AwayTeam", "count"))
        discipline = home_cards.join(away_cards)
        discipline["CardsPerGame_Home"] = (discipline["HomeYellows"] + discipline["HomeReds"]) / discipline["HomeGames"]
        discipline["CardsPerGame_Away"] = (discipline["AwayYellows"] + discipline["AwayReds"]) / discipline["AwayGames"]
        discipline["AggressionDelta"] = discipline["CardsPerGame_Away"] - discipline["CardsPerGame_Home"]
        delta_sorted = discipline.sort_values("AggressionDelta", ascending=False)
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(x=delta_sorted["AggressionDelta"], y=delta_sorted.index, palette=["red" if x > 0 else "blue" for x in delta_sorted["AggressionDelta"]], ax=ax)
        ax.set_title("Aggression Delta (Away - Home Cards/Game)")
        ax.axvline(0, color="black", linestyle="--")
        ax.set_xlabel("Cards/Game Difference")
        st.pyplot(fig)




 

    with col4:
        st.markdown("#### Liverpool Outcomes After Red Card")
        df_lfc = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()
        df_lfc["HomeRed"] = df_lfc["HomeRedCards"] > 0
        df_lfc["AwayRed"] = df_lfc["AwayRedCards"] > 0
        df_lfc["RedToLFC"] = df_lfc.apply(lambda row: (row["HomeTeam"] == "Liverpool" and row["HomeRed"]) or (row["AwayTeam"] == "Liverpool" and row["AwayRed"]), axis=1)
        lfc_red = df_lfc[df_lfc["RedToLFC"]].copy()
        def get_lfc_result(row):
            if row["HomeTeam"] == "Liverpool":
                return "Win" if row["FullTimeResult"] == "H" else "Loss" if row["FullTimeResult"] == "A" else "Draw"
            else:
                return "Win" if row["FullTimeResult"] == "A" else "Loss" if row["FullTimeResult"] == "H" else "Draw"
        lfc_red["LiverpoolResult"] = lfc_red.apply(get_lfc_result, axis=1)
        result_counts = lfc_red["LiverpoolResult"].value_counts().reindex(["Loss", "Draw", "Win"]).fillna(0)
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(result_counts, labels=result_counts.index, autopct="%1.1f%%", colors=["#930828", "#FFD166", "#06D65D"], startangle=140)
        ax.set_title("Liverpool Outcomes After Receiving a Red Card")
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("🛡️ Defensive & Draw Analysis")

    col5, col6 = st.columns(2)
    with col5:
        st.markdown("#### Defensive Efficiency (Goals Conceded / xG Faced)")
        df_copy = pd.read_csv("EPL_result.csv")
        home_def = df_copy.groupby("Home")[["G_Away"]].sum().rename(columns={"G_Away": "GoalsConceded_Home"})
        away_def = df_copy.groupby("Away")[["G_Home"]].sum().rename(columns={"G_Home": "GoalsConceded_Away"})
        team_def = pd.concat([home_def, away_def], axis=1).fillna(0)
        home_shots = df_copy.groupby("Home")[["xG_Away"]].sum()
        away_shots = df_copy.groupby("Away")[["xG_Home"]].sum()
        team_def["ShotsFaced"] = home_shots["xG_Away"] + away_shots["xG_Home"]
        team_def["GoalsConceded"] = team_def["GoalsConceded_Home"] + team_def["GoalsConceded_Away"]
        team_def["ConcededPerShot"] = team_def["GoalsConceded"] / team_def["ShotsFaced"]
        defensive_ranking = team_def.sort_values("ConcededPerShot", ascending=False)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(defensive_ranking.index, defensive_ranking["ConcededPerShot"], color='darkred')
        ax.set_title("Worst Defensive Teams (Goals Conceded per xG Faced)")
        ax.set_xticklabels(defensive_ranking.index, rotation=45)
        st.pyplot(fig)

    with col6:
        st.markdown("#### Teams with Most Draws")
        df_copy["FullTimeResult"] = df_copy.apply(lambda row: "H" if row["G_Home"] > row["G_Away"] else "A" if row["G_Home"] < row["G_Away"] else "D", axis=1)
        df_copy["IsDraw"] = df_copy["FullTimeResult"] == "D"
        draws = df_copy.groupby("Home")["IsDraw"].sum() + df_copy.groupby("Away")["IsDraw"].sum()
        draws = draws.sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=draws.head(10).values, y=draws.head(10).index, palette="Blues_d", ax=ax)
        ax.set_title("Top 10 Teams with Most Draws")
        st.pyplot(fig)




with tab9:
    st.header("🏆 Liverpool's 2019 & 2020 Title-Winning Performance")

    grid_col1, grid_col2 = st.columns(2)

    with grid_col1:
        df = pd.read_csv("epl_final.csv")
        lfc_df = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()
        lfc_df["Venue"] = lfc_df["HomeTeam"].apply(lambda x: "Home" if x == "Liverpool" else "Away")

        def get_result(row):
            if row["HomeTeam"] == "Liverpool":
                return "Win" if row["FullTimeResult"] == "H" else "Draw" if row["FullTimeResult"] == "D" else "Loss"
            else:
                return "Win" if row["FullTimeResult"] == "A" else "Draw" if row["FullTimeResult"] == "D" else "Loss"

        lfc_df["Result"] = lfc_df.apply(get_result, axis=1)
        venue_stats = lfc_df.groupby("Venue")["Result"].value_counts().unstack().fillna(0)
        venue_stats["Total"] = venue_stats.sum(axis=1)
        venue_stats["Win Ratio"] = venue_stats["Win"] / venue_stats["Total"]
        venue_stats_reset = venue_stats.reset_index()

        plt.figure(figsize=(8, 5))
        sns.barplot(data=venue_stats_reset, x="Win Ratio", y="Venue", palette="Greens_r")
        plt.title("Liverpool Win Ratio by Venue (Home vs Away)")
        plt.xlabel("Win Ratio")
        plt.ylabel("Venue")
        plt.xlim(0, 1)
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
        plt.tight_layout()
        st.pyplot(plt)

    with grid_col2:
        liverpool_matches = df[(df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")].copy()
        liverpool_matches["MatchDate"] = pd.to_datetime(liverpool_matches["MatchDate"], errors="coerce")
        liverpool_matches = liverpool_matches[liverpool_matches["MatchDate"].dt.year.isin([2019, 2020])].sort_values("MatchDate")
        liverpool_matches["Liverpool Goals"] = liverpool_matches.apply(
            lambda row: row["FullTimeHomeGoals"] if row["HomeTeam"] == "Liverpool" else row["FullTimeAwayGoals"], axis=1)
        liverpool_matches["Opponent Goals"] = liverpool_matches.apply(
            lambda row: row["FullTimeAwayGoals"] if row["HomeTeam"] == "Liverpool" else row["FullTimeHomeGoals"], axis=1)

        plt.figure(figsize=(14, 5))
        plt.plot(liverpool_matches["MatchDate"], liverpool_matches["Liverpool Goals"], label="Liverpool Goals", marker="o")
        plt.plot(liverpool_matches["MatchDate"], liverpool_matches["Opponent Goals"], label="Opponent Goals", marker="x")
        plt.title("Liverpool Goals vs Opponent Goals (2019–2020)")
        plt.xlabel("Match Date")
        plt.ylabel("Goals")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)

    # Load Liverpool shot data
    liverpool_shots = pd.read_csv("shots_EPL_1920.csv")
    liverpool_shots["date"] = pd.to_datetime(liverpool_shots["date"], errors="coerce")
    liverpool_shots = liverpool_shots[liverpool_shots["date"].dt.year.isin([2019, 2020])]
    liverpool_shots = liverpool_shots[
        ((liverpool_shots["h_team"] == "Liverpool") & (liverpool_shots["h_a"] == "h")) |
        ((liverpool_shots["a_team"] == "Liverpool") & (liverpool_shots["h_a"] == "a"))
    ].copy()
    liverpool_shots["Venue"] = liverpool_shots["h_a"].apply(lambda x: "Home" if x == "h" else "Away")
    liverpool_shots["isGoal"] = liverpool_shots["result"] == "Goal"

    # Top Scorers and Assists
    top_scorers = liverpool_shots[liverpool_shots["result"] == "Goal"].groupby("player")["result"].count().sort_values(ascending=False).head(10)
    top_assists = liverpool_shots[liverpool_shots["player_assisted"].notna()].groupby("player_assisted")["id"].count().sort_values(ascending=False).head(10)

    fig, axs = plt.subplots(1, 2, figsize=(16, 5))
    sns.barplot(x=top_scorers.values, y=top_scorers.index, ax=axs[0])
    axs[0].set_title("Top Liverpool Scorers")
    axs[0].set_xlabel("Goals")
    sns.barplot(x=top_assists.values, y=top_assists.index, ax=axs[1])
    axs[1].set_title("Top Liverpool Assist Providers")
    axs[1].set_xlabel("Assists")
    plt.tight_layout()
    st.pyplot(plt)

    # Shot Map by Venue
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    for ax, title in zip(axes, ["Home", "Away"]):
        subset = liverpool_shots[liverpool_shots["Venue"] == title]
        sns.scatterplot(data=subset, x="X", y="Y", hue="isGoal", palette={True: "green", False: "red"}, ax=ax, s=30)
        ax.set_title(f"Liverpool Shot Map ({title})")
        ax.set_xlim(0.7, 1.05)
        ax.set_ylim(0.2, 0.9)
        ax.set_xlabel("Normalized X")
        ax.set_ylabel("Normalized Y")
        ax.set_aspect('equal')
        ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

    # Shot Types
    plt.figure(figsize=(12, 6))
    shot_types = liverpool_shots.groupby(["Venue", "shotType"])["id"].count().unstack().fillna(0)
    shot_types.T.plot(kind='bar')
    plt.title("Liverpool Shot Types: Home vs Away")
    plt.ylabel("Number of Shots")
    plt.tight_layout()
    st.pyplot(plt)

    # Shot Situations
    plt.figure(figsize=(12, 6))
    situations = liverpool_shots.groupby(["Venue", "situation"])["id"].count().unstack().fillna(0)
    situations.T.plot(kind='bar')
    plt.title("Shot Situations: Home vs Away")
    plt.ylabel("Number of Shots")
    plt.tight_layout()
    st.pyplot(plt)

    # xG Top Contributors
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

    # Team Shot Density Heatmaps
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    for ax, venue in zip(axes, ["Home", "Away"]):
        subset = liverpool_shots[liverpool_shots["Venue"] == venue]
        sns.kdeplot(data=subset, x="X", y="Y", fill=True, thresh=0, levels=100, cmap="Reds", ax=ax)
        ax.set_title(f"Liverpool Shot Density – {venue} Matches")
        ax.set_xlim(0.7, 1.05)
        ax.set_ylim(0.2, 0.9)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.set_xlabel("Normalized X (Goal Right)")
        ax.set_ylabel("Normalized Y (Pitch Height)")
    plt.tight_layout()
    st.pyplot(plt)

    # Salah vs Firmino Shot Density
    key_players = ["Mohamed Salah", "Roberto Firmino"]
    player_shots = liverpool_shots[liverpool_shots["player"].isin(key_players)]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12), sharex=True, sharey=True)
    for i, player in enumerate(key_players):
        for j, venue in enumerate(["Home", "Away"]):
            subset = player_shots[(player_shots["player"] == player) & (player_shots["Venue"] == venue)]
            ax = axes[i][j]
            sns.kdeplot(data=subset, x="X", y="Y", fill=True, thresh=0, levels=100, cmap="Reds", ax=ax)
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

