import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

# Configure page
st.set_page_config(
    page_title="Liverpool FC Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Liverpool-themed custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #C8102E 0%, #00A398 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #C8102E 0%, #8B0000 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .tab-content {
        background-color: #FAFAFA;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #00A398;
        margin-top: 1rem;
    }
    
    .ynwa-footer {
        background-color: #C8102E;
        color: white;
        text-align: center;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>⚽ Liverpool FC Analytics Dashboard</h1>
        <h3>🔴 Comprehensive Performance Analysis & Statistics</h3>
        <p><em>"You'll Never Walk Alone"</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Analysis Tabs
    st.markdown("## 📊 Detailed Analysis")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Venue Win Stats", 
        "🦠 COVID Period Breakdown", 
        "📈 Timeline & Goals", 
        "📊 EPL xG Comparison",
        "🕰️ Club Trends & Manager Era",
        "📊 Team Momentum & Conversion",
        "🔥 Attacking Trends",
        "🛡️ Physicality & Discipline",
        "🏆 Liverpool's 2019 & 2020 Title-Winning Performance"
    ])
    
    with tab1:
        st.markdown("""
        <div class="tab-content">
            <h3>📊 Venue Win Stats Analysis</h3>
            <p>Comprehensive analysis of Liverpool's performance across different venues</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load your CSV data
            df = pd.read_csv('Liverpool_2015_2023_Matches.csv')
            
            # Add Venue column
            df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)
            
            # Add Result column
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
            
            # Add additional analysis columns
            df['GoalsFor'] = df.apply(lambda row: row['HomeGoals'] if row['Venue'] == 'Home' else row['AwayGoals'], axis=1)
            df['GoalsAgainst'] = df.apply(lambda row: row['AwayGoals'] if row['Venue'] == 'Home' else row['HomeGoals'], axis=1)
            df['GoalDifference'] = df['GoalsFor'] - df['GoalsAgainst']
            df['Date'] = pd.to_datetime(df['Date'])
            df['Season'] = df['Date'].dt.year.apply(lambda x: f"{x-1}-{str(x)[2:]}" if x > 2014 else "2014-15")
            
            # Create Summary Table
            summary = df.groupby('Venue').agg(
                Total_Matches=('Result', 'count'),
                Wins=('Result', lambda x: (x == 'Win').sum()),
                Draws=('Result', lambda x: (x == 'Draw').sum()),
                Losses=('Result', lambda x: (x == 'Loss').sum()),
                Goals_For=('GoalsFor', 'sum'),
                Goals_Against=('GoalsAgainst', 'sum'),
                Avg_Goals_For=('GoalsFor', 'mean'),
                Avg_Goals_Against=('GoalsAgainst', 'mean'),
                Clean_Sheets=('GoalsAgainst', lambda x: (x == 0).sum())
            ).reset_index()
            summary['Win_Percentage'] = (summary['Wins'] / summary['Total_Matches'] * 100).round(1)
            summary['Goal_Difference'] = summary['Goals_For'] - summary['Goals_Against']
            summary['Points'] = summary['Wins'] * 3 + summary['Draws']
            summary['Points_Per_Game'] = (summary['Points'] / summary['Total_Matches']).round(2)
            
            # Display summary statistics
            st.markdown("### 📊 Enhanced Venue Statistics")
            
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            
            with summary_col1:
                home_data = summary[summary['Venue'] == 'Home'].iloc[0]
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏠 Home (Anfield)</h3>
                    <h2>{home_data['Wins']}/{home_data['Total_Matches']}</h2>
                    <h1>{home_data['Win_Percentage']}%</h1>
                    <small>{home_data['Points_Per_Game']} PPG</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col2:
                away_data = summary[summary['Venue'] == 'Away'].iloc[0]
                st.markdown(f"""
                <div class="metric-card">
                    <h3>✈️ Away</h3>
                    <h2>{away_data['Wins']}/{away_data['Total_Matches']}</h2>
                    <h1>{away_data['Win_Percentage']}%</h1>
                    <small>{away_data['Points_Per_Game']} PPG</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col3:
                home_advantage = home_data['Win_Percentage'] - away_data['Win_Percentage']
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏠 Home Advantage</h3>
                    <h2>+{home_advantage:.1f}%</h2>
                    <h1>Win Rate</h1>
                    <small>Difference</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col4:
                total_wins = summary['Wins'].sum()
                total_matches = summary['Total_Matches'].sum()
                overall_win_rate = (total_wins / total_matches * 100).round(1)
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚽ Overall</h3>
                    <h2>{total_wins}/{total_matches}</h2>
                    <h1>{overall_win_rate}%</h1>
                    <small>Win Rate</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Chart selection with more options
            st.markdown("### 📊 Detailed Venue Analysis")
            venue_chart_selection = st.selectbox(
                "Choose Analysis Type",
                ["All Analysis", "Win Rate Comparison", "Goals Analysis", "Season Trends", 
                 "Home vs Away Deep Dive", "Performance Matrix", "Head-to-Head Stats"],
                index=0,
                key="venue_chart_selection"
            )
            
            # Chart 1: Win Rate Comparison with more details
            if venue_chart_selection in ["All Analysis", "Win Rate Comparison"]:
                st.markdown("#### 🏆 Comprehensive Win Rate Analysis")
                
                fig_win_comparison = px.bar(
                    summary,
                    x='Venue',
                    y='Win_Percentage',
                    text='Win_Percentage',
                    color='Venue',
                    color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'},
                    title='Win Rate: Home vs Away Performance',
                    labels={'Win_Percentage': 'Win Rate (%)', 'Venue': 'Venue'},
                    template='plotly_white'
                )
                
                fig_win_comparison.update_traces(
                    texttemplate='%{text}%',
                    textposition='outside',
                    customdata=summary[['Points_Per_Game', 'Total_Matches', 'Goal_Difference']].values,
                    hovertemplate='<b>Venue:</b> %{x}<br>' +
                                '<b>Win Rate:</b> %{y}%<br>' +
                                '<b>Points per Game:</b> %{customdata[0]}<br>' +
                                '<b>Total Games:</b> %{customdata[1]}<br>' +
                                '<b>Goal Difference:</b> %{customdata[2]}<extra></extra>'
                )
                
                fig_win_comparison.update_layout(
                    height=500,
                    showlegend=False,
                    yaxis=dict(range=[0, max(summary['Win_Percentage']) * 1.1])
                )
                
                st.plotly_chart(fig_win_comparison, use_container_width=True)
                
                # Add insight
                st.success(f"🏠 **Anfield Advantage:** {home_advantage:.1f}% higher win rate at home ({home_data['Win_Percentage']}% vs {away_data['Win_Percentage']}%)")
            
            # Chart 2: Goals Analysis
            if venue_chart_selection in ["All Analysis", "Goals Analysis"]:
                st.markdown("#### ⚽ Goals Scored & Conceded Analysis")
                
                goals_col1, goals_col2 = st.columns(2)
                
                with goals_col1:
                    # Goals for/against comparison
                    goals_data = summary.melt(
                        id_vars='Venue',
                        value_vars=['Avg_Goals_For', 'Avg_Goals_Against'],
                        var_name='Goal_Type',
                        value_name='Goals'
                    )
                    
                    fig_goals = px.bar(
                        goals_data,
                        x='Venue',
                        y='Goals',
                        color='Goal_Type',
                        barmode='group',
                        title='Average Goals: Scored vs Conceded',
                        color_discrete_map={'Avg_Goals_For': '#C8102E', 'Avg_Goals_Against': '#7F7F7F'},
                        template='plotly_white'
                    )
                    
                    fig_goals.update_traces(
                        text=goals_data['Goals'].round(2),
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_goals, use_container_width=True)
                
                with goals_col2:
                    # Clean sheets analysis
                    fig_clean_sheets = px.bar(
                        summary,
                        x='Venue',
                        y='Clean_Sheets',
                        text='Clean_Sheets',
                        color='Venue',
                        title='Clean Sheets by Venue',
                        color_discrete_map={'Home': '#00A398', 'Away': '#FFB84D'},
                        template='plotly_white'
                    )
                    
                    fig_clean_sheets.update_traces(textposition='outside')
                    st.plotly_chart(fig_clean_sheets, use_container_width=True)
            
            # Chart 3: Season Trends
            if venue_chart_selection in ["All Analysis", "Season Trends"]:
                st.markdown("#### 📈 Season-by-Season Venue Performance")
                
                season_analysis = df.groupby(['Season', 'Venue']).agg({
                    'Result': ['count', lambda x: (x == 'Win').sum()],
                    'GoalsFor': 'mean',
                    'GoalsAgainst': 'mean'
                }).round(2)
                
                season_analysis.columns = ['Total_Games', 'Wins', 'Avg_Goals_For', 'Avg_Goals_Against']
                season_analysis['Win_Rate'] = ((season_analysis['Wins'] / season_analysis['Total_Games']) * 100).round(1)
                season_analysis = season_analysis.reset_index()
                
                fig_season_trends = px.line(
                    season_analysis,
                    x='Season',
                    y='Win_Rate',
                    color='Venue',
                    markers=True,
                    title='Win Rate Trends by Season',
                    color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'},
                    template='plotly_white'
                )
                
                fig_season_trends.update_layout(
                    xaxis_tickangle=45,
                    height=500
                )
                
                st.plotly_chart(fig_season_trends, use_container_width=True)
            
            # Chart 4: Home vs Away Deep Dive
            if venue_chart_selection in ["All Analysis", "Home vs Away Deep Dive"]:
                st.markdown("#### 🔍 Home vs Away Deep Dive Analysis")
                
                deep_dive_col1, deep_dive_col2 = st.columns(2)
                
                with deep_dive_col1:
                    # Result distribution pie charts
                    for venue in ['Home', 'Away']:
                        venue_data = summary[summary['Venue'] == venue].iloc[0]
                        
                        fig_pie = px.pie(
                            values=[venue_data['Wins'], venue_data['Draws'], venue_data['Losses']],
                            names=['Wins', 'Draws', 'Losses'],
                            title=f'{venue} Results Distribution',
                            color_discrete_map={'Wins': '#C8102E', 'Draws': '#FFB84D', 'Losses': '#7F7F7F'},
                            template='plotly_white'
                        )
                        
                        fig_pie.update_traces(
                            textposition='inside',
                            textinfo='percent+label'
                        )
                        
                        fig_pie.update_layout(height=400)
                        
                        st.plotly_chart(fig_pie, use_container_width=True)
                
                with deep_dive_col2:
                    # Performance metrics comparison
                    metrics_comparison = pd.DataFrame({
                        'Metric': ['Win Rate %', 'Points per Game', 'Goals per Game', 'Goals Against per Game', 'Clean Sheets %'],
                        'Home': [
                            home_data['Win_Percentage'],
                            home_data['Points_Per_Game'],
                            home_data['Avg_Goals_For'].round(2),
                            home_data['Avg_Goals_Against'].round(2),
                            ((home_data['Clean_Sheets'] / home_data['Total_Matches']) * 100).round(1)
                        ],
                        'Away': [
                            away_data['Win_Percentage'],
                            away_data['Points_Per_Game'],
                            away_data['Avg_Goals_For'].round(2),
                            away_data['Avg_Goals_Against'].round(2),
                            ((away_data['Clean_Sheets'] / away_data['Total_Matches']) * 100).round(1)
                        ]
                    })
                    
                    metrics_comparison['Difference'] = metrics_comparison['Home'] - metrics_comparison['Away']
                    metrics_comparison['Home_Advantage'] = metrics_comparison['Difference'].apply(
                        lambda x: '✅ Better' if x > 0 else '❌ Worse' if x < 0 else '➖ Same'
                    )
                    
                    st.markdown("##### 📊 Performance Metrics Comparison")
                    st.dataframe(
                        metrics_comparison.style.background_gradient(
                            subset=['Difference'], 
                            cmap='RdYlGn'
                        ),
                        use_container_width=True
                    )
            
            # Chart 5: Performance Matrix
            if venue_chart_selection in ["All Analysis", "Performance Matrix"]:
                st.markdown("#### 📊 Liverpool Performance Matrix")
                
                # Create a comprehensive heatmap-style analysis
                matrix_data = []
                
                for season in df['Season'].unique():
                    for venue in ['Home', 'Away']:
                        season_venue_data = df[(df['Season'] == season) & (df['Venue'] == venue)]
                        if len(season_venue_data) > 0:
                            win_rate = (season_venue_data['Result'] == 'Win').sum() / len(season_venue_data) * 100
                            matrix_data.append({
                                'Season': season,
                                'Venue': venue,
                                'Win_Rate': win_rate,
                                'Games': len(season_venue_data),
                                'Goals_Per_Game': season_venue_data['GoalsFor'].mean()
                            })
                
                matrix_df = pd.DataFrame(matrix_data)
                
                # Create pivot for heatmap
                win_rate_pivot = matrix_df.pivot(index='Season', columns='Venue', values='Win_Rate').fillna(0)
                
                fig_heatmap = px.imshow(
                    win_rate_pivot,
                    color_continuous_scale='RdYlGn',
                    title='Win Rate Heatmap: Season vs Venue',
                    aspect='auto',
                    text_auto='.1f'
                )
                
                fig_heatmap.update_layout(
                    xaxis_title='Venue',
                    yaxis_title='Season',
                    height=600
                )
                
                st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Chart 6: Head-to-Head Stats
            if venue_chart_selection in ["All Analysis", "Head-to-Head Stats"]:
                st.markdown("#### ⚔️ Head-to-Head: Home vs Away Performance")
                
                h2h_col1, h2h_col2 = st.columns(2)
                
                with h2h_col1:
                    # Radar chart comparison
                    categories = ['Win Rate', 'Goals/Game', 'Clean Sheets %', 'Points/Game']
                    
                    home_values = [
                        home_data['Win_Percentage'],
                        home_data['Avg_Goals_For'] * 20,  # Scaled for visualization
                        (home_data['Clean_Sheets'] / home_data['Total_Matches']) * 100,
                        home_data['Points_Per_Game'] * 33.33  # Scaled to 0-100
                    ]
                    
                    away_values = [
                        away_data['Win_Percentage'],
                        away_data['Avg_Goals_For'] * 20,  # Scaled for visualization
                        (away_data['Clean_Sheets'] / away_data['Total_Matches']) * 100,
                        away_data['Points_Per_Game'] * 33.33  # Scaled to 0-100
                    ]
                    
                    fig_radar = go.Figure()
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=home_values + [home_values[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        name='Home',
                        line_color='#C8102E'
                    ))
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=away_values + [away_values[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        name='Away',
                        line_color='#00A398',
                        opacity=0.7
                    ))
                    
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100]
                            )
                        ),
                        showlegend=True,
                        title='Performance Radar: Home vs Away',
                        height=500
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True)
                
                with h2h_col2:
                    # Goal difference distribution
                    fig_goal_diff = px.histogram(
                        df,
                        x='GoalDifference',
                        color='Venue',
                        barmode='group',
                        title='Goal Difference Distribution',
                        color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'},
                        template='plotly_white'
                    )
                    
                    fig_goal_diff.update_layout(
                        xaxis_title='Goal Difference',
                        yaxis_title='Frequency',
                        height=500
                    )
                    
                    st.plotly_chart(fig_goal_diff, use_container_width=True)
            
            # Enhanced breakdown table with more insights
            st.markdown("### 📋 Comprehensive Venue Statistics")
            
            enhanced_summary = summary.copy()
            enhanced_summary['Clean_Sheet_Rate_%'] = ((enhanced_summary['Clean_Sheets'] / enhanced_summary['Total_Matches']) * 100).round(1)
            enhanced_summary['Goals_Per_Game'] = enhanced_summary['Avg_Goals_For'].round(2)
            enhanced_summary['Goals_Against_Per_Game'] = enhanced_summary['Avg_Goals_Against'].round(2)
            
            display_enhanced = enhanced_summary[[
                'Venue', 'Total_Matches', 'Wins', 'Draws', 'Losses', 'Win_Percentage',
                'Points_Per_Game', 'Goals_Per_Game', 'Goals_Against_Per_Game', 
                'Goal_Difference', 'Clean_Sheets', 'Clean_Sheet_Rate_%'
            ]].copy()
            
            display_enhanced.columns = [
                'Venue', 'Games', 'Wins', 'Draws', 'Losses', 'Win %',
                'PPG', 'Goals/Game', 'Conceded/Game', 'Goal Diff', 'Clean Sheets', 'Clean Sheet %'
            ]
            
            st.dataframe(
                display_enhanced.style.background_gradient(
                    subset=['Win %', 'PPG', 'Goals/Game', 'Clean Sheet %'], 
                    cmap='RdYlGn'
                ),
                use_container_width=True
            )
            
            # Additional insights
            st.markdown("### 🎯 Key Venue Insights")
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                st.info(f"🏠 **Anfield Impact:** {home_advantage:.1f}% better win rate at home")
                home_goals_advantage = home_data['Avg_Goals_For'] - away_data['Avg_Goals_For']
                st.info(f"⚽ **Scoring Boost:** {home_goals_advantage:.2f} more goals per game at home")
            
            with insight_col2:
                home_defensive = away_data['Avg_Goals_Against'] - home_data['Avg_Goals_Against']
                st.info(f"🛡️ **Defensive Strength:** {home_defensive:.2f} fewer goals conceded at home")
                clean_sheet_advantage = ((home_data['Clean_Sheets'] / home_data['Total_Matches']) - 
                                       (away_data['Clean_Sheets'] / away_data['Total_Matches'])) * 100
                st.info(f"🥅 **Clean Sheet Advantage:** {clean_sheet_advantage:.1f}% more clean sheets at home")
            
            with insight_col3:
                points_advantage = home_data['Points_Per_Game'] - away_data['Points_Per_Game']
                st.info(f"📈 **Points Advantage:** {points_advantage:.2f} more points per game at home")
                home_fortress_rating = (home_data['Win_Percentage'] / 100) * (home_data['Points_Per_Game'] / 3) * 100
                st.info(f"🏰 **Fortress Rating:** {home_fortress_rating:.0f}/100 (Home strength index)")
                
        except FileNotFoundError:
            st.error("❌ Error: 'Liverpool_2015_2023_Matches.csv' file not found.")
            st.info("""
            📋 **To use this dashboard:**
            1. Place your 'Liverpool_2015_2023_Matches.csv' file in the same directory as this script
            2. Make sure the CSV has columns: 'Date', 'Home', 'Away', 'HomeGoals', 'AwayGoals'
            3. Refresh the page
            """)
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    
   
    with tab2:
        st.markdown("""
        <div class="tab-content">
            <h3>🦠 COVID Period Breakdown</h3>
            <p>Impact analysis of COVID-19 on Liverpool's performance (2015-2023)</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load the CSV
            df = pd.read_csv("Liverpool_2015_2023_Matches.csv")
            
            # Add Venue column
            df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)
            
            # Add Result column
            def get_result(row):
                if row['Venue'] == 'Home':
                    return 'Win' if row['HomeGoals'] > row['AwayGoals'] else 'Draw' if row['HomeGoals'] == row['AwayGoals'] else 'Loss'
                else:
                    return 'Win' if row['AwayGoals'] > row['HomeGoals'] else 'Draw' if row['AwayGoals'] == row['HomeGoals'] else 'Loss'
            
            df['Result'] = df.apply(get_result, axis=1)
            
            # Add CovidPeriod column with more precise dates
            df['Date'] = pd.to_datetime(df['Date'])
            
            def covid_period(date):
                if date < pd.to_datetime('2020-03-11'):  # WHO declared pandemic
                    return 'Pre-COVID'
                elif date < pd.to_datetime('2021-08-01'):  # End of major restrictions
                    return 'During COVID'
                else:
                    return 'Post-COVID'
            
            df['CovidPeriod'] = df['Date'].apply(covid_period)
            
            # Add additional analysis columns
            df['GoalsFor'] = df.apply(lambda row: row['HomeGoals'] if row['Venue'] == 'Home' else row['AwayGoals'], axis=1)
            df['GoalsAgainst'] = df.apply(lambda row: row['AwayGoals'] if row['Venue'] == 'Home' else row['HomeGoals'], axis=1)
            df['GoalDifference'] = df['GoalsFor'] - df['GoalsAgainst']
            df['Points'] = df['Result'].map({'Win': 3, 'Draw': 1, 'Loss': 0})
            
            # Calculate comprehensive COVID period summary
            covid_summary = df.groupby('CovidPeriod').agg({
                'Result': ['count', lambda x: (x == 'Win').sum(), lambda x: (x == 'Draw').sum(), lambda x: (x == 'Loss').sum()],
                'GoalsFor': ['sum', 'mean'],
                'GoalsAgainst': ['sum', 'mean'],
                'Points': 'sum',
                'GoalDifference': 'mean'
            }).round(2)
            
            covid_summary.columns = ['Total_Games', 'Wins', 'Draws', 'Losses', 'Total_Goals_For', 'Avg_Goals_For', 
                                   'Total_Goals_Against', 'Avg_Goals_Against', 'Total_Points', 'Avg_Goal_Diff']
            covid_summary['Win_Rate'] = ((covid_summary['Wins'] / covid_summary['Total_Games']) * 100).round(1)
            covid_summary['Points_Per_Game'] = (covid_summary['Total_Points'] / covid_summary['Total_Games']).round(2)
            covid_summary['Clean_Sheets'] = df.groupby('CovidPeriod')['GoalsAgainst'].apply(lambda x: (x == 0).sum()).values
            covid_summary['Clean_Sheet_Rate'] = ((covid_summary['Clean_Sheets'] / covid_summary['Total_Games']) * 100).round(1)
            covid_summary = covid_summary.reset_index()
            
            # Display enhanced COVID period summary statistics
            st.markdown("### 📊 Enhanced COVID Impact Analysis")
            
            covid_col1, covid_col2, covid_col3 = st.columns(3)
            
            periods = ['Pre-COVID', 'During COVID', 'Post-COVID']
            colors = ['#00A398', '#C8102E', '#FFD700']
            
            for i, (col, period, color) in enumerate(zip([covid_col1, covid_col2, covid_col3], periods, colors)):
                period_data = covid_summary[covid_summary['CovidPeriod'] == period]
                if not period_data.empty:
                    data = period_data.iloc[0]
                    
                    with col:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, {color} 0%, #8B0000 100%); 
                                    padding: 1.5rem; border-radius: 10px; color: white; text-align: center; 
                                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                            <h3>🦠 {period}</h3>
                            <h2>{data['Wins']}/{data['Total_Games']}</h2>
                            <h1>{data['Win_Rate']}%</h1>
                            <small>{data['Points_Per_Game']} PPG | {data['Clean_Sheet_Rate']}% CS</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Enhanced chart selection
            st.markdown("### 📊 COVID Period Analysis Selection")
            covid_chart_selection = st.selectbox(
                "Choose COVID Analysis",
                ["All COVID Analysis", "Period Performance Comparison", "Timeline Impact Analysis", 
                 "Home vs Away COVID Impact", "Performance Metrics Deep Dive", "COVID Recovery Analysis"],
                index=0,
                key="covid_chart_selection"
            )
            
            # Chart 1: Period Performance Comparison
            if covid_chart_selection in ["All COVID Analysis", "Period Performance Comparison"]:
                st.markdown("#### 📈 Performance Comparison Across COVID Periods")
                
                comparison_col1, comparison_col2 = st.columns(2)
                
                with comparison_col1:
                    # Win Rate Comparison
                    fig_win_comparison = px.bar(
                        covid_summary,
                        x='CovidPeriod',
                        y='Win_Rate',
                        text='Win_Rate',
                        color='CovidPeriod',
                        color_discrete_map={'Pre-COVID': '#00A398', 'During COVID': '#C8102E', 'Post-COVID': '#FFD700'},
                        title='Win Rate by COVID Period',
                        template='plotly_white'
                    )
                    
                    fig_win_comparison.update_traces(
                        texttemplate='%{text}%',
                        textposition='outside'
                    )
                    
                    fig_win_comparison.update_layout(
                        showlegend=False,
                        yaxis=dict(range=[0, max(covid_summary['Win_Rate']) * 1.1])
                    )
                    
                    st.plotly_chart(fig_win_comparison, use_container_width=True)
                
                with comparison_col2:
                    # Points per Game Comparison
                    fig_ppg_comparison = px.bar(
                        covid_summary,
                        x='CovidPeriod',
                        y='Points_Per_Game',
                        text='Points_Per_Game',
                        color='CovidPeriod',
                        color_discrete_map={'Pre-COVID': '#00A398', 'During COVID': '#C8102E', 'Post-COVID': '#FFD700'},
                        title='Points per Game by COVID Period',
                        template='plotly_white'
                    )
                    
                    fig_ppg_comparison.update_traces(
                        texttemplate='%{text}',
                        textposition='outside'
                    )
                    
                    fig_ppg_comparison.update_layout(showlegend=False)
                    
                    st.plotly_chart(fig_ppg_comparison, use_container_width=True)
            
            # Chart 2: Timeline Impact Analysis
            if covid_chart_selection in ["All COVID Analysis", "Timeline Impact Analysis"]:
                st.markdown("#### 📅 COVID Impact Timeline Analysis")
                
                try:
                    # Show basic period comparison first
                    st.info("Showing COVID period analysis...")
                    
                    # Create the most basic analysis possible
                    period_data = []
                    
                    for period in ['Pre-COVID', 'During COVID', 'Post-COVID']:
                        period_matches = df[df['CovidPeriod'] == period]
                        
                        if len(period_matches) > 0:
                            total_games = len(period_matches)
                            wins = len(period_matches[period_matches['Result'] == 'Win'])
                            win_rate = round((wins / total_games) * 100, 1)
                            avg_goals = round(period_matches['GoalsFor'].mean(), 2)
                            
                            period_data.append({
                                'Period': period,
                                'Games': total_games,
                                'Wins': wins,
                                'Win_Rate': win_rate,
                                'Avg_Goals': avg_goals
                            })
                    
                    if period_data:
                        period_df = pd.DataFrame(period_data)
                        
                        # Create simple bar chart
                        fig_periods = px.bar(
                            period_df,
                            x='Period',
                            y='Win_Rate',
                            text='Win_Rate',
                            title='Win Rate by COVID Period',
                            color='Period',
                            color_discrete_map={'Pre-COVID': '#00A398', 'During COVID': '#C8102E', 'Post-COVID': '#FFD700'},
                            template='plotly_white'
                        )
                        
                        fig_periods.update_traces(
                            texttemplate='%{text}%',
                            textposition='outside'
                        )
                        
                        fig_periods.update_layout(
                            showlegend=False,
                            height=400
                        )
                        
                        st.plotly_chart(fig_periods, use_container_width=True)
                        
                        # Show detailed breakdown
                        st.markdown("##### 📊 Period Breakdown")
                        
                        breakdown_col1, breakdown_col2, breakdown_col3 = st.columns(3)
                        
                        for i, (col, data) in enumerate(zip([breakdown_col1, breakdown_col2, breakdown_col3], period_data)):
                            with col:
                                st.metric(
                                    label=f"{data['Period']}",
                                    value=f"{data['Win_Rate']}%",
                                    delta=f"{data['Wins']}/{data['Games']} games"
                                )
                        
                        # Try to create a simple yearly timeline
                        st.markdown("##### 📅 Yearly Performance Timeline")
                        
                        try:
                            # Simple yearly analysis
                            df_yearly = df.copy()
                            df_yearly['Year'] = df_yearly['Date'].dt.year
                            
                            yearly_data = []
                            for year in sorted(df_yearly['Year'].unique()):
                                year_data = df_yearly[df_yearly['Year'] == year]
                                if len(year_data) > 0:
                                    wins = len(year_data[year_data['Result'] == 'Win'])
                                    total = len(year_data)
                                    win_rate = round((wins / total) * 100, 1)
                                    
                                    # Determine COVID period for this year
                                    if year < 2020:
                                        covid_period = 'Pre-COVID'
                                    elif year <= 2021:
                                        covid_period = 'During COVID'
                                    else:
                                        covid_period = 'Post-COVID'
                                    
                                    yearly_data.append({
                                        'Year': str(year),
                                        'Win_Rate': win_rate,
                                        'Games': total,
                                        'CovidPeriod': covid_period
                                    })
                            
                            if yearly_data:
                                yearly_df = pd.DataFrame(yearly_data)
                                
                                fig_yearly = px.line(
                                    yearly_df,
                                    x='Year',
                                    y='Win_Rate',
                                    color='CovidPeriod',
                                    markers=True,
                                    title='Yearly Win Rate Timeline',
                                    color_discrete_map={'Pre-COVID': '#00A398', 'During COVID': '#C8102E', 'Post-COVID': '#FFD700'},
                                    template='plotly_white'
                                )
                                
                                fig_yearly.update_layout(height=400)
                                st.plotly_chart(fig_yearly, use_container_width=True)
                                
                        except Exception as yearly_error:
                            st.warning(f"Could not create yearly timeline: {str(yearly_error)}")
                    
                    else:
                        st.error("No COVID period data found")
                        
                except Exception as e:
                    st.error(f"Error in timeline analysis: {str(e)}")
                    
                    # Show absolute minimum - just the summary we already calculated
                    st.info("Showing basic COVID summary from main analysis...")
                    
                    # Use the covid_summary that was already calculated successfully
                    fig_fallback = px.bar(
                        covid_summary,
                        x='CovidPeriod',
                        y='Win_Rate',
                        text='Win_Rate',
                        title='COVID Period Win Rate (Fallback)',
                        template='plotly_white'
                    )
                    
                    fig_fallback.update_traces(
                        texttemplate='%{text}%',
                        textposition='outside'
                    )
                    
                    st.plotly_chart(fig_fallback, use_container_width=True)
            
            # Chart 3: Home vs Away COVID Impact
            if covid_chart_selection in ["All COVID Analysis", "Home vs Away COVID Impact"]:
                st.markdown("#### 🏠 COVID Impact: Home vs Away Analysis")
                
                venue_covid_analysis = df.groupby(['CovidPeriod', 'Venue']).agg({
                    'Result': ['count', lambda x: (x == 'Win').sum()],
                    'GoalsFor': 'mean',
                    'GoalsAgainst': 'mean',
                    'Points': 'mean'
                }).round(2)
                
                venue_covid_analysis.columns = ['Games', 'Wins', 'Avg_Goals_For', 'Avg_Goals_Against', 'Avg_Points']
                venue_covid_analysis['Win_Rate'] = ((venue_covid_analysis['Wins'] / venue_covid_analysis['Games']) * 100).round(1)
                venue_covid_analysis = venue_covid_analysis.reset_index()
                
                venue_col1, venue_col2 = st.columns(2)
                
                with venue_col1:
                    # Home advantage across periods
                    home_advantage_data = venue_covid_analysis.pivot(
                        index='CovidPeriod', 
                        columns='Venue', 
                        values='Win_Rate'
                    ).reset_index()
                    home_advantage_data['Home_Advantage'] = home_advantage_data['Home'] - home_advantage_data['Away']
                    
                    fig_home_advantage = px.bar(
                        home_advantage_data,
                        x='CovidPeriod',
                        y='Home_Advantage',
                        text='Home_Advantage',
                        title='Home Advantage by COVID Period',
                        color='Home_Advantage',
                        color_continuous_scale='RdYlGn',
                        template='plotly_white'
                    )
                    
                    fig_home_advantage.update_traces(
                        texttemplate='%{text:.1f}%',
                        textposition='outside'
                    )
                    
                    fig_home_advantage.update_layout(coloraxis_showscale=False)
                    
                    st.plotly_chart(fig_home_advantage, use_container_width=True)
                
                with venue_col2:
                    # Venue performance heatmap
                    venue_heatmap_data = venue_covid_analysis.pivot(
                        index='CovidPeriod',
                        columns='Venue',
                        values='Win_Rate'
                    )
                    
                    fig_venue_heatmap = px.imshow(
                        venue_heatmap_data,
                        color_continuous_scale='RdYlGn',
                        title='Win Rate Heatmap: COVID Periods vs Venue',
                        aspect='auto',
                        text_auto='.1f'
                    )
                    
                    st.plotly_chart(fig_venue_heatmap, use_container_width=True)
            
            # Chart 4: Performance Metrics Deep Dive
            if covid_chart_selection in ["All COVID Analysis", "Performance Metrics Deep Dive"]:
                st.markdown("#### 🎯 Performance Metrics Deep Dive")
                
                metrics_col1, metrics_col2 = st.columns(2)
                
                with metrics_col1:
                    # Goals analysis
                    goals_data = covid_summary.melt(
                        id_vars='CovidPeriod',
                        value_vars=['Avg_Goals_For', 'Avg_Goals_Against'],
                        var_name='Goal_Type',
                        value_name='Goals'
                    )
                    
                    fig_goals_analysis = px.bar(
                        goals_data,
                        x='CovidPeriod',
                        y='Goals',
                        color='Goal_Type',
                        barmode='group',
                        title='Goals Analysis by COVID Period',
                        color_discrete_map={'Avg_Goals_For': '#C8102E', 'Avg_Goals_Against': '#7F7F7F'},
                        template='plotly_white'
                    )
                    
                    fig_goals_analysis.update_traces(text=goals_data['Goals'].round(2), textposition='outside')
                    
                    st.plotly_chart(fig_goals_analysis, use_container_width=True)
                
                with metrics_col2:
                    # Clean sheet analysis
                    fig_clean_sheets = px.bar(
                        covid_summary,
                        x='CovidPeriod',
                        y='Clean_Sheet_Rate',
                        text='Clean_Sheet_Rate',
                        color='CovidPeriod',
                        title='Clean Sheet Rate by COVID Period',
                        color_discrete_map={'Pre-COVID': '#00A398', 'During COVID': '#C8102E', 'Post-COVID': '#FFD700'},
                        template='plotly_white'
                    )
                    
                    fig_clean_sheets.update_traces(
                        texttemplate='%{text}%',
                        textposition='outside'
                    )
                    
                    fig_clean_sheets.update_layout(showlegend=False)
                    
                    st.plotly_chart(fig_clean_sheets, use_container_width=True)
            
            # Chart 5: COVID Recovery Analysis
            if covid_chart_selection in ["All COVID Analysis", "COVID Recovery Analysis"]:
                st.markdown("#### 🔄 COVID Recovery & Adaptation Analysis")
                
                try:
                    # Quarterly performance to show recovery pattern
                    df_recovery = df.copy()
                    df_recovery['Quarter'] = df_recovery['Date'].dt.to_period('Q')
                    
                    # Group quarterly data properly
                    quarterly_groups = df_recovery.groupby(['Quarter', 'CovidPeriod'])
                    quarterly_wins = quarterly_groups['Result'].apply(lambda x: (x == 'Win').sum()).reset_index()
                    quarterly_games = quarterly_groups.size().reset_index(name='Games')
                    quarterly_goals = quarterly_groups['GoalsFor'].mean().reset_index()
                    quarterly_points = quarterly_groups['Points'].sum().reset_index()
                    
                    # Merge quarterly data
                    quarterly_analysis = quarterly_wins.merge(quarterly_games, on=['Quarter', 'CovidPeriod'])
                    quarterly_analysis = quarterly_analysis.merge(quarterly_goals, on=['Quarter', 'CovidPeriod'])
                    quarterly_analysis = quarterly_analysis.merge(quarterly_points, on=['Quarter', 'CovidPeriod'])
                    
                    quarterly_analysis.columns = ['Quarter', 'CovidPeriod', 'Wins', 'Games', 'Avg_Goals', 'Total_Points']
                    
                    quarterly_analysis['Win_Rate'] = ((quarterly_analysis['Wins'] / quarterly_analysis['Games']) * 100).round(1)
                    quarterly_analysis['Points_Per_Game'] = (quarterly_analysis['Total_Points'] / quarterly_analysis['Games']).round(2)
                    quarterly_analysis['Quarter_str'] = quarterly_analysis['Quarter'].astype(str)
                    
                    # Focus on 2019-2022 for recovery analysis and filter valid data
                    recovery_data = quarterly_analysis[
                        (quarterly_analysis['Quarter_str'] >= '2019Q1') & 
                        (quarterly_analysis['Quarter_str'] <= '2022Q4') &
                        (quarterly_analysis['Games'] > 0)
                    ].copy()
                    
                    if not recovery_data.empty:
                        recovery_col1, recovery_col2 = st.columns(2)
                        
                        with recovery_col1:
                            # Recovery trend line with simplified approach
                            recovery_data_sorted = recovery_data.sort_values('Quarter_str')
                            
                            # Simple scatter plot without complex trendline
                            fig_recovery = px.scatter(
                                recovery_data_sorted,
                                x='Quarter_str',
                                y='Win_Rate',
                                color='CovidPeriod',
                                size='Games',
                                title='Quarterly Win Rate: COVID Recovery Pattern',
                                color_discrete_map={'Pre-COVID': '#00A398', 'During COVID': '#C8102E', 'Post-COVID': '#FFD700'},
                                template='plotly_white'
                            )
                            
                            # Add a simple line connecting the points
                            fig_recovery.add_trace(go.Scatter(
                                x=recovery_data_sorted['Quarter_str'],
                                y=recovery_data_sorted['Win_Rate'],
                                mode='lines',
                                name='Trend',
                                line=dict(dash='dash', color='gray', width=1),
                                showlegend=False
                            ))
                            
                            fig_recovery.update_layout(
                                xaxis_tickangle=45,
                                height=400,
                                xaxis_title='Quarter'
                            )
                            
                            st.plotly_chart(fig_recovery, use_container_width=True)
                        
                        with recovery_col2:
                            # Performance consistency analysis
                            if len(recovery_data['CovidPeriod'].unique()) > 1:
                                consistency_data = recovery_data.groupby('CovidPeriod')['Win_Rate'].agg(['mean', 'std']).reset_index()
                                consistency_data.columns = ['CovidPeriod', 'Avg_Win_Rate', 'Win_Rate_Std']
                                # Handle NaN std (when only one data point)
                                consistency_data['Win_Rate_Std'] = consistency_data['Win_Rate_Std'].fillna(0)
                                consistency_data['Consistency_Score'] = (consistency_data['Avg_Win_Rate'] / (consistency_data['Win_Rate_Std'] + 1)).round(2)
                                
                                fig_consistency = px.bar(
                                    consistency_data,
                                    x='CovidPeriod',
                                    y='Consistency_Score',
                                    text='Consistency_Score',
                                    color='CovidPeriod',
                                    title='Performance Consistency Score',
                                    color_discrete_map={'Pre-COVID': '#00A398', 'During COVID': '#C8102E', 'Post-COVID': '#FFD700'},
                                    template='plotly_white'
                                )
                                
                                fig_consistency.update_traces(textposition='outside')
                                fig_consistency.update_layout(showlegend=False, height=400)
                                
                                st.plotly_chart(fig_consistency, use_container_width=True)
                            else:
                                st.info("Insufficient data for consistency analysis across COVID periods.")
                    else:
                        st.warning("No sufficient quarterly data found for recovery analysis.")
                        
                except Exception as e:
                    st.error(f"Error in recovery analysis: {str(e)}")
                    # Show simplified recovery analysis
                    st.info("Showing simplified recovery metrics...")
                    
                    simple_recovery = covid_summary[['CovidPeriod', 'Win_Rate', 'Points_Per_Game']].copy()
                    
                    fig_simple_recovery = px.bar(
                        simple_recovery,
                        x='CovidPeriod',
                        y='Points_Per_Game',
                        title='Points per Game by COVID Period',
                        color='CovidPeriod',
                        color_discrete_map={'Pre-COVID': '#00A398', 'During COVID': '#C8102E', 'Post-COVID': '#FFD700'}
                    )
                    
                    st.plotly_chart(fig_simple_recovery, use_container_width=True)
            
            # Enhanced breakdown tables
            st.markdown("### 📋 Comprehensive COVID Period Analysis")
            
            detailed_col1, detailed_col2 = st.columns(2)
            
            with detailed_col1:
                st.markdown("#### 📊 Performance Summary")
                display_covid_summary = covid_summary.copy()
                display_covid_summary = display_covid_summary[[
                    'CovidPeriod', 'Total_Games', 'Wins', 'Draws', 'Losses', 
                    'Win_Rate', 'Points_Per_Game', 'Clean_Sheet_Rate'
                ]]
                display_covid_summary.columns = [
                    'Period', 'Games', 'Wins', 'Draws', 'Losses', 
                    'Win %', 'PPG', 'Clean Sheet %'
                ]
                
                st.dataframe(
                    display_covid_summary.style.background_gradient(
                        subset=['Win %', 'PPG', 'Clean Sheet %'], 
                        cmap='RdYlGn'
                    ),
                    use_container_width=True
                )
            
            with detailed_col2:
                st.markdown("#### ⚽ Goals Analysis")
                goals_summary = covid_summary[[
                    'CovidPeriod', 'Avg_Goals_For', 'Avg_Goals_Against', 'Avg_Goal_Diff'
                ]].copy()
                goals_summary.columns = ['Period', 'Goals For/Game', 'Goals Against/Game', 'Goal Diff/Game']
                
                st.dataframe(
                    goals_summary.style.background_gradient(
                        subset=['Goals For/Game', 'Goal Diff/Game'], 
                        cmap='RdYlGn'
                    ).background_gradient(
                        subset=['Goals Against/Game'], 
                        cmap='RdYlGn_r'  # Reverse for goals against (lower is better)
                    ),
                    use_container_width=True
                )
            
            # Key insights section
            st.markdown("### 🎯 Key COVID Impact Insights")
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            # Calculate key comparisons
            pre_covid = covid_summary[covid_summary['CovidPeriod'] == 'Pre-COVID'].iloc[0]
            during_covid = covid_summary[covid_summary['CovidPeriod'] == 'During COVID'].iloc[0]
            post_covid = covid_summary[covid_summary['CovidPeriod'] == 'Post-COVID'].iloc[0]
            
            with insight_col1:
                win_rate_impact = during_covid['Win_Rate'] - pre_covid['Win_Rate']
                ppg_impact = during_covid['Points_Per_Game'] - pre_covid['Points_Per_Game']
                
                if win_rate_impact >= 0:
                    st.success(f"📈 **COVID Resilience:** Win rate {win_rate_impact:+.1f}% during COVID")
                else:
                    st.error(f"📉 **COVID Impact:** Win rate {win_rate_impact:.1f}% during COVID")
                
                st.info(f"📊 **Points Impact:** {ppg_impact:+.2f} PPG during COVID")
            
            with insight_col2:
                goals_impact = during_covid['Avg_Goals_For'] - pre_covid['Avg_Goals_For']
                defense_impact = during_covid['Avg_Goals_Against'] - pre_covid['Avg_Goals_Against']
                
                if goals_impact >= 0:
                    st.success(f"⚽ **Attack:** {goals_impact:+.2f} goals/game during COVID")
                else:
                    st.warning(f"⚽ **Attack:** {goals_impact:.2f} goals/game during COVID")
                
                if defense_impact <= 0:
                    st.success(f"🛡️ **Defense:** {defense_impact:+.2f} goals against/game")
                else:
                    st.warning(f"🛡️ **Defense:** {defense_impact:+.2f} goals against/game")
            
            with insight_col3:
                recovery_rate = post_covid['Win_Rate'] - during_covid['Win_Rate']
                recovery_ppg = post_covid['Points_Per_Game'] - during_covid['Points_Per_Game']
                
                if recovery_rate > 0:
                    st.success(f"🔄 **Recovery:** {recovery_rate:+.1f}% win rate improvement")
                else:
                    st.warning(f"🔄 **Recovery:** {recovery_rate:.1f}% win rate change")
                
                st.info(f"📈 **PPG Recovery:** {recovery_ppg:+.2f} points per game")
            
            # Overall COVID impact assessment
            overall_impact = "Positive" if during_covid['Win_Rate'] >= pre_covid['Win_Rate'] else "Negative"
            recovery_status = "Strong" if post_covid['Win_Rate'] > during_covid['Win_Rate'] else "Ongoing"
            
            st.markdown(f"""
            ### 🏥 COVID Impact Assessment
            
            **Overall Impact:** {overall_impact} - Liverpool's performance during COVID was {'better than' if overall_impact == 'Positive' else 'worse than'} pre-pandemic levels.
            
            **Recovery Status:** {recovery_status} - Post-COVID performance shows {'significant improvement' if recovery_status == 'Strong' else 'continued adaptation'}.
            
            **Key Findings:**
            - Pre-COVID: {pre_covid['Win_Rate']:.1f}% win rate, {pre_covid['Points_Per_Game']:.2f} PPG
            - During COVID: {during_covid['Win_Rate']:.1f}% win rate, {during_covid['Points_Per_Game']:.2f} PPG
            - Post-COVID: {post_covid['Win_Rate']:.1f}% win rate, {post_covid['Points_Per_Game']:.2f} PPG
            """)
            
        except FileNotFoundError:
            st.error("❌ Error: 'Liverpool_2015_2023_Matches.csv' file not found.")
            st.info("""
            📋 **To use this dashboard:**
            1. Place your 'Liverpool_2015_2023_Matches.csv' file in the same directory as this script
            2. Make sure the CSV has columns: 'Date', 'Home', 'Away', 'HomeGoals', 'AwayGoals'
            3. Refresh the page
            """)
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    with tab3:
        st.markdown("""
        <div class="tab-content">
            <h3>📈 Timeline & Goals</h3>
            <p>Comprehensive goal scoring patterns and performance timeline analysis (2015-2023)</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load the complete dataset
            df = pd.read_csv('Liverpool_2015_2023_Matches.csv')
            
            # Add comprehensive data preparation
            df['Venue'] = df.apply(lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1)
            
            def get_result(row):
                if row['Venue'] == 'Home':
                    return 'Win' if row['HomeGoals'] > row['AwayGoals'] else 'Draw' if row['HomeGoals'] == row['AwayGoals'] else 'Loss'
                else:
                    return 'Win' if row['AwayGoals'] > row['HomeGoals'] else 'Draw' if row['AwayGoals'] == row['HomeGoals'] else 'Loss'
            
            df['Result'] = df.apply(get_result, axis=1)
            
            # Enhanced date and time processing
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
            df['Quarter'] = df['Date'].dt.quarter
            
            # Goal analysis columns
            df['GoalsFor'] = df.apply(lambda row: row['HomeGoals'] if row['Venue'] == 'Home' else row['AwayGoals'], axis=1)
            df['GoalsAgainst'] = df.apply(lambda row: row['AwayGoals'] if row['Venue'] == 'Home' else row['HomeGoals'], axis=1)
            df['GoalDifference'] = df['GoalsFor'] - df['GoalsAgainst']
            df['Points'] = df['Result'].map({'Win': 3, 'Draw': 1, 'Loss': 0})
            
            # Season creation with proper mapping
            df['Season'] = df['Year'].apply(lambda x: f"{x-1}-{str(x)[2:]}" if x > 2015 else "2014-15")
            
            # Goal scoring categories
            def goal_category(goals):
                if goals == 0:
                    return 'No Goals'
                elif goals == 1:
                    return '1 Goal'
                elif goals == 2:
                    return '2 Goals'
                elif goals == 3:
                    return '3 Goals'
                else:
                    return '4+ Goals'
            
            df['GoalCategory'] = df['GoalsFor'].apply(goal_category)
            
            # Enhanced summary statistics
            st.markdown("### 📊 Enhanced Timeline Summary Statistics")
            
            timeline_col1, timeline_col2, timeline_col3, timeline_col4 = st.columns(4)
            
            with timeline_col1:
                total_wins = len(df[df['Result'] == 'Win'])
                total_matches = len(df)
                win_rate = round((total_wins / total_matches * 100), 1) if total_matches > 0 else 0
                total_goals = df['GoalsFor'].sum()
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏆 Overall Performance</h3>
                    <h2>{total_wins}/{total_matches}</h2>
                    <h1>{win_rate}%</h1>
                    <small>{total_goals} Total Goals</small>
                </div>
                """, unsafe_allow_html=True)
            
            with timeline_col2:
                home_wins = len(df[(df['Result'] == 'Win') & (df['Venue'] == 'Home')])
                home_matches = len(df[df['Venue'] == 'Home'])
                home_win_rate = round((home_wins / home_matches * 100), 1) if home_matches > 0 else 0
                home_goals = df[df['Venue'] == 'Home']['GoalsFor'].sum()
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏠 Home (Anfield)</h3>
                    <h2>{home_wins}/{home_matches}</h2>
                    <h1>{home_win_rate}%</h1>
                    <small>{home_goals} Goals</small>
                </div>
                """, unsafe_allow_html=True)
            
            with timeline_col3:
                away_wins = len(df[(df['Result'] == 'Win') & (df['Venue'] == 'Away')])
                away_matches = len(df[df['Venue'] == 'Away'])
                away_win_rate = round((away_wins / away_matches * 100), 1) if away_matches > 0 else 0
                away_goals = df[df['Venue'] == 'Away']['GoalsFor'].sum()
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>✈️ Away</h3>
                    <h2>{away_wins}/{away_matches}</h2>
                    <h1>{away_win_rate}%</h1>
                    <small>{away_goals} Goals</small>
                </div>
                """, unsafe_allow_html=True)
            
            with timeline_col4:
                avg_goals = round(df['GoalsFor'].mean(), 2) if not df['GoalsFor'].isna().all() else 0
                best_season = df.groupby('Season')['GoalsFor'].mean().idxmax()
                best_season_avg = round(df.groupby('Season')['GoalsFor'].mean().max(), 2)
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚽ Goals Analysis</h3>
                    <h2>{avg_goals}</h2>
                    <h1>Per Game</h1>
                    <small>Best: {best_season_avg} ({best_season})</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced chart selection with comprehensive options
            st.markdown("### 📊 Comprehensive Timeline Analysis")
            chart_selection = st.selectbox(
                "Choose Analysis Type",
                ["All Timeline Analysis", "Performance Overview", "Goal Scoring Patterns", "Seasonal Trends", 
                 "Monthly Performance", "Result Distribution", "Goal Categories Analysis", "Performance Timeline",
                 "Advanced Goal Analysis", "Venue Comparison Deep Dive"],
                index=0,
                key="timeline_chart_selection"
            )
            
            # Chart 1: Performance Overview
            if chart_selection in ["All Timeline Analysis", "Performance Overview"]:
                st.markdown("#### 🏆 Liverpool Performance Overview (2015-2023)")
                
                overview_col1, overview_col2 = st.columns(2)
                
                with overview_col1:
                    # Win rate comparison home vs away
                    wins_venue = df.groupby('Venue').agg({
                        'Result': ['count', lambda x: (x == 'Win').sum(), lambda x: (x == 'Draw').sum(), lambda x: (x == 'Loss').sum()]
                    }).reset_index()
                    wins_venue.columns = ['Venue', 'Total', 'Wins', 'Draws', 'Losses']
                    wins_venue['Win_Rate'] = (wins_venue['Wins'] / wins_venue['Total'] * 100).round(1)
                    
                    fig_overview = px.bar(
                        wins_venue,
                        x='Venue',
                        y='Win_Rate',
                        text='Win_Rate',
                        color='Venue',
                        title='Win Rate: Home vs Away',
                        color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'},
                        template='plotly_white'
                    )
                    
                    fig_overview.update_traces(
                        texttemplate='%{text}%',
                        textposition='outside'
                    )
                    
                    fig_overview.update_layout(showlegend=False, height=400)
                    
                    st.plotly_chart(fig_overview, use_container_width=True)
                
                with overview_col2:
                    # Goals comparison
                    goals_venue = df.groupby('Venue')['GoalsFor'].agg(['sum', 'mean']).reset_index()
                    goals_venue.columns = ['Venue', 'Total_Goals', 'Avg_Goals']
                    
                    fig_goals_overview = px.bar(
                        goals_venue,
                        x='Venue',
                        y='Avg_Goals',
                        text='Avg_Goals',
                        color='Venue',
                        title='Average Goals per Game',
                        color_discrete_map={'Home': '#FF6B35', 'Away': '#004E89'},
                        template='plotly_white'
                    )
                    
                    fig_goals_overview.update_traces(
                        texttemplate='%{text:.2f}',
                        textposition='outside'
                    )
                    
                    fig_goals_overview.update_layout(showlegend=False, height=400)
                    
                    st.plotly_chart(fig_goals_overview, use_container_width=True)
            
            # Chart 2: Goal Scoring Patterns
            if chart_selection in ["All Timeline Analysis", "Goal Scoring Patterns"]:
                st.markdown("#### ⚽ Goal Scoring Patterns Analysis")
                
                patterns_col1, patterns_col2 = st.columns(2)
                
                with patterns_col1:
                    # Goal frequency distribution
                    goal_freq = df['GoalsFor'].value_counts().sort_index().reset_index()
                    goal_freq.columns = ['Goals', 'Frequency']
                    
                    fig_goal_freq = px.bar(
                        goal_freq,
                        x='Goals',
                        y='Frequency',
                        text='Frequency',
                        title='Goal Frequency Distribution',
                        color='Goals',
                        color_continuous_scale='Reds',
                        template='plotly_white'
                    )
                    
                    fig_goal_freq.update_traces(textposition='outside')
                    fig_goal_freq.update_layout(coloraxis_showscale=False, height=400)
                    
                    st.plotly_chart(fig_goal_freq, use_container_width=True)
                
                with patterns_col2:
                    # Goal categories pie chart
                    goal_cat_counts = df['GoalCategory'].value_counts().reset_index()
                    goal_cat_counts.columns = ['Category', 'Count']
                    
                    fig_goal_categories = px.pie(
                        goal_cat_counts,
                        values='Count',
                        names='Category',
                        title='Goal Categories Distribution',
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        template='plotly_white'
                    )
                    
                    fig_goal_categories.update_traces(
                        textposition='inside',
                        textinfo='percent+label'
                    )
                    
                    fig_goal_categories.update_layout(height=400)
                    
                    st.plotly_chart(fig_goal_categories, use_container_width=True)
            
            # Chart 3: Seasonal Trends
            if chart_selection in ["All Timeline Analysis", "Seasonal Trends"]:
                st.markdown("#### 📅 Seasonal Performance Trends (2015-2023)")
                
                seasonal_col1, seasonal_col2 = st.columns(2)
                
                with seasonal_col1:
                    # Season-by-season win rate
                    seasonal_performance = df.groupby(['Season', 'Venue']).agg({
                        'Result': ['count', lambda x: (x == 'Win').sum()],
                        'GoalsFor': 'mean'
                    }).reset_index()
                    
                    seasonal_performance.columns = ['Season', 'Venue', 'Games', 'Wins', 'Avg_Goals']
                    seasonal_performance['Win_Rate'] = (seasonal_performance['Wins'] / seasonal_performance['Games'] * 100).round(1)
                    
                    fig_seasonal_wr = px.line(
                        seasonal_performance,
                        x='Season',
                        y='Win_Rate',
                        color='Venue',
                        markers=True,
                        title='Win Rate by Season',
                        color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'},
                        template='plotly_white'
                    )
                    
                    fig_seasonal_wr.update_layout(
                        xaxis_tickangle=45,
                        height=450
                    )
                    
                    st.plotly_chart(fig_seasonal_wr, use_container_width=True)
                
                with seasonal_col2:
                    # Season goals trend
                    fig_seasonal_goals = px.line(
                        seasonal_performance,
                        x='Season',
                        y='Avg_Goals',
                        color='Venue',
                        markers=True,
                        title='Average Goals by Season',
                        color_discrete_map={'Home': '#FF6B35', 'Away': '#004E89'},
                        template='plotly_white'
                    )
                    
                    fig_seasonal_goals.update_layout(
                        xaxis_tickangle=45,
                        height=450
                    )
                    
                    st.plotly_chart(fig_seasonal_goals, use_container_width=True)
            
            # Chart 4: Monthly Performance
            if chart_selection in ["All Timeline Analysis", "Monthly Performance"]:
                st.markdown("#### 📆 Monthly Performance Analysis")
                
                # Create month names
                month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
                
                monthly_performance = df.groupby(['Month', 'Venue']).agg({
                    'Result': ['count', lambda x: (x == 'Win').sum()],
                    'GoalsFor': 'mean',
                    'Points': 'mean'
                }).reset_index()
                
                monthly_performance.columns = ['Month', 'Venue', 'Games', 'Wins', 'Avg_Goals', 'Avg_Points']
                monthly_performance['Win_Rate'] = (monthly_performance['Wins'] / monthly_performance['Games'] * 100).round(1)
                monthly_performance['Month_Name'] = monthly_performance['Month'].map(month_names)
                
                monthly_col1, monthly_col2 = st.columns(2)
                
                with monthly_col1:
                    # Monthly win rate heatmap
                    monthly_pivot = monthly_performance.pivot(index='Month_Name', columns='Venue', values='Win_Rate')
                    
                    fig_monthly_heatmap = px.imshow(
                        monthly_pivot,
                        color_continuous_scale='RdYlGn',
                        title='Monthly Win Rate Heatmap',
                        aspect='auto',
                        text_auto='.1f'
                    )
                    
                    fig_monthly_heatmap.update_layout(
                        xaxis_title='Venue',
                        yaxis_title='Month',
                        height=400
                    )
                    
                    st.plotly_chart(fig_monthly_heatmap, use_container_width=True)
                
                with monthly_col2:
                    # Monthly goals analysis
                    fig_monthly_goals = px.bar(
                        monthly_performance,
                        x='Month_Name',
                        y='Avg_Goals',
                        color='Venue',
                        barmode='group',
                        title='Average Goals by Month',
                        color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'},
                        template='plotly_white'
                    )
                    
                    fig_monthly_goals.update_layout(height=400)
                    
                    st.plotly_chart(fig_monthly_goals, use_container_width=True)
            
            # Chart 5: Result Distribution
            if chart_selection in ["All Timeline Analysis", "Result Distribution"]:
                st.markdown("#### ⚖️ Result Distribution Analysis")
                
                result_col1, result_col2 = st.columns(2)
                
                with result_col1:
                    # Overall result distribution
                    result_counts = df['Result'].value_counts().reset_index()
                    result_counts.columns = ['Result', 'Count']
                    
                    fig_result_dist = px.pie(
                        result_counts,
                        values='Count',
                        names='Result',
                        title='Overall Result Distribution',
                        color_discrete_map={'Win': '#00B04F', 'Draw': '#FFD23F', 'Loss': '#D32F2F'},
                        template='plotly_white'
                    )
                    
                    fig_result_dist.update_traces(
                        textposition='inside',
                        textinfo='percent+label'
                    )
                    
                    fig_result_dist.update_layout(height=400)
                    
                    st.plotly_chart(fig_result_dist, use_container_width=True)
                
                with result_col2:
                    # Result distribution by venue
                    venue_results = df.groupby(['Venue', 'Result']).size().reset_index(name='Count')
                    venue_results['Percentage'] = venue_results['Count'] / venue_results.groupby('Venue')['Count'].transform('sum') * 100
                    
                    fig_venue_results = px.bar(
                        venue_results,
                        x='Venue',
                        y='Percentage',
                        color='Result',
                        title='Result Distribution by Venue',
                        color_discrete_map={'Win': '#00B04F', 'Draw': '#FFD23F', 'Loss': '#D32F2F'},
                        template='plotly_white'
                    )
                    
                    fig_venue_results.update_traces(
                        text=venue_results['Percentage'].round(1),
                        texttemplate='%{text}%',
                        textposition='inside'
                    )
                    
                    fig_venue_results.update_layout(height=400)
                    
                    st.plotly_chart(fig_venue_results, use_container_width=True)
            
            # Chart 6: Goal Categories Analysis
            if chart_selection in ["All Timeline Analysis", "Goal Categories Analysis"]:
                st.markdown("#### 🎯 Goal Categories Deep Dive")
                
                goal_cat_col1, goal_cat_col2 = st.columns(2)
                
                with goal_cat_col1:
                    # Goal categories by venue
                    goal_cat_venue = df.groupby(['Venue', 'GoalCategory']).size().reset_index(name='Count')
                    
                    fig_goal_cat_venue = px.bar(
                        goal_cat_venue,
                        x='GoalCategory',
                        y='Count',
                        color='Venue',
                        barmode='group',
                        title='Goal Categories by Venue',
                        color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'},
                        template='plotly_white'
                    )
                    
                    fig_goal_cat_venue.update_layout(
                        xaxis_title='Goal Category',
                        height=400
                    )
                    
                    st.plotly_chart(fig_goal_cat_venue, use_container_width=True)
                
                with goal_cat_col2:
                    # Win rate by goal category
                    goal_cat_wins = df.groupby('GoalCategory').agg({
                        'Result': ['count', lambda x: (x == 'Win').sum()]
                    }).reset_index()
                    
                    goal_cat_wins.columns = ['GoalCategory', 'Total', 'Wins']
                    goal_cat_wins['Win_Rate'] = (goal_cat_wins['Wins'] / goal_cat_wins['Total'] * 100).round(1)
                    
                    fig_goal_cat_wr = px.bar(
                        goal_cat_wins,
                        x='GoalCategory',
                        y='Win_Rate',
                        text='Win_Rate',
                        title='Win Rate by Goal Category',
                        color='Win_Rate',
                        color_continuous_scale='RdYlGn',
                        template='plotly_white'
                    )
                    
                    fig_goal_cat_wr.update_traces(
                        texttemplate='%{text}%',
                        textposition='outside'
                    )
                    
                    fig_goal_cat_wr.update_layout(
                        coloraxis_showscale=False,
                        height=400
                    )
                    
                    st.plotly_chart(fig_goal_cat_wr, use_container_width=True)
            
            # Chart 7: Performance Timeline
            if chart_selection in ["All Timeline Analysis", "Performance Timeline"]:
                st.markdown("#### 📈 Liverpool Performance Timeline Evolution")
                
                # Create cumulative performance metrics
                df_sorted = df.sort_values('Date').reset_index(drop=True)
                df_sorted['Cumulative_Wins'] = (df_sorted['Result'] == 'Win').cumsum()
                df_sorted['Cumulative_Games'] = range(1, len(df_sorted) + 1)
                df_sorted['Cumulative_Win_Rate'] = (df_sorted['Cumulative_Wins'] / df_sorted['Cumulative_Games'] * 100).round(2)
                df_sorted['Cumulative_Goals'] = df_sorted['GoalsFor'].cumsum()
                df_sorted['Cumulative_Points'] = df_sorted['Points'].cumsum()
                
                timeline_col1, timeline_col2 = st.columns(2)
                
                with timeline_col1:
                    # Cumulative win rate evolution
                    fig_cumulative_wr = px.line(
                        df_sorted,
                        x='Date',
                        y='Cumulative_Win_Rate',
                        title='Cumulative Win Rate Evolution',
                        template='plotly_white'
                    )
                    
                    fig_cumulative_wr.update_traces(line_color='#C8102E', line_width=3)
                    
                    fig_cumulative_wr.update_layout(
                        yaxis_title='Cumulative Win Rate (%)',
                        height=400
                    )
                    
                    st.plotly_chart(fig_cumulative_wr, use_container_width=True)
                
                with timeline_col2:
                    # Goals progression
                    fig_goals_progression = px.line(
                        df_sorted,
                        x='Date',
                        y='Cumulative_Goals',
                        title='Total Goals Progression',
                        template='plotly_white'
                    )
                    
                    fig_goals_progression.update_traces(line_color='#FF6B35', line_width=3)
                    
                    fig_goals_progression.update_layout(
                        yaxis_title='Total Goals',
                        height=400
                    )
                    
                    st.plotly_chart(fig_goals_progression, use_container_width=True)
            
            # Chart 8: Advanced Goal Analysis
            if chart_selection in ["All Timeline Analysis", "Advanced Goal Analysis"]:
                st.markdown("#### 🔥 Advanced Goal Scoring Analysis")
                
                advanced_col1, advanced_col2 = st.columns(2)
                
                with advanced_col1:
                    # Goals vs results correlation
                    goal_result_corr = df.groupby(['GoalsFor', 'Result']).size().reset_index(name='Count')
                    
                    fig_goal_result = px.scatter(
                        goal_result_corr,
                        x='GoalsFor',
                        y='Count',
                        color='Result',
                        size='Count',
                        title='Goals vs Results Correlation',
                        color_discrete_map={'Win': '#00B04F', 'Draw': '#FFD23F', 'Loss': '#D32F2F'},
                        template='plotly_white'
                    )
                    
                    fig_goal_result.update_layout(height=400)
                    
                    st.plotly_chart(fig_goal_result, use_container_width=True)
                
                with advanced_col2:
                    # Goal difference impact
                    goal_diff_results = df.groupby(['GoalDifference', 'Result']).size().reset_index(name='Count')
                    
                    fig_goal_diff = px.bar(
                        goal_diff_results,
                        x='GoalDifference',
                        y='Count',
                        color='Result',
                        title='Goal Difference vs Results',
                        color_discrete_map={'Win': '#00B04F', 'Draw': '#FFD23F', 'Loss': '#D32F2F'},
                        template='plotly_white'
                    )
                    
                    fig_goal_diff.update_layout(height=400)
                    
                    st.plotly_chart(fig_goal_diff, use_container_width=True)
            
            # Chart 9: Venue Comparison Deep Dive
            if chart_selection in ["All Timeline Analysis", "Venue Comparison Deep Dive"]:
                st.markdown("#### 🏠 vs ✈️ Comprehensive Venue Analysis")
                
                venue_deep_col1, venue_deep_col2 = st.columns(2)
                
                with venue_deep_col1:
                    # Box plot comparison of goals by venue
                    fig_venue_goals_box = px.box(
                        df,
                        x='Venue',
                        y='GoalsFor',
                        color='Venue',
                        title='Goal Distribution by Venue',
                        color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'},
                        template='plotly_white'
                    )
                    
                    fig_venue_goals_box.update_layout(showlegend=False, height=400)
                    
                    st.plotly_chart(fig_venue_goals_box, use_container_width=True)
                
                with venue_deep_col2:
                    # Performance metrics comparison
                    venue_metrics = df.groupby('Venue').agg({
                        'Result': 'count',
                        'GoalsFor': ['mean', 'sum'],
                        'GoalsAgainst': 'mean',
                        'Points': 'mean'
                    }).round(2)
                    
                    venue_metrics.columns = ['Games', 'Avg_Goals', 'Total_Goals', 'Avg_Against', 'Avg_Points']
                    venue_metrics = venue_metrics.reset_index()
                    
                    # Radar chart for venue comparison
                    fig_venue_radar = go.Figure()
                    
                    categories = ['Avg Goals', 'Avg Points', 'Total Goals (scaled)', 'Defensive (inverse)']
                    
                    for venue in venue_metrics['Venue']:
                        venue_data = venue_metrics[venue_metrics['Venue'] == venue].iloc[0]
                        
                        values = [
                            venue_data['Avg_Goals'],
                            venue_data['Avg_Points'],
                            venue_data['Total_Goals'] / 100,  # Scale down total goals
                            3 - venue_data['Avg_Against']  # Inverse for defensive performance
                        ]
                        
                        fig_venue_radar.add_trace(go.Scatterpolar(
                            r=values + [values[0]],
                            theta=categories + [categories[0]],
                            fill='toself',
                            name=venue,
                            line=dict(color='#C8102E' if venue == 'Home' else '#00A398')
                        ))
                    
                    fig_venue_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 3])
                        ),
                        title='Venue Performance Comparison',
                        height=400
                    )
                    
                    st.plotly_chart(fig_venue_radar, use_container_width=True)
            
            # Enhanced data tables and insights
            st.markdown("### 📋 Comprehensive Timeline Statistics")
            
            stats_col1, stats_col2 = st.columns(2)
            
            with stats_col1:
                st.markdown("#### 🏆 Season-by-Season Performance")
                
                season_comprehensive = df.groupby(['Season']).agg({
                    'Result': ['count', lambda x: (x == 'Win').sum(), lambda x: (x == 'Draw').sum(), lambda x: (x == 'Loss').sum()],
                    'GoalsFor': ['sum', 'mean'],
                    'GoalsAgainst': ['sum', 'mean'],
                    'Points': 'sum'
                }).round(2)
                
                season_comprehensive.columns = ['Games', 'Wins', 'Draws', 'Losses', 'Goals_For', 'Avg_Goals', 'Goals_Against', 'Avg_Against', 'Points']
                season_comprehensive['Win_Rate'] = (season_comprehensive['Wins'] / season_comprehensive['Games'] * 100).round(1)
                season_comprehensive['PPG'] = (season_comprehensive['Points'] / season_comprehensive['Games']).round(2)
                season_comprehensive = season_comprehensive.reset_index()
                
                display_season = season_comprehensive[['Season', 'Games', 'Wins', 'Win_Rate', 'Avg_Goals', 'PPG']].copy()
                display_season.columns = ['Season', 'Games', 'Wins', 'Win %', 'Goals/Game', 'PPG']
                
                st.dataframe(
                    display_season.style.background_gradient(
                        subset=['Win %', 'Goals/Game', 'PPG'], 
                        cmap='RdYlGn'
                    ),
                    use_container_width=True
                )
            
            with stats_col2:
                st.markdown("#### 📊 Venue Detailed Statistics")
                
                venue_detailed = df.groupby('Venue').agg({
                    'Result': ['count', lambda x: (x == 'Win').sum(), lambda x: (x == 'Draw').sum(), lambda x: (x == 'Loss').sum()],
                    'GoalsFor': ['sum', 'mean', 'max'],
                    'GoalsAgainst': ['sum', 'mean'],
                    'Points': 'sum'
                }).round(2)
                
                venue_detailed.columns = ['Games', 'Wins', 'Draws', 'Losses', 'Goals_For', 'Avg_Goals', 'Max_Goals', 'Goals_Against', 'Avg_Against', 'Points']
                venue_detailed['Win_Rate'] = (venue_detailed['Wins'] / venue_detailed['Games'] * 100).round(1)
                venue_detailed['Clean_Sheets'] = df.groupby('Venue')['GoalsAgainst'].apply(lambda x: (x == 0).sum()).values
                venue_detailed['PPG'] = (venue_detailed['Points'] / venue_detailed['Games']).round(2)
                venue_detailed = venue_detailed.reset_index()
                
                display_venue = venue_detailed[['Venue', 'Games', 'Wins', 'Win_Rate', 'Avg_Goals', 'Max_Goals', 'Clean_Sheets', 'PPG']].copy()
                display_venue.columns = ['Venue', 'Games', 'Wins', 'Win %', 'Avg Goals', 'Best Game', 'Clean Sheets', 'PPG']
                
                st.dataframe(
                    display_venue.style.background_gradient(
                        subset=['Win %', 'Avg Goals', 'PPG'], 
                        cmap='RdYlGn'
                    ),
                    use_container_width=True
                )
            
            # Key insights and trends
            st.markdown("### 🎯 Key Timeline Insights & Trends")
            
            insights_col1, insights_col2, insights_col3 = st.columns(3)
            
            # Calculate key insights
            best_season = season_comprehensive.loc[season_comprehensive['Win_Rate'].idxmax()]
            worst_season = season_comprehensive.loc[season_comprehensive['Win_Rate'].idxmin()]
            highest_scoring_season = season_comprehensive.loc[season_comprehensive['Avg_Goals'].idxmax()]
            
            with insights_col1:
                st.success(f"🏆 **Best Season:** {best_season['Season']} ({best_season['Win_Rate']}% win rate)")
                st.info(f"⚽ **Highest Scoring:** {highest_scoring_season['Season']} ({highest_scoring_season['Avg_Goals']} goals/game)")
                
                home_advantage = venue_detailed[venue_detailed['Venue'] == 'Home']['Win_Rate'].values[0] - \
                               venue_detailed[venue_detailed['Venue'] == 'Away']['Win_Rate'].values[0]
                st.info(f"🏠 **Home Advantage:** {home_advantage:.1f}% higher win rate at Anfield")
            
            with insights_col2:
                # Goal scoring trends
                total_goals_scored = df['GoalsFor'].sum()
                big_wins = len(df[df['GoalsFor'] >= 4])
                clean_sheets = len(df[df['GoalsAgainst'] == 0])
                
                st.info(f"🔥 **Total Goals (2015-2023):** {total_goals_scored}")
                st.success(f"💥 **4+ Goal Games:** {big_wins} matches")
                st.success(f"🥅 **Clean Sheets:** {clean_sheets} matches")
            
            with insights_col3:
                # Performance consistency
                season_win_rates = season_comprehensive['Win_Rate']
                consistency_std = season_win_rates.std().round(1)
                avg_win_rate = season_win_rates.mean().round(1)
                
                st.info(f"📊 **Average Win Rate:** {avg_win_rate}% across all seasons")
                st.info(f"📈 **Consistency:** {consistency_std}% standard deviation")
                
                if consistency_std < 10:
                    st.success("✅ **High Consistency** - Stable performance across seasons")
                elif consistency_std < 15:
                    st.warning("⚠️ **Moderate Consistency** - Some variation between seasons")
                else:
                    st.error("🔄 **Variable Performance** - Significant ups and downs")
            
            # Performance evolution summary
            st.markdown("### 📈 Performance Evolution Summary")
            
            evolution_summary = f"""
            **Liverpool's 2015-2023 Journey:**
            
            📊 **Overall Record:** {total_wins} wins in {total_matches} games ({win_rate}% win rate)
            
            🏠 **Home Performance:** {home_wins}/{home_matches} ({home_win_rate}% win rate) - Fortress Anfield
            
            ✈️ **Away Performance:** {away_wins}/{away_matches} ({away_win_rate}% win rate) - Road Warriors
            
            ⚽ **Goal Scoring:** {total_goals_scored} goals total ({avg_goals} per game average)
            
            🏆 **Peak Season:** {best_season['Season']} with {best_season['Win_Rate']}% win rate and {best_season['PPG']} points per game
            
            🔥 **Scoring Peak:** {highest_scoring_season['Season']} with {highest_scoring_season['Avg_Goals']} goals per game
            
            🎯 **Key Strength:** {home_advantage:.1f}% home advantage shows the power of Anfield
            
            📈 **Consistency:** {consistency_std}% variation in win rate shows {'excellent' if consistency_std < 10 else 'good' if consistency_std < 15 else 'mixed'} consistency
            """
            
            st.markdown(evolution_summary)
            
        except FileNotFoundError:
            st.error("❌ Error: 'Liverpool_2015_2023_Matches.csv' file not found.")
            st.info("""
            📋 **To use this dashboard:**
            1. Place your 'Liverpool_2015_2023_Matches.csv' file in the same directory as this script
            2. Make sure the CSV has columns: 'Date', 'Home', 'Away', 'HomeGoals', 'AwayGoals'
            3. Refresh the page
            """)
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    
    with tab4:
        st.markdown("""
        <div class="tab-content">
            <h3>📊 EPL xG Comparison</h3>
            <p>Expected Goals analysis compared to Premier League teams</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load EPL dataset
            df = pd.read_csv('EPL_result.csv')
            
            # Team abbreviations dictionary
            team_abb = {
                'Everton': 'EVE', 'Aston Villa': 'AVL', 'Leicester City': 'LEI', 'Arsenal': 'ARS',
                'Liverpool': 'LIV', 'Tottenham': 'TOT', 'Chelsea': 'CHE', 'Leeds United': 'LEE',
                'Newcastle Utd': 'NEW', 'West Ham': 'WHU', 'Southampton': 'SOU', 'Crystal Palace': 'CRY',
                'Wolves': 'WOL', 'Manchester City': 'MCI', 'Brighton': 'BHA', 'Manchester Utd': 'MUN',
                'West Brom': 'WBA', 'Burnley': 'BUR', 'Sheffield Utd': 'SHU', 'Fulham': 'FUL'
            }
            
            # Apply team abbreviations
            df['Home'] = df['Home'].apply(lambda x: team_abb[x])
            df['Away'] = df['Away'].apply(lambda x: team_abb[x])
            
            # Calculate additional metrics
            df['GD'] = df['G_Home'] - df['G_Away']
            df['Pts_Home'] = df['GD'].apply(lambda x: 3 if x > 0 else (0 if x < 0 else 1))
            df['Pts_Away'] = df['GD'].apply(lambda x: 0 if x > 0 else (3 if x < 0 else 1))
            
            # Set gameweek parameters
            gw_last = 7
            gw_next = gw_last + 1
            
            # Create comprehensive team statistics
            df_temp = pd.DataFrame({'Team': list(team_abb.values())})
            
            # Calculate matches played
            df_temp['M_h'] = df_temp['Team'].apply(lambda x: df[df['Home'] == x][df['GW'] < gw_next].count()[0])
            df_temp['M_a'] = df_temp['Team'].apply(lambda x: df[df['Away'] == x][df['GW'] < gw_next].count()[0])
            df_temp['M'] = df_temp['M_h'] + df_temp['M_a']
            
            # Calculate xG statistics (fixed deprecated syntax)
            df_temp['xG_h'] = df_temp['Team'].apply(lambda x: df.loc[(df['Home'] == x) & (df['GW'] < gw_next), 'xG_Home'].sum())
            df_temp['xG_a'] = df_temp['Team'].apply(lambda x: df.loc[(df['Away'] == x) & (df['GW'] < gw_next), 'xG_Away'].sum())
            df_temp['xG'] = df_temp['xG_a'] + df_temp['xG_h']
            df_temp['xGpm_h'] = df_temp['xG_h'] / df_temp['M_h']
            df_temp['xGpm_a'] = df_temp['xG_a'] / df_temp['M_a']
            df_temp['xGpm'] = df_temp['xG'] / df_temp['M']
            
            # Calculate xGA statistics (fixed deprecated syntax)
            df_temp['xGA_h'] = df_temp['Team'].apply(lambda x: df.loc[(df['Home'] == x) & (df['GW'] < gw_next), 'xG_Away'].sum())
            df_temp['xGA_a'] = df_temp['Team'].apply(lambda x: df.loc[(df['Away'] == x) & (df['GW'] < gw_next), 'xG_Home'].sum())
            df_temp['xGA'] = df_temp['xGA_a'] + df_temp['xGA_h']
            df_temp['xGApm_h'] = df_temp['xGA_h'] / df_temp['M_h']
            df_temp['xGApm_a'] = df_temp['xGA_a'] / df_temp['M_a']
            df_temp['xGApm'] = df_temp['xGA'] / df_temp['M']
            
            # Calculate deltas
            df_temp['delta_xGpm'] = df_temp['xGpm'] - df_temp['xGApm']
            df_temp['delta_xG_ha'] = df_temp['xG_h'] - df_temp['xG_a']
            
            # Calculate actual goals (fixed deprecated syntax)
            df_temp['G_h'] = df_temp['Team'].apply(lambda x: df.loc[(df['Home'] == x) & (df['GW'] < gw_next), 'G_Home'].sum())
            df_temp['G_a'] = df_temp['Team'].apply(lambda x: df.loc[(df['Away'] == x) & (df['GW'] < gw_next), 'G_Away'].sum())
            df_temp['G'] = df_temp['G_a'] + df_temp['G_h']
            
            # Display summary statistics
            st.markdown("### 📊 EPL xG Summary Statistics")
            
            # Find Liverpool's stats
            liverpool_stats = df_temp[df_temp['Team'] == 'LIV'].iloc[0]
            
            xg_col1, xg_col2, xg_col3, xg_col4 = st.columns(4)
            
            with xg_col1:
                liverpool_rank = (df_temp['xGpm'] > liverpool_stats['xGpm']).sum() + 1
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚽ Liverpool xG</h3>
                    <h2>{liverpool_stats['xGpm']:.2f}</h2>
                    <h1>#{liverpool_rank}</h1>
                    <small>Per Match (Rank)</small>
                </div>
                """, unsafe_allow_html=True)
            
            with xg_col2:
                liverpool_xga_rank = (df_temp['xGApm'] < liverpool_stats['xGApm']).sum() + 1
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🛡️ Liverpool xGA</h3>
                    <h2>{liverpool_stats['xGApm']:.2f}</h2>
                    <h1>#{liverpool_xga_rank}</h1>
                    <small>Per Match (Rank)</small>
                </div>
                """, unsafe_allow_html=True)
            
            with xg_col3:
                liverpool_delta_rank = (df_temp['delta_xGpm'] > liverpool_stats['delta_xGpm']).sum() + 1
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📈 Liverpool ΔxG</h3>
                    <h2>{liverpool_stats['delta_xGpm']:.2f}</h2>
                    <h1>#{liverpool_delta_rank}</h1>
                    <small>Difference (Rank)</small>
                </div>
                """, unsafe_allow_html=True)
            
            with xg_col4:
                best_xg_team = df_temp.loc[df_temp['xGpm'].idxmax(), 'Team']
                best_xg_value = df_temp['xGpm'].max()
                st.markdown(f"""
                <div class="metric-card">
                    <h3>👑 Best xG</h3>
                    <h2>{best_xg_team}</h2>
                    <h1>{best_xg_value:.2f}</h1>
                    <small>Per Match</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Chart selection
            st.markdown("### 📊 xG Analysis Charts")
            chart_selection = st.selectbox(
                "Choose Visualization",
                ["All Charts", "Home xG vs Goals", "xG vs xGA Comparison", "Dot Plot Analysis", 
                 "Delta xG Ranking", "xG Home vs Away", "Liverpool Season Performance"],
                index=0,
                key="xg_chart_selection"
            )
            
            # Chart 0: Home xG vs Actual Goals
            if chart_selection in ["All Charts", "Home xG vs Goals"]:
                st.markdown("#### ⚽ Average Home xG vs Actual Goals per Team")
                
                # Create home stats without abbreviations (use original team names)
                df_original = pd.read_csv('EPL_result.csv')  # Load original without abbreviations
                home_stats = df_original.groupby('Home').agg(
                    Avg_xG_Home=('xG_Home', 'mean'),
                    Avg_G_Home=('G_Home', 'mean')
                ).reset_index()
                
                # Melt for grouped bar
                home_stats_melted = home_stats.melt(
                    id_vars='Home',
                    value_vars=['Avg_xG_Home', 'Avg_G_Home'],
                    var_name='Metric',
                    value_name='Goals'
                )
                
                # Add highlighting for Liverpool
                home_stats_melted['Highlight'] = home_stats_melted['Home'].apply(
                    lambda x: 'Liverpool' if x == 'Liverpool' else 'Other'
                )
                
                # Create the plot
                fig_home = px.bar(
                    home_stats_melted,
                    x='Home',
                    y='Goals',
                    color='Metric',
                    barmode='group',
                    text='Goals',
                    title='⚽ Average Home xG vs Actual Goals per Team',
                    template='plotly_white',
                    color_discrete_map={
                        'Avg_xG_Home': '#1f77b4',  # royal blue
                        'Avg_G_Home': '#d62728'    # crimson red
                    }
                )
                
                # Aesthetic improvements
                fig_home.update_traces(
                    texttemplate='%{text:.2f}',
                    textposition='outside',
                    marker_line_color='white',
                    marker_line_width=1.2
                )
                
                fig_home.update_layout(
                    xaxis_title='Club (Home Games)',
                    yaxis_title='Goals (Average)',
                    font=dict(size=14),
                    xaxis_tickangle=45,
                    bargap=0.25
                )
                
                st.plotly_chart(fig_home, use_container_width=True)
            
            # Chart 1: xG vs xGA Horizontal Bar Chart
            if chart_selection in ["All Charts", "xG vs xGA Comparison"]:
                st.markdown("#### ⚖️ xG vs xGA per Match Comparison")
                
                # Sort by xGpm for better visualization
                df_sorted = df_temp.sort_values(by='xGpm', ascending=True)
                
                fig1 = go.Figure()
                
                fig1.add_trace(go.Bar(
                    x=df_sorted['xGpm'],
                    y=df_sorted['Team'],
                    name='xG per Match',
                    orientation='h',
                    marker=dict(color='#C8102E'),
                    hovertemplate='Team: %{y}<br>xG: %{x:.2f}<extra></extra>'
                ))
                
                fig1.add_trace(go.Bar(
                    x=df_sorted['xGApm'],
                    y=df_sorted['Team'],
                    name='xGA per Match',
                    orientation='h',
                    marker=dict(color='#00A398'),
                    hovertemplate='Team: %{y}<br>xGA: %{x:.2f}<extra></extra>'
                ))
                
                fig1.update_layout(
                    title='⚽ EPL: xG vs xGA per Match (Side-by-Side)',
                    barmode='group',
                    template='plotly_white',
                    height=600,
                    xaxis_title='Per Match Value'
                )
                
                st.plotly_chart(fig1, use_container_width=True)
            
            # Chart 2: Dot Plot (Lollipop Style)
            if chart_selection in ["All Charts", "Dot Plot Analysis"]:
                st.markdown("#### 🎯 xG vs xGA Dot Plot Analysis")
                
                fig3 = go.Figure()
                
                for i, row in df_temp.iterrows():
                    # Add connecting line
                    fig3.add_trace(go.Scatter(
                        x=[row['xGApm'], row['xGpm']],
                        y=[row['Team'], row['Team']],
                        mode='lines',
                        line=dict(color='gray', width=2),
                        hoverinfo='skip',
                        showlegend=False
                    ))
                    
                    # Add xGA marker
                    fig3.add_trace(go.Scatter(
                        x=[row['xGApm']],
                        y=[row['Team']],
                        mode='markers',
                        marker=dict(color='#00A398', size=12),
                        name='xGA' if i == 0 else None,
                        hovertemplate='Team: %{y}<br>xGA: %{x:.2f}<extra></extra>',
                        showlegend=(i == 0)
                    ))
                    
                    # Add xG marker
                    fig3.add_trace(go.Scatter(
                        x=[row['xGpm']],
                        y=[row['Team']],
                        mode='markers',
                        marker=dict(color='#C8102E', size=12),
                        name='xG' if i == 0 else None,
                        hovertemplate='Team: %{y}<br>xG: %{x:.2f}<extra></extra>',
                        showlegend=(i == 0)
                    ))
                
                fig3.update_layout(
                    title="⚽ EPL: xG vs xGA per Match (Dot Plot)",
                    template="plotly_white",
                    xaxis_title="Per Match Value",
                    height=800
                )
                
                st.plotly_chart(fig3, use_container_width=True)
            
            # Chart 3: Delta xG Ranking
            if chart_selection in ["All Charts", "Delta xG Ranking"]:
                st.markdown("#### 📈 Delta xG Ranking (xG - xGA)")
                
                df_sorted_delta = df_temp.sort_values(by='delta_xGpm', ascending=True)
                
                # Color code based on positive/negative values
                colors = ['#C8102E' if x >= 0 else '#7F7F7F' for x in df_sorted_delta['delta_xGpm']]
                
                fig_delta = px.bar(
                    df_sorted_delta,
                    x='delta_xGpm',
                    y='Team',
                    orientation='h',
                    text='delta_xGpm',
                    title='⚽ EPL: Delta xG (Scored - Conceded) Ranking',
                    labels={'delta_xGpm': 'Delta xG per Match', 'Team': 'Team'},
                    template='plotly_white'
                )
                
                fig_delta.update_traces(
                    texttemplate='%{x:.2f}',
                    textposition='outside',
                    marker_color=colors
                )
                
                fig_delta.update_layout(
                    xaxis_title='ΔxG per Match',
                    height=600
                )
                
                st.plotly_chart(fig_delta, use_container_width=True)
            
            # Chart 4: xG Home vs Away
            if chart_selection in ["All Charts", "xG Home vs Away"]:
                st.markdown("#### 🏠 xG Home vs Away Performance")
                
                df_sorted_home = df_temp.sort_values(by='xGpm_h', ascending=True)
                
                fig_ha = go.Figure()
                
                fig_ha.add_trace(go.Bar(
                    x=df_sorted_home['xGpm_h'],
                    y=df_sorted_home['Team'],
                    name='xG at Home',
                    orientation='h',
                    marker=dict(color='#FF4136'),
                    hovertemplate='Team: %{y}<br>xG at Home: %{x:.2f}<extra></extra>'
                ))
                
                fig_ha.add_trace(go.Bar(
                    x=df_sorted_home['xGpm_a'],
                    y=df_sorted_home['Team'],
                    name='xG Away',
                    orientation='h',
                    marker=dict(color='#2ECC40'),
                    hovertemplate='Team: %{y}<br>xG Away: %{x:.2f}<extra></extra>'
                ))
                
                fig_ha.update_layout(
                    title='⚽ EPL: xG per Match — Home vs Away',
                    barmode='group',
                    template='plotly_white',
                    height=600,
                    xaxis_title='xG per Match'
                )
                
                st.plotly_chart(fig_ha, use_container_width=True)
            
            # Chart 5: Liverpool Season Performance
            if chart_selection in ["All Charts", "Liverpool Season Performance"]:
                st.markdown("#### 📈 Liverpool Complete Season Performance (2020-21)")
                
                try:
                    # Use Liverpool_2015_2023_Matches.csv for complete season data
                    df_liverpool = pd.read_csv('Liverpool_2015_2023_Matches.csv')
                    
                    # Convert date column
                    df_liverpool['Date'] = pd.to_datetime(df_liverpool['Date'])
                    
                    # Filter for 2020-21 season (August 2020 to May 2021)
                    season_2020_21 = df_liverpool[
                        (df_liverpool['Date'] >= '2020-08-01') & 
                        (df_liverpool['Date'] <= '2021-05-31')
                    ].copy()
                    
                    if not season_2020_21.empty:
                        # Add venue and result columns
                        season_2020_21['Venue'] = season_2020_21.apply(
                            lambda row: 'Home' if row['Home'] == 'Liverpool' else 'Away', axis=1
                        )
                        
                        def get_result(row):
                            if row['Venue'] == 'Home':
                                return 'Win' if row['HomeGoals'] > row['AwayGoals'] else 'Draw' if row['HomeGoals'] == row['AwayGoals'] else 'Loss'
                            else:
                                return 'Win' if row['AwayGoals'] > row['HomeGoals'] else 'Draw' if row['AwayGoals'] == row['HomeGoals'] else 'Loss'
                        
                        season_2020_21['Result'] = season_2020_21.apply(get_result, axis=1)
                        season_2020_21['GoalsFor'] = season_2020_21.apply(
                            lambda row: row['HomeGoals'] if row['Venue'] == 'Home' else row['AwayGoals'], axis=1
                        )
                        season_2020_21['GoalsAgainst'] = season_2020_21.apply(
                            lambda row: row['AwayGoals'] if row['Venue'] == 'Home' else row['HomeGoals'], axis=1
                        )
                        
                        # Sort by date to get chronological order
                        season_2020_21 = season_2020_21.sort_values('Date').reset_index(drop=True)
                        
                        # Add gameweek numbers
                        season_2020_21['Gameweek'] = range(1, len(season_2020_21) + 1)
                        
                        # Calculate cumulative and rolling metrics
                        season_2020_21['Cumulative_Goals'] = season_2020_21['GoalsFor'].cumsum()
                        season_2020_21['Cumulative_Wins'] = (season_2020_21['Result'] == 'Win').cumsum()
                        season_2020_21['Cumulative_Points'] = season_2020_21['Result'].map(
                            {'Win': 3, 'Draw': 1, 'Loss': 0}
                        ).cumsum()
                        
                        # Rolling averages (last 5 games)
                        season_2020_21['Rolling_Goals'] = season_2020_21['GoalsFor'].rolling(window=5, min_periods=1).mean()
                        season_2020_21['Rolling_GA'] = season_2020_21['GoalsAgainst'].rolling(window=5, min_periods=1).mean()
                        
                        # Create comprehensive performance chart
                        fig_complete = go.Figure()
                        
                        # Goals per game
                        fig_complete.add_trace(go.Scatter(
                            x=season_2020_21['Gameweek'],
                            y=season_2020_21['GoalsFor'],
                            mode='lines+markers',
                            name='Goals Scored',
                            line=dict(color='#C8102E', width=3),
                            marker=dict(size=6)
                        ))
                        
                        # Goals against
                        fig_complete.add_trace(go.Scatter(
                            x=season_2020_21['Gameweek'],
                            y=season_2020_21['GoalsAgainst'],
                            mode='lines+markers',
                            name='Goals Conceded',
                            line=dict(color='#7F7F7F', width=2),
                            marker=dict(size=4)
                        ))
                        
                        # Rolling average goals
                        fig_complete.add_trace(go.Scatter(
                            x=season_2020_21['Gameweek'],
                            y=season_2020_21['Rolling_Goals'],
                            mode='lines',
                            name='5-Game Avg Goals',
                            line=dict(color='#00A398', width=2, dash='dash')
                        ))
                        
                        # Add win markers
                        wins_data = season_2020_21[season_2020_21['Result'] == 'Win']
                        fig_complete.add_trace(go.Scatter(
                            x=wins_data['Gameweek'],
                            y=[max(season_2020_21['GoalsFor']) * 1.1] * len(wins_data),
                            mode='markers',
                            name='Wins',
                            marker=dict(symbol='star', size=10, color='#FFD700'),
                            showlegend=True
                        ))
                        
                        fig_complete.update_layout(
                            title='🔴 Liverpool 2020-21 Complete Season: Goals & Performance',
                            xaxis_title='Gameweek',
                            yaxis_title='Goals',
                            template='plotly_white',
                            height=600,
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig_complete, use_container_width=True)
                        
                        # Season progression metrics
                        st.markdown("##### 📊 Season Progression")
                        
                        prog_col1, prog_col2 = st.columns(2)
                        
                        with prog_col1:
                            # Cumulative points chart
                            fig_points = px.line(
                                season_2020_21,
                                x='Gameweek',
                                y='Cumulative_Points',
                                title='Cumulative Points Throughout Season',
                                template='plotly_white',
                                markers=True
                            )
                            fig_points.update_traces(line_color='#C8102E')
                            st.plotly_chart(fig_points, use_container_width=True)
                        
                        with prog_col2:
                            # Form chart (last 5 games performance)
                            form_data = []
                            for i in range(len(season_2020_21)):
                                start_idx = max(0, i-4)
                                last_5_results = season_2020_21.iloc[start_idx:i+1]['Result']
                                wins_in_5 = (last_5_results == 'Win').sum()
                                form_data.append(wins_in_5)
                            
                            season_2020_21['Form'] = form_data
                            
                            fig_form = px.line(
                                season_2020_21,
                                x='Gameweek',
                                y='Form',
                                title='Form (Wins in Last 5 Games)',
                                template='plotly_white',
                                markers=True
                            )
                            fig_form.update_traces(line_color='#00A398')
                            fig_form.update_layout(yaxis=dict(range=[0, 5]))
                            st.plotly_chart(fig_form, use_container_width=True)
                        
                        # Final season summary
                        st.markdown("##### 🏆 Complete 2020-21 Season Summary")
                        
                        final_col1, final_col2, final_col3, final_col4 = st.columns(4)
                        
                        with final_col1:
                            total_games = len(season_2020_21)
                            total_wins = (season_2020_21['Result'] == 'Win').sum()
                            st.metric("Total Games", total_games)
                            st.metric("Total Wins", total_wins)
                        
                        with final_col2:
                            total_goals = season_2020_21['GoalsFor'].sum()
                            goals_per_game = total_goals / total_games
                            st.metric("Total Goals", total_goals)
                            st.metric("Goals/Game", f"{goals_per_game:.2f}")
                        
                        with final_col3:
                            total_conceded = season_2020_21['GoalsAgainst'].sum()
                            clean_sheets = (season_2020_21['GoalsAgainst'] == 0).sum()
                            st.metric("Goals Conceded", total_conceded)
                            st.metric("Clean Sheets", clean_sheets)
                        
                        with final_col4:
                            final_points = season_2020_21['Cumulative_Points'].iloc[-1]
                            win_rate = (total_wins / total_games * 100)
                            st.metric("Final Points", final_points)
                            st.metric("Win Rate", f"{win_rate:.1f}%")
                        
                        # League position context
                        st.info(f"📈 **2020-21 Season Context:** Liverpool finished with {final_points} points from {total_games} games, scoring {total_goals} goals with a {win_rate:.1f}% win rate.")
                    
                    else:
                        st.warning("No 2020-21 season data found in Liverpool_2015_2023_Matches.csv")
                        
                except Exception as e:
                    st.warning(f"Error loading complete season data: {str(e)}")
                    st.info("Make sure Liverpool_2015_2023_Matches.csv contains 2020-21 season data with proper date formatting.")
            
            # Additional Analysis Section
            st.markdown("### 📊 Additional xG Analysis")
            
            analysis_col1, analysis_col2 = st.columns(2)
            
            with analysis_col1:
                # xG Difference Analysis
                st.markdown("#### 📊 Average xG Difference (Home Teams)")
                
                # Calculate xG difference for home teams
                df_original = pd.read_csv('EPL_result.csv')
                df_original['xG_diff'] = df_original['xG_Home'] - df_original['xG_Away']
                team_xg_diff = df_original.groupby('Home')['xG_diff'].mean().sort_values(ascending=False).reset_index()
                
                fig_diff = px.bar(
                    team_xg_diff, 
                    x='Home', 
                    y='xG_diff',
                    title='📊 Average xG Difference (Home Teams)',
                    template='plotly_white',
                    color='xG_diff',
                    color_continuous_scale='RdYlGn'
                )
                
                fig_diff.update_layout(
                    xaxis_tickangle=45,
                    coloraxis_showscale=False
                )
                
                st.plotly_chart(fig_diff, use_container_width=True)
            
            with analysis_col2:
                # Scatter plot with quadrant analysis (converted from matplotlib)
                st.markdown("#### 🎯 xG Quadrant Analysis")
                
                fig_scatter = px.scatter(
                    df_temp,
                    x='xGApm',
                    y='xGpm',
                    text='Team',
                    title='⚽ xG Scored vs xG Conceded per Match',
                    labels={'xGApm': 'xG Conceded per Match', 'xGpm': 'xG Scored per Match'},
                    template='plotly_white'
                )
                
                # Highlight Liverpool
                liverpool_color = ['#C8102E' if team == 'LIV' else '#1f77b4' for team in df_temp['Team']]
                liverpool_size = [15 if team == 'LIV' else 8 for team in df_temp['Team']]
                
                fig_scatter.update_traces(
                    marker=dict(color=liverpool_color, size=liverpool_size),
                    textposition='top center'
                )
                
                # Add mean lines
                mean_xg = df_temp['xGpm'].mean()
                mean_xga = df_temp['xGApm'].mean()
                
                fig_scatter.add_hline(y=mean_xg, line_dash="dash", line_color="gray")
                fig_scatter.add_vline(x=mean_xga, line_dash="dash", line_color="gray")
                
                # Add quadrant labels
                fig_scatter.add_annotation(
                    x=df_temp['xGApm'].max() * 0.8, 
                    y=df_temp['xGpm'].max() * 0.9,
                    text="Q1: Strong Attack<br>Weak Defence", 
                    showarrow=False,
                    bgcolor="rgba(255,255,255,0.8)", 
                    font=dict(color="red", size=10)
                )
                
                fig_scatter.add_annotation(
                    x=df_temp['xGApm'].min() * 1.2, 
                    y=df_temp['xGpm'].max() * 0.9,
                    text="Q2: Strong Attack<br>Strong Defence", 
                    showarrow=False,
                    bgcolor="rgba(255,255,255,0.8)", 
                    font=dict(color="green", size=10)
                )
                
                fig_scatter.add_annotation(
                    x=df_temp['xGApm'].min() * 1.2, 
                    y=df_temp['xGpm'].min() * 1.2,
                    text="Q3: Weak Attack<br>Strong Defence", 
                    showarrow=False,
                    bgcolor="rgba(255,255,255,0.8)", 
                    font=dict(color="orange", size=10)
                )
                
                fig_scatter.add_annotation(
                    x=df_temp['xGApm'].max() * 0.8, 
                    y=df_temp['xGpm'].min() * 1.2,
                    text="Q4: Weak Attack<br>Weak Defence", 
                    showarrow=False,
                    bgcolor="rgba(255,255,255,0.8)", 
                    font=dict(color="red", size=10)
                )
                
                fig_scatter.update_layout(height=500)
                
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Enhanced insights and analysis
            st.markdown("### 🎯 Enhanced xG Insights & Analysis")
            
            # Calculate additional metrics for insights
            df_temp_sorted = df_temp.sort_values('delta_xGpm', ascending=False)
            
            insights_col1, insights_col2, insights_col3 = st.columns(3)
            
            with insights_col1:
                best_attack = df_temp.loc[df_temp['xGpm'].idxmax()]
                best_defense = df_temp.loc[df_temp['xGApm'].idxmin()]
                
                st.success(f"🔥 **Best Attack:** {best_attack['Team']} ({best_attack['xGpm']:.2f} xG/match)")
                st.info(f"🛡️ **Best Defense:** {best_defense['Team']} ({best_defense['xGApm']:.2f} xGA/match)")
                
                # Liverpool positioning
                liverpool_attack_rank = liverpool_rank
                liverpool_defense_rank = liverpool_xga_rank
                
                if liverpool_attack_rank <= 3:
                    st.success(f"🔴 **Liverpool Attack:** Elite (#{liverpool_attack_rank})")
                elif liverpool_attack_rank <= 6:
                    st.info(f"🔴 **Liverpool Attack:** Strong (#{liverpool_attack_rank})")
                else:
                    st.warning(f"🔴 **Liverpool Attack:** Room for improvement (#{liverpool_attack_rank})")
                
                if liverpool_defense_rank <= 3:
                    st.success(f"🔴 **Liverpool Defense:** Elite (#{liverpool_defense_rank})")
                elif liverpool_defense_rank <= 6:
                    st.info(f"🔴 **Liverpool Defense:** Strong (#{liverpool_defense_rank})")
                else:
                    st.warning(f"🔴 **Liverpool Defense:** Room for improvement (#{liverpool_defense_rank})")
            
            with insights_col2:
                # Home advantage analysis
                home_xg_advantage = liverpool_stats['xGpm_h'] - liverpool_stats['xGpm_a']
                
                st.info(f"🏠 **Liverpool Home Advantage:** {home_xg_advantage:+.2f} xG difference")
                
                # Team balance analysis
                balanced_teams = len(df_temp[abs(df_temp['delta_xGpm']) < 0.3])
                attack_heavy = len(df_temp[(df_temp['xGpm'] > df_temp['xGpm'].median()) & (df_temp['xGApm'] > df_temp['xGApm'].median())])
                
                st.info(f"⚖️ **Balanced Teams:** {balanced_teams}/20 (|ΔxG| < 0.3)")
                st.info(f"🔥 **Attack Heavy:** {attack_heavy}/20 teams")
                
                # Liverpool's team type
                if abs(liverpool_stats['delta_xGpm']) < 0.3:
                    team_type = "Balanced"
                elif liverpool_stats['xGpm'] > df_temp['xGpm'].median():
                    team_type = "Attack-focused"
                else:
                    team_type = "Defense-focused"
                
                st.success(f"🔴 **Liverpool Style:** {team_type}")
            
            with insights_col3:
                # League distribution analysis
                top_quarter = len(df_temp[df_temp['delta_xGpm'] > df_temp['delta_xGpm'].quantile(0.75)])
                bottom_quarter = len(df_temp[df_temp['delta_xGpm'] < df_temp['delta_xGpm'].quantile(0.25)])
                
                st.info(f"📊 **Top Quarter (ΔxG):** {top_quarter}/20 teams")
                st.info(f"📊 **Bottom Quarter (ΔxG):** {bottom_quarter}/20 teams")
                
                # Liverpool's quartile
                liverpool_percentile = ((df_temp['delta_xGpm'] < liverpool_stats['delta_xGpm']).sum() / len(df_temp) * 100)
                
                if liverpool_percentile >= 75:
                    quartile = "Top 25%"
                    color = "success"
                elif liverpool_percentile >= 50:
                    quartile = "Top 50%"
                    color = "info"
                elif liverpool_percentile >= 25:
                    quartile = "Bottom 50%"
                    color = "warning"
                else:
                    quartile = "Bottom 25%"
                    color = "error"
                
                if color == "success":
                    st.success(f"🔴 **Liverpool Position:** {quartile}")
                elif color == "info":
                    st.info(f"🔴 **Liverpool Position:** {quartile}")
                elif color == "warning":
                    st.warning(f"🔴 **Liverpool Position:** {quartile}")
                else:
                    st.error(f"🔴 **Liverpool Position:** {quartile}")
            
            # Summary table
            st.markdown("### 📋 Complete xG Statistics Table")
            
            # Enhanced summary table with more metrics
            enhanced_summary = df_temp.copy()
            enhanced_summary['xG_Balance'] = enhanced_summary['xGpm'] / enhanced_summary['xGApm']
            enhanced_summary['Home_Away_xG_Diff'] = enhanced_summary['xGpm_h'] - enhanced_summary['xGpm_a']
            
            # Display comprehensive statistics table
            display_columns = ['Team', 'M', 'xGpm', 'xGApm', 'delta_xGpm', 'xGpm_h', 'xGpm_a', 'Home_Away_xG_Diff']
            summary_table = enhanced_summary[display_columns].sort_values('delta_xGpm', ascending=False)
            summary_table = summary_table.round(2)
            summary_table.columns = ['Team', 'Matches', 'xG/Match', 'xGA/Match', 'ΔxG/Match', 'xG Home', 'xG Away', 'Home Adv']
            
            st.dataframe(
                summary_table.style.background_gradient(
                    subset=['ΔxG/Match', 'xG/Match'], 
                    cmap='RdYlGn'
                ).background_gradient(
                    subset=['xGA/Match'], 
                    cmap='RdYlGn_r'  # Reverse for defense (lower is better)
                ),
                use_container_width=True
            )
            
            # Final comprehensive analysis summary
            st.markdown("### 📈 EPL xG Analysis Summary")
            
            league_avg_xg = df_temp['xGpm'].mean()
            league_avg_xga = df_temp['xGApm'].mean()
            
            summary_text = f"""
            **Premier League xG Analysis Overview:**
            
            📊 **Liverpool's Overall Position:** #{liverpool_delta_rank}/20 (ΔxG: {liverpool_stats['delta_xGpm']:.2f})
            
            🔥 **Attack Analysis:** #{liverpool_rank}/20 - {liverpool_stats['xGpm']:.2f} xG per match (League avg: {league_avg_xg:.2f})
            
            🛡️ **Defense Analysis:** #{liverpool_xga_rank}/20 - {liverpool_stats['xGApm']:.2f} xGA per match (League avg: {league_avg_xga:.2f})
            
            🏠 **Home Advantage:** {liverpool_stats['xGpm_h']:.2f} vs {liverpool_stats['xGpm_a']:.2f} ({home_xg_advantage:+.2f} difference)
            
            🎯 **Liverpool's Strengths:** {'Elite attack' if liverpool_rank <= 3 else 'Strong attack' if liverpool_rank <= 6 else 'Developing attack'} combined with {'elite defense' if liverpool_xga_rank <= 3 else 'solid defense' if liverpool_xga_rank <= 6 else 'improving defense'}
            
            🏆 **Title Race Position:** {'Excellent' if liverpool_delta_rank <= 3 else 'Strong' if liverpool_delta_rank <= 6 else 'Competitive'} xG metrics suggest {'title contention' if liverpool_delta_rank <= 3 else 'top 4 contention' if liverpool_delta_rank <= 6 else 'mid-table performance'}
            
            📈 **League Context:** Liverpool ranks in the {quartile.lower()} of Premier League teams by overall xG performance
            """
            
            st.markdown(summary_text)
            
        except FileNotFoundError:
            st.error("❌ Error: 'EPL_result.csv' file not found.")
            st.info("""
            📋 **To use this dashboard:**
            1. Place your 'EPL_result.csv' file in the same directory as this script
            2. Make sure the CSV has columns: 'Home', 'Away', 'xG_Home', 'xG_Away', 'G_Home', 'G_Away', 'GW'
            3. Refresh the page
            """)
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    with tab5:
        st.markdown("""
        <div class="tab-content">
            <h3>🕰️ Club Trends & Manager Era</h3>
            <p>Performance trends across different managerial periods</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load manager data
            managers_df = pd.read_csv("liverpoolfc_managers.csv", sep=';')
            
            # Fix name formatting - remove commas and reverse order
            def fix_name(name):
                if ',' in name:
                    parts = name.split(',')
                    return f"{parts[1].strip()} {parts[0].strip()}"
                return name
            
            managers_df['Name'] = managers_df['Name'].apply(fix_name)
            
            # Convert date strings
            managers_df['From'] = pd.to_datetime(managers_df['From'])
            managers_df['To'] = pd.to_datetime(managers_df['To'])
            
            # Calculate duration
            managers_df['Days'] = (managers_df['To'] - managers_df['From']).dt.days
            managers_df['Years'] = (managers_df['Days'] / 365).round(1)
            
            # Calculate additional metrics for home performance analysis
            managers_df['Points_per_Game'] = ((managers_df['W'] * 3 + managers_df['D']) / managers_df['P']).round(2)
            managers_df['Loss_Rate'] = ((managers_df['L'] / managers_df['P']) * 100).round(1)
            
            # Sort chronologically
            managers_df = managers_df.sort_values(by='From')
            
            # Display manager summary statistics
            st.markdown("### 📊 Liverpool Manager Impact Analysis")
            
            # Find key managers
            longest_tenure = managers_df.loc[managers_df['Years'].idxmax()]
            highest_win_rate = managers_df.loc[managers_df['win_perc'].idxmax()]
            most_games = managers_df.loc[managers_df['P'].idxmax()]
            highest_ppg = managers_df.loc[managers_df['Points_per_Game'].idxmax()]
            
            manager_col1, manager_col2, manager_col3, manager_col4 = st.columns(4)
            
            with manager_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⏱️ Longest Tenure</h3>
                    <h2>{longest_tenure['Name']}</h2>
                    <h1>{longest_tenure['Years']} years</h1>
                    <small>{longest_tenure['win_perc']}% Win Rate</small>
                </div>
                """, unsafe_allow_html=True)
            
            with manager_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏆 Highest Win %</h3>
                    <h2>{highest_win_rate['Name']}</h2>
                    <h1>{highest_win_rate['win_perc']}%</h1>
                    <small>{highest_win_rate['P']} games</small>
                </div>
                """, unsafe_allow_html=True)
            
            with manager_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚽ Most Games</h3>
                    <h2>{most_games['Name']}</h2>
                    <h1>{int(most_games['P'])}</h1>
                    <small>{most_games['Years']} years</small>
                </div>
                """, unsafe_allow_html=True)
            
            with manager_col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📈 Best Points/Game</h3>
                    <h2>{highest_ppg['Name']}</h2>
                    <h1>{highest_ppg['Points_per_Game']}</h1>
                    <small>Points per Game</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Chart selection for manager analysis
            st.markdown("### 📊 Manager Performance Analysis")
            manager_chart_selection = st.selectbox(
                "Choose Manager Analysis",
                ["Manager Impact Overview", "Win Rate Evolution", "Performance vs Tenure", 
                 "Home Advantage Impact", "Manager Efficiency Comparison", "Success Timeline",
                 "Manager Comparison Matrix", "Performance Radar Chart", "Tenure vs Success Bubble"],
                index=0,
                key="manager_chart_selection"
            )
            
            # Chart 1: Manager Impact Overview - Clear Comparison
            if manager_chart_selection == "Manager Impact Overview":
                st.markdown("#### 🔴 Manager Performance Comparison - Win Rate & Tenure")
                
                # Filter to managers with significant tenure (more than 50 games)
                significant_managers = managers_df[managers_df['P'] >= 50].copy()
                significant_managers = significant_managers.sort_values('win_perc', ascending=True)
                
                fig_overview = px.bar(
                    significant_managers,
                    x='win_perc',
                    y='Name',
                    orientation='h',
                    text='win_perc',
                    title="Manager Win Percentage (Minimum 50 Games)",
                    labels={'win_perc': 'Win Percentage (%)', 'Name': 'Manager'},
                    color='win_perc',
                    color_continuous_scale=['#ff4444', '#ffaa00', '#00aa00'],
                    template='plotly_white'
                )
                
                fig_overview.update_traces(
                    texttemplate='%{text}%',
                    textposition='outside',
                    marker_line_color='white',
                    marker_line_width=2
                )
                
                fig_overview.update_layout(
                    height=max(400, len(significant_managers) * 60),
                    showlegend=False,
                    coloraxis_showscale=False,
                    font=dict(size=14),
                    xaxis=dict(range=[0, max(significant_managers['win_perc']) * 1.1]),
                    title_font=dict(size=20)
                )
                
                st.plotly_chart(fig_overview, use_container_width=True)
                
                # Add insight
                best_manager = significant_managers.loc[significant_managers['win_perc'].idxmax()]
                worst_manager = significant_managers.loc[significant_managers['win_perc'].idxmin()]
                st.success(f"🏆 **Best:** {best_manager['Name']} ({best_manager['win_perc']}%) vs **Lowest:** {worst_manager['Name']} ({worst_manager['win_perc']}%) - **{best_manager['win_perc'] - worst_manager['win_perc']}% difference**")
            
            # Chart 2: Win Rate Evolution Over Time
            elif manager_chart_selection == "Win Rate Evolution":
                st.markdown("#### 📈 Liverpool's Managerial Success Evolution")
                
                fig_evolution = px.scatter(
                    managers_df,
                    x='From',
                    y='win_perc',
                    size='P',
                    color='win_perc',
                    text='Name',
                    title='Manager Success Rate Over Time (Bubble Size = Games Managed)',
                    labels={'From': 'Year Started', 'win_perc': 'Win Percentage (%)'},
                    color_continuous_scale='RdYlGn',
                    template='plotly_white',
                    size_max=30
                )
                
                fig_evolution.update_traces(
                    textposition='top center',
                    marker_line_color='white',
                    marker_line_width=2
                )
                
                fig_evolution.update_layout(
                    height=600,
                    xaxis_tickformat='%Y',
                    showlegend=False,
                    coloraxis_colorbar=dict(title="Win %"),
                    font=dict(size=12),
                    title_font=dict(size=20)
                )
                
                # Add trend line
                fig_evolution.add_trace(
                    px.scatter(managers_df, x='From', y='win_perc', trendline="lowess").data[1]
                )
                
                st.plotly_chart(fig_evolution, use_container_width=True)
                
                # Add insight about trends
                recent_managers = managers_df[managers_df['From'] >= '1990-01-01']
                avg_recent_win_rate = recent_managers['win_perc'].mean()
                old_managers = managers_df[managers_df['From'] < '1990-01-01']
                avg_old_win_rate = old_managers['win_perc'].mean()
                
                if avg_recent_win_rate > avg_old_win_rate:
                    st.info(f"📈 **Trend:** Recent managers (post-1990) average {avg_recent_win_rate:.1f}% vs older era {avg_old_win_rate:.1f}% - **{avg_recent_win_rate - avg_old_win_rate:.1f}% improvement**")
                else:
                    st.warning(f"📉 **Trend:** Older managers averaged {avg_old_win_rate:.1f}% vs recent {avg_recent_win_rate:.1f}% - **{avg_old_win_rate - avg_recent_win_rate:.1f}% decline**")
            
            # Chart 3: Performance vs Tenure Analysis
            elif manager_chart_selection == "Performance vs Tenure":
                st.markdown("#### ⚖️ Success Rate vs Time Given (Does Tenure = Success?)")
                
                fig_tenure = px.scatter(
                    managers_df,
                    x='Years',
                    y='win_perc',
                    size='P',
                    color='Points_per_Game',
                    text='Name',
                    title='Win Rate vs Tenure Length (Color = Points per Game)',
                    labels={'Years': 'Years in Charge', 'win_perc': 'Win Percentage (%)', 'P': 'Games Managed'},
                    color_continuous_scale='Viridis',
                    template='plotly_white',
                    size_max=25
                )
                
                fig_tenure.update_traces(
                    textposition='top center',
                    marker_line_color='white',
                    marker_line_width=2
                )
                
                fig_tenure.update_layout(
                    height=600,
                    coloraxis_colorbar=dict(title="Points/Game"),
                    font=dict(size=12),
                    title_font=dict(size=18)
                )
                
                # Add correlation line
                import numpy as np
                correlation = np.corrcoef(managers_df['Years'], managers_df['win_perc'])[0,1]
                
                st.plotly_chart(fig_tenure, use_container_width=True)
                
                if correlation > 0.3:
                    st.success(f"📈 **Positive Correlation:** {correlation:.2f} - Longer tenure generally means better success rate")
                elif correlation < -0.3:
                    st.error(f"📉 **Negative Correlation:** {correlation:.2f} - Longer tenure associated with lower win rates")
                else:
                    st.info(f"🔄 **Weak Correlation:** {correlation:.2f} - Tenure length doesn't strongly predict success")
            
            # Chart 4: Home Advantage Impact
            elif manager_chart_selection == "Home Advantage Impact":
                st.markdown("#### 🏠 How Different Managers Impact Home Performance")
                
                # Create home advantage analysis
                # Assume average home advantage is around 55-60% win rate
                league_avg_home_win = 55  # Typical home advantage in football
                
                # Create home performance proxy using win rate and loss rate
                managers_df['Home_Performance_Index'] = managers_df['win_perc'] + (100 - managers_df['Loss_Rate']) * 0.3
                managers_df['Home_Advantage_Impact'] = managers_df['win_perc'] - league_avg_home_win
                
                # Filter managers with significant games
                home_analysis = managers_df[managers_df['P'] >= 30].copy()
                home_analysis = home_analysis.sort_values('Home_Advantage_Impact', ascending=True)
                
                fig_home = px.bar(
                    home_analysis,
                    x='Home_Advantage_Impact',
                    y='Name',
                    orientation='h',
                    text='win_perc',
                    title='Manager Impact on Home Performance vs League Average (55%)',
                    labels={'Home_Advantage_Impact': 'Win Rate Above/Below League Average (%)', 'Name': 'Manager'},
                    color='Home_Advantage_Impact',
                    color_continuous_scale='RdYlGn',
                    template='plotly_white'
                )
                
                fig_home.update_traces(
                    texttemplate='%{text}%',
                    textposition='outside',
                    marker_line_color='white',
                    marker_line_width=2
                )
                
                fig_home.update_layout(
                    height=max(400, len(home_analysis) * 50),
                    showlegend=False,
                    coloraxis_showscale=False,
                    font=dict(size=12),
                    title_font=dict(size=18)
                )
                
                # Add vertical line at zero (league average)
                fig_home.add_vline(x=0, line_dash="dash", line_color="gray", 
                                 annotation_text="League Average", annotation_position="top")
                
                st.plotly_chart(fig_home, use_container_width=True)
                
                # Home advantage insights
                best_home_manager = home_analysis.loc[home_analysis['Home_Advantage_Impact'].idxmax()]
                worst_home_manager = home_analysis.loc[home_analysis['Home_Advantage_Impact'].idxmin()]
                
                st.success(f"🏠 **Best Home Impact:** {best_home_manager['Name']} (+{best_home_manager['Home_Advantage_Impact']:.1f}% above average)")
                st.error(f"🏠 **Weakest Home Impact:** {worst_home_manager['Name']} ({worst_home_manager['Home_Advantage_Impact']:.1f}% below average)")
                
                above_avg_count = len(home_analysis[home_analysis['Home_Advantage_Impact'] > 0])
                st.info(f"📊 **{above_avg_count}/{len(home_analysis)} managers** performed above league average home win rate")
            
            # Chart 5: Manager Efficiency Comparison
            elif manager_chart_selection == "Manager Efficiency Comparison":
                st.markdown("#### ⚡ Manager Efficiency: Points per Game Comparison")
                
                # Focus on efficiency
                efficiency_df = managers_df[managers_df['P'] >= 20].copy()  # Minimum 20 games
                efficiency_df = efficiency_df.sort_values('Points_per_Game', ascending=True)
                
                fig_efficiency = px.bar(
                    efficiency_df,
                    x='Points_per_Game',
                    y='Name',
                    orientation='h',
                    text='Points_per_Game',
                    title='Points per Game - Manager Efficiency Ranking',
                    labels={'Points_per_Game': 'Points per Game', 'Name': 'Manager'},
                    color='Points_per_Game',
                    color_continuous_scale=['#ff0000', '#ffaa00', '#00cc00'],
                    template='plotly_white'
                )
                
                fig_efficiency.update_traces(
                    texttemplate='%{text}',
                    textposition='outside',
                    marker_line_color='white',
                    marker_line_width=2
                )
                
                fig_efficiency.update_layout(
                    height=max(400, len(efficiency_df) * 55),
                    showlegend=False,
                    coloraxis_showscale=False,
                    font=dict(size=14),
                    title_font=dict(size=18),
                    xaxis=dict(range=[0, max(efficiency_df['Points_per_Game']) * 1.1])
                )
                
                # Add efficiency benchmarks
                fig_efficiency.add_vline(x=2.0, line_dash="dash", line_color="green", 
                                       annotation_text="Title Form (2.0+ PPG)", annotation_position="top")
                fig_efficiency.add_vline(x=1.5, line_dash="dash", line_color="orange", 
                                       annotation_text="Europa League (1.5+ PPG)", annotation_position="bottom")
                
                st.plotly_chart(fig_efficiency, use_container_width=True)
                
                # Efficiency insights
                title_form_managers = efficiency_df[efficiency_df['Points_per_Game'] >= 2.0]
                europa_form_managers = efficiency_df[efficiency_df['Points_per_Game'] >= 1.5]
                
                st.success(f"🏆 **Title Form (2.0+ PPG):** {len(title_form_managers)} managers")
                st.info(f"🌍 **Europa Form (1.5+ PPG):** {len(europa_form_managers)} managers")
                st.warning(f"⚠️ **Below Europa Form:** {len(efficiency_df) - len(europa_form_managers)} managers")
            
            # Chart 6: Success Timeline - Gantt Style
            elif manager_chart_selection == "Success Timeline":
                st.markdown("#### 📅 Manager Success Timeline (Color = Performance)")
                
                # Create timeline with performance bands
                timeline_managers = managers_df[managers_df['P'] >= 30].copy()
                
                fig_gantt = px.timeline(
                    timeline_managers,
                    x_start='From',
                    x_end='To',
                    y='Name',
                    color='win_perc',
                    title='Manager Tenure Timeline (Color Intensity = Success Rate)',
                    color_continuous_scale='RdYlGn',
                    template='plotly_white'
                )
                
                fig_gantt.update_layout(
                    height=max(400, len(timeline_managers) * 40),
                    xaxis_title='Years',
                    yaxis_title='Manager',
                    coloraxis_colorbar=dict(title="Win %"),
                    font=dict(size=12)
                )
                
                # Add hover information
                fig_gantt.update_traces(
                    hovertemplate='<b>%{y}</b><br>' +
                                'From: %{x}<br>' +
                                'Duration: %{customdata[0]:.1f} years<br>' +
                                'Win Rate: %{customdata[1]}%<extra></extra>',
                    customdata=timeline_managers[['Years', 'win_perc']].values
                )
                
                st.plotly_chart(fig_gantt, use_container_width=True)
                
                # Timeline insights
                longest_successful = timeline_managers[timeline_managers['win_perc'] >= 50].sort_values('Years', ascending=False).iloc[0]
                st.success(f"🎯 **Most Successful Long-Term Manager:** {longest_successful['Name']} ({longest_successful['Years']} years, {longest_successful['win_perc']}% win rate)")
            
            # Chart 7: Manager Comparison Matrix
            elif manager_chart_selection == "Manager Comparison Matrix":
                st.markdown("#### 📊 Multi-Dimensional Manager Comparison")
                
                # Create comparison for top managers
                top_managers = managers_df.nlargest(8, 'P')  # Top 8 by games managed
                
                # Prepare data for radar/parallel coordinates
                comparison_metrics = top_managers[['Name', 'win_perc', 'Points_per_Game', 'Years', 'P']].copy()
                comparison_metrics['Games_Scaled'] = (comparison_metrics['P'] / comparison_metrics['P'].max() * 100)
                comparison_metrics['Tenure_Scaled'] = (comparison_metrics['Years'] / comparison_metrics['Years'].max() * 100)
                
                # Parallel coordinates plot
                fig_parallel = px.parallel_coordinates(
                    comparison_metrics,
                    dimensions=['win_perc', 'Points_per_Game', 'Tenure_Scaled', 'Games_Scaled'],
                    color='win_perc',
                    labels={
                        'win_perc': 'Win %',
                        'Points_per_Game': 'Points/Game', 
                        'Tenure_Scaled': 'Tenure (Scaled)',
                        'Games_Scaled': 'Experience (Scaled)'
                    },
                    title='Manager Multi-Dimensional Comparison',
                    color_continuous_scale='RdYlGn',
                    template='plotly_white'
                )
                
                fig_parallel.update_layout(
                    height=500,
                    font=dict(size=12)
                )
                
                st.plotly_chart(fig_parallel, use_container_width=True)
                
                # Add explanation
                st.info("💡 **How to read:** Each line represents a manager. Higher values = better performance. Look for managers with consistently high lines across all dimensions.")
            
            # Chart 8: Performance Radar Chart
            elif manager_chart_selection == "Performance Radar Chart":
                st.markdown("#### 🎯 Manager Performance Radar Chart")
                
                # Select top 5 managers for radar chart
                radar_managers = managers_df.nlargest(5, 'win_perc')
                
                fig_radar = go.Figure()
                
                categories = ['Win %', 'Points/Game', 'Longevity', 'Experience', 'Consistency']
                
                for _, manager in radar_managers.iterrows():
                    # Normalize metrics to 0-100 scale for radar chart
                    win_perc_norm = manager['win_perc']
                    ppg_norm = (manager['Points_per_Game'] / 3.0) * 100  # Max 3 points per game
                    longevity_norm = min((manager['Years'] / 10) * 100, 100)  # Scale to max 10 years
                    experience_norm = min((manager['P'] / 500) * 100, 100)  # Scale to max 500 games
                    consistency_norm = max(0, 100 - manager['Loss_Rate'])  # Inverse of loss rate
                    
                    values = [win_perc_norm, ppg_norm, longevity_norm, experience_norm, consistency_norm]
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values + [values[0]],  # Close the polygon
                        theta=categories + [categories[0]],
                        fill='toself',
                        name=manager['Name'],
                        line=dict(width=2)
                    ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    title='Top 5 Managers - Performance Radar',
                    height=600,
                    font=dict(size=12)
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
                
                st.info("🎯 **Radar Explanation:** Larger area = better overall performance. Each spoke represents a key performance dimension.")
            
            # Chart 9: Advanced Bubble Chart
            elif manager_chart_selection == "Tenure vs Success Bubble":
                st.markdown("#### 🫧 Advanced Manager Analysis (3D Bubble Chart)")
                
                bubble_managers = managers_df[managers_df['P'] >= 25]  # Minimum 25 games
                
                fig_advanced_bubble = px.scatter(
                    bubble_managers,
                    x='Years',
                    y='win_perc',
                    size='P',
                    color='Points_per_Game',
                    hover_name='Name',
                    size_max=30,
                    title='Manager Success Analysis: Tenure vs Win Rate (Bubble=Games, Color=Efficiency)',
                    labels={
                        'Years': 'Years in Charge',
                        'win_perc': 'Win Percentage (%)',
                        'P': 'Games Managed',
                        'Points_per_Game': 'Points per Game'
                    },
                    color_continuous_scale='Viridis',
                    template='plotly_white'
                )
                
                # Add text annotations for key managers
                for _, manager in bubble_managers.iterrows():
                    if manager['win_perc'] > 55 or manager['Years'] > 8:  # Highlight successful or long-serving managers
                        fig_advanced_bubble.add_annotation(
                            x=manager['Years'],
                            y=manager['win_perc'],
                            text=manager['Name'],
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=1,
                            arrowcolor='red',
                            font=dict(size=10)
                        )
                
                fig_advanced_bubble.update_layout(
                    height=600,
                    coloraxis_colorbar=dict(title="Points/Game"),
                    font=dict(size=12)
                )
                
                st.plotly_chart(fig_advanced_bubble, use_container_width=True)
                
                # Advanced insights
                ideal_managers = bubble_managers[(bubble_managers['win_perc'] > 50) & (bubble_managers['Years'] > 3)]
                st.success(f"⭐ **Ideal Balance (50%+ wins, 3+ years):** {len(ideal_managers)} managers achieved sustainable success")
            
            # Enhanced Manager Comparison Table with more insights
            st.markdown("### 📋 Comprehensive Manager Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏆 Top Performers")
                
                top_performers = managers_df.nlargest(8, 'win_perc')[['Name', 'win_perc', 'P', 'Years', 'Points_per_Game']].copy()
                top_performers.columns = ['Manager', 'Win %', 'Games', 'Years', 'PPG']
                
                st.dataframe(
                    top_performers.style.background_gradient(subset=['Win %', 'PPG'], cmap='RdYlGn'),
                    use_container_width=True
                )
            
            with col2:
                st.markdown("#### ⏳ Longest Serving")
                
                longest_serving = managers_df.nlargest(8, 'Years')[['Name', 'Years', 'win_perc', 'P', 'Points_per_Game']].copy()
                longest_serving.columns = ['Manager', 'Years', 'Win %', 'Games', 'PPG']
                
                st.dataframe(
                    longest_serving.style.background_gradient(subset=['Years', 'Win %'], cmap='RdYlGn'),
                    use_container_width=True
                )
            
            # Comprehensive Manager Comparison Table
            st.markdown("### 📋 Manager Performance Summary")
            
            # Create clear comparison table
            comparison_df = managers_df.copy()
            comparison_df = comparison_df.sort_values('win_perc', ascending=False)
            
            display_comparison = comparison_df[[
                'Name', 'Years', 'P', 'W', 'D', 'L', 
                'win_perc', 'Points_per_Game'
            ]].head(15)  # Top 15 managers
            
            display_comparison.columns = [
                'Manager', 'Years', 'Games', 'Wins', 'Draws', 'Losses', 
                'Win %', 'Points/Game'
            ]
            
            # Color-code the dataframe
            st.dataframe(
                display_comparison.style.background_gradient(
                    subset=['Win %', 'Points/Game'], 
                    cmap='RdYlGn'
                ),
                use_container_width=True
            )
                
        except FileNotFoundError:
            
            # Manager Era Performance Analysis
            st.markdown("### 🔄 Manager Era Insights")
            
            era_col1, era_col2 = st.columns(2)
            
            with era_col1:
                # Success rate vs tenure analysis
                st.markdown("#### 🎯 Success vs Tenure Analysis")
                
                fig_success = px.scatter(
                    managers_df,
                    x='Years',
                    y='win_perc',
                    size='P',
                    text='Name',
                    title='Success Rate vs Tenure Length',
                    labels={'Years': 'Years in Charge', 'win_perc': 'Win %', 'P': 'Games'},
                    template='plotly_white'
                )
                
                fig_success.update_traces(
                    marker=dict(color='#C8102E', opacity=0.7),
                    textposition='top center'
                )
                
                fig_success.update_layout(height=400)
                
                st.plotly_chart(fig_success, use_container_width=True)
            
            with era_col2:
                # Manager efficiency analysis
                st.markdown("#### 📈 Manager Efficiency Metrics")
                
                # Calculate efficiency metrics from the managers data
                efficiency_metrics = managers_df.copy()
                efficiency_metrics['Points_per_Game'] = ((efficiency_metrics['W'] * 3 + efficiency_metrics['D']) / efficiency_metrics['P']).round(2)
                efficiency_metrics['Games_per_Year'] = (efficiency_metrics['P'] / efficiency_metrics['Years']).round(1)
                
                fig_efficiency = px.bar(
                    efficiency_metrics.head(8),  # Top 8 managers
                    x='Name',
                    y='Points_per_Game',
                    color='Points_per_Game',
                    title='Points per Game by Manager',
                    color_continuous_scale='RdYlGn',
                    template='plotly_white'
                )
                
                fig_efficiency.update_layout(
                    xaxis_tickangle=45,
                    height=400,
                    coloraxis_showscale=False
                )
                
                st.plotly_chart(fig_efficiency, use_container_width=True)
            
            # Comprehensive Manager Statistics Table
            st.markdown("### 📋 Complete Manager Statistics")
            
            # Create comprehensive stats table using only managers data
            comprehensive_stats = managers_df.copy()
            comprehensive_stats['Points_per_Game'] = ((comprehensive_stats['W'] * 3 + comprehensive_stats['D']) / comprehensive_stats['P']).round(2)
            comprehensive_stats['Draw_Rate_%'] = ((comprehensive_stats['D'] / comprehensive_stats['P']) * 100).round(1)
            comprehensive_stats['Loss_Rate_%'] = ((comprehensive_stats['L'] / comprehensive_stats['P']) * 100).round(1)
            comprehensive_stats['Games_per_Year'] = (comprehensive_stats['P'] / comprehensive_stats['Years']).round(1)
            
            # Display comprehensive table
            display_comprehensive = comprehensive_stats[[
                'Name', 'From', 'To', 'Years', 'P', 'W', 'D', 'L', 
                'win_perc', 'Points_per_Game', 'Games_per_Year'
            ]].copy()
            
            display_comprehensive['From'] = display_comprehensive['From'].dt.strftime('%Y')
            display_comprehensive['To'] = display_comprehensive['To'].dt.strftime('%Y')
            
            display_comprehensive.columns = [
                'Manager', 'From', 'To', 'Years', 'Games', 'Wins', 'Draws', 'Losses', 
                'Win %', 'Pts/Game', 'Games/Year'
            ]
            
            # Sort by win percentage
            display_comprehensive = display_comprehensive.sort_values('Win %', ascending=False)
            
            st.dataframe(display_comprehensive, use_container_width=True)
            
            # Manager Era Insights Summary
            st.markdown("### 📊 Key Manager Era Insights")
            
            insight_col1, insight_col2, insight_col3 = st.columns(3)
            
            with insight_col1:
                avg_tenure = managers_df['Years'].mean()
                st.metric("Average Tenure", f"{avg_tenure:.1f} years")
                
                total_managers = len(managers_df)
                st.metric("Total Managers", total_managers)
            
            with insight_col2:
                avg_win_rate = managers_df['win_perc'].mean()
                st.metric("Average Win Rate", f"{avg_win_rate:.1f}%")
                
                total_games = managers_df['P'].sum()
                st.metric("Total Games", f"{total_games:,}")
            
            with insight_col3:
                most_successful_era = managers_df.loc[managers_df['win_perc'].idxmax()]
                st.metric("Best Win Rate", f"{most_successful_era['win_perc']}%")
                st.metric("Best Manager", most_successful_era['Name'])
                
        except FileNotFoundError:
            st.error("❌ Error: 'liverpoolfc_managers.csv' file not found.")
            st.info("""
            📋 **To use this manager analysis:**
            1. Place your 'liverpoolfc_managers.csv' file in the same directory
            2. Make sure the CSV has columns: 'Name', 'From', 'To', 'P', 'W', 'D', 'L', 'win_perc'
            3. Refresh the page
            """)
        except Exception as e:
            st.error(f"❌ Error loading manager data: {str(e)}")
    
    
    with tab6:
        st.markdown("""
        <div class="tab-content">
            <h3>📊 Team Momentum & Conversion</h3>
            <p>Comprehensive analysis of EPL team performance, halftime conversions, and comeback statistics</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load EPL dataset
            df = pd.read_csv('epl_final.csv')
            
            # STRICT EPL ONLY - Teams that played in Premier League (2015-2023)
            premier_league_teams = {
                # Core EPL Teams (consistently in Premier League 2015-2023)
                'Arsenal', 'Aston Villa', 'Brighton', 'Brighton & Hove Albion', 
                'Brighton and Hove Albion', 'Burnley', 'Chelsea', 'Crystal Palace', 
                'Everton', 'Liverpool', 'Manchester City', 'Manchester United', 
                'Manchester Utd', 'Newcastle United', 'Newcastle Utd', 
                'Southampton', 'Tottenham', 'Tottenham Hotspur', 'West Ham', 
                'West Ham United', 'Wolverhampton Wanderers', 'Wolves',
                
                # Teams that played EPL during 2015-2023 period
                'Bournemouth', 'AFC Bournemouth', 'Brentford', 'Cardiff City', 
                'Fulham', 'Huddersfield', 'Huddersfield Town', 'Hull City', 
                'Leicester City', 'Leeds United', 'Leeds', 'Norwich City', 
                'Nottingham Forest', 'Sheffield United', 'Sheffield Utd',
                'Watford', 'West Bromwich Albion', 'West Brom'
            }
            
            # EXCLUDED from original list:
            # 'Luton Town', 'Luton' - Only promoted to EPL in 2023-24 (not in 2015-2023 data)
            # 'Middlesbrough', 'QPR', 'Stoke City', 'Swansea City' - Championship teams
            # 'Sunderland', 'Blackpool', 'Bolton', 'Wigan' - Lower division teams
            
            # Get all teams in dataset
            all_home_teams = set(df['HomeTeam'].unique())
            all_away_teams = set(df['AwayTeam'].unique())
            all_teams = all_home_teams.union(all_away_teams)
            
            # Find EPL teams that exist in the dataset
            epl_teams_in_data = []
            non_epl_teams = []
            
            for team in all_teams:
                # Check if team matches any Premier League team (case insensitive)
                is_epl = False
                for epl_team in premier_league_teams:
                    if team.lower().strip() == epl_team.lower().strip():
                        epl_teams_in_data.append(team)
                        is_epl = True
                        break
                
                if not is_epl:
                    non_epl_teams.append(team)
            
            # Filter dataframe to include ONLY EPL teams
            df = df[
                (df['HomeTeam'].isin(epl_teams_in_data)) & 
                (df['AwayTeam'].isin(epl_teams_in_data))
            ].copy()
            
            st.success(f"✅ **EPL Only Filter:** {len(epl_teams_in_data)} Premier League teams kept")
            
            # Show what was filtered out
            if non_epl_teams:
                with st.expander(f"🚫 Excluded Non-EPL Teams ({len(non_epl_teams)} teams)"):
                    st.write(", ".join(sorted(non_epl_teams)))
            
            # Show EPL teams included
            with st.expander(f"⚽ EPL Teams in Analysis ({len(epl_teams_in_data)} teams)"):
                st.write(", ".join(sorted(epl_teams_in_data)))
            
            # Basic data info
            df_copy = df.copy()
            
            # Add result indicators
            df_copy["HomeWin"] = df_copy["FullTimeResult"] == "H"
            df_copy["AwayWin"] = df_copy["FullTimeResult"] == "A"
            df_copy["Draw"] = df_copy["FullTimeResult"] == "D"
            df_copy["AwayLoss"] = df_copy["FullTimeResult"] == "H"
            df_copy["HomeLoss"] = df_copy["FullTimeResult"] == "A"
            
            # Team performance calculations
            home_stats = df_copy.groupby("HomeTeam")[["HomeWin", "Draw"]].sum()
            away_stats = df_copy.groupby("AwayTeam")[["AwayWin", "Draw"]].sum()
            home_stats.columns = ["HomeWins", "HomeDraws"]
            away_stats.columns = ["AwayWins", "AwayDraws"]
            team_performance = pd.concat([home_stats, away_stats], axis=1).fillna(0)
            team_performance = team_performance.reset_index()
            
            # Loss analysis
            away_loss_stats = df_copy.groupby("AwayTeam")[["AwayLoss"]].sum()
            home_loss_stats = df_copy.groupby("HomeTeam")[["HomeLoss"]].sum()
            away_loss_stats.columns = ["AwayLoss"]
            home_loss_stats.columns = ["HomeLoss"]
            team_performance_l = pd.concat([home_loss_stats, away_loss_stats], axis=1).fillna(0)
            team_performance_l = team_performance_l.reset_index()
            
            # Goals analysis
            home_goals = df_copy.groupby("HomeTeam")["FullTimeHomeGoals"].mean().rename("AvgHomeGoals")
            away_goals = df_copy.groupby("AwayTeam")["FullTimeAwayGoals"].mean().rename("AvgAwayGoals")
            avg_goals = pd.concat([home_goals, away_goals], axis=1).fillna(0).reset_index()
            
            # Initialize team_conversion variable early to avoid scope issues
            team_conversion = pd.DataFrame()
            
            # Team analysis for halftime conversions (only if HalfTimeResult column exists)
            if 'HalfTimeResult' in df.columns:
                team_analysis = df[df["HalfTimeResult"].isin(["H", "A"])].copy()
                
                if not team_analysis.empty:
                    # Determine if lead was held
                    team_analysis["LeadHeld"] = (
                        ((team_analysis["HalfTimeResult"] == "H") & (team_analysis["FullTimeResult"] == "H")) |
                        ((team_analysis["HalfTimeResult"] == "A") & (team_analysis["FullTimeResult"] == "A"))
                    ).astype(int)
                    
                    # Identify leading team
                    team_analysis["LeadingTeam"] = team_analysis.apply(
                        lambda row: row["HomeTeam"] if row["HalfTimeResult"] == "H" else row["AwayTeam"], axis=1
                    )
                    
                    # Calculate conversion rates
                    team_conversion = team_analysis.groupby("LeadingTeam")["LeadHeld"].agg(["sum", "count"])
                    team_conversion["ConversionRate"] = (team_conversion["sum"] / team_conversion["count"]) * 100
                    team_conversion = team_conversion.reset_index()
                    
                    # Comeback analysis
                    team_analysis["ComebackWin"] = (
                        ((team_analysis["HalfTimeResult"] == "A") & (team_analysis["FullTimeResult"] == "H")) |
                        ((team_analysis["HalfTimeResult"] == "H") & (team_analysis["FullTimeResult"] == "A"))
                    ).astype(int)
                    
                    comeback_stats = team_analysis.groupby("LeadingTeam").agg(
                        ComebackWins=('ComebackWin', 'sum'),
                        TotalOpportunities=('ComebackWin', 'count')
                    ).reset_index()
                    comeback_stats["RemontadaRate"] = (comeback_stats["ComebackWins"] / comeback_stats["TotalOpportunities"]) * 100
                else:
                    st.warning("⚠️ No valid halftime result data found for conversion analysis")
            else:
                st.warning("⚠️ HalfTimeResult column not found in dataset")
            
            # Display summary statistics
            st.markdown("### 📊 Premier League Teams Only - Performance Summary")
            
            # Show filtered team count
            epl_team_count = len(epl_teams_in_data)
            total_matches = len(df)
            
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            
            with summary_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚽ Premier League</h3>
                    <h2>{epl_team_count}</h2>
                    <h1>EPL Teams</h1>
                    <small>{total_matches:,} EPL Matches</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col2:
                # Find team with most home wins
                top_home_wins = team_performance.loc[team_performance['HomeWins'].idxmax()]
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏠 Home Dominance</h3>
                    <h2>{top_home_wins['index']}</h2>
                    <h1>{int(top_home_wins['HomeWins'])}</h1>
                    <small>Home Wins</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col3:
                # Find team with most away wins  
                top_away_wins = team_performance.loc[team_performance['AwayWins'].idxmax()]
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>✈️ Away Warriors</h3>
                    <h2>{top_away_wins['index']}</h2>
                    <h1>{int(top_away_wins['AwayWins'])}</h1>
                    <small>Away Wins</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col4:
                # Liverpool home advantage analysis
                liverpool_data = avg_goals[avg_goals['index'] == 'Liverpool']
                
                if not liverpool_data.empty:
                    liv_home_avg = liverpool_data['AvgHomeGoals'].iloc[0]
                    liv_away_avg = liverpool_data['AvgAwayGoals'].iloc[0]
                    home_advantage = liv_home_avg - liv_away_avg
                    
                    # Determine pattern strength
                    if home_advantage > 0.5:
                        pattern = "Strong"
                        color_class = "metric-card"
                    elif home_advantage > 0.2:
                        pattern = "Moderate"  
                        color_class = "metric-card"
                    else:
                        pattern = "Weak"
                        color_class = "metric-card"
                    
                    st.markdown(f"""
                    <div class="{color_class}">
                        <h3>🏠 Liverpool Pattern</h3>
                        <h2>+{home_advantage:.2f}</h2>
                        <h1>{pattern}</h1>
                        <small>Home Advantage (Goals/Game)</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add insight below
                    if home_advantage > 0.3:
                        st.success(f"💪 **Anfield Effect:** Liverpool scores {home_advantage:.2f} more goals per game at home - shows strong home crowd impact and familiarity with Anfield conditions")
                    elif home_advantage > 0:
                        st.info(f"🏠 **Home Boost:** {home_advantage:.2f} goal advantage at Anfield suggests moderate home benefit")
                    else:
                        st.warning(f"⚠️ **Consistent Away:** Liverpool actually performs equally well away from home - rare resilience!")
                        
                else:
                    # Fallback 
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🔴 Liverpool Analysis</h3>
                        <h2>N/A</h2>
                        <h1>No Data</h1>
                        <small>Liverpool not found</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Chart selection
            st.markdown("### 📊 Team Performance Analysis")
            momentum_chart_selection = st.selectbox(
                "Choose Analysis Type",
                ["All Analysis", "Home vs Away Draws", "Team Losses Analysis", "Goal Scoring Patterns", 
                 "Liverpool Season Analysis", "Halftime Conversion Analysis", "Comeback Analysis", 
                 "Liverpool Momentum Trends", "Team Comparison Matrix"],
                index=0,
                key="momentum_chart_selection"
            )
            
            # Chart 1: Home vs Away Draws Analysis
            if momentum_chart_selection in ["All Analysis", "Home vs Away Draws"]:
                st.markdown("#### ⚖️ Top 10 EPL Teams by Home Draws Analysis")
                
                draws_col1, draws_col2 = st.columns(2)
                
                with draws_col1:
                    # Top 10 teams by home draws
                    top_10_by_home_draws = team_performance.sort_values("HomeDraws", ascending=False).head(10)
                    
                    fig_draws = px.bar(
                        top_10_by_home_draws,
                        x='index',
                        y=['HomeDraws', 'AwayDraws'],
                        title='Top 10 Teams by Home Draws (with Away Draws)',
                        labels={'index': 'Team', 'value': 'Number of Draws', 'variable': 'Venue'},
                        color_discrete_map={'HomeDraws': '#C8102E', 'AwayDraws': '#00A398'},
                        template='plotly_white',
                        barmode='group'
                    )
                    
                    fig_draws.update_layout(
                        xaxis_tickangle=45,
                        height=500,
                        legend_title_text='Venue'
                    )
                    
                    st.plotly_chart(fig_draws, use_container_width=True)
                
                with draws_col2:
                    # Total draws analysis instead of efficiency
                    team_performance['TotalDraws'] = team_performance['HomeDraws'] + team_performance['AwayDraws']
                    top_total_draws = team_performance.sort_values('TotalDraws', ascending=False).head(10)
                    
                    fig_total_draws = px.bar(
                        top_total_draws,
                        x='index',
                        y='TotalDraws',
                        title='Teams with Most Total Draws (Home + Away)',
                        labels={'index': 'Team', 'TotalDraws': 'Total Draws'},
                        color='TotalDraws',
                        color_continuous_scale='Blues',
                        template='plotly_white'
                    )
                    
                    fig_total_draws.update_layout(
                        xaxis_tickangle=45,
                        height=500,
                        coloraxis_showscale=False
                    )
                    
                    st.plotly_chart(fig_total_draws, use_container_width=True)
                
                # Insights
                most_home_draws = top_10_by_home_draws.iloc[0]
                st.success(f"🏠 **Draw Specialists:** {most_home_draws['index']} leads with {int(most_home_draws['HomeDraws'])} home draws and {int(most_home_draws['AwayDraws'])} away draws")
            
            # Chart 2: Team Losses Analysis
            if momentum_chart_selection in ["All Analysis", "Team Losses Analysis"]:
                st.markdown("#### 📉 Team Losses Analysis - Best Defensive Records")
                
                losses_col1, losses_col2 = st.columns(2)
                
                with losses_col1:
                    # Teams with fewest home losses (best home defensive record)
                    best_home_defense = team_performance_l.sort_values("HomeLoss", ascending=True).head(10)
                    
                    fig_home_losses = px.bar(
                        best_home_defense,
                        x='index',
                        y=['HomeLoss', 'AwayLoss'],
                        title='Best Home Defensive Records (Fewest Losses)',
                        labels={'index': 'Team', 'value': 'Number of Losses', 'variable': 'Venue'},
                        color_discrete_map={'HomeLoss': '#FF6B6B', 'AwayLoss': '#4ECDC4'},
                        template='plotly_white',
                        barmode='group'
                    )
                    
                    fig_home_losses.update_layout(
                        xaxis_tickangle=45,
                        height=500,
                        legend_title_text='Loss Type'
                    )
                    
                    st.plotly_chart(fig_home_losses, use_container_width=True)
                
                with losses_col2:
                    # Loss comparison pie chart for top teams
                    team_performance_l['TotalLosses'] = team_performance_l['HomeLoss'] + team_performance_l['AwayLoss']
                    best_overall_defense = team_performance_l.sort_values('TotalLosses', ascending=True).head(5)
                    
                    # Create data for pie chart
                    avg_home_losses = best_overall_defense['HomeLoss'].mean()
                    avg_away_losses = best_overall_defense['AwayLoss'].mean()
                    
                    fig_loss_pie = px.pie(
                        values=[avg_home_losses, avg_away_losses],
                        names=['Average Home Losses', 'Average Away Losses'],
                        title='Loss Distribution: Home vs Away (Top 5 Defenses)',
                        color_discrete_map={'Average Home Losses': '#FF6B6B', 'Average Away Losses': '#4ECDC4'},
                        template='plotly_white'
                    )
                    
                    fig_loss_pie.update_traces(textposition='inside', textinfo='percent+label')
                    fig_loss_pie.update_layout(height=500)
                    
                    st.plotly_chart(fig_loss_pie, use_container_width=True)
                
                # Defensive insights
                best_defense = best_home_defense.iloc[0]
                st.success(f"🛡️ **Defensive Fortress:** {best_defense['index']} has the best home record with only {int(best_defense['HomeLoss'])} home losses")
            
            # Chart 3: Goal Scoring Patterns
            if momentum_chart_selection in ["All Analysis", "Goal Scoring Patterns"]:
                st.markdown("#### ⚽ Goal Scoring Analysis - Top Attacking Teams")
                
                goals_col1, goals_col2 = st.columns(2)
                
                with goals_col1:
                    # Top 10 teams by average home goals
                    top_10_avg_goals = avg_goals.sort_values("AvgHomeGoals", ascending=False).head(10)
                    
                    fig_goals = px.bar(
                        top_10_avg_goals,
                        x='index',
                        y=['AvgHomeGoals', 'AvgAwayGoals'],
                        title='Top 10 Teams by Average Goals per Match',
                        labels={'index': 'Team', 'value': 'Average Goals per Match', 'variable': 'Venue'},
                        color_discrete_map={'AvgHomeGoals': '#FF6B35', 'AvgAwayGoals': '#004E89'},
                        template='plotly_white',
                        barmode='group'
                    )
                    
                    fig_goals.update_layout(
                        xaxis_tickangle=45,
                        height=500,
                        legend_title_text='Goals'
                    )
                    
                    st.plotly_chart(fig_goals, use_container_width=True)
                
                with goals_col2:
                    # Home advantage in scoring
                    avg_goals['HomeAdvantage'] = avg_goals['AvgHomeGoals'] - avg_goals['AvgAwayGoals']
                    home_advantage_goals = avg_goals.sort_values('HomeAdvantage', ascending=False).head(10)
                    
                    fig_home_adv = px.bar(
                        home_advantage_goals,
                        x='index',
                        y='HomeAdvantage',
                        title='Home Advantage in Goal Scoring',
                        labels={'index': 'Team', 'HomeAdvantage': 'Home Advantage (Goals/Game)'},
                        color='HomeAdvantage',
                        color_continuous_scale='RdYlGn',
                        template='plotly_white'
                    )
                    
                    fig_home_adv.update_layout(
                        xaxis_tickangle=45,
                        height=500,
                        coloraxis_showscale=False
                    )
                    
                    fig_home_adv.add_hline(y=0, line_dash="dash", line_color="gray")
                    
                    st.plotly_chart(fig_home_adv, use_container_width=True)
                
                # Goal scoring insights
                top_scorer = top_10_avg_goals.iloc[0]
                st.success(f"🔥 **Top Scorer:** {top_scorer['index']} averages {top_scorer['AvgHomeGoals']:.2f} goals at home and {top_scorer['AvgAwayGoals']:.2f} away")
            
            # Chart 4: Liverpool Season Analysis
            if momentum_chart_selection in ["All Analysis", "Liverpool Season Analysis"]:
                st.markdown("#### 🔴 Liverpool Season Performance Analysis")
                
                # Liverpool losses by season
                team_name = "Liverpool"
                df_copy["TeamLoss"] = (
                    ((df_copy["HomeTeam"] == team_name) & (df_copy["FullTimeResult"] == "A")) |
                    ((df_copy["AwayTeam"] == team_name) & (df_copy["FullTimeResult"] == "H"))
                ).astype(int)
                
                team_losses_by_season = df_copy.groupby("Season")["TeamLoss"].sum().sort_values(ascending=False)
                
                liverpool_col1, liverpool_col2 = st.columns(2)
                
                with liverpool_col1:
                    # Liverpool losses by season
                    season_losses_df = team_losses_by_season.head(10).reset_index()
                    
                    fig_lpool_losses = px.bar(
                        season_losses_df,
                        x='Season',
                        y='TeamLoss',
                        title='Liverpool: Most Losses by Season (Top 10)',
                        labels={'Season': 'Season', 'TeamLoss': 'Number of Losses'},
                        color='TeamLoss',
                        color_continuous_scale='Reds',
                        template='plotly_white'
                    )
                    
                    fig_lpool_losses.update_layout(
                        xaxis_tickangle=45,
                        height=500,
                        coloraxis_showscale=False
                    )
                    
                    st.plotly_chart(fig_lpool_losses, use_container_width=True)
                
                with liverpool_col2:
                    # Liverpool performance trend
                    liverpool_wins = df_copy[(df_copy["HomeTeam"] == team_name) | (df_copy["AwayTeam"] == team_name)].copy()
                    liverpool_wins["LiverpoolWin"] = (
                        ((liverpool_wins["HomeTeam"] == team_name) & (liverpool_wins["FullTimeResult"] == "H")) |
                        ((liverpool_wins["AwayTeam"] == team_name) & (liverpool_wins["FullTimeResult"] == "A"))
                    ).astype(int)
                    
                    season_performance = liverpool_wins.groupby("Season").agg({
                        'LiverpoolWin': 'sum',
                        'TeamLoss': 'sum'
                    }).reset_index()
                    season_performance['TotalGames'] = season_performance['LiverpoolWin'] + season_performance['TeamLoss']
                    season_performance['WinRate'] = (season_performance['LiverpoolWin'] / season_performance['TotalGames'] * 100).round(1)
                    
                    # Take last 10 seasons for trend
                    recent_performance = season_performance.tail(10)
                    
                    fig_lpool_trend = px.line(
                        recent_performance,
                        x='Season',
                        y='WinRate',
                        markers=True,
                        title='Liverpool Win Rate Trend (Last 10 Seasons)',
                        labels={'Season': 'Season', 'WinRate': 'Win Rate (%)'},
                        template='plotly_white'
                    )
                    
                    fig_lpool_trend.update_traces(line_color='#C8102E', marker_size=8)
                    fig_lpool_trend.update_layout(
                        xaxis_tickangle=45,
                        height=500,
                        yaxis=dict(range=[0, 100])
                    )
                    
                    st.plotly_chart(fig_lpool_trend, use_container_width=True)
                
                # Liverpool insights
                worst_season = team_losses_by_season.index[0]
                worst_losses = team_losses_by_season.iloc[0]
                st.error(f"📉 **Toughest Season:** {worst_season} with {worst_losses} losses")
                
                if len(recent_performance) >= 2:
                    recent_trend = recent_performance['WinRate'].iloc[-1] - recent_performance['WinRate'].iloc[-2]
                    if recent_trend > 0:
                        st.success(f"📈 **Recent Form:** Win rate improved by {recent_trend:.1f}% in latest season")
                    else:
                        st.warning(f"📉 **Recent Form:** Win rate declined by {abs(recent_trend):.1f}% in latest season")
            
            # Chart 5: Halftime Conversion Analysis  
            if momentum_chart_selection in ["All Analysis", "Halftime Conversion Analysis"]:
                st.markdown("#### 🕐 Halftime Lead Conversion Analysis")
                
                if not team_conversion.empty:
                    conversion_col1, conversion_col2 = st.columns(2)
                    
                    with conversion_col1:
                        # Top 10 teams by conversion rate (filter for minimum games)
                        top_10_conversion = team_conversion[
                            team_conversion['count'] >= 5  # Minimum 5 halftime leads for relevance
                        ].sort_values("ConversionRate", ascending=False).head(10)
                        
                        if not top_10_conversion.empty:
                            fig_conversion = px.bar(
                                top_10_conversion,
                                x='LeadingTeam',
                                y='ConversionRate',
                                title='Top 10 Teams: Halftime Lead to Full-time Win Conversion',
                                labels={'LeadingTeam': 'Team', 'ConversionRate': 'Conversion Rate (%)'},
                                color='ConversionRate',
                                color_continuous_scale='RdYlGn',
                                template='plotly_white'
                            )
                            
                            fig_conversion.update_layout(
                                xaxis_tickangle=45,
                                height=500,
                                coloraxis_showscale=False,
                                yaxis=dict(range=[0, 100])
                            )
                            
                            st.plotly_chart(fig_conversion, use_container_width=True)
                        else:
                            st.info("Not enough halftime conversion data for meaningful analysis")
                    
                    with conversion_col2:
                        # Liverpool specific analysis
                        liverpool_matches = df[(df['HomeTeam'] == 'Liverpool') | (df['AwayTeam'] == 'Liverpool')].copy()
                        
                        if not liverpool_matches.empty and 'HalfTimeResult' in liverpool_matches.columns:
                            liverpool_matches['Venue'] = liverpool_matches.apply(
                                lambda row: 'Home' if row['HomeTeam'] == 'Liverpool' else 'Away', axis=1
                            )
                            
                            # Liverpool halftime leads
                            liverpool_leads = liverpool_matches[
                                ((liverpool_matches['HomeTeam'] == 'Liverpool') & (liverpool_matches['HalfTimeResult'] == 'H')) |
                                ((liverpool_matches['AwayTeam'] == 'Liverpool') & (liverpool_matches['HalfTimeResult'] == 'A'))
                            ].copy()
                            
                            if not liverpool_leads.empty:
                                liverpool_leads["LeadHeld"] = (
                                    ((liverpool_leads["HomeTeam"] == "Liverpool") & 
                                     (liverpool_leads["HalfTimeResult"] == "H") & 
                                     (liverpool_leads["FullTimeResult"] == "H")) |
                                    ((liverpool_leads["AwayTeam"] == "Liverpool") & 
                                     (liverpool_leads["HalfTimeResult"] == "A") & 
                                     (liverpool_leads["FullTimeResult"] == "A"))
                                ).astype(int)
                                
                                liverpool_leads["Venue"] = liverpool_leads.apply(
                                    lambda row: "Home" if row["HomeTeam"] == "Liverpool" else "Away", axis=1
                                )
                                
                                # Conversion by venue
                                conversion_summary = liverpool_leads.groupby("Venue")["LeadHeld"].agg(["sum", "count"])
                                conversion_summary["ConversionRate"] = (conversion_summary["sum"] / conversion_summary["count"]) * 100
                                conversion_summary = conversion_summary.reset_index()
                                
                                fig_lpool_conv = px.bar(
                                    conversion_summary,
                                    x='Venue',
                                    y='ConversionRate',
                                    title='Liverpool: Halftime Lead Conversion by Venue',
                                    labels={'Venue': 'Venue', 'ConversionRate': 'Conversion Rate (%)'},
                                    color='ConversionRate',
                                    color_discrete_sequence=['#C8102E', '#00A398'],
                                    template='plotly_white'
                                )
                                
                                fig_lpool_conv.update_layout(
                                    height=500,
                                    yaxis=dict(range=[0, 100])
                                )
                                
                                st.plotly_chart(fig_lpool_conv, use_container_width=True)
                            else:
                                st.info("No Liverpool halftime lead data available")
                        else:
                            st.info("No Liverpool data or halftime results available")
                    
                    # Conversion insights
                    if not top_10_conversion.empty:
                        best_converter = top_10_conversion.iloc[0]
                        st.success(f"👑 **Best Converter:** {best_converter['LeadingTeam']} converts {best_converter['ConversionRate']:.1f}% of halftime leads to wins")
                else:
                    st.info("🕐 **No halftime conversion data available** - requires HalfTimeResult column in dataset")
            
            # Chart 6: Comeback Analysis
            if momentum_chart_selection in ["All Analysis", "Comeback Analysis"]:
                st.markdown("#### 🔄 Comeback Analysis - Teams That Fight Back")
                
                if not team_conversion.empty and 'comeback_stats' in locals():
                    comeback_col1, comeback_col2 = st.columns(2)
                    
                    with comeback_col1:
                        # EPL teams with lowest comeback rate (most consistent when leading)
                        most_consistent = comeback_stats[
                            comeback_stats['TotalOpportunities'] >= 5  # Minimum 5 opportunities for relevance
                        ].sort_values("RemontadaRate", ascending=True).head(10)
                        
                        if not most_consistent.empty:
                            fig_consistent = px.bar(
                                most_consistent,
                                x='LeadingTeam',
                                y='RemontadaRate',
                                title='Most Consistent Teams (Lowest Comeback Rate Against)',
                                labels={'LeadingTeam': 'Team', 'RemontadaRate': 'Opponent Comeback Rate (%)'},
                                color='RemontadaRate',
                                color_continuous_scale='RdYlGn_r',
                                template='plotly_white'
                            )
                            
                            fig_consistent.update_layout(
                                xaxis_tickangle=45,
                                height=500,
                                coloraxis_showscale=False,
                                yaxis=dict(range=[0, max(most_consistent['RemontadaRate']) * 1.1])
                            )
                            
                            st.plotly_chart(fig_consistent, use_container_width=True)
                        else:
                            st.info("Not enough comeback data for consistency analysis")
                    
                    with comeback_col2:
                        # Liverpool comeback analysis
                        if 'HalfTimeResult' in df.columns:
                            liverpool_remontada = df[
                                ((df["HomeTeam"] == "Liverpool") | (df["AwayTeam"] == "Liverpool")) &
                                (df["HalfTimeResult"].isin(["H", "A"]))
                            ].copy()
                            
                            if not liverpool_remontada.empty:
                                liverpool_remontada["ComebackWin"] = (
                                    ((liverpool_remontada["HomeTeam"] == "Liverpool") &
                                     (liverpool_remontada["HalfTimeResult"] == "A") &
                                     (liverpool_remontada["FullTimeResult"] == "H")) |
                                    ((liverpool_remontada["AwayTeam"] == "Liverpool") &
                                     (liverpool_remontada["HalfTimeResult"] == "H") &
                                     (liverpool_remontada["FullTimeResult"] == "A"))
                                ).astype(int)
                                
                                remontada_rate = (liverpool_remontada["ComebackWin"].sum() / len(liverpool_remontada)) * 100
                                total_comebacks = liverpool_remontada["ComebackWin"].sum()
                                total_opportunities = len(liverpool_remontada)
                                
                                # Create a simple visualization for Liverpool's comeback stats
                                comeback_data = pd.DataFrame({
                                    'Metric': ['Comeback Wins', 'Failed Comebacks'],
                                    'Count': [total_comebacks, total_opportunities - total_comebacks]
                                })
                                
                                fig_lpool_comeback = px.pie(
                                    comeback_data,
                                    values='Count',
                                    names='Metric',
                                    title=f'Liverpool Comeback Analysis ({remontada_rate:.1f}% Success Rate)',
                                    color_discrete_map={'Comeback Wins': '#C8102E', 'Failed Comebacks': '#7F7F7F'},
                                    template='plotly_white'
                                )
                                
                                fig_lpool_comeback.update_traces(textposition='inside', textinfo='percent+label')
                                fig_lpool_comeback.update_layout(height=500)
                                
                                st.plotly_chart(fig_lpool_comeback, use_container_width=True)
                                
                                st.info(f"🔁 **Liverpool's Comeback Rate:** {remontada_rate:.2f}% ({total_comebacks}/{total_opportunities} matches)")
                            else:
                                st.info("No Liverpool comeback data available")
                        else:
                            st.info("HalfTimeResult data required for comeback analysis")
                    
                    # Comeback insights
                    if not most_consistent.empty:
                        most_solid = most_consistent.iloc[0]
                        st.success(f"🛡️ **Most Solid When Leading:** {most_solid['LeadingTeam']} - opponents only comeback {most_solid['RemontadaRate']:.1f}% of the time")
                else:
                    st.info("🔄 **No comeback data available** - requires halftime and full-time results")
            
            # Chart 7: Liverpool Momentum Trends
            if momentum_chart_selection in ["All Analysis", "Liverpool Momentum Trends"]:
                st.markdown("#### 📈 Liverpool Seasonal Momentum Analysis")
                
                # Check if we have the necessary data
                if 'HalfTimeResult' in df.columns and 'Season' in df.columns:
                    # Liverpool leads by season conversion
                    liverpool_matches = df[(df['HomeTeam'] == 'Liverpool') | (df['AwayTeam'] == 'Liverpool')].copy()
                    
                    if not liverpool_matches.empty:
                        liverpool_leads = liverpool_matches[
                            ((liverpool_matches['HomeTeam'] == 'Liverpool') & (liverpool_matches['HalfTimeResult'] == 'H')) |
                            ((liverpool_matches['AwayTeam'] == 'Liverpool') & (liverpool_matches['HalfTimeResult'] == 'A'))
                        ].copy()
                        
                        if not liverpool_leads.empty:
                            liverpool_leads["LeadHeld"] = (
                                ((liverpool_leads["HomeTeam"] == "Liverpool") & 
                                 (liverpool_leads["HalfTimeResult"] == "H") & 
                                 (liverpool_leads["FullTimeResult"] == "H")) |
                                ((liverpool_leads["AwayTeam"] == "Liverpool") & 
                                 (liverpool_leads["HalfTimeResult"] == "A") & 
                                 (liverpool_leads["FullTimeResult"] == "A"))
                            ).astype(int)
                            
                            liverpool_season_conversion = liverpool_leads.groupby("Season")["LeadHeld"].agg(["sum", "count"])
                            liverpool_season_conversion["ConversionRate"] = (
                                liverpool_season_conversion["sum"] / liverpool_season_conversion["count"]
                            ) * 100
                            liverpool_season_conversion = liverpool_season_conversion.reset_index()
                            
                            if len(liverpool_season_conversion) > 1:
                                momentum_col1, momentum_col2 = st.columns(2)
                                
                                with momentum_col1:
                                    # Liverpool conversion rate by season
                                    fig_season_conv = px.line(
                                        liverpool_season_conversion,
                                        x='Season',
                                        y='ConversionRate',
                                        markers=True,
                                        title='Liverpool: Halftime Lead Conversion by Season',
                                        labels={'Season': 'Season', 'ConversionRate': 'Conversion Rate (%)'},
                                        template='plotly_white'
                                    )
                                    
                                    fig_season_conv.update_traces(line_color='#C8102E', marker_size=8)
                                    fig_season_conv.update_layout(
                                        xaxis_tickangle=45,
                                        height=500,
                                        yaxis=dict(range=[0, 100])
                                    )
                                    
                                    st.plotly_chart(fig_season_conv, use_container_width=True)
                                
                                with momentum_col2:
                                    # Season performance distribution
                                    liverpool_season_conversion['Performance'] = liverpool_season_conversion['ConversionRate'].apply(
                                        lambda x: 'Excellent' if x >= 80 else 'Good' if x >= 60 else 'Average' if x >= 40 else 'Poor'
                                    )
                                    
                                    perf_counts = liverpool_season_conversion['Performance'].value_counts().reset_index()
                                    perf_counts.columns = ['Performance', 'Count']
                                    
                                    fig_perf_dist = px.bar(
                                        perf_counts,
                                        x='Performance',
                                        y='Count',
                                        title='Liverpool: Season Performance Distribution',
                                        labels={'Performance': 'Performance Level', 'Count': 'Number of Seasons'},
                                        color='Performance',
                                        color_discrete_map={'Excellent': '#00B04F', 'Good': '#FFD700', 'Average': '#FF8C00', 'Poor': '#DC143C'},
                                        template='plotly_white'
                                    )
                                    
                                    fig_perf_dist.update_layout(height=500)
                                    
                                    st.plotly_chart(fig_perf_dist, use_container_width=True)
                                
                                # Momentum insights
                                best_season = liverpool_season_conversion.loc[liverpool_season_conversion['ConversionRate'].idxmax()]
                                worst_season = liverpool_season_conversion.loc[liverpool_season_conversion['ConversionRate'].idxmin()]
                                
                                st.success(f"🏆 **Best Momentum Season:** {best_season['Season']} ({best_season['ConversionRate']:.1f}% conversion)")
                                st.error(f"📉 **Challenging Season:** {worst_season['Season']} ({worst_season['ConversionRate']:.1f}% conversion)")
                            else:
                                st.info("Insufficient Liverpool season data for trend analysis")
                        else:
                            st.info("No Liverpool halftime lead data found")
                    else:
                        st.info("No Liverpool matches found in dataset")
                else:
                    st.info("📈 **Season momentum analysis requires:** HalfTimeResult and Season columns")
            
            # Chart 8: Team Comparison Matrix
            if momentum_chart_selection in ["All Analysis", "Team Comparison Matrix"]:
                st.markdown("#### 📊 Comprehensive Team Performance Matrix")
                
                matrix_col1, matrix_col2 = st.columns(2)
                
                with matrix_col1:
                    if not team_conversion.empty and not avg_goals.empty:
                        # Performance vs consistency matrix
                        try:
                            # Merge different team stats
                            team_matrix = team_performance.merge(
                                team_conversion[['LeadingTeam', 'ConversionRate']], 
                                left_on='index', right_on='LeadingTeam', how='inner'
                            )
                            team_matrix = team_matrix.merge(avg_goals[['index', 'AvgHomeGoals']], on='index', how='inner')
                            
                            if not team_matrix.empty:
                                # Calculate total performance score
                                team_matrix['WinTotal'] = team_matrix['HomeWins'] + team_matrix['AwayWins']
                                team_matrix['PerformanceScore'] = (
                                    team_matrix['WinTotal'] * 0.4 + 
                                    team_matrix['ConversionRate'] * 0.3 + 
                                    team_matrix['AvgHomeGoals'] * 10 * 0.3
                                )
                                
                                top_performers = team_matrix.nlargest(10, 'PerformanceScore')
                                
                                fig_matrix = px.scatter(
                                    top_performers,
                                    x='ConversionRate',
                                    y='AvgHomeGoals',
                                    size='WinTotal',
                                    color='PerformanceScore',
                                    text='index',
                                    title='Team Performance Matrix: Conversion vs Goals (Size=Wins)',
                                    labels={'ConversionRate': 'Halftime Conversion Rate (%)', 
                                           'AvgHomeGoals': 'Average Home Goals',
                                           'WinTotal': 'Total Wins'},
                                    color_continuous_scale='Viridis',
                                    template='plotly_white'
                                )
                                
                                fig_matrix.update_traces(textposition='top center')
                                fig_matrix.update_layout(height=600)
                                
                                st.plotly_chart(fig_matrix, use_container_width=True)
                            else:
                                st.info("Insufficient data for performance matrix after merging")
                        except Exception as e:
                            st.warning(f"Could not create performance matrix: {str(e)}")
                            
                            # Fallback: simple goals vs wins scatter
                            if not avg_goals.empty:
                                simple_matrix = team_performance.merge(avg_goals[['index', 'AvgHomeGoals']], on='index', how='inner')
                                simple_matrix['TotalWins'] = simple_matrix['HomeWins'] + simple_matrix['AwayWins']
                                
                                fig_simple = px.scatter(
                                    simple_matrix.head(15),
                                    x='AvgHomeGoals',
                                    y='TotalWins',
                                    text='index',
                                    title='Team Performance: Goals vs Wins',
                                    labels={'AvgHomeGoals': 'Average Home Goals', 'TotalWins': 'Total Wins'},
                                    template='plotly_white'
                                )
                                
                                fig_simple.update_traces(textposition='top center')
                                fig_simple.update_layout(height=500)
                                
                                st.plotly_chart(fig_simple, use_container_width=True)
                    else:
                        st.info("Performance matrix requires both conversion and goals data")
                
                with matrix_col2:
                    # Top teams summary table
                    try:
                        if not team_conversion.empty and not avg_goals.empty:
                            summary_stats = team_conversion.merge(
                                avg_goals[['index', 'AvgHomeGoals', 'AvgAwayGoals']], 
                                left_on='LeadingTeam', right_on='index', how='inner'
                            )
                            summary_stats = summary_stats.merge(
                                team_performance[['index', 'HomeWins', 'AwayWins']], 
                                on='index', how='inner'
                            )
                            
                            summary_display = summary_stats[['LeadingTeam', 'ConversionRate', 'AvgHomeGoals', 'HomeWins']].copy()
                            summary_display = summary_display.sort_values('ConversionRate', ascending=False).head(10)
                            summary_display.columns = ['Team', 'Conversion %', 'Home Goals/Game', 'Home Wins']
                            summary_display = summary_display.round(2)
                            
                            st.markdown("##### 🏆 Top 10 Teams Performance Summary")
                            
                            st.dataframe(
                                summary_display.style.background_gradient(
                                    subset=['Conversion %', 'Home Goals/Game'], 
                                    cmap='RdYlGn'
                                ),
                                use_container_width=True
                            )
                            
                            # Performance insights
                            if not summary_display.empty:
                                best_overall = summary_display.iloc[0]
                                st.success(f"🏅 **Best Overall Performance:** {best_overall['Team']} - {best_overall['Conversion %']:.1f}% conversion, {best_overall['Home Goals/Game']:.2f} goals/game")
                        else:
                            st.info("Summary table requires both conversion and goals data")
                    except Exception as e:
                        st.warning(f"Could not create summary table: {str(e)}")
                        
                        # Fallback: basic team stats
                        basic_summary = team_performance.merge(avg_goals[['index', 'AvgHomeGoals']], on='index', how='inner')
                        basic_summary['TotalWins'] = basic_summary['HomeWins'] + basic_summary['AwayWins']
                        basic_display = basic_summary[['index', 'TotalWins', 'AvgHomeGoals']].sort_values('TotalWins', ascending=False).head(10)
                        basic_display.columns = ['Team', 'Total Wins', 'Home Goals/Game']
                        
                        st.markdown("##### 📊 Basic Team Statistics")
                        st.dataframe(basic_display.round(2), use_container_width=True)
            
            # Enhanced Summary Statistics Table
            st.markdown("### 📋 Comprehensive Team Performance Statistics")
            
            try:
                if not team_conversion.empty and not avg_goals.empty:
                    # Create comprehensive summary
                    final_summary = team_performance.merge(
                        team_conversion[['LeadingTeam', 'ConversionRate', 'sum', 'count']], 
                        left_on='index', right_on='LeadingTeam', how='left'
                    )
                    final_summary = final_summary.merge(avg_goals[['index', 'AvgHomeGoals', 'AvgAwayGoals']], on='index', how='left')
                    final_summary = final_summary.merge(team_performance_l[['index', 'HomeLoss', 'AwayLoss']], on='index', how='left')
                    
                    # Calculate additional metrics
                    final_summary['TotalWins'] = final_summary['HomeWins'] + final_summary['AwayWins']
                    final_summary['TotalDraws'] = final_summary['HomeDraws'] + final_summary['AwayDraws']  
                    final_summary['TotalLosses'] = final_summary['HomeLoss'] + final_summary['AwayLoss']
                    final_summary['HomeAdvantage'] = final_summary['AvgHomeGoals'] - final_summary['AvgAwayGoals']
                    
                    # Display comprehensive table
                    display_final = final_summary[[
                        'index', 'TotalWins', 'TotalDraws', 'TotalLosses', 
                        'AvgHomeGoals', 'AvgAwayGoals', 'HomeAdvantage', 'ConversionRate'
                    ]].copy()
                    
                    display_final = display_final.sort_values('TotalWins', ascending=False)
                    display_final.columns = [
                        'Team', 'Total Wins', 'Total Draws', 'Total Losses',
                        'Home Goals/Game', 'Away Goals/Game', 'Home Advantage', 'HT Conversion %'
                    ]
                    display_final = display_final.fillna(0).round(2)
                    
                    st.dataframe(
                        display_final.style.background_gradient(
                            subset=['Total Wins', 'Home Goals/Game', 'Home Advantage', 'HT Conversion %'], 
                            cmap='RdYlGn'
                        ),
                        use_container_width=True
                    )
                else:
                    # Fallback basic table
                    basic_summary = team_performance.merge(avg_goals[['index', 'AvgHomeGoals', 'AvgAwayGoals']], on='index', how='inner')
                    basic_summary['TotalWins'] = basic_summary['HomeWins'] + basic_summary['AwayWins']
                    basic_summary['HomeAdvantage'] = basic_summary['AvgHomeGoals'] - basic_summary['AvgAwayGoals']
                    
                    basic_display = basic_summary[[
                        'index', 'TotalWins', 'AvgHomeGoals', 'AvgAwayGoals', 'HomeAdvantage'
                    ]].sort_values('TotalWins', ascending=False)
                    
                    basic_display.columns = ['Team', 'Total Wins', 'Home Goals/Game', 'Away Goals/Game', 'Home Advantage']
                    basic_display = basic_display.round(2)
                    
                    st.dataframe(basic_display, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating summary table: {str(e)}")
                st.info("Basic team performance data shown instead")
            
            # Key Insights Summary
            st.markdown("### 🎯 Key Team Momentum & Conversion Insights")
            
            insights_col1, insights_col2, insights_col3 = st.columns(3)
            
            with insights_col1:
                st.info(f"🏆 **Main Teams:** {epl_team_count}")
                st.info(f"📊 **Matches Analyzed:** {total_matches:,}")
                
                if not team_conversion.empty:
                    # Filter for teams with sufficient data
                    valid_conversion = team_conversion[team_conversion['count'] >= 3]
                    if not valid_conversion.empty:
                        avg_conversion = valid_conversion['ConversionRate'].mean()
                        st.success(f"📈 **Avg HT Conversion:** {avg_conversion:.1f}%")
                    else:
                        st.info("📈 **HT Conversion:** Insufficient data")
                else:
                    st.info("📈 **HT Conversion:** No data available")
            
            with insights_col2:
                if not avg_goals.empty:
                    avg_home_goals = avg_goals['AvgHomeGoals'].mean()
                    avg_away_goals = avg_goals['AvgAwayGoals'].mean()
                    st.info(f"⚽ **Average Home Goals:** {avg_home_goals:.2f} per game")
                    st.info(f"✈️ **Average Away Goals:** {avg_away_goals:.2f} per game")
                    st.success(f"🏠 **Home Advantage:** {avg_home_goals - avg_away_goals:.2f} goals")
            
            with insights_col3:
                if not team_performance_l.empty:
                    avg_home_losses = team_performance_l['HomeLoss'].mean()
                    avg_away_losses = team_performance_l['AwayLoss'].mean()
                    st.info(f"🏠 **Avg Home Losses:** {avg_home_losses:.1f}")
                    st.info(f"✈️ **Avg Away Losses:** {avg_away_losses:.1f}")
                    
                    if avg_home_losses < avg_away_losses:
                        st.success("🛡️ **Home defensive advantage confirmed**")
                    else:
                        st.warning("⚠️ **Away teams competitive defensively**")
            
            # Final momentum analysis summary
            st.markdown("### 📊 EPL Momentum Analysis Summary")
            
            momentum_summary = f"""
            **Key Findings from EPL Team Momentum & Conversion Analysis (Premier League Teams Only):**
            
            🏆 **EPL Performance Leaders:** Top Premier League teams show strong correlation between home advantage and overall success
            
            📈 **EPL Conversion Rates:** Premier League teams with higher halftime lead conversion rates tend to have better overall records
            
            🔄 **EPL Comeback Analysis:** Most consistent Premier League teams (lowest opponent comeback rate) typically have strong defensive structures
            
            ⚽ **EPL Goal Patterns:** Home advantage is clearly evident in goal-scoring statistics across Premier League teams
            
            🔴 **Liverpool EPL Insights:** Detailed season-by-season analysis shows Liverpool's momentum trends against Premier League opposition
            
            📊 **Premier League Balance:** Data reveals the competitive nature of the EPL with varying team strengths and weaknesses among top-flight clubs
            
            **Teams Analyzed:** {epl_team_count} Premier League clubs across {total_matches:,} matches
            """
            
            st.markdown(momentum_summary)
            
        except FileNotFoundError:
            st.error("❌ Error: 'epl_final.csv' file not found.")
            st.info("""
            📋 **To use this momentum analysis:**
            1. Place your 'epl_final.csv' file in the same directory as this script
            2. Make sure the CSV has required columns: 'HomeTeam', 'AwayTeam', 'FullTimeResult', 'HalfTimeResult', 'Season', etc.
            3. Refresh the page
            """)
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    
    with tab7:
        st.markdown("""
        <div class="tab-content">
            <h3>🔥 Attacking Trends</h3>
            <p>Comprehensive analysis of attacking patterns and shot conversion trends</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load EPL dataset
            df = pd.read_csv('epl_final.csv')
            
            # Filter for EPL teams only (same as Tab6)
            premier_league_teams = {
                'Arsenal', 'Aston Villa', 'Brighton', 'Brighton & Hove Albion', 
                'Brighton and Hove Albion', 'Burnley', 'Chelsea', 'Crystal Palace', 
                'Everton', 'Liverpool', 'Manchester City', 'Manchester United', 
                'Manchester Utd', 'Newcastle United', 'Newcastle Utd', 
                'Southampton', 'Tottenham', 'Tottenham Hotspur', 'West Ham', 
                'West Ham United', 'Wolverhampton Wanderers', 'Wolves',
                'Bournemouth', 'AFC Bournemouth', 'Brentford', 'Cardiff City', 
                'Fulham', 'Huddersfield', 'Huddersfield Town', 'Hull City', 
                'Leicester City', 'Leeds United', 'Leeds', 'Norwich City', 
                'Nottingham Forest', 'Sheffield United', 'Sheffield Utd',
                'Watford', 'West Bromwich Albion', 'West Brom'
            }
            
            # Get EPL teams in dataset
            all_teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
            epl_teams_in_data = [team for team in all_teams 
                               if any(team.lower().strip() == epl_team.lower().strip() 
                                    for epl_team in premier_league_teams)]
            
            # Filter for EPL teams only
            df = df[
                (df['HomeTeam'].isin(epl_teams_in_data)) & 
                (df['AwayTeam'].isin(epl_teams_in_data))
            ].copy()
            
            # Create working copy
            df_copy = df.copy()
            
            # Calculate match-level attacking features
            df_copy["TotalGoals"] = df_copy["FullTimeHomeGoals"] + df_copy["FullTimeAwayGoals"]
            
            # Check if shot data exists
            has_shots_data = 'HomeShots' in df_copy.columns and 'AwayShots' in df_copy.columns
            if has_shots_data:
                df_copy["TotalShots"] = df_copy["HomeShots"] + df_copy["AwayShots"]
            
            df_copy["WinMargin"] = abs(df_copy["FullTimeHomeGoals"] - df_copy["FullTimeAwayGoals"])
            
            # Display summary statistics
            st.markdown("### 🔥 EPL Attacking Trends Summary")
            
            # Calculate key attacking metrics
            avg_goals_per_match = df_copy["TotalGoals"].mean()
            if has_shots_data:
                avg_shots_per_match = df_copy["TotalShots"].mean()
                avg_conversion_rate = (avg_goals_per_match / avg_shots_per_match * 100) if avg_shots_per_match > 0 else 0
            avg_win_margin = df_copy["WinMargin"].mean()
            
            # Liverpool specific metrics
            liverpool_matches = df_copy[(df_copy["HomeTeam"] == "Liverpool") | (df_copy["AwayTeam"] == "Liverpool")].copy()
            liverpool_matches['Venue'] = liverpool_matches.apply(
                lambda row: 'Home' if row['HomeTeam'] == 'Liverpool' else 'Away', axis=1
            )
            
            # Liverpool goals by venue
            liverpool_home_goals = liverpool_matches[liverpool_matches['Venue'] == 'Home']['TotalGoals'].mean()
            liverpool_away_goals = liverpool_matches[liverpool_matches['Venue'] == 'Away']['TotalGoals'].mean()
            home_attacking_advantage = liverpool_home_goals - liverpool_away_goals
            
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            
            with summary_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚽ EPL Average</h3>
                    <h2>{avg_goals_per_match:.1f}</h2>
                    <h1>Goals/Match</h1>
                    <small>League Average</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col2:
                if has_shots_data:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🎯 Conversion Rate</h3>
                        <h2>{avg_conversion_rate:.1f}%</h2>
                        <h1>League Avg</h1>
                        <small>Goals per Shot</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📊 Win Margins</h3>
                        <h2>{avg_win_margin:.1f}</h2>
                        <h1>Goals</h1>
                        <small>Average Difference</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            with summary_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔴 Liverpool Home</h3>
                    <h2>{liverpool_home_goals:.1f}</h2>
                    <h1>Goals/Match</h1>
                    <small>At Anfield</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col4:
                # Home attacking advantage analysis
                if home_attacking_advantage > 0.5:
                    advantage_level = "Strong"
                    advantage_color = "#00B04F"
                elif home_attacking_advantage > 0.2:
                    advantage_level = "Moderate"
                    advantage_color = "#FFD700"
                else:
                    advantage_level = "Minimal"
                    advantage_color = "#FF6B6B"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {advantage_color} 0%, #8B0000 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
                    <h3>🏠 Home Attack Boost</h3>
                    <h2>+{home_attacking_advantage:.1f}</h2>
                    <h1>{advantage_level}</h1>
                    <small>Goals/Match Advantage</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Chart selection
            st.markdown("### 🔥 Attacking Analysis Selection")
            attacking_chart_selection = st.selectbox(
                "Choose Attacking Analysis",
                ["All Analysis", "League Attack Trends", "Liverpool Attack Evolution", 
                 "Liverpool Home vs Away Attack", "Shot Conversion Analysis", "Liverpool Shot Efficiency",
                 "Attack Trend Comparison", "Goal Margin Analysis"],
                index=0,
                key="attacking_chart_selection"
            )
            
            # Chart 1: League Attack Trends Over Time
            if attacking_chart_selection in ["All Analysis", "League Attack Trends"]:
                st.markdown("#### 📈 Is the League Becoming More Attack-Oriented Over Time?")
                
                if 'Season' in df_copy.columns:
                    # Group by Season and calculate average attacking metrics
                    columns_to_analyze = ["TotalGoals", "WinMargin"]
                    if has_shots_data:
                        columns_to_analyze.append("TotalShots")
                    
                    attack_trend = df_copy.groupby("Season")[columns_to_analyze].mean()
                    attack_trend = attack_trend.sort_index()
                    
                    # Create the attacking trends chart
                    fig_attack_trend = go.Figure()
                    
                    # Goals trend
                    fig_attack_trend.add_trace(go.Scatter(
                        x=attack_trend.index,
                        y=attack_trend["TotalGoals"],
                        mode='lines+markers',
                        name='Goals per Match',
                        line=dict(color='#C8102E', width=3),
                        marker=dict(size=8)
                    ))
                    
                    # Shots trend (if available)
                    if has_shots_data:
                        # Scale shots to fit with goals (divide by 10 for visualization)
                        fig_attack_trend.add_trace(go.Scatter(
                            x=attack_trend.index,
                            y=attack_trend["TotalShots"] / 10,  # Scale down for visualization
                            mode='lines+markers',
                            name='Shots per Match (÷10)',
                            line=dict(color='#00A398', width=2),
                            marker=dict(size=6, symbol='square')
                        ))
                    
                    # Win Margin trend
                    fig_attack_trend.add_trace(go.Scatter(
                        x=attack_trend.index,
                        y=attack_trend["WinMargin"],
                        mode='lines+markers',
                        name='Win Margin',
                        line=dict(color='#FFB84D', width=2),
                        marker=dict(size=6, symbol='triangle-up')
                    ))
                    
                    fig_attack_trend.update_layout(
                        title='EPL Attack Trends: Is Football Becoming More Offensive?',
                        xaxis_title='Season',
                        yaxis_title='Average per Match',
                        template='plotly_white',
                        height=500,
                        xaxis_tickangle=45
                    )
                    
                    st.plotly_chart(fig_attack_trend, use_container_width=True)
                    
                    # Analysis insights
                    goals_trend = attack_trend["TotalGoals"].iloc[-1] - attack_trend["TotalGoals"].iloc[0]
                    if goals_trend > 0.2:
                        st.success(f"📈 **League Evolution:** Goals per match increased by {goals_trend:.2f} - EPL becoming more attack-oriented!")
                    elif goals_trend < -0.2:
                        st.info(f"🛡️ **Defensive Era:** Goals per match decreased by {abs(goals_trend):.2f} - more tactical/defensive football")
                    else:
                        st.info(f"⚖️ **Stable Era:** Goals per match relatively stable ({goals_trend:+.2f} change)")
                else:
                    st.warning("Season data not available for trend analysis")
            
            # Chart 2: Liverpool Attack Evolution
            if attacking_chart_selection in ["All Analysis", "Liverpool Attack Evolution"]:
                st.markdown("#### 🔴 Liverpool Attack Evolution Over Time")
                
                if 'Season' in liverpool_matches.columns and not liverpool_matches.empty:
                    # Liverpool seasonal attack trends
                    columns_to_analyze = ["TotalGoals", "WinMargin"]
                    if has_shots_data:
                        columns_to_analyze.append("TotalShots")
                    
                    liverpool_trend = liverpool_matches.groupby("Season")[columns_to_analyze].mean()
                    liverpool_trend = liverpool_trend.sort_index()
                    
                    fig_liverpool_evolution = go.Figure()
                    
                    # Liverpool goals trend
                    fig_liverpool_evolution.add_trace(go.Scatter(
                        x=liverpool_trend.index,
                        y=liverpool_trend["TotalGoals"],
                        mode='lines+markers',
                        name='Goals per Match',
                        line=dict(color='#C8102E', width=3),
                        marker=dict(size=8)
                    ))
                    
                    # Liverpool shots trend (if available)
                    if has_shots_data and "TotalShots" in liverpool_trend.columns:
                        fig_liverpool_evolution.add_trace(go.Scatter(
                            x=liverpool_trend.index,
                            y=liverpool_trend["TotalShots"] / 10,  # Scale for visualization
                            mode='lines+markers',
                            name='Shots per Match (÷10)',
                            line=dict(color='#00A398', width=2),
                            marker=dict(size=6, symbol='square')
                        ))
                    
                    # Liverpool win margin trend
                    fig_liverpool_evolution.add_trace(go.Scatter(
                        x=liverpool_trend.index,
                        y=liverpool_trend["WinMargin"],
                        mode='lines+markers',
                        name='Win Margin',
                        line=dict(color='#FFB84D', width=2),
                        marker=dict(size=6, symbol='triangle-up')
                    ))
                    
                    fig_liverpool_evolution.update_layout(
                        title='Liverpool Attack Evolution: Becoming More Offensive Over Time?',
                        xaxis_title='Season',
                        yaxis_title='Average per Match',
                        template='plotly_white',
                        height=500,
                        xaxis_tickangle=45
                    )
                    
                    st.plotly_chart(fig_liverpool_evolution, use_container_width=True)
                    
                    # Liverpool evolution insights
                    liverpool_goals_trend = liverpool_trend["TotalGoals"].iloc[-1] - liverpool_trend["TotalGoals"].iloc[0]
                    if liverpool_goals_trend > 0.3:
                        st.success(f"🔥 **Liverpool Evolution:** Attack improved by {liverpool_goals_trend:.2f} goals/match - more aggressive style!")
                    elif liverpool_goals_trend < -0.3:
                        st.info(f"🛡️ **Tactical Shift:** Attack decreased by {abs(liverpool_goals_trend):.2f} goals/match - more controlled approach")
                    else:
                        st.info(f"⚖️ **Consistent Style:** Liverpool's attack relatively stable ({liverpool_goals_trend:+.2f} change)")
                else:
                    st.warning("Insufficient Liverpool season data for evolution analysis")
            
            # Chart 3: Liverpool Home vs Away Attack Patterns
            if attacking_chart_selection in ["All Analysis", "Liverpool Home vs Away Attack"]:
                st.markdown("#### 🏠 Liverpool Attack: Home vs Away Deep Analysis")
                
                if 'Season' in liverpool_matches.columns and not liverpool_matches.empty:
                    # Group by Season and Venue for detailed analysis
                    venue_attack_analysis = liverpool_matches.groupby(["Season", "Venue"])[
                        ["TotalGoals", "WinMargin"] + (["TotalShots"] if has_shots_data else [])
                    ].mean().reset_index()
                    
                    venue_col1, venue_col2 = st.columns(2)
                    
                    with venue_col1:
                        # Goals comparison Home vs Away
                        goals_pivot = venue_attack_analysis.pivot(index="Season", columns="Venue", values="TotalGoals")
                        
                        fig_venue_goals = go.Figure()
                        
                        if 'Home' in goals_pivot.columns:
                            fig_venue_goals.add_trace(go.Scatter(
                                x=goals_pivot.index,
                                y=goals_pivot['Home'],
                                mode='lines+markers',
                                name='Home (Anfield)',
                                line=dict(color='#C8102E', width=3),
                                marker=dict(size=8)
                            ))
                        
                        if 'Away' in goals_pivot.columns:
                            fig_venue_goals.add_trace(go.Scatter(
                                x=goals_pivot.index,
                                y=goals_pivot['Away'],
                                mode='lines+markers',
                                name='Away',
                                line=dict(color='#00A398', width=3),
                                marker=dict(size=8)
                            ))
                        
                        fig_venue_goals.update_layout(
                            title='Liverpool: Goals per Match (Home vs Away)',
                            xaxis_title='Season',
                            yaxis_title='Goals per Match',
                            template='plotly_white',
                            height=400,
                            xaxis_tickangle=45
                        )
                        
                        st.plotly_chart(fig_venue_goals, use_container_width=True)
                    
                    with venue_col2:
                        # Shots comparison (if available) or Win Margin
                        if has_shots_data and "TotalShots" in venue_attack_analysis.columns:
                            shots_pivot = venue_attack_analysis.pivot(index="Season", columns="Venue", values="TotalShots")
                            
                            fig_venue_shots = go.Figure()
                            
                            if 'Home' in shots_pivot.columns:
                                fig_venue_shots.add_trace(go.Scatter(
                                    x=shots_pivot.index,
                                    y=shots_pivot['Home'],
                                    mode='lines+markers',
                                    name='Home (Anfield)',
                                    line=dict(color='#FF6B35', width=3),
                                    marker=dict(size=8, symbol='square')
                                ))
                            
                            if 'Away' in shots_pivot.columns:
                                fig_venue_shots.add_trace(go.Scatter(
                                    x=shots_pivot.index,
                                    y=shots_pivot['Away'],
                                    mode='lines+markers',
                                    name='Away',
                                    line=dict(color='#004E89', width=3),
                                    marker=dict(size=8, symbol='square')
                                ))
                            
                            fig_venue_shots.update_layout(
                                title='Liverpool: Shots per Match (Home vs Away)',
                                xaxis_title='Season',
                                yaxis_title='Shots per Match',
                                template='plotly_white',
                                height=400,
                                xaxis_tickangle=45
                            )
                            
                            st.plotly_chart(fig_venue_shots, use_container_width=True)
                        else:
                            # Win Margin comparison
                            margin_pivot = venue_attack_analysis.pivot(index="Season", columns="Venue", values="WinMargin")
                            
                            fig_venue_margin = go.Figure()
                            
                            if 'Home' in margin_pivot.columns:
                                fig_venue_margin.add_trace(go.Scatter(
                                    x=margin_pivot.index,
                                    y=margin_pivot['Home'],
                                    mode='lines+markers',
                                    name='Home (Anfield)',
                                    line=dict(color='#FFD700', width=3),
                                    marker=dict(size=8, symbol='triangle-up')
                                ))
                            
                            if 'Away' in margin_pivot.columns:
                                fig_venue_margin.add_trace(go.Scatter(
                                    x=margin_pivot.index,
                                    y=margin_pivot['Away'],
                                    mode='lines+markers',
                                    name='Away',
                                    line=dict(color='#7F7F7F', width=3),
                                    marker=dict(size=8, symbol='triangle-up')
                                ))
                            
                            fig_venue_margin.update_layout(
                                title='Liverpool: Win Margin (Home vs Away)',
                                xaxis_title='Season',
                                yaxis_title='Win Margin',
                                template='plotly_white',
                                height=400,
                                xaxis_tickangle=45
                            )
                            
                            st.plotly_chart(fig_venue_margin, use_container_width=True)
                    
                    # Home advantage insights
                    st.markdown("### 🏠 What This Proves About Liverpool's Home Attack")
                    
                    if 'Home' in goals_pivot.columns and 'Away' in goals_pivot.columns:
                        avg_home_goals = goals_pivot['Home'].mean()
                        avg_away_goals = goals_pivot['Away'].mean()
                        attack_advantage = avg_home_goals - avg_away_goals
                        
                        insight_col1, insight_col2, insight_col3 = st.columns(3)
                        
                        with insight_col1:
                            if attack_advantage > 0.5:
                                st.success(f"🔥 **Anfield Attack Boost:** +{attack_advantage:.2f} goals/match at home")
                                st.info("**Proves:** Anfield crowd and familiarity significantly enhance Liverpool's attacking play")
                            elif attack_advantage > 0.2:
                                st.info(f"🏠 **Moderate Home Boost:** +{attack_advantage:.2f} goals/match advantage")
                                st.info("**Proves:** Home comfort provides attacking benefit")
                            else:
                                st.warning(f"⚖️ **Consistent Attack:** Only +{attack_advantage:.2f} difference")
                                st.info("**Proves:** Liverpool attacks well everywhere - sign of mental strength")
                        
                        with insight_col2:
                            home_consistency = goals_pivot['Home'].std() if 'Home' in goals_pivot.columns else 0
                            away_consistency = goals_pivot['Away'].std() if 'Away' in goals_pivot.columns else 0
                            
                            if home_consistency < away_consistency:
                                st.success("📈 **More Consistent at Home**")
                                st.info("**Proves:** Anfield provides stable attacking platform")
                            else:
                                st.info("📊 **Consistent Everywhere**")
                                st.info("**Proves:** Professional attacking approach regardless of venue")
                        
                        with insight_col3:
                            recent_seasons = goals_pivot.tail(3) if len(goals_pivot) >= 3 else goals_pivot
                            if not recent_seasons.empty and 'Home' in recent_seasons.columns and 'Away' in recent_seasons.columns:
                                recent_home_avg = recent_seasons['Home'].mean()
                                recent_away_avg = recent_seasons['Away'].mean()
                                recent_advantage = recent_home_avg - recent_away_avg
                                
                                if recent_advantage > attack_advantage:
                                    st.success("📈 **Growing Home Advantage**")
                                    st.info("**Proves:** Anfield effect becoming stronger over time")
                                else:
                                    st.info("📊 **Stable Pattern**")
                                    st.info("**Proves:** Consistent attacking identity maintained")
                
                else:
                    st.warning("Insufficient Liverpool data for home vs away attack analysis")
            
            # Chart 4: Shot Conversion Analysis (League-wide)
            if attacking_chart_selection in ["All Analysis", "Shot Conversion Analysis"] and has_shots_data:
                st.markdown("#### 🎯 EPL Shot Conversion Analysis")
                
                if 'Season' in df_copy.columns:
                    # Calculate league shot conversion by season
                    attack_trend = df_copy.groupby("Season")[["TotalGoals", "TotalShots"]].mean()
                    attack_trend["ShotConversion"] = (attack_trend["TotalGoals"] / attack_trend["TotalShots"]) * 100
                    
                    fig_conversion = go.Figure()
                    
                    # Conversion rate line
                    fig_conversion.add_trace(go.Scatter(
                        x=attack_trend.index,
                        y=attack_trend["ShotConversion"],
                        mode='lines+markers',
                        name='Shot Conversion Rate (%)',
                        line=dict(color='purple', width=3),
                        marker=dict(size=8)
                    ))
                    
                    # Average line
                    avg_conversion = attack_trend["ShotConversion"].mean()
                    fig_conversion.add_hline(
                        y=avg_conversion,
                        line_dash="dash",
                        line_color="gray",
                        annotation_text=f"Average: {avg_conversion:.1f}%"
                    )
                    
                    # Highlight best and worst seasons
                    max_season = attack_trend["ShotConversion"].idxmax()
                    max_val = attack_trend["ShotConversion"].max()
                    min_season = attack_trend["ShotConversion"].idxmin()
                    min_val = attack_trend["ShotConversion"].min()
                    
                    fig_conversion.add_annotation(
                        x=max_season,
                        y=max_val,
                        text=f"Highest: {max_val:.1f}%",
                        arrowhead=2,
                        arrowcolor="green",
                        bgcolor="lightgreen",
                        bordercolor="green"
                    )
                    
                    fig_conversion.add_annotation(
                        x=min_season,
                        y=min_val,
                        text=f"Lowest: {min_val:.1f}%",
                        arrowhead=2,
                        arrowcolor="red",
                        bgcolor="lightcoral",
                        bordercolor="red"
                    )
                    
                    fig_conversion.update_layout(
                        title='EPL Shot Conversion Rate Over Seasons',
                        xaxis_title='Season',
                        yaxis_title='Conversion Rate (%)',
                        template='plotly_white',
                        height=500,
                        xaxis_tickangle=45
                    )
                    
                    st.plotly_chart(fig_conversion, use_container_width=True)
                    
                    # Conversion insights
                    conversion_trend = attack_trend["ShotConversion"].iloc[-1] - attack_trend["ShotConversion"].iloc[0]
                    if conversion_trend > 1:
                        st.success(f"🎯 **Improving Efficiency:** Shot conversion improved by {conversion_trend:.1f}% - better finishing!")
                    elif conversion_trend < -1:
                        st.info(f"📉 **Declining Efficiency:** Shot conversion decreased by {abs(conversion_trend):.1f}% - more shots, same goals")
                    else:
                        st.info(f"⚖️ **Stable Efficiency:** Shot conversion relatively stable ({conversion_trend:+.1f}%)")
                else:
                    st.warning("Season data not available for conversion analysis")
            
            # Chart 5: Liverpool Shot Efficiency 
            if attacking_chart_selection in ["All Analysis", "Liverpool Shot Efficiency"] and has_shots_data:
                st.markdown("#### 🔴 Liverpool Shot Efficiency Analysis")
                
                if 'Season' in liverpool_matches.columns and not liverpool_matches.empty:
                    # Liverpool shot conversion by season
                    liverpool_conversion = liverpool_matches.groupby("Season")[["TotalGoals", "TotalShots"]].mean()
                    liverpool_conversion["ShotConversion"] = (liverpool_conversion["TotalGoals"] / liverpool_conversion["TotalShots"]) * 100
                    
                    fig_liv_conversion = go.Figure()
                    
                    # Liverpool conversion rate
                    fig_liv_conversion.add_trace(go.Scatter(
                        x=liverpool_conversion.index,
                        y=liverpool_conversion["ShotConversion"],
                        mode='lines+markers',
                        name='Liverpool Conversion Rate (%)',
                        line=dict(color='#C8102E', width=3),
                        marker=dict(size=8)
                    ))
                    
                    # Liverpool average line
                    liverpool_avg_conversion = liverpool_conversion["ShotConversion"].mean()
                    fig_liv_conversion.add_hline(
                        y=liverpool_avg_conversion,
                        line_dash="dash",
                        line_color="#C8102E",
                        annotation_text=f"Liverpool Average: {liverpool_avg_conversion:.1f}%",
                        annotation_position="top right"
                    )
                    
                    # Highlight Liverpool's best and worst seasons
                    max_season = liverpool_conversion["ShotConversion"].idxmax()
                    max_val = liverpool_conversion["ShotConversion"].max()
                    min_season = liverpool_conversion["ShotConversion"].idxmin()
                    min_val = liverpool_conversion["ShotConversion"].min()
                    
                    fig_liv_conversion.add_annotation(
                        x=max_season,
                        y=max_val,
                        text=f"Best: {max_val:.1f}%",
                        arrowhead=2,
                        arrowcolor="green",
                        bgcolor="lightgreen",
                        bordercolor="green"
                    )
                    
                    fig_liv_conversion.add_annotation(
                        x=min_season,
                        y=min_val,
                        text=f"Worst: {min_val:.1f}%",
                        arrowhead=2,
                        arrowcolor="red",
                        bgcolor="lightcoral",
                        bordercolor="red"
                    )
                    
                    fig_liv_conversion.update_layout(
                        title='Liverpool Shot Conversion Rate Over Seasons',
                        xaxis_title='Season',
                        yaxis_title='Conversion Rate (%)',
                        template='plotly_white',
                        height=500,
                        xaxis_tickangle=45
                    )
                    
                    st.plotly_chart(fig_liv_conversion, use_container_width=True)
                    
                    # Liverpool efficiency insights
                    liverpool_conversion_trend = liverpool_conversion["ShotConversion"].iloc[-1] - liverpool_conversion["ShotConversion"].iloc[0]
                    
                    efficiency_col1, efficiency_col2 = st.columns(2)
                    
                    with efficiency_col1:
                        if liverpool_conversion_trend > 1:
                            st.success(f"🔥 **Improving Finishing:** Liverpool's conversion improved by {liverpool_conversion_trend:.1f}%")
                            st.info("**Proves:** Better striker coaching, improved player quality, or tactical changes")
                        elif liverpool_conversion_trend < -1:
                            st.info(f"📊 **More Shots, Same Goals:** Conversion decreased by {abs(liverpool_conversion_trend):.1f}%")
                            st.info("**Proves:** More aggressive attacking play, taking more difficult chances")
                        else:
                            st.info(f"⚖️ **Consistent Finishing:** Conversion stable ({liverpool_conversion_trend:+.1f}%)")
                            st.info("**Proves:** Consistent attacking quality maintained")
                    
                    with efficiency_col2:
                        # Compare Liverpool to league average (if we calculated it earlier)
                        if 'attack_trend' in locals() and "ShotConversion" in attack_trend.columns:
                            league_avg_conversion = attack_trend["ShotConversion"].mean()
                            liverpool_vs_league = liverpool_avg_conversion - league_avg_conversion
                            
                            if liverpool_vs_league > 2:
                                st.success(f"🏆 **Elite Finishing:** {liverpool_vs_league:+.1f}% above league average")
                                st.info("**Proves:** Superior attacking quality and clinical finishing")
                            elif liverpool_vs_league > 0:
                                st.success(f"📈 **Above Average:** {liverpool_vs_league:+.1f}% better than league")
                                st.info("**Proves:** Good attacking efficiency")
                            else:
                                st.warning(f"📊 **Room for Improvement:** {abs(liverpool_vs_league):.1f}% below league average")
                                st.info("**Suggests:** Focus needed on finishing or shot selection")
                else:
                    st.warning("Insufficient Liverpool data for shot efficiency analysis")
            
            # Enhanced Summary Analysis
            st.markdown("### 🎯 What Liverpool's Attacking Patterns Prove About Home Advantage")
            
            if not liverpool_matches.empty:
                # Calculate comprehensive attacking metrics
                home_matches = liverpool_matches[liverpool_matches['Venue'] == 'Home']
                away_matches = liverpool_matches[liverpool_matches['Venue'] == 'Away']
                
                if not home_matches.empty and not away_matches.empty:
                    # Goals analysis
                    home_goals_avg = home_matches['TotalGoals'].mean()
                    away_goals_avg = away_matches['TotalGoals'].mean()
                    goals_advantage = home_goals_avg - away_goals_avg
                    
                    # Win margin analysis
                    home_margin_avg = home_matches['WinMargin'].mean()
                    away_margin_avg = away_matches['WinMargin'].mean()
                    margin_advantage = home_margin_avg - away_margin_avg
                    
                    # Shots analysis (if available)
                    if has_shots_data:
                        home_shots_avg = home_matches['TotalShots'].mean()
                        away_shots_avg = away_matches['TotalShots'].mean()
                        shots_advantage = home_shots_avg - away_shots_avg
                        
                        home_conversion = (home_goals_avg / home_shots_avg * 100) if home_shots_avg > 0 else 0
                        away_conversion = (away_goals_avg / away_shots_avg * 100) if away_shots_avg > 0 else 0
                        conversion_advantage = home_conversion - away_conversion
                    
                    proof_col1, proof_col2, proof_col3 = st.columns(3)
                    
                    with proof_col1:
                        st.markdown("#### 🏠 Anfield Attack Advantage")
                        
                        if goals_advantage > 0.3:
                            st.success(f"🔥 **Strong Home Attack:** +{goals_advantage:.2f} goals/match")
                            st.info("**This Proves:**")
                            st.write("• Anfield crowd energizes attacking play")
                            st.write("• Home familiarity improves movement")
                            st.write("• Confident, expansive football at home")
                        elif goals_advantage > 0:
                            st.info(f"🏠 **Moderate Home Boost:** +{goals_advantage:.2f} goals/match")
                            st.info("**This Proves:**")
                            st.write("• Some home advantage in attack")
                            st.write("• Comfortable attacking approach")
                        else:
                            st.warning(f"⚖️ **No Home Attack Advantage:** {goals_advantage:+.2f}")
                            st.info("**This Proves:**")
                            st.write("• Consistent attacking quality everywhere")
                            st.write("• Mental strength and adaptability")
                    
                    with proof_col2:
                        st.markdown("#### 🎯 Attacking Efficiency")
                        
                        if has_shots_data:
                            if conversion_advantage > 1:
                                st.success(f"🎯 **Better Finishing at Home:** +{conversion_advantage:.1f}%")
                                st.info("**This Proves:**")
                                st.write("• More clinical finishing at Anfield")
                                st.write("• Less pressure, better composure")
                                st.write("• Quality over quantity approach")
                            elif conversion_advantage > -1:
                                st.info(f"📊 **Similar Efficiency:** {conversion_advantage:+.1f}%")
                                st.info("**This Proves:**")
                                st.write("• Consistent finishing quality")
                                st.write("• Professional approach everywhere")
                            else:
                                st.warning(f"📉 **Less Efficient at Home:** {conversion_advantage:.1f}%")
                                st.info("**This Could Mean:**")
                                st.write("• More ambitious attempts at home")
                                st.write("• Taking more difficult chances")
                        else:
                            if margin_advantage > 0.2:
                                st.success(f"💥 **Bigger Wins at Home:** +{margin_advantage:.2f}")
                                st.info("**This Proves:**")
                                st.write("• More dominant home performances")
                                st.write("• Ability to overwhelm opponents")
                            else:
                                st.info(f"⚖️ **Consistent Margins:** {margin_advantage:+.2f}")
                    
                    with proof_col3:
                        st.markdown("#### 📈 Attacking Patterns")
                        
                        home_high_scoring = len(home_matches[home_matches['TotalGoals'] >= 3]) / len(home_matches) * 100
                        away_high_scoring = len(away_matches[away_matches['TotalGoals'] >= 3]) / len(away_matches) * 100
                        
                        st.metric(
                            "High-Scoring Games (3+ goals)",
                            f"{home_high_scoring:.1f}% (H) vs {away_high_scoring:.1f}% (A)",
                            f"{home_high_scoring - away_high_scoring:+.1f}%"
                        )
                        
                        if home_high_scoring > away_high_scoring + 5:
                            st.success("🔥 **More Entertaining at Home**")
                            st.info("**This Proves:**")
                            st.write("• Anfield encourages open, attacking football")
                            st.write("• Home crowd demands excitement")
                        else:
                            st.info("📊 **Consistent Entertainment Value**")
                            st.info("**This Proves:**")
                            st.write("• Professional approach everywhere")
                    
                    # Final comprehensive assessment
                    st.markdown("### 🏆 Liverpool Home Attacking Assessment")
                    
                    total_advantages = sum([
                        1 if goals_advantage > 0.2 else 0,
                        1 if margin_advantage > 0.2 else 0,
                        1 if has_shots_data and conversion_advantage > 0.5 else 0,
                        1 if home_high_scoring > away_high_scoring + 3 else 0
                    ])
                    
                    if total_advantages >= 3:
                        st.success("🏠 **STRONG ANFIELD ADVANTAGE:** Multiple attacking metrics show clear home benefit")
                        st.info("**Overall Assessment:** Anfield significantly enhances Liverpool's attacking play through crowd support, familiarity, and confidence")
                    elif total_advantages >= 2:
                        st.info("🏠 **MODERATE HOME BENEFIT:** Some attacking advantages at home")  
                        st.info("**Overall Assessment:** Anfield provides meaningful but not overwhelming attacking boost")
                    else:
                        st.warning("⚖️ **CONSISTENT EVERYWHERE:** Limited home attacking advantage")
                        st.info("**Overall Assessment:** Liverpool's attacking quality is remarkably consistent regardless of venue - sign of mental strength")
            
            # Data summary table
            if not liverpool_matches.empty:
                st.markdown("### 📋 Liverpool Attacking Statistics Summary")
                
                summary_data = []
                for venue in ['Home', 'Away']:
                    venue_data = liverpool_matches[liverpool_matches['Venue'] == venue]
                    if not venue_data.empty:
                        row = {
                            'Venue': venue,
                            'Matches': len(venue_data),
                            'Avg Goals/Match': venue_data['TotalGoals'].mean().round(2),
                            'Avg Win Margin': venue_data['WinMargin'].mean().round(2),
                            'High Scoring (3+)': f"{len(venue_data[venue_data['TotalGoals'] >= 3]) / len(venue_data) * 100:.1f}%"
                        }
                        
                        if has_shots_data:
                            row['Avg Shots/Match'] = venue_data['TotalShots'].mean().round(1)
                            row['Shot Conversion %'] = f"{venue_data['TotalGoals'].sum() / venue_data['TotalShots'].sum() * 100:.1f}%"
                        
                        summary_data.append(row)
                
                if summary_data:
                    summary_df = pd.DataFrame(summary_data)
                    st.dataframe(summary_df, use_container_width=True)
            
        except FileNotFoundError:
            st.error("❌ Error: 'epl_final.csv' file not found.")
            st.info("""
            📋 **To use this attacking analysis:**
            1. Place your 'epl_final.csv' file in the same directory as this script
            2. Make sure the CSV has columns: 'HomeTeam', 'AwayTeam', 'FullTimeHomeGoals', 'FullTimeAwayGoals'
            3. Optional: 'HomeShots', 'AwayShots', 'Season' for enhanced analysis
            4. Refresh the page
            """)
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    
    with tab8:
        st.markdown("""
        <div class="tab-content">
            <h3>🛡️ Physicality & Discipline</h3>
            <p>Comprehensive analysis of fouls, cards, and physical play patterns in the EPL</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load EPL dataset
            df = pd.read_csv('epl_final.csv')
            
            # Filter for EPL teams only (same as previous tabs)
            premier_league_teams = {
                'Arsenal', 'Aston Villa', 'Brighton', 'Brighton & Hove Albion', 
                'Brighton and Hove Albion', 'Burnley', 'Chelsea', 'Crystal Palace', 
                'Everton', 'Liverpool', 'Manchester City', 'Manchester United', 
                'Manchester Utd', 'Newcastle United', 'Newcastle Utd', 
                'Southampton', 'Tottenham', 'Tottenham Hotspur', 'West Ham', 
                'West Ham United', 'Wolverhampton Wanderers', 'Wolves',
                'Bournemouth', 'AFC Bournemouth', 'Brentford', 'Cardiff City', 
                'Fulham', 'Huddersfield', 'Huddersfield Town', 'Hull City', 
                'Leicester City', 'Leeds United', 'Leeds', 'Norwich City', 
                'Nottingham Forest', 'Sheffield United', 'Sheffield Utd',
                'Watford', 'West Bromwich Albion', 'West Brom'
            }
            
            # Get EPL teams in dataset
            all_teams = set(df['HomeTeam'].unique()) | set(df['AwayTeam'].unique())
            epl_teams_in_data = [team for team in all_teams 
                               if any(team.lower().strip() == epl_team.lower().strip() 
                                    for epl_team in premier_league_teams)]
            
            # Filter for EPL teams only
            df = df[
                (df['HomeTeam'].isin(epl_teams_in_data)) & 
                (df['AwayTeam'].isin(epl_teams_in_data))
            ].copy()
            
            st.success(f"✅ **EPL Teams Only:** {len(epl_teams_in_data)} Premier League teams analyzed")
            
            # Create working copy
            df_copy = df.copy()
            
            # Check for required physicality columns
            required_columns = ['HomeFouls', 'AwayFouls', 'HomeYellowCards', 'AwayYellowCards', 'HomeRedCards', 'AwayRedCards']
            missing_columns = [col for col in required_columns if col not in df_copy.columns]
            
            if missing_columns:
                st.error(f"❌ Missing columns for physicality analysis: {missing_columns}")
                st.info("Required columns: HomeFouls, AwayFouls, HomeYellowCards, AwayYellowCards, HomeRedCards, AwayRedCards")
                return
            
            # Calculate physicality metrics
            df_copy["TotalFouls"] = df_copy["HomeFouls"] + df_copy["AwayFouls"]
            df_copy["TotalYellowCards"] = df_copy["HomeYellowCards"] + df_copy["AwayYellowCards"]
            df_copy["TotalRedCards"] = df_copy["HomeRedCards"] + df_copy["AwayRedCards"]
            df_copy["TotalCards"] = df_copy["TotalYellowCards"] + df_copy["TotalRedCards"]
            
            # Liverpool specific analysis
            liverpool_matches = df_copy[(df_copy["HomeTeam"] == "Liverpool") | (df_copy["AwayTeam"] == "Liverpool")].copy()
            liverpool_matches['Venue'] = liverpool_matches.apply(
                lambda row: 'Home' if row['HomeTeam'] == 'Liverpool' else 'Away', axis=1
            )
            
            # Liverpool discipline by venue
            liverpool_home_fouls = liverpool_matches[liverpool_matches['Venue'] == 'Home']['TotalFouls'].mean()
            liverpool_away_fouls = liverpool_matches[liverpool_matches['Venue'] == 'Away']['TotalFouls'].mean()
            discipline_advantage = liverpool_away_fouls - liverpool_home_fouls  # Positive means more disciplined at home
            
            # Display summary statistics
            st.markdown("### 🛡️ EPL Physicality & Discipline Summary")
            
            # Calculate key metrics
            avg_fouls_per_match = df_copy["TotalFouls"].mean()
            avg_yellows_per_match = df_copy["TotalYellowCards"].mean()
            avg_reds_per_match = df_copy["TotalRedCards"].mean()
            
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            
            with summary_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚽ EPL Average</h3>
                    <h2>{avg_fouls_per_match:.1f}</h2>
                    <h1>Fouls/Match</h1>
                    <small>League Average</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🟨 Yellow Cards</h3>
                    <h2>{avg_yellows_per_match:.1f}</h2>
                    <h1>Per Match</h1>
                    <small>League Average</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔴 Liverpool Home</h3>
                    <h2>{liverpool_home_fouls:.1f}</h2>
                    <h1>Fouls/Match</h1>
                    <small>At Anfield</small>
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col4:
                # Home discipline impact analysis
                if discipline_advantage > 1:
                    impact_level = "Strong"
                    impact_color = "#00B04F"
                    impact_description = "Home Advantage"
                elif discipline_advantage > -1:
                    impact_level = "Moderate"
                    impact_color = "#FFD700" 
                    impact_description = "Balanced"
                else:
                    impact_level = "Negative"
                    impact_color = "#FF6B6B"
                    impact_description = "Away Better"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {impact_color} 0%, #8B0000 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;">
                    <h3>🏠 Home Impact</h3>
                    <h2>{discipline_advantage:+.1f}</h2>
                    <h1>{impact_level}</h1>
                    <small>{impact_description}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Add home impact insight below
                if discipline_advantage > 0.5:
                    st.success(f"💪 **Anfield Discipline Effect:** Liverpool commits {discipline_advantage:.1f} fewer fouls at home - shows Anfield provides tactical control and composure")
                elif discipline_advantage < -0.5:
                    st.warning(f"🔥 **Home Intensity:** Liverpool commits {abs(discipline_advantage):.1f} more fouls at home - Anfield crowd may encourage more physical play")
                else:
                    st.info(f"⚖️ **Professional Consistency:** Liverpool maintains similar discipline home and away - sign of mental strength")
            
            # Chart selection
            st.markdown("### 🛡️ Physicality & Discipline Analysis Selection")
            discipline_chart_selection = st.selectbox(
                "Choose Discipline Analysis",
                ["All Analysis", "League Physicality Trends", "Liverpool Discipline Evolution", 
                 "Liverpool Home vs Away Discipline", "Red Card Impact Analysis", "Liverpool Red Card Analysis",
                 "Team Aggression Comparison", "Defensive Efficiency Analysis"],
                index=0,
                key="discipline_chart_selection"
            )
            
            # Chart 1: League Physicality Trends Over Time
            if discipline_chart_selection in ["All Analysis", "League Physicality Trends"]:
                st.markdown("#### 📈 Are Matches Becoming More Physical Over Time?")
                
                if 'Season' in df_copy.columns:
                    # Group by Season and calculate average physicality metrics
                    physical_trends = df_copy.groupby("Season")[
                        ["TotalFouls", "TotalYellowCards", "TotalRedCards"]
                    ].mean()
                    physical_trends = physical_trends.sort_index()
                    
                    # Create subplots for different metrics
                    fig_physical_trends = make_subplots(
                        rows=1, cols=3,
                        subplot_titles=("Fouls per Match", "Yellow Cards per Match", "Red Cards per Match"),
                        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
                    )
                    
                    # Fouls trend
                    fig_physical_trends.add_trace(
                        go.Scatter(
                            x=physical_trends.index,
                            y=physical_trends["TotalFouls"],
                            mode='lines+markers',
                            name='Fouls',
                            line=dict(color='#1f77b4', width=3),
                            marker=dict(size=8)
                        ),
                        row=1, col=1
                    )
                    
                    # Yellow cards trend
                    fig_physical_trends.add_trace(
                        go.Scatter(
                            x=physical_trends.index,
                            y=physical_trends["TotalYellowCards"],
                            mode='lines+markers',
                            name='Yellow Cards',
                            line=dict(color='#ff7f0e', width=3),
                            marker=dict(size=8)
                        ),
                        row=1, col=2
                    )
                    
                    # Red cards trend
                    fig_physical_trends.add_trace(
                        go.Scatter(
                            x=physical_trends.index,
                            y=physical_trends["TotalRedCards"],
                            mode='lines+markers',
                            name='Red Cards',
                            line=dict(color='#d62728', width=3),
                            marker=dict(size=8)
                        ),
                        row=1, col=3
                    )
                    
                    fig_physical_trends.update_layout(
                        title_text='EPL Physicality Trends: Is Football Becoming More Physical?',
                        height=500,
                        showlegend=False,
                        template='plotly_white'
                    )
                    
                    fig_physical_trends.update_xaxes(tickangle=45)
                    fig_physical_trends.update_yaxes(title_text="Average per Match")
                    
                    st.plotly_chart(fig_physical_trends, use_container_width=True)
                    
                    # Analysis insights
                    fouls_trend = physical_trends["TotalFouls"].iloc[-1] - physical_trends["TotalFouls"].iloc[0]
                    cards_trend = physical_trends["TotalYellowCards"].iloc[-1] - physical_trends["TotalYellowCards"].iloc[0]
                    
                    trend_col1, trend_col2 = st.columns(2)
                    
                    with trend_col1:
                        if fouls_trend > 1:
                            st.warning(f"📈 **More Physical:** Fouls increased by {fouls_trend:.1f} per match")
                            st.info("**Suggests:** Game becoming more intense and physical")
                        elif fouls_trend < -1:
                            st.success(f"📉 **Less Physical:** Fouls decreased by {abs(fouls_trend):.1f} per match")
                            st.info("**Suggests:** Better discipline or stricter refereeing")
                        else:
                            st.info(f"⚖️ **Stable Physicality:** Fouls relatively stable ({fouls_trend:+.1f})")
                    
                    with trend_col2:
                        if cards_trend > 0.5:
                            st.warning(f"🟨 **More Cards:** Yellow cards increased by {cards_trend:.1f} per match")
                            st.info("**Suggests:** Stricter refereeing or more aggressive play")
                        elif cards_trend < -0.5:
                            st.success(f"🟨 **Fewer Cards:** Yellow cards decreased by {abs(cards_trend):.1f} per match")
                            st.info("**Suggests:** Better player discipline")
                        else:
                            st.info(f"🟨 **Stable Discipline:** Cards relatively stable ({cards_trend:+.1f})")
                else:
                    st.warning("Season data not available for physicality trend analysis")
            
            # Chart 2: Liverpool Discipline Evolution
            if discipline_chart_selection in ["All Analysis", "Liverpool Discipline Evolution"]:
                st.markdown("#### 🔴 Liverpool Discipline Evolution Over Time")
                
                if 'Season' in liverpool_matches.columns and not liverpool_matches.empty:
                    # Liverpool seasonal discipline trends
                    liverpool_physical_trends = liverpool_matches.groupby("Season")[
                        ["TotalFouls", "TotalYellowCards", "TotalRedCards"]
                    ].mean()
                    liverpool_physical_trends = liverpool_physical_trends.sort_index()
                    
                    # Create Liverpool discipline evolution chart
                    fig_lpool_discipline = make_subplots(
                        rows=1, cols=3,
                        subplot_titles=("Liverpool Fouls/Match", "Liverpool Yellow Cards/Match", "Liverpool Red Cards/Match")
                    )
                    
                    # Liverpool fouls
                    fig_lpool_discipline.add_trace(
                        go.Scatter(
                            x=liverpool_physical_trends.index,
                            y=liverpool_physical_trends["TotalFouls"],
                            mode='lines+markers',
                            name='Fouls',
                            line=dict(color='#C8102E', width=3),
                            marker=dict(size=8)
                        ),
                        row=1, col=1
                    )
                    
                    # Liverpool yellows
                    fig_lpool_discipline.add_trace(
                        go.Scatter(
                            x=liverpool_physical_trends.index,
                            y=liverpool_physical_trends["TotalYellowCards"],
                            mode='lines+markers',
                            name='Yellow Cards',
                            line=dict(color='#FFD700', width=3),
                            marker=dict(size=8)
                        ),
                        row=1, col=2
                    )
                    
                    # Liverpool reds
                    fig_lpool_discipline.add_trace(
                        go.Scatter(
                            x=liverpool_physical_trends.index,
                            y=liverpool_physical_trends["TotalRedCards"],
                            mode='lines+markers',
                            name='Red Cards',
                            line=dict(color='#DC143C', width=3),
                            marker=dict(size=8)
                        ),
                        row=1, col=3
                    )
                    
                    fig_lpool_discipline.update_layout(
                        title_text='Liverpool Discipline Evolution: Becoming More/Less Physical?',
                        height=500,
                        showlegend=False,
                        template='plotly_white'
                    )
                    
                    fig_lpool_discipline.update_xaxes(tickangle=45)
                    fig_lpool_discipline.update_yaxes(title_text="Average per Match")
                    
                    st.plotly_chart(fig_lpool_discipline, use_container_width=True)
                    
                    # Liverpool discipline insights
                    lpool_fouls_trend = liverpool_physical_trends["TotalFouls"].iloc[-1] - liverpool_physical_trends["TotalFouls"].iloc[0]
                    lpool_cards_trend = liverpool_physical_trends["TotalYellowCards"].iloc[-1] - liverpool_physical_trends["TotalYellowCards"].iloc[0]
                    
                    lpool_trend_col1, lpool_trend_col2 = st.columns(2)
                    
                    with lpool_trend_col1:
                        if lpool_fouls_trend > 1:
                            st.warning(f"⚠️ **Liverpool More Physical:** Fouls increased by {lpool_fouls_trend:.1f}")
                            st.info("**Suggests:** More aggressive pressing or tactical intensity")
                        elif lpool_fouls_trend < -1:
                            st.success(f"✅ **Liverpool More Disciplined:** Fouls decreased by {abs(lpool_fouls_trend):.1f}")
                            st.info("**Suggests:** Better discipline or technical improvement")
                        else:
                            st.info(f"⚖️ **Consistent Approach:** Fouls stable ({lpool_fouls_trend:+.1f})")
                    
                    with lpool_trend_col2:
                        if lpool_cards_trend > 0.3:
                            st.warning(f"🟨 **More Cards:** Liverpool cards increased by {lpool_cards_trend:.1f}")
                            st.info("**Could indicate:** More intense playing style or referee targeting")
                        elif lpool_cards_trend < -0.3:
                            st.success(f"🟨 **Better Discipline:** Cards decreased by {abs(lpool_cards_trend):.1f}")
                            st.info("**Proves:** Improved player discipline and control")
                        else:
                            st.info(f"🟨 **Stable Discipline:** Cards stable ({lpool_cards_trend:+.1f})")
                else:
                    st.warning("Insufficient Liverpool season data for discipline evolution analysis")
            
            # Chart 3: Liverpool Home vs Away Discipline
            if discipline_chart_selection in ["All Analysis", "Liverpool Home vs Away Discipline"]:
                st.markdown("#### 🏠 Liverpool Discipline: Home vs Away Analysis")
                
                if not liverpool_matches.empty:
                    # Group by Season and Venue for detailed analysis
                    venue_discipline_analysis = liverpool_matches.groupby(["Season", "Venue"])[
                        ["TotalFouls", "TotalYellowCards", "TotalRedCards"]
                    ].mean().reset_index()
                    
                    discipline_venue_col1, discipline_venue_col2 = st.columns(2)
                    
                    with discipline_venue_col1:
                        # Fouls comparison Home vs Away
                        fouls_pivot = venue_discipline_analysis.pivot(index="Season", columns="Venue", values="TotalFouls")
                        
                        fig_venue_fouls = go.Figure()
                        
                        if 'Home' in fouls_pivot.columns:
                            fig_venue_fouls.add_trace(go.Scatter(
                                x=fouls_pivot.index,
                                y=fouls_pivot['Home'],
                                mode='lines+markers',
                                name='Home (Anfield)',
                                line=dict(color='#C8102E', width=3),
                                marker=dict(size=8)
                            ))
                        
                        if 'Away' in fouls_pivot.columns:
                            fig_venue_fouls.add_trace(go.Scatter(
                                x=fouls_pivot.index,
                                y=fouls_pivot['Away'],
                                mode='lines+markers',
                                name='Away',
                                line=dict(color='#00A398', width=3),
                                marker=dict(size=8)
                            ))
                        
                        fig_venue_fouls.update_layout(
                            title='Liverpool: Fouls per Match (Home vs Away)',
                            xaxis_title='Season',
                            yaxis_title='Fouls per Match',
                            template='plotly_white',
                            height=400,
                            xaxis_tickangle=45
                        )
                        
                        st.plotly_chart(fig_venue_fouls, use_container_width=True)
                    
                    with discipline_venue_col2:
                        # Cards comparison Home vs Away
                        cards_pivot = venue_discipline_analysis.pivot(index="Season", columns="Venue", values="TotalYellowCards")
                        
                        fig_venue_cards = go.Figure()
                        
                        if 'Home' in cards_pivot.columns:
                            fig_venue_cards.add_trace(go.Scatter(
                                x=cards_pivot.index,
                                y=cards_pivot['Home'],
                                mode='lines+markers',
                                name='Home (Anfield)',
                                line=dict(color='#FFD700', width=3),
                                marker=dict(size=8, symbol='square')
                            ))
                        
                        if 'Away' in cards_pivot.columns:
                            fig_venue_cards.add_trace(go.Scatter(
                                x=cards_pivot.index,
                                y=cards_pivot['Away'],
                                mode='lines+markers',
                                name='Away',
                                line=dict(color='#FF8C00', width=3),
                                marker=dict(size=8, symbol='square')
                            ))
                        
                        fig_venue_cards.update_layout(
                            title='Liverpool: Yellow Cards per Match (Home vs Away)',
                            xaxis_title='Season',
                            yaxis_title='Yellow Cards per Match',
                            template='plotly_white',
                            height=400,
                            xaxis_tickangle=45
                        )
                        
                        st.plotly_chart(fig_venue_cards, use_container_width=True)
                    
                    # Home discipline advantage insights
                    st.markdown("### 🏠 How Liverpool's Discipline Impacts Their Home Performance")
                    
                    if 'Home' in fouls_pivot.columns and 'Away' in fouls_pivot.columns:
                        avg_home_fouls = fouls_pivot['Home'].mean()
                        avg_away_fouls = fouls_pivot['Away'].mean()
                        fouls_impact = avg_away_fouls - avg_home_fouls  # Positive = more disciplined at home
                        
                        if 'Home' in cards_pivot.columns and 'Away' in cards_pivot.columns:
                            avg_home_cards = cards_pivot['Home'].mean()
                            avg_away_cards = cards_pivot['Away'].mean()
                            cards_impact = avg_away_cards - avg_home_cards  # Positive = fewer cards at home
                        else:
                            cards_impact = 0
                        
                        impact_col1, impact_col2, impact_col3 = st.columns(3)
                        
                        with impact_col1:
                            st.markdown("#### 🎯 Tactical Control Impact")
                            
                            if fouls_impact > 0.5:
                                st.success(f"✅ **Better Control at Home:** {fouls_impact:.1f} fewer fouls/match")
                                st.info("**Home Performance Impact:**")
                                st.write("• More time on ball = better possession")
                                st.write("• Fewer free kicks against = less danger")
                                st.write("• Controlled tempo = tactical advantage")
                                st.write("• **Result:** Enhanced home dominance")
                            elif fouls_impact < -0.5:
                                st.warning(f"⚡ **More Intense at Home:** {abs(fouls_impact):.1f} more fouls/match")
                                st.info("**Home Performance Impact:**")
                                st.write("• High-intensity pressing at Anfield")
                                st.write("• Crowd demands aggressive play")
                                st.write("• Physical intimidation of opponents")
                                st.write("• **Result:** Anfield becomes fortress through intensity")
                            else:
                                st.info(f"⚖️ **Consistent Approach:** {fouls_impact:+.1f} fouls difference")
                                st.write("• Professional discipline everywhere")
                                st.write("• **Result:** Reliable performance pattern")
                        
                        with impact_col2:
                            st.markdown("#### 🟨 Referee Relationship Impact")
                            
                            if cards_impact > 0.3:
                                st.success(f"🟨 **Card Advantage at Home:** {cards_impact:.1f} fewer cards/match")
                                st.info("**Home Performance Impact:**")
                                st.write("• Key players stay on pitch longer")
                                st.write("• Maintains tactical structure")
                                st.write("• Less disruption to game plan")
                                st.write("• **Result:** Consistent XI throughout match")
                            elif cards_impact < -0.3:
                                st.warning(f"🟨 **More Cards at Home:** {abs(cards_impact):.1f} more cards/match")
                                st.info("**Home Performance Impact:**")
                                st.write("• Emotional reactions to home pressure")
                                st.write("• Higher expectations create tension")
                                st.write("• Referee neutrality regardless of venue")
                                st.write("• **Result:** Must manage emotions better")
                            else:
                                st.info(f"🟨 **Balanced Officiating:** {cards_impact:+.1f} cards difference")
                                st.write("• Fair refereeing home and away")
                                st.write("• **Result:** No referee bias advantage")
                        
                        with impact_col3:
                            st.markdown("#### 🏆 Overall Home Impact Score")
                            
                            # Calculate composite home impact score
                            tactical_score = 2 if fouls_impact > 0.5 else (1 if fouls_impact > 0 else 0)
                            referee_score = 2 if cards_impact > 0.3 else (1 if cards_impact > 0 else 0)
                            total_impact_score = tactical_score + referee_score
                            
                            if total_impact_score >= 3:
                                st.success("🏠 **STRONG HOME DISCIPLINE ADVANTAGE**")
                                st.info("**Performance Boost:**")
                                st.write("• Anfield significantly improves discipline")
                                st.write("• Better tactical control at home")
                                st.write("• Enhanced match management")
                                st.write("• **Impact:** Major home advantage factor")
                            elif total_impact_score >= 2:
                                st.info("🏠 **MODERATE HOME BENEFIT**")
                                st.info("**Performance Boost:**")
                                st.write("• Some discipline advantages at home")
                                st.write("• Contributes to home record")
                                st.write("• **Impact:** Helpful but not decisive")
                            else:
                                st.warning("⚖️ **MINIMAL DISCIPLINE ADVANTAGE**")
                                st.info("**Performance Impact:**")
                                st.write("• Discipline doesn't favor home venue")
                                st.write("• Home advantage comes from other factors")
                                st.write("• **Impact:** Professional consistency everywhere")
                else:
                    st.warning("Insufficient Liverpool data for home vs away discipline analysis")
            
            # Chart 4: Red Card Impact Analysis
            if discipline_chart_selection in ["All Analysis", "Red Card Impact Analysis"]:
                st.markdown("#### 🟥 Red Card Impact Analysis - Who Wins After Red Cards?")
                
                # Red card analysis
                df_reds = df_copy.copy()
                df_reds["HomeRed"] = df_reds["HomeRedCards"] > 0
                df_reds["AwayRed"] = df_reds["AwayRedCards"] > 0
                
                # Who got the red card
                df_reds["RedCardTeam"] = df_reds.apply(
                    lambda row: "Home Team" if row["HomeRed"] else "Away Team" if row["AwayRed"] else "No Red",
                    axis=1
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
                
                if not df_with_red.empty:
                    # Calculate percentages
                    summary = df_with_red.groupby(["RedCardTeam", "RedCardOutcome"]).size().reset_index(name="MatchCount")
                    summary["Percentage"] = (
                        summary["MatchCount"] / summary.groupby("RedCardTeam")["MatchCount"].transform("sum") * 100
                    )
                    
                    # Create red card impact visualization
                    fig_red_impact = px.bar(
                        summary,
                        x="RedCardOutcome",
                        y="Percentage",
                        color="RedCardTeam",
                        title="EPL Match Outcomes After a Red Card",
                        labels={'Percentage': 'Percentage of Matches', 'RedCardOutcome': 'Outcome for Team That Got Red Card'},
                        color_discrete_map={'Home Team': '#5B47EF', 'Away Team': '#118AB2'},
                        text='Percentage',
                        template='plotly_white'
                    )
                    
                    fig_red_impact.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    fig_red_impact.update_layout(height=500, yaxis=dict(range=[0, 100]))
                    
                    st.plotly_chart(fig_red_impact, use_container_width=True)
                    
                    # Red card insights
                    home_losses = summary[(summary['RedCardTeam'] == 'Home Team') & (summary['RedCardOutcome'] == 'Loss')]['Percentage'].values
                    away_losses = summary[(summary['RedCardTeam'] == 'Away Team') & (summary['RedCardOutcome'] == 'Loss')]['Percentage'].values
                    
                    red_insight_col1, red_insight_col2 = st.columns(2)
                    
                    with red_insight_col1:
                        if len(home_losses) > 0:
                            st.error(f"🏠 **Home Team Red Cards:** {home_losses[0]:.1f}% result in losses")
                            st.info("**Analysis:** Red cards significantly hurt home teams' chances")
                    
                    with red_insight_col2:
                        if len(away_losses) > 0:
                            st.error(f"✈️ **Away Team Red Cards:** {away_losses[0]:.1f}% result in losses")
                            st.info("**Analysis:** Red cards are costly for away teams too")
                    
                    # Overall red card impact
                    total_red_cards = len(df_with_red)
                    st.success(f"📊 **Total Red Card Matches Analyzed:** {total_red_cards} in EPL dataset")
                else:
                    st.warning("No red card data available for impact analysis")
            
            # Chart 5: Liverpool Red Card Analysis
            if discipline_chart_selection in ["All Analysis", "Liverpool Red Card Analysis"]:
                st.markdown("#### 🔴 Liverpool Red Card Analysis - How Do They Perform?")
                
                # Liverpool specific red card analysis
                liverpool_reds = liverpool_matches.copy()
                liverpool_reds["HomeRed"] = liverpool_reds["HomeRedCards"] > 0
                liverpool_reds["AwayRed"] = liverpool_reds["AwayRedCards"] > 0
                
                # Who got the red card (Liverpool or Opponent)
                liverpool_reds["RedCardTo"] = liverpool_reds.apply(
                    lambda row: "Liverpool" if (row["HomeTeam"] == "Liverpool" and row["HomeRed"]) or 
                                              (row["AwayTeam"] == "Liverpool" and row["AwayRed"])
                                else "Opponent" if row["HomeRed"] or row["AwayRed"] else "No Red",
                    axis=1
                )
                
                # Liverpool result
                def get_liverpool_result(row):
                    if row["HomeTeam"] == "Liverpool":
                        return "Win" if row["FullTimeResult"] == "H" else "Loss" if row["FullTimeResult"] == "A" else "Draw"
                    else:
                        return "Win" if row["FullTimeResult"] == "A" else "Loss" if row["FullTimeResult"] == "H" else "Draw"
                
                liverpool_reds["LiverpoolResult"] = liverpool_reds.apply(get_liverpool_result, axis=1)
                
                # Only games with red cards
                liverpool_red_only = liverpool_reds[liverpool_reds["RedCardTo"] != "No Red"]
                
                if not liverpool_red_only.empty:
                    red_col1, red_col2 = st.columns(2)
                    
                    with red_col1:
                        # Liverpool red card outcomes
                        liverpool_summary = liverpool_red_only.groupby(["RedCardTo", "LiverpoolResult"]).size().reset_index(name="MatchCount")
                        liverpool_summary["Percentage"] = (
                            liverpool_summary["MatchCount"] / 
                            liverpool_summary.groupby("RedCardTo")["MatchCount"].transform("sum") * 100
                        )
                        
                        fig_liverpool_red = px.bar(
                            liverpool_summary,
                            x="LiverpoolResult",
                            y="Percentage",
                            color="RedCardTo",
                            title="Liverpool: Match Outcomes When Red Cards Given",
                            labels={'Percentage': 'Percentage of Matches', 'LiverpoolResult': 'Liverpool Result'},
                            color_discrete_map={'Liverpool': '#EF476F', 'Opponent': '#06D6A0'},
                            text='Percentage',
                            template='plotly_white'
                        )
                        
                        fig_liverpool_red.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                        fig_liverpool_red.update_layout(height=400, yaxis=dict(range=[0, 100]))
                        
                        st.plotly_chart(fig_liverpool_red, use_container_width=True)
                    
                    with red_col2:
                        # Liverpool red card by venue
                        liverpool_venue_reds = liverpool_reds[liverpool_reds["RedCardTo"] == "Liverpool"]
                        
                        if not liverpool_venue_reds.empty:
                            venue_red_summary = liverpool_venue_reds.groupby(["Venue", "LiverpoolResult"]).size().reset_index(name="Count")
                            
                            # Create pie charts for home and away
                            fig_venue_reds = make_subplots(
                                rows=1, cols=2,
                                specs=[[{"type": "pie"}, {"type": "pie"}]],
                                subplot_titles=("Liverpool Reds at Home", "Liverpool Reds Away")
                            )
                            
                            for i, venue in enumerate(['Home', 'Away']):
                                venue_data = venue_red_summary[venue_red_summary['Venue'] == venue]
                                if not venue_data.empty:
                                    fig_venue_reds.add_trace(
                                        go.Pie(
                                            labels=venue_data['LiverpoolResult'],
                                            values=venue_data['Count'],
                                            name=venue,
                                            marker_colors=['#930828', '#FFD166', '#06D65D']
                                        ),
                                        row=1, col=i+1
                                    )
                            
                            fig_venue_reds.update_traces(textposition='inside', textinfo='percent+label')
                            fig_venue_reds.update_layout(height=400, title_text="Liverpool Red Card Outcomes by Venue")
                            
                            st.plotly_chart(fig_venue_reds, use_container_width=True)
                        else:
                            st.info("No Liverpool red card data available for venue analysis")
                    
                    # Liverpool red card insights
                    liverpool_red_count = len(liverpool_red_only[liverpool_red_only["RedCardTo"] == "Liverpool"])
                    opponent_red_count = len(liverpool_red_only[liverpool_red_only["RedCardTo"] == "Opponent"])
                    
                    red_insights_col1, red_insights_col2 = st.columns(2)
                    
                    with red_insights_col1:
                        liverpool_win_with_red = liverpool_summary[
                            (liverpool_summary['RedCardTo'] == 'Liverpool') & 
                            (liverpool_summary['LiverpoolResult'] == 'Win')
                        ]['Percentage'].values
                        
                        if len(liverpool_win_with_red) > 0:
                            st.error(f"🔴 **Liverpool Red Cards:** {liverpool_win_with_red[0]:.1f}% still result in wins")
                            st.info("**Shows:** Mental strength even when down to 10 men")
                        
                        st.metric("Liverpool Red Cards", liverpool_red_count)
                    
                    with red_insights_col2:
                        liverpool_win_opponent_red = liverpool_summary[
                            (liverpool_summary['RedCardTo'] == 'Opponent') & 
                            (liverpool_summary['LiverpoolResult'] == 'Win')
                        ]['Percentage'].values
                        
                        if len(liverpool_win_opponent_red) > 0:
                            st.success(f"🟢 **Opponent Red Cards:** {liverpool_win_opponent_red[0]:.1f}% Liverpool wins")
                            st.info("**Shows:** Liverpool capitalizes on opponent mistakes")
                        
                        st.metric("Opponent Red Cards", opponent_red_count)
                else:
                    st.info("No red card data available in Liverpool matches")
            
            # Chart 6: Team Aggression Comparison
            if discipline_chart_selection in ["All Analysis", "Team Aggression Comparison"]:
                st.markdown("#### ⚔️ EPL Team Aggression Analysis")
                
                # Calculate team discipline stats
                home_discipline = df_copy.groupby("HomeTeam").agg(
                    HomeYellows=("HomeYellowCards", "sum"),
                    HomeReds=("HomeRedCards", "sum"),
                    HomeFouls=("HomeFouls", "sum"),
                    HomeGames=("HomeTeam", "count")
                )
                
                away_discipline = df_copy.groupby("AwayTeam").agg(
                    AwayYellows=("AwayYellowCards", "sum"),
                    AwayReds=("AwayRedCards", "sum"),
                    AwayFouls=("AwayFouls", "sum"),
                    AwayGames=("AwayTeam", "count")
                )
                
                # Combine stats
                discipline_stats = home_discipline.join(away_discipline, how="inner")
                discipline_stats.index.name = "Team"
                
                # Calculate rates
                discipline_stats["Cards_Home"] = discipline_stats["HomeYellows"] + discipline_stats["HomeReds"]
                discipline_stats["Cards_Away"] = discipline_stats["AwayYellows"] + discipline_stats["AwayReds"]
                discipline_stats["CardsPerGame_Home"] = discipline_stats["Cards_Home"] / discipline_stats["HomeGames"]
                discipline_stats["CardsPerGame_Away"] = discipline_stats["Cards_Away"] / discipline_stats["AwayGames"]
                discipline_stats["AggressionDelta"] = discipline_stats["CardsPerGame_Away"] - discipline_stats["CardsPerGame_Home"]
                
                # Sort by aggression delta
                delta_sorted = discipline_stats.sort_values("AggressionDelta", ascending=False).head(15)
                
                aggression_col1, aggression_col2 = st.columns(2)
                
                with aggression_col1:
                    # Aggression delta chart
                    colors = ['red' if x > 0 else 'blue' for x in delta_sorted["AggressionDelta"]]
                    
                    fig_aggression = go.Figure(data=[
                        go.Bar(
                            x=delta_sorted["AggressionDelta"],
                            y=delta_sorted.index,
                            orientation='h',
                            marker_color=colors,
                            text=delta_sorted["AggressionDelta"].round(2),
                            textposition='outside'
                        )
                    ])
                    
                    fig_aggression.add_vline(x=0, line_dash="dash", line_color="black")
                    fig_aggression.update_layout(
                        title="Team Aggression Delta: Away - Home Cards/Game",
                        xaxis_title="Difference (Away - Home)",
                        yaxis_title="Team",
                        template='plotly_white',
                        height=500
                    )
                    
                    st.plotly_chart(fig_aggression, use_container_width=True)
                
                with aggression_col2:
                    # Overall cards per game ranking
                    discipline_stats['TotalCardsPerGame'] = (
                        (discipline_stats['Cards_Home'] + discipline_stats['Cards_Away']) /
                        (discipline_stats['HomeGames'] + discipline_stats['AwayGames'])
                    )
                    
                    most_aggressive = discipline_stats.sort_values('TotalCardsPerGame', ascending=False).head(10)
                    
                    fig_most_aggressive = px.bar(
                        x=most_aggressive['TotalCardsPerGame'],
                        y=most_aggressive.index,
                        orientation='h',
                        title="Most Aggressive EPL Teams (Cards per Game)",
                        labels={'x': 'Cards per Game', 'y': 'Team'},
                        color=most_aggressive['TotalCardsPerGame'],
                        color_continuous_scale='Reds',
                        template='plotly_white'
                    )
                    
                    fig_most_aggressive.update_layout(height=500, coloraxis_showscale=False)
                    
                    st.plotly_chart(fig_most_aggressive, use_container_width=True)
                
                # Aggression insights
                if 'Liverpool' in delta_sorted.index:
                    liverpool_delta = delta_sorted.loc['Liverpool', 'AggressionDelta']
                    
                    if liverpool_delta > 0.1:
                        st.warning(f"⚠️ **Liverpool More Aggressive Away:** +{liverpool_delta:.2f} cards/game away")
                        st.info("**Suggests:** Different tactical approach or referee bias")
                    elif liverpool_delta < -0.1:
                        st.success(f"✅ **Liverpool More Disciplined Away:** {liverpool_delta:.2f} cards/game difference")
                        st.info("**Shows:** Better discipline away from home pressure")
                    else:
                        st.info(f"⚖️ **Liverpool Consistent:** {liverpool_delta:+.2f} cards/game difference")
                        st.success("**Shows:** Professional approach regardless of venue")
            
            # Enhanced Summary Analysis
            if not liverpool_matches.empty:
                st.markdown("### 🏠 How Liverpool's Discipline Patterns Impact Home Performance")
                
                # Calculate comprehensive discipline metrics
                home_discipline_matches = liverpool_matches[liverpool_matches['Venue'] == 'Home']
                away_discipline_matches = liverpool_matches[liverpool_matches['Venue'] == 'Away']
                
                if not home_discipline_matches.empty and not away_discipline_matches.empty:
                    # Comprehensive discipline impact analysis
                    home_fouls_avg = home_discipline_matches['TotalFouls'].mean()
                    away_fouls_avg = away_discipline_matches['TotalFouls'].mean()
                    home_cards_avg = home_discipline_matches['TotalCards'].mean()
                    away_cards_avg = away_discipline_matches['TotalCards'].mean()
                    
                    discipline_impact = away_fouls_avg - home_fouls_avg  # Positive = more disciplined at home
                    card_impact = away_cards_avg - home_cards_avg  # Positive = fewer cards at home
                    
                    # Red card impact analysis
                    home_reds = home_discipline_matches['TotalRedCards'].sum()
                    away_reds = away_discipline_matches['TotalRedCards'].sum()
                    home_games = len(home_discipline_matches)
                    away_games = len(away_discipline_matches)
                    
                    impact_col1, impact_col2, impact_col3 = st.columns(3)
                    
                    with impact_col1:
                        st.markdown("#### ⚽ Game Control Impact")
                        
                        if discipline_impact > 0.5:
                            st.success(f"🎯 **Enhanced Ball Possession:** {discipline_impact:.1f} fewer fouls at home")
                            st.info("**Direct Home Performance Benefits:**")
                            st.write("• More uninterrupted possession spells")
                            st.write("• Fewer dangerous free kicks conceded")
                            st.write("• Better rhythm and flow control")
                            st.write("• Opponents get fewer set-piece chances")
                            st.success("**Result: More dominant home displays**")
                        elif discipline_impact < -0.5:
                            st.warning(f"🔥 **High-Intensity Pressing:** {abs(discipline_impact):.1f} more fouls at home")
                            st.info("**Strategic Home Performance Impact:**")
                            st.write("• Aggressive pressing disrupts opponents")
                            st.write("• Physical intimidation at Anfield")
                            st.write("• Crowd-influenced intensity")
                            st.write("• Prevents opponent possession")
                            st.info("**Result: Fortress mentality through physicality**")
                        else:
                            st.info(f"⚖️ **Consistent Control:** {discipline_impact:+.1f} fouls difference")
                            st.write("**Professional approach maintains quality**")
                    
                    with impact_col2:
                        st.markdown("#### 🕐 Match Management Impact")
                        
                        if card_impact > 0.2:
                            st.success(f"🟨 **Better Match Management:** {card_impact:.1f} fewer cards at home")
                            st.info("**Key Home Performance Advantages:**")
                            st.write("• Full squad available longer")
                            st.write("• No tactical disruptions from cards")
                            st.write("• Maintains formation integrity")
                            st.write("• Key players avoid suspensions")
                            st.success("**Result: Consistent XI and tactics**")
                        elif card_impact < -0.2:
                            st.warning(f"🟨 **Emotional Pressure Impact:** {abs(card_impact):.1f} more cards at home")
                            st.info("**Home Performance Challenges:**")
                            st.write("• Home expectations create pressure")
                            st.write("• Emotional reactions to decisions")
                            st.write("• Need better composure management")
                            st.write("• Risk of key player suspensions")
                            st.warning("**Result: Must control emotions better**")
                        else:
                            st.info(f"🟨 **Stable Discipline:** {card_impact:+.1f} cards difference")
                            st.write("**Consistent professionalism benefits performance**")
                    
                    with impact_col3:
                        st.markdown("#### 🏆 Overall Home Impact Rating")
                        
                        # Calculate comprehensive home discipline impact score
                        control_impact = 3 if discipline_impact > 0.5 else (2 if discipline_impact > 0 else 1)
                        management_impact = 3 if card_impact > 0.2 else (2 if card_impact > 0 else 1)
                        red_impact = 3 if (home_reds / home_games) <= (away_reds / away_games) else 1
                        
                        total_home_impact = (control_impact + management_impact + red_impact) / 3
                        
                        if total_home_impact >= 2.5:
                            st.success("🏠 **MAJOR HOME ADVANTAGE**")
                            st.success("**Performance Impact Level: HIGH**")
                            st.info("📈 **Discipline significantly boosts home performance through:**")
                            st.write("• Better tactical control")
                            st.write("• Enhanced possession quality")
                            st.write("• Reduced opponent opportunities")
                            st.write("• Consistent team selection")
                            st.success("🎯 **Anfield discipline = competitive edge**")
                        elif total_home_impact >= 2:
                            st.info("🏠 **MODERATE HOME BENEFIT**")
                            st.info("**Performance Impact Level: MEDIUM**")
                            st.write("📊 **Discipline provides some home advantages:**")
                            st.write("• Contributes to better home record")
                            st.write("• Helps maintain game control")
                            st.write("• Part of overall home advantage")
                            st.info("⚖️ **Useful but not the main factor**")
                        else:
                            st.warning("🏠 **LIMITED DISCIPLINE ADVANTAGE**")
                            st.warning("**Performance Impact Level: LOW**")
                            st.write("📋 **Home advantage comes from other factors:**")
                            st.write("• Crowd support and atmosphere")
                            st.write("• Tactical familiarity")
                            st.write("• Opponent travel fatigue")
                            st.write("• Discipline remains consistent")
                            st.info("✅ **Shows professional mentality**")
                    
                    # Specific performance correlation
                    st.markdown("### 📊 Discipline Impact on Home Results")
                    
                    # Analyze correlation between discipline and results
                    home_results = liverpool_matches[liverpool_matches['Venue'] == 'Home'].copy()
                    
                    # Add result column
                    def get_liverpool_result(row):
                        if row["HomeTeam"] == "Liverpool":
                            return "Win" if row["FullTimeResult"] == "H" else "Loss" if row["FullTimeResult"] == "A" else "Draw"
                        else:
                            return "Win" if row["FullTimeResult"] == "A" else "Loss" if row["FullTimeResult"] == "H" else "Draw"
                    
                    home_results["LiverpoolResult"] = home_results.apply(get_liverpool_result, axis=1)
                    
                    # Calculate discipline by result
                    discipline_by_result = home_results.groupby('LiverpoolResult')[['TotalFouls', 'TotalCards']].mean()
                    
                    result_col1, result_col2 = st.columns(2)
                    
                    with result_col1:
                        if not discipline_by_result.empty and 'Win' in discipline_by_result.index:
                            wins_fouls = discipline_by_result.loc['Win', 'TotalFouls'] if 'Win' in discipline_by_result.index else 0
                            losses_fouls = discipline_by_result.loc['Loss', 'TotalFouls'] if 'Loss' in discipline_by_result.index else wins_fouls
                            
                            fouls_correlation = wins_fouls - losses_fouls
                            
                            if fouls_correlation < -1:
                                st.success(f"🏆 **Wins = Better Discipline:** {abs(fouls_correlation):.1f} fewer fouls in wins")
                                st.info("**This Proves:** Controlled play at home leads to better results")
                            elif fouls_correlation > 1:
                                st.info(f"💪 **Wins = More Intensity:** {fouls_correlation:.1f} more fouls in wins")
                                st.info("**This Shows:** Aggressive pressing at home brings success")
                            else:
                                st.info(f"⚖️ **Results Independent of Fouls:** {fouls_correlation:+.1f} difference")
                    
                    with result_col2:
                        if not discipline_by_result.empty and 'Win' in discipline_by_result.index:
                            wins_cards = discipline_by_result.loc['Win', 'TotalCards'] if 'Win' in discipline_by_result.index else 0
                            losses_cards = discipline_by_result.loc['Loss', 'TotalCards'] if 'Loss' in discipline_by_result.index else wins_cards
                            
                            cards_correlation = wins_cards - losses_cards
                            
                            if cards_correlation < -0.3:
                                st.success(f"🟨 **Wins = Fewer Cards:** {abs(cards_correlation):.1f} fewer cards in wins")
                                st.info("**This Proves:** Disciplined play at home = better results")
                            elif cards_correlation > 0.3:
                                st.warning(f"🟨 **Wins = More Cards:** {cards_correlation:.1f} more cards in wins")
                                st.info("**This Could Mean:** Intense battles lead to wins but cost discipline")
                            else:
                                st.info(f"🟨 **Cards Don't Affect Results:** {cards_correlation:+.1f} difference")
                    
                    # Final home discipline impact assessment
                    st.markdown("### 🎯 Final Assessment: How Discipline Impacts Liverpool's Home Performance")
                    
                    impact_summary = f"""
                    **Liverpool Home Discipline Analysis Summary:**
                    
                    🏠 **Discipline Impact Score:** {total_home_impact:.1f}/3.0 ({'High' if total_home_impact >= 2.5 else 'Medium' if total_home_impact >= 2 else 'Low'})
                    
                    📊 **Key Home Performance Effects:**
                    - **Tactical Control:** {'Enhanced' if discipline_impact > 0.5 else 'Intense' if discipline_impact < -0.5 else 'Consistent'} - {discipline_impact:+.1f} fouls difference
                    - **Match Management:** {'Improved' if card_impact > 0.2 else 'Challenging' if card_impact < -0.2 else 'Stable'} - {card_impact:+.1f} cards difference
                    - **Result Correlation:** {'Positive' if fouls_correlation < -0.5 else 'Neutral'} discipline-performance relationship
                    
                    🏆 **Home Advantage Contribution:**
                    - {'Major factor in home success' if total_home_impact >= 2.5 else 'Moderate contributor to home record' if total_home_impact >= 2 else 'Minor role in home advantage - success comes from other factors'}
                    
                    ⚽ **Anfield Effect on Discipline:**
                    - {f'Anfield significantly improves discipline and control' if discipline_impact > 0.5 and card_impact > 0.2 else f'Anfield encourages intensity and aggression' if discipline_impact < -0.5 else 'Professional consistency regardless of venue'}
                    
                    📈 **Overall Impact:** {'Liverpool gains meaningful home advantage through superior discipline at Anfield' if total_home_impact >= 2.5 else 'Discipline provides some home benefit but other factors more important' if total_home_impact >= 2 else 'Home success driven by factors other than discipline - shows consistent professionalism'}
                    """
                    
                    st.markdown(impact_summary)
            
            # Data summary table
            if not liverpool_matches.empty:
                st.markdown("### 📋 Liverpool Discipline Statistics Summary")
                
                discipline_summary_data = []
                for venue in ['Home', 'Away']:
                    venue_data = liverpool_matches[liverpool_matches['Venue'] == venue]
                    if not venue_data.empty:
                        row = {
                            'Venue': venue,
                            'Matches': len(venue_data),
                            'Avg Fouls/Match': venue_data['TotalFouls'].mean().round(1),
                            'Avg Yellow Cards/Match': venue_data['TotalYellowCards'].mean().round(1),
                            'Total Red Cards': venue_data['TotalRedCards'].sum(),
                            'Red Cards/Game': (venue_data['TotalRedCards'].sum() / len(venue_data)).round(3),
                            'Total Cards/Match': venue_data['TotalCards'].mean().round(1)
                        }
                        discipline_summary_data.append(row)
                
                if discipline_summary_data:
                    discipline_summary_df = pd.DataFrame(discipline_summary_data)
                    
                    # Color code the dataframe
                    st.dataframe(
                        discipline_summary_df.style.background_gradient(
                            subset=['Avg Fouls/Match', 'Total Cards/Match'], 
                            cmap='RdYlGn_r'  # Reverse - lower is better for discipline
                        ),
                        use_container_width=True
                    )
            
        except FileNotFoundError:
            st.error("❌ Error: 'epl_final.csv' file not found.")
            st.info("""
            📋 **To use this physicality analysis:**
            1. Place your 'epl_final.csv' file in the same directory as this script
            2. Make sure the CSV has columns: 'HomeTeam', 'AwayTeam', 'HomeFouls', 'AwayFouls', 'HomeYellowCards', 'AwayYellowCards', 'HomeRedCards', 'AwayRedCards'
            3. Optional: 'Season' for trend analysis
            4. Refresh the page
            """)
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    with tab9:
        st.markdown("""
        <div class="tab-content">
            <h3>🏆 Liverpool's 2019-20 Title-Winning Performance</h3>
            <p>Comprehensive analysis of how Liverpool's statistics powered their Premier League triumph</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            # Load the shot data based on the Python code you provided
            import numpy as np
            
            # Try to load actual data first, fallback to simulated data
            try:
                # Try to load the actual CSV files mentioned in your Python code
                match_infos = pd.read_csv("match_infos_EPL_1920.csv")
                shots = pd.read_csv("shots_EPL_1920.csv")
                
                # Filter Liverpool data from actual files
                liverpool_matches = match_infos[(match_infos['team_h'] == 'Liverpool') | (match_infos['team_a'] == 'Liverpool')].copy()
                liverpool_shots = shots[(shots['h_team'] == 'Liverpool') | (shots['a_team'] == 'Liverpool')].copy()
                
                # Process actual data
                liverpool_matches["date"] = pd.to_datetime(liverpool_matches["date"])
                liverpool_shots["date"] = pd.to_datetime(liverpool_shots["date"])
                liverpool_shots["Venue"] = liverpool_shots.apply(lambda row: "Home" if row["h_team"] == "Liverpool" else "Away", axis=1)
                liverpool_shots["isGoal"] = liverpool_shots["result"] == "Goal"
                
                # Calculate match results
                liverpool_matches["Liverpool_Goals"] = liverpool_matches.apply(
                    lambda row: row["h_goals"] if row["team_h"] == "Liverpool" else row["a_goals"], axis=1)
                liverpool_matches["Opponent_Goals"] = liverpool_matches.apply(
                    lambda row: row["a_goals"] if row["team_h"] == "Liverpool" else row["h_goals"], axis=1)
                liverpool_matches["Venue"] = liverpool_matches.apply(
                    lambda row: "Home" if row["team_h"] == "Liverpool" else "Away", axis=1)
                
                # Calculate results
                def get_result(row):
                    if row['Liverpool_Goals'] > row['Opponent_Goals']:
                        return 'Win'
                    elif row['Liverpool_Goals'] == row['Opponent_Goals']:
                        return 'Draw'
                    else:
                        return 'Loss'
                
                liverpool_matches['Result'] = liverpool_matches.apply(get_result, axis=1)
                liverpool_matches['Points'] = liverpool_matches['Result'].map({'Win': 3, 'Draw': 1, 'Loss': 0})
                
                # Sort by date and calculate cumulative points
                liverpool_matches = liverpool_matches.sort_values('date').reset_index(drop=True)
                liverpool_matches['Match_Number'] = range(1, len(liverpool_matches) + 1)
                liverpool_matches['Cumulative_Points'] = liverpool_matches['Points'].cumsum()
                
                st.success("✅ **Using Actual 2019-20 Liverpool Data**")
                using_real_data = True
                
            except FileNotFoundError:
                st.info("📊 **Using Simulated Data Based on Liverpool's 2019-20 Performance**")
                using_real_data = False
                
                # Create comprehensive simulated match data for 2019-20 season
                np.random.seed(42)  # For consistent results
                
                liverpool_matches = pd.DataFrame({
                    'Match_Number': range(1, 39),  # 38 Premier League matches
                    'date': pd.date_range('2019-08-09', periods=38, freq='10D'),
                    'Venue': ['Home' if i % 2 == 0 else 'Away' for i in range(38)],
                    'Liverpool_Goals': np.random.choice([1, 2, 3, 4, 5], 38, p=[0.1, 0.3, 0.4, 0.15, 0.05]),
                    'Opponent_Goals': np.random.choice([0, 1, 2], 38, p=[0.6, 0.3, 0.1]),
                })
                
                # Calculate results and cumulative stats
                liverpool_matches['Goal_Difference'] = liverpool_matches['Liverpool_Goals'] - liverpool_matches['Opponent_Goals']
                liverpool_matches['Result'] = liverpool_matches.apply(
                    lambda row: 'Win' if row['Liverpool_Goals'] > row['Opponent_Goals'] 
                    else 'Draw' if row['Liverpool_Goals'] == row['Opponent_Goals'] else 'Loss', axis=1
                )
                liverpool_matches['Points'] = liverpool_matches['Result'].map({'Win': 3, 'Draw': 1, 'Loss': 0})
                liverpool_matches['Cumulative_Points'] = liverpool_matches['Points'].cumsum()
                
                # Create shot data
                total_shots = len(liverpool_matches) * 15  # Approximate shots per game
                liverpool_shots = pd.DataFrame({
                    'player': np.random.choice(['Mohamed Salah', 'Sadio Mané', 'Roberto Firmino', 'Jordan Henderson', 'Georginio Wijnaldum'], total_shots, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
                    'Venue': np.random.choice(['Home', 'Away'], total_shots, p=[0.5, 0.5]),
                    'X': np.random.uniform(0.7, 1.05, total_shots),
                    'Y': np.random.uniform(0.2, 0.9, total_shots),
                    'xG': np.random.uniform(0.05, 0.8, total_shots),
                    'result': np.random.choice(['Goal', 'Saved', 'Missed'], total_shots, p=[0.15, 0.4, 0.45]),
                    'shotType': np.random.choice(['RightFoot', 'LeftFoot', 'Header'], total_shots, p=[0.5, 0.3, 0.2]),
                    'situation': np.random.choice(['OpenPlay', 'SetPiece', 'Counter', 'Penalty'], total_shots, p=[0.7, 0.15, 0.1, 0.05])
                })
                liverpool_shots["isGoal"] = liverpool_shots["result"] == "Goal"
            
            # Calculate key performance indicators from the data
            total_points = liverpool_matches['Points'].sum()
            total_wins = len(liverpool_matches[liverpool_matches['Result'] == 'Win'])
            total_draws = len(liverpool_matches[liverpool_matches['Result'] == 'Draw'])
            total_losses = len(liverpool_matches[liverpool_matches['Result'] == 'Loss'])
            goals_scored = liverpool_matches['Liverpool_Goals'].sum()
            goals_conceded = liverpool_matches['Opponent_Goals'].sum()
            goal_difference = goals_scored - goals_conceded
            
            # Home vs Away split (fix the Goal_Difference reference)
            home_matches = liverpool_matches[liverpool_matches['Venue'] == 'Home']
            away_matches = liverpool_matches[liverpool_matches['Venue'] == 'Away']
            home_points = home_matches['Points'].sum()
            away_points = away_matches['Points'].sum()
            home_wins = len(home_matches[home_matches['Result'] == 'Win'])
            away_wins = len(away_matches[away_matches['Result'] == 'Win'])
            
            # Display championship summary
            st.markdown("### 🏆 2019-20 Championship Season Summary")
            
            title_col1, title_col2, title_col3, title_col4 = st.columns(4)
            
            with title_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🏆 Final Points</h3>
                    <h2>{total_points}</h2>
                    <h1>Champions</h1>
                    <small>Premier League Winners</small>
                </div>
                """, unsafe_allow_html=True)
            
            with title_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🔥 Attack Power</h3>
                    <h2>{goals_scored}</h2>
                    <h1>Goals</h1>
                    <small>{goals_scored/len(liverpool_matches):.1f} per game</small>
                </div>
                """, unsafe_allow_html=True)
            
            with title_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🛡️ Defense</h3>
                    <h2>{goals_conceded}</h2>
                    <h1>Conceded</h1>
                    <small>{goals_conceded/len(liverpool_matches):.1f} per game</small>
                </div>
                """, unsafe_allow_html=True)
            
            with title_col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📈 Record</h3>
                    <h2>{total_wins}-{total_draws}-{total_losses}</h2>
                    <h1>{total_wins/len(liverpool_matches)*100:.1f}%</h1>
                    <small>Win Rate</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Chart selection for title analysis
            st.markdown("### 🏆 Championship Analysis")
            title_chart_selection = st.selectbox(
                "Choose Title-Winning Analysis",
                ["How Statistics Won The Title", "Points Accumulation Journey", "Attack vs Defense Balance", 
                 "Home Fortress Analysis", "Top Scorers & Assists", "Shot Analysis & Efficiency", 
                 "Key Players Performance", "Season Timeline"],
                index=0,
                key="title_chart_selection"
            )
            
            # Chart 1: How Statistics Won The Title
            if title_chart_selection == "How Statistics Won The Title":
                st.markdown("#### 🎯 The Statistical Blueprint That Won Liverpool The Title")
                
                # Create comprehensive winning factors analysis
                winning_factors = {
                    'Factor': [
                        'Home Fortress', 'Clinical Finishing', 'Defensive Solidity', 
                        'Key Players', 'Squad Depth', 'Mental Strength'
                    ],
                    'Impact_Score': [
                        min(100, (home_points/57)*100),  # Home point percentage
                        min(100, (goals_scored/70)*100),  # Attack efficiency
                        max(20, 100-(goals_conceded*2)),  # Defense efficiency
                        85, 80, 90  # Estimated scores
                    ]
                }
                
                factors_df = pd.DataFrame(winning_factors)
                
                title_factor_col1, title_factor_col2 = st.columns(2)
                
                with title_factor_col1:
                    # Impact score breakdown
                    fig_impact = px.bar(
                        factors_df,
                        x='Impact_Score',
                        y='Factor',
                        orientation='h',
                        title='Championship Impact Scores',
                        color='Impact_Score',
                        color_continuous_scale='Reds',
                        text='Impact_Score'
                    )
                    
                    fig_impact.update_traces(textposition='outside')
                    fig_impact.update_layout(
                        height=500,
                        coloraxis_showscale=False,
                        xaxis=dict(range=[0, 100])
                    )
                    
                    st.plotly_chart(fig_impact, use_container_width=True)
                
                with title_factor_col2:
                    # Home vs Away performance breakdown
                    venue_comparison = pd.DataFrame({
                        'Venue': ['Home', 'Away'],
                        'Points': [home_points, away_points],
                        'Points_Percentage': [home_points/57*100, away_points/57*100],
                        'Wins': [home_wins, away_wins]
                    })
                    
                    fig_venue = px.pie(
                        venue_comparison,
                        values='Points',
                        names='Venue',
                        title=f'Points Distribution (Total: {total_points})',
                        color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'}
                    )
                    
                    fig_venue.update_traces(textposition='inside', textinfo='percent+label')
                    fig_venue.update_layout(height=400)
                    
                    st.plotly_chart(fig_venue, use_container_width=True)
                
                # How these statistics won the title
                st.markdown("### 🏆 How These Statistics Delivered The Championship")
                
                winning_col1, winning_col2, winning_col3 = st.columns(3)
                
                with winning_col1:
                    st.success(f"🏠 **Home Fortress ({home_points/57*100:.1f}% of home points)**")
                    st.info("**How this won the title:**")
                    st.write(f"• {home_wins} home wins out of {len(home_matches)} games")
                    st.write(f"• {home_points} points from {len(home_matches)} home games") 
                    st.write(f"• Home goal difference: +{home_matches['Liverpool_Goals'].sum() - home_matches['Opponent_Goals'].sum()}")
                    st.write("• Anfield became a fortress")
                    st.success("**Result: Guaranteed point foundation**")
                
                with winning_col2:
                    clean_sheets = len(liverpool_matches[liverpool_matches['Opponent_Goals'] == 0])
                    st.success(f"🛡️ **Defensive Excellence ({100-(goals_conceded*2.5):.0f}/100)**")
                    st.info("**How this won the title:**")
                    st.write(f"• Only {goals_conceded} goals conceded in {len(liverpool_matches)} games")
                    st.write(f"• {clean_sheets} clean sheets")
                    st.write(f"• {goals_conceded/len(liverpool_matches):.2f} goals conceded per game")
                    st.write("• Solid defensive foundation")
                    st.success("**Result: Points through clean sheets**")
                
                with winning_col3:
                    big_wins = len(liverpool_matches[liverpool_matches['Liverpool_Goals'] >= 3])
                    st.success(f"⚽ **Clinical Attack ({min(100, goals_scored*1.2):.0f}/100)**")
                    st.info("**How this won the title:**")
                    st.write(f"• {goals_scored} goals in {len(liverpool_matches)} games")
                    st.write(f"• {big_wins} games with 3+ goals")
                    st.write(f"• {goals_scored/len(liverpool_matches):.2f} goals per game average")
                    st.write("• Clinical finishing in key moments")
                    st.success("**Result: Goals when needed most**")
            
            # Chart 2: Points Accumulation Journey
            elif title_chart_selection == "Points Accumulation Journey":
                st.markdown("#### 📈 The Road to the Title - Championship Journey")
                
                journey_col1, journey_col2 = st.columns(2)
                
                with journey_col1:
                    # Points accumulation chart
                    fig_points = go.Figure()
                    
                    # Liverpool's points progression
                    fig_points.add_trace(go.Scatter(
                        x=liverpool_matches['Match_Number'],
                        y=liverpool_matches['Cumulative_Points'],
                        mode='lines+markers',
                        name='Liverpool Points',
                        line=dict(color='#C8102E', width=4),
                        marker=dict(size=6)
                    ))
                    
                    # Add title-winning pace lines
                    matches_played = liverpool_matches['Match_Number']
                    title_pace = matches_played * 2.5  # 95 points over 38 games pace
                    comfortable_pace = matches_played * 2.3  # 87 points pace
                    
                    fig_points.add_trace(go.Scatter(
                        x=matches_played,
                        y=title_pace,
                        mode='lines',
                        name='Title-Winning Pace (95 pts)',
                        line=dict(color='gold', dash='dash', width=2)
                    ))
                    
                    fig_points.add_trace(go.Scatter(
                        x=matches_played,
                        y=comfortable_pace,
                        mode='lines',
                        name='Comfortable Pace (87 pts)',
                        line=dict(color='green', dash='dot', width=2)
                    ))
                    
                    fig_points.update_layout(
                        title='Liverpool Points Accumulation 2019-20',
                        xaxis_title='Match Number',
                        yaxis_title='Cumulative Points',
                        height=500,
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig_points, use_container_width=True)
                
                with journey_col2:
                    # Key milestones in the journey
                    st.markdown("##### 🏆 Championship Milestones")
                    
                    # Calculate milestones based on actual data
                    quarter_mark = len(liverpool_matches) // 4
                    half_mark = len(liverpool_matches) // 2
                    three_quarter_mark = (len(liverpool_matches) * 3) // 4
                    
                    if quarter_mark < len(liverpool_matches):
                        quarter_points = liverpool_matches.iloc[quarter_mark-1]['Cumulative_Points']
                        st.metric(f"After {quarter_mark} games", f"{quarter_points} points", "Strong start")
                    
                    if half_mark < len(liverpool_matches):
                        half_points = liverpool_matches.iloc[half_mark-1]['Cumulative_Points']
                        st.metric(f"Halfway ({half_mark} games)", f"{half_points} points", "Title pace")
                    
                    if three_quarter_mark < len(liverpool_matches):
                        three_q_points = liverpool_matches.iloc[three_quarter_mark-1]['Cumulative_Points']
                        st.metric(f"After {three_quarter_mark} games", f"{three_q_points} points", "Championship form")
                    
                    st.metric(f"Final ({len(liverpool_matches)} games)", f"{total_points} points", "CHAMPIONS!")
                
                # Performance trend analysis
                st.markdown("### 📊 Performance Trends Throughout Season")
                
                # Calculate rolling averages
                liverpool_matches['Points_Rolling_5'] = liverpool_matches['Points'].rolling(window=5, min_periods=1).mean()
                liverpool_matches['Goals_Rolling_5'] = liverpool_matches['Liverpool_Goals'].rolling(window=5, min_periods=1).mean()
                
                trend_col1, trend_col2 = st.columns(2)
                
                with trend_col1:
                    fig_rolling_points = px.line(
                        liverpool_matches,
                        x='Match_Number',
                        y='Points_Rolling_5',
                        title='Rolling 5-Game Points Average',
                        markers=True
                    )
                    fig_rolling_points.update_traces(line_color='#C8102E')
                    fig_rolling_points.update_layout(height=400)
                    st.plotly_chart(fig_rolling_points, use_container_width=True)
                
                with trend_col2:
                    fig_rolling_goals = px.line(
                        liverpool_matches,
                        x='Match_Number',
                        y='Goals_Rolling_5',
                        title='Rolling 5-Game Goals Average',
                        markers=True
                    )
                    fig_rolling_goals.update_traces(line_color='#00A398')
                    fig_rolling_goals.update_layout(height=400)
                    st.plotly_chart(fig_rolling_goals, use_container_width=True)
            
            # Chart 3: Attack vs Defense Balance
            elif title_chart_selection == "Attack vs Defense Balance":
                st.markdown("#### ⚔️ The Perfect Balance: Liverpool's Attack & Defense")
                
                balance_col1, balance_col2 = st.columns(2)
                
                with balance_col1:
                    # Goals for vs against over time
                    fig_balance = go.Figure()
                    
                    fig_balance.add_trace(go.Scatter(
                        x=liverpool_matches['Match_Number'],
                        y=liverpool_matches['Liverpool_Goals'],
                        mode='markers',
                        name='Goals Scored',
                        marker=dict(color='#C8102E', size=8),
                        opacity=0.7
                    ))
                    
                    fig_balance.add_trace(go.Scatter(
                        x=liverpool_matches['Match_Number'],
                        y=liverpool_matches['Opponent_Goals'],
                        mode='markers',
                        name='Goals Conceded',
                        marker=dict(color='#7F7F7F', size=8),
                        opacity=0.7
                    ))
                    
                    # Add trend lines
                    fig_balance.add_trace(go.Scatter(
                        x=liverpool_matches['Match_Number'],
                        y=liverpool_matches['Liverpool_Goals'].rolling(window=5).mean(),
                        mode='lines',
                        name='Attack Trend',
                        line=dict(color='#C8102E', width=3)
                    ))
                    
                    fig_balance.add_trace(go.Scatter(
                        x=liverpool_matches['Match_Number'],
                        y=liverpool_matches['Opponent_Goals'].rolling(window=5).mean(),
                        mode='lines',
                        name='Defense Trend',
                        line=dict(color='#7F7F7F', width=3)
                    ))
                    
                    fig_balance.update_layout(
                        title='Goals Scored vs Conceded Throughout Season',
                        xaxis_title='Match Number',
                        yaxis_title='Goals',
                        height=500,
                        template='plotly_white'
                    )
                    
                    st.plotly_chart(fig_balance, use_container_width=True)
                
                with balance_col2:
                    # Balance metrics and venue comparison
                    st.markdown("##### 🎯 Balance Metrics")
                    
                    avg_goals_for = liverpool_matches['Liverpool_Goals'].mean()
                    avg_goals_against = liverpool_matches['Opponent_Goals'].mean()
                    balance_ratio = avg_goals_for / avg_goals_against if avg_goals_against > 0 else avg_goals_for
                    
                    st.metric("Average Goals For/Game", f"{avg_goals_for:.2f}")
                    st.metric("Average Goals Against/Game", f"{avg_goals_against:.2f}")
                    st.metric("Attack:Defense Ratio", f"{balance_ratio:.1f}:1")
                    
                    if balance_ratio > 3:
                        st.success("🔥 **Elite Balance Achieved**")
                    elif balance_ratio > 2:
                        st.success("💪 **Excellent Balance**")
                    else:
                        st.info("⚖️ **Good Balance**")
                    
                    # Home vs Away balance
                    st.markdown("##### 🏠 Venue Balance")
                    home_goals_for = home_matches['Liverpool_Goals'].mean()
                    home_goals_against = home_matches['Opponent_Goals'].mean()
                    away_goals_for = away_matches['Liverpool_Goals'].mean()
                    away_goals_against = away_matches['Opponent_Goals'].mean()
                    
                    venue_balance = pd.DataFrame({
                        'Venue': ['Home', 'Away'],
                        'Goals_For': [home_goals_for, away_goals_for],
                        'Goals_Against': [home_goals_against, away_goals_against]
                    })
                    
                    fig_venue_balance = px.bar(
                        venue_balance,
                        x='Venue',
                        y=['Goals_For', 'Goals_Against'],
                        title='Goals For/Against by Venue',
                        barmode='group',
                        color_discrete_map={'Goals_For': '#C8102E', 'Goals_Against': '#7F7F7F'}
                    )
                    fig_venue_balance.update_layout(height=400)
                    st.plotly_chart(fig_venue_balance, use_container_width=True)
            
            # Chart 4: Home Fortress Analysis  
            elif title_chart_selection == "Home Fortress Analysis":
                st.markdown("#### 🏠 Anfield Fortress: Home Dominance Analysis")
                
                fortress_col1, fortress_col2 = st.columns(2)
                
                with fortress_col1:
                    # Home record breakdown
                    home_wins = len(home_matches[home_matches['Result'] == 'Win'])
                    home_draws = len(home_matches[home_matches['Result'] == 'Draw'])
                    home_losses = len(home_matches[home_matches['Result'] == 'Loss'])
                    
                    home_record = pd.DataFrame({
                        'Result': ['Wins', 'Draws', 'Losses'],
                        'Count': [home_wins, home_draws, home_losses],
                        'Points': [home_wins*3, home_draws*1, home_losses*0]
                    })
                    
                    fig_home_record = px.pie(
                        home_record,
                        values='Count',
                        names='Result',
                        title=f'Home Record ({len(home_matches)} games)',
                        color_discrete_map={'Wins': '#00B04F', 'Draws': '#FFD700', 'Losses': '#DC143C'}
                    )
                    
                    fig_home_record.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_home_record, use_container_width=True)
                
                with fortress_col2:
                    # Home vs Away comparison
                    comparison_data = pd.DataFrame({
                        'Metric': ['Win Rate %', 'Points/Game', 'Goals/Game', 'Clean Sheets %'],
                        'Home': [
                            home_wins/len(home_matches)*100,
                            home_points/len(home_matches),
                            home_matches['Liverpool_Goals'].mean(),
                            len(home_matches[home_matches['Opponent_Goals'] == 0])/len(home_matches)*100
                        ],
                        'Away': [
                            away_wins/len(away_matches)*100,
                            away_points/len(away_matches),
                            away_matches['Liverpool_Goals'].mean(),
                            len(away_matches[away_matches['Opponent_Goals'] == 0])/len(away_matches)*100
                        ]
                    })
                    
                    comparison_data['Home_Advantage'] = comparison_data['Home'] - comparison_data['Away']
                    
                    fig_comparison = px.bar(
                        comparison_data,
                        x='Metric',
                        y='Home_Advantage',
                        title='Home Advantage Across Metrics',
                        color='Home_Advantage',
                        color_continuous_scale='RdYlGn'
                    )
                    fig_comparison.update_layout(coloraxis_showscale=False)
                    st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Home fortress statistics
                st.markdown("### 🏰 Fortress Statistics")
                home_stats_col1, home_stats_col2, home_stats_col3 = st.columns(3)
                
                with home_stats_col1:
                    st.metric("Home Points", f"{home_points}/{len(home_matches)*3}", f"{home_points/(len(home_matches)*3)*100:.1f}%")
                    st.metric("Home Wins", f"{home_wins}/{len(home_matches)}", f"{home_wins/len(home_matches)*100:.1f}%")
                
                with home_stats_col2:
                    home_goals_total = home_matches['Liverpool_Goals'].sum()
                    home_goals_against_total = home_matches['Opponent_Goals'].sum()
                    st.metric("Home Goals For", home_goals_total, f"{home_goals_total/len(home_matches):.2f}/game")
                    st.metric("Home Goals Against", home_goals_against_total, f"{home_goals_against_total/len(home_matches):.2f}/game")
                
                with home_stats_col3:
                    home_clean_sheets = len(home_matches[home_matches['Opponent_Goals'] == 0])
                    home_gd = home_goals_total - home_goals_against_total
                    st.metric("Home Clean Sheets", home_clean_sheets, f"{home_clean_sheets/len(home_matches)*100:.1f}%")
                    st.metric("Home Goal Difference", f"+{home_gd}", "Dominance")
            
            # Chart 5: Top Scorers & Assists
            elif title_chart_selection == "Top Scorers & Assists":
                st.markdown("#### ⚽ Top Scorers and Assist Providers")
                
                if using_real_data and not liverpool_shots.empty:
                    # Real data analysis
                    top_scorers = liverpool_shots[liverpool_shots["result"] == "Goal"].groupby("player")["result"].count().sort_values(ascending=False).head(10)
                    top_assists = liverpool_shots[liverpool_shots["player_assisted"].notna()].groupby("player_assisted").size().sort_values(ascending=False).head(10)
                    
                    scorers_col1, scorers_col2 = st.columns(2)
                    
                    with scorers_col1:
                        fig_scorers = px.bar(
                            x=top_scorers.values,
                            y=top_scorers.index,
                            orientation='h',
                            title="Top Liverpool Scorers 2019-20",
                            labels={'x': 'Goals', 'y': 'Player'},
                            color=top_scorers.values,
                            color_continuous_scale='Reds'
                        )
                        fig_scorers.update_layout(height=500, coloraxis_showscale=False)
                        st.plotly_chart(fig_scorers, use_container_width=True)
                    
                    with scorers_col2:
                        if not top_assists.empty:
                            fig_assists = px.bar(
                                x=top_assists.values,
                                y=top_assists.index,
                                orientation='h',
                                title="Top Liverpool Assist Providers",
                                labels={'x': 'Assists', 'y': 'Player'},
                                color=top_assists.values,
                                color_continuous_scale='Blues'
                            )
                            fig_assists.update_layout(height=500, coloraxis_showscale=False)
                            st.plotly_chart(fig_assists, use_container_width=True)
                        else:
                            st.info("Assist data not available in current dataset")
                else:
                    # Simulated data for key players
                    key_players_stats = pd.DataFrame({
                        'Player': ['Mohamed Salah', 'Sadio Mané', 'Roberto Firmino', 'Jordan Henderson', 'Georginio Wijnaldum'],
                        'Goals': [19, 18, 9, 4, 3],
                        'Assists': [10, 7, 8, 5, 1],
                        'Key_Contribution': ['Top Scorer', 'Consistent Threat', 'False 9 Genius', 'Captain Leader', 'Midfield Engine']
                    })
                    
                    players_col1, players_col2 = st.columns(2)
                    
                    with players_col1:
                        fig_player_goals = px.bar(
                            key_players_stats,
                            x='Goals',
                            y='Player',
                            orientation='h',
                            title='Top Scorers 2019-20',
                            color='Goals',
                            color_continuous_scale='Reds',
                            text='Goals'
                        )
                        fig_player_goals.update_traces(textposition='outside')
                        fig_player_goals.update_layout(height=400, coloraxis_showscale=False)
                        st.plotly_chart(fig_player_goals, use_container_width=True)
                    
                    with players_col2:
                        fig_player_assists = px.bar(
                            key_players_stats,
                            x='Assists',
                            y='Player',
                            orientation='h',
                            title='Top Assist Providers 2019-20',
                            color='Assists',
                            color_continuous_scale='Blues',
                            text='Assists'
                        )
                        fig_player_assists.update_traces(textposition='outside')
                        fig_player_assists.update_layout(height=400, coloraxis_showscale=False)
                        st.plotly_chart(fig_player_assists, use_container_width=True)
                
                # Player contribution analysis
                st.markdown("### 🌟 Key Player Contributions to Title")
                
                contrib_col1, contrib_col2, contrib_col3 = st.columns(3)
                
                with contrib_col1:
                    st.success("👑 **Mohamed Salah**")
                    st.write("• 19 Premier League goals")
                    st.write("• 10 assists")
                    st.write("• Consistent threat from right wing")
                    st.write("• Clutch goals in big moments")
                    st.success("**Impact: 29 goal contributions**")
                
                with contrib_col2:
                    st.info("🔥 **Sadio Mané**")
                    st.write("• 18 Premier League goals")
                    st.write("• 7 assists")
                    st.write("• Electric pace and finishing")
                    st.write("• Big game player")
                    st.success("**Impact: 25 goal contributions**")
                
                with contrib_col3:
                    st.warning("🎭 **Roberto Firmino**")
                    st.write("• 9 Premier League goals")
                    st.write("• 8 assists")
                    st.write("• False 9 creativity")
                    st.write("• Enables Salah & Mané")
                    st.success("**Impact: Link-up play genius**")
            
            # Chart 6: Shot Analysis & Efficiency
            elif title_chart_selection == "Shot Analysis & Efficiency":
                st.markdown("#### 🎯 Shot Analysis and Conversion Efficiency")
                
                if using_real_data and not liverpool_shots.empty:
                    shot_col1, shot_col2 = st.columns(2)
                    
                    with shot_col1:
                        # Shot map
                        fig_shots = px.scatter(
                            liverpool_shots,
                            x='X',
                            y='Y',
                            color='isGoal',
                            color_discrete_map={True: '#00B04F', False: '#DC143C'},
                            title='Liverpool Shot Map 2019-20',
                            labels={'X': 'Field Position X', 'Y': 'Field Position Y'},
                            hover_data=['player', 'xG', 'shotType']
                        )
                        fig_shots.update_layout(height=500)
                        fig_shots.update_yaxes(scaleanchor="x", scaleratio=1)
                        st.plotly_chart(fig_shots, use_container_width=True)
                    
                    with shot_col2:
                        # Shot efficiency by player
                        shot_efficiency = liverpool_shots.groupby('player').agg({
                            'result': 'count',
                            'isGoal': 'sum',
                            'xG': 'sum'
                        }).reset_index()
                        shot_efficiency.columns = ['Player', 'Total_Shots', 'Goals', 'Total_xG']
                        shot_efficiency['Conversion_Rate'] = (shot_efficiency['Goals'] / shot_efficiency['Total_Shots'] * 100).round(1)
                        shot_efficiency = shot_efficiency[shot_efficiency['Total_Shots'] >= 10].sort_values('Goals', ascending=False)
                        
                        fig_efficiency = px.scatter(
                            shot_efficiency,
                            x='Total_Shots',
                            y='Goals',
                            size='Total_xG',
                            color='Conversion_Rate',
                            hover_data=['Player'],
                            title='Shot Efficiency: Goals vs Shots',
                            color_continuous_scale='Viridis'
                        )
                        fig_efficiency.update_layout(height=500)
                        st.plotly_chart(fig_efficiency, use_container_width=True)
                    
                    # Shot type analysis
                    st.markdown("### 📊 Shot Type Analysis")
                    
                    shot_types = liverpool_shots.groupby(['Venue', 'shotType']).size().reset_index(name='Count')
                    shot_situations = liverpool_shots.groupby(['Venue', 'situation']).size().reset_index(name='Count')
                    
                    type_col1, type_col2 = st.columns(2)
                    
                    with type_col1:
                        fig_shot_types = px.bar(
                            shot_types,
                            x='shotType',
                            y='Count',
                            color='Venue',
                            title='Shot Types: Home vs Away',
                            barmode='group',
                            color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'}
                        )
                        st.plotly_chart(fig_shot_types, use_container_width=True)
                    
                    with type_col2:
                        fig_situations = px.bar(
                            shot_situations,
                            x='situation',
                            y='Count',
                            color='Venue',
                            title='Shot Situations: Home vs Away',
                            barmode='group',
                            color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'}
                        )
                        st.plotly_chart(fig_situations, use_container_width=True)
                else:
                    st.info("📊 **Shot Analysis**: This would show detailed shot maps, conversion rates, and shooting efficiency analysis using the shot data from your Python code.")
                    st.write("Shot analysis would include:")
                    st.write("• Shot maps showing goal locations")
                    st.write("• Conversion rates by player")
                    st.write("• Shot types analysis")
                    st.write("• Home vs away shooting patterns")
            
            # Chart 7: Key Players Performance
            elif title_chart_selection == "Key Players Performance":
                st.markdown("#### 🌟 Key Players Performance Analysis")
                
                # Comprehensive player analysis
                if using_real_data and not liverpool_shots.empty:
                    key_players = ['Mohamed Salah', 'Roberto Firmino']
                    if all(player in liverpool_shots['player'].values for player in key_players):
                        
                        # Performance comparison
                        player_stats = liverpool_shots[liverpool_shots['player'].isin(key_players)].groupby(['player', 'Venue']).agg({
                            'result': 'count',
                            'isGoal': 'sum',
                            'xG': 'sum'
                        }).reset_index()
                        player_stats.columns = ['Player', 'Venue', 'Total_Shots', 'Goals', 'Total_xG']
                        
                        player_col1, player_col2 = st.columns(2)
                        
                        with player_col1:
                            # Goals by venue
                            fig_player_goals = px.bar(
                                player_stats,
                                x='Player',
                                y='Goals',
                                color='Venue',
                                title='Key Players: Goals by Venue',
                                barmode='group',
                                color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'}
                            )
                            st.plotly_chart(fig_player_goals, use_container_width=True)
                        
                        with player_col2:
                            # xG comparison
                            fig_player_xg = px.bar(
                                player_stats,
                                x='Player',
                                y='Total_xG',
                                color='Venue',
                                title='Expected Goals (xG) by Venue',
                                barmode='group',
                                color_discrete_map={'Home': '#FF6B35', 'Away': '#004E89'}
                            )
                            st.plotly_chart(fig_player_xg, use_container_width=True)
                        
                        # Heat maps for key players
                        st.markdown("### 🔥 Player Heat Maps")
                        
                        for player in key_players:
                            player_shots = liverpool_shots[liverpool_shots['player'] == player]
                            if not player_shots.empty:
                                st.markdown(f"#### {player} Shot Density")
                                
                                fig_heatmap = px.density_heatmap(
                                    player_shots,
                                    x='X',
                                    y='Y',
                                    facet_col='Venue',
                                    title=f'{player} - Shot Density Map',
                                    color_continuous_scale='Reds'
                                )
                                fig_heatmap.update_layout(height=400)
                                st.plotly_chart(fig_heatmap, use_container_width=True)
                
                # Player impact on title
                st.markdown("### 🏆 How Key Players Won The Title")
                
                impact_col1, impact_col2 = st.columns(2)
                
                with impact_col1:
                    st.success("👑 **Mohamed Salah's Title Impact**")
                    st.write("• Consistent goal scoring throughout season")
                    st.write("• Penalty specialist - crucial spot kicks")
                    st.write("• Big game performer")
                    st.write("• Right wing dominance")
                    st.success("**Result: 19 goals provided title firepower**")
                
                with impact_col2:
                    st.info("🎭 **Roberto Firmino's Title Impact**")
                    st.write("• False 9 role created space for wingers")
                    st.write("• Crucial assists and link-up play")
                    st.write("• Work rate and pressing from front")
                    st.write("• Tactical intelligence")
                    st.success("**Result: Enabled front three to flourish**")
            
            # Chart 8: Season Timeline
            elif title_chart_selection == "Season Timeline":
                st.markdown("#### 📅 Complete Season Timeline")
                
                timeline_col1, timeline_col2 = st.columns(2)
                
                with timeline_col1:
                    # Match results over time - Fixed color mapping
                    result_colors = {'Win': '#00B04F', 'Draw': '#FFD700', 'Loss': '#DC143C'}
                    
                    # Debug: Show what results we have
                    st.write(f"**Results breakdown:** {liverpool_matches['Result'].value_counts().to_dict()}")
                    
                    fig_timeline = px.scatter(
                        liverpool_matches,
                        x='Match_Number',
                        y='Liverpool_Goals',
                        color='Result',
                        size='Points',
                        title='Season Timeline: Goals and Results',
                        color_discrete_map=result_colors,
                        hover_data=['Opponent_Goals', 'Venue'],
                        category_orders={"Result": ["Win", "Draw", "Loss"]}  # Ensure all categories show
                    )
                    
                    # Force show all categories in legend
                    fig_timeline.update_layout(
                        height=500,
                        showlegend=True
                    )
                    
                    # Add manual legend entries if needed
                    for result_type, color in result_colors.items():
                        result_data = liverpool_matches[liverpool_matches['Result'] == result_type]
                        if not result_data.empty:
                            fig_timeline.add_trace(
                                go.Scatter(
                                    x=result_data['Match_Number'],
                                    y=result_data['Liverpool_Goals'],
                                    mode='markers',
                                    name=result_type,
                                    marker=dict(
                                        color=color,
                                        size=[p*3 + 3 for p in result_data['Points']]  # Size based on points
                                    ),
                                    showlegend=True,
                                    hovertemplate=f'<b>{result_type}</b><br>Match: %{{x}}<br>Goals: %{{y}}<br>Venue: %{{customdata[1]}}<br>Score: %{{y}}-%{{customdata[0]}}<extra></extra>',
                                    customdata=result_data[['Opponent_Goals', 'Venue']]
                                )
                            )
                    
                    st.plotly_chart(fig_timeline, use_container_width=True)
                
                with timeline_col2:
                    # Venue performance timeline
                    venue_timeline = liverpool_matches.groupby(['Match_Number', 'Venue'])['Points'].sum().reset_index()
                    
                    fig_venue_timeline = px.scatter(
                        liverpool_matches,
                        x='Match_Number',
                        y='Points',
                        color='Venue',
                        size='Liverpool_Goals',
                        title='Points by Venue Throughout Season',
                        color_discrete_map={'Home': '#C8102E', 'Away': '#00A398'}
                    )
                    fig_venue_timeline.update_layout(height=500)
                    st.plotly_chart(fig_venue_timeline, use_container_width=True)
                
                # Key moments in season
                st.markdown("### 🎯 Key Moments in Championship Season")
                
                # Identify key matches
                big_wins = liverpool_matches[liverpool_matches['Liverpool_Goals'] >= 4]
                crucial_wins = liverpool_matches[(liverpool_matches['Result'] == 'Win') & (liverpool_matches['Opponent_Goals'] >= 2)]
                
                moments_col1, moments_col2 = st.columns(2)
                
                with moments_col1:
                    st.success("💥 **Big Statement Wins**")
                    for _, match in big_wins.iterrows():
                        st.write(f"• Match {match['Match_Number']}: {match['Liverpool_Goals']}-{match['Opponent_Goals']} ({match['Venue']})")
                    
                    if big_wins.empty:
                        st.write("• Multiple dominant performances")
                        st.write("• Consistent attacking displays")
                        st.write("• Goals when needed")
                
                with moments_col2:
                    st.warning("🔥 **Crucial Character Wins**")
                    for _, match in crucial_wins.iterrows():
                        st.write(f"• Match {match['Match_Number']}: {match['Liverpool_Goals']}-{match['Opponent_Goals']} ({match['Venue']})")
                    
                    if crucial_wins.empty:
                        st.write("• Solid defensive performances")
                        st.write("• Rarely conceded multiple goals")
                        st.write("• Clinical when chances came")
            
            # Final championship summary
            st.markdown("### 🏆 Championship Success Summary")
            
            # Calculate final statistics
            win_rate = total_wins / len(liverpool_matches) * 100
            home_win_rate = home_wins / len(home_matches) * 100
            away_win_rate = away_wins / len(away_matches) * 100
            
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            
            with summary_col1:
                st.metric("Final Position", "1st", "CHAMPIONS!")
                st.metric("Total Points", total_points, f"Out of {len(liverpool_matches)*3}")
            
            with summary_col2:
                st.metric("Win Rate", f"{win_rate:.1f}%", f"{total_wins} wins")
                st.metric("Goal Difference", f"+{goal_difference}", f"{goals_scored}-{goals_conceded}")
            
            with summary_col3:
                st.metric("Home Record", f"{home_win_rate:.1f}%", f"{home_wins} wins")
                st.metric("Away Record", f"{away_win_rate:.1f}%", f"{away_wins} wins")
            
            with summary_col4:
                clean_sheets = len(liverpool_matches[liverpool_matches['Opponent_Goals'] == 0])
                st.metric("Clean Sheets", clean_sheets, f"{clean_sheets/len(liverpool_matches)*100:.1f}%")
                st.metric("Big Wins (3+ goals)", len(liverpool_matches[liverpool_matches['Liverpool_Goals'] >= 3]), "Dominance")
            
            # How statistics delivered the title
            st.success(f"""
            ### 🏆 How Liverpool's Statistics Won The Premier League Title
            
            **The Perfect Championship Formula:**
            
            📊 **Dominant Statistics:**
            - **{total_points} Points**: Exceptional total showing sustained excellence
            - **{win_rate:.1f}% Win Rate**: Incredible consistency across 38 games  
            - **+{goal_difference} Goal Difference**: Perfect balance of attack and defense
            - **{home_points}/{len(home_matches)*3} Home Points**: Anfield became fortress with {home_win_rate:.1f}% win rate
            
            🎯 **Key Success Factors:**
            1. **Home Dominance**: {home_wins} wins from {len(home_matches)} home games provided unshakeable foundation
            2. **Defensive Excellence**: Only {goals_conceded} goals conceded with {clean_sheets} clean sheets
            3. **Clinical Attack**: {goals_scored} goals scored at {goals_scored/len(liverpool_matches):.1f} per game average
            4. **Mental Strength**: {total_losses} losses all season - incredible resilience
            
            🏠 **The Anfield Effect**: 
            Home advantage was crucial - {home_points} points from {len(home_matches)} games vs {away_points} from {len(away_matches)} away games
            
            ⚽ **Perfect Balance**: 
            Attack ({goals_scored/len(liverpool_matches):.2f} goals/game) + Defense ({goals_conceded/len(liverpool_matches):.2f} conceded/game) = Championship
            
            **Final Verdict**: Liverpool didn't just win the title - they dominated through statistical excellence in every department. The combination of Anfield fortress, defensive solidity, clinical finishing, and mental strength created the perfect championship machine.
            
            🔴 **30-year wait finally over - You'll Never Walk Alone!** 🔴
            """)
            
        except Exception as e:
            st.error(f"❌ Error in championship analysis: {str(e)}")
            st.info("""
            📋 **Note**: This analysis works with:
            1. Actual data files: 'match_infos_EPL_1920.csv' and 'shots_EPL_1920.csv' 
            2. Or simulated data based on Liverpool's 2019-20 performance
            
            Place the CSV files in the same directory for complete analysis with real match and shot data.
            """)
    
    # Footer
    st.markdown("""
    <div class="ynwa-footer">
        <h3>🔴 You'll Never Walk Alone 🔴</h3>
        <p>Liverpool FC Analytics Dashboard | Interactive Performance Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# Run the dashboard
if __name__ == "__main__":
    main()