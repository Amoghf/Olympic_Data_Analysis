import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go



df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("🏅 Olympics Analysis")
st.sidebar.image('https://animationvisarts.com/wp-content/uploads/2016/11/Olympics-Logo.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")
    else:
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("📊 Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x="Year", y="NO. Of Countries")
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    events_over_time = helper.events_conducting_each_year(df)
    fig1 = px.line(events_over_time, x="Year", y="Events Conducted", title="Number of Events Held Over Time")
    st.title("Events Held Each Olympic Edition")
    st.plotly_chart(fig1)

    athletes_over_time = helper.athletes_participating_each_year(df)
    fig2 = px.line(athletes_over_time, x="Year", y="Participants", title="Number of Athletes Participating Each Year")
    st.title("Athletes Participating Each Year")
    st.plotly_chart(fig2)

    st.title("Number of Events Over Time")
    fig4, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig4)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    if country_df is None or country_df.empty:
        st.write(f"No medal data available for {selected_country}.")
    else:
        fig = px.line(country_df, x="Year", y="Medal", title=selected_country + " Medal Tally Over the Years")
        st.title(selected_country + " Medal Tally Over the Years")
        st.plotly_chart(fig)

    st.title(selected_country + " Performance in Different Sports")
    pt = helper.country_event_heatmap(df, selected_country)
    if pt is None or pt.empty:
        st.write(f"No performance data available for {selected_country}.")
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    if top10_df is None or top10_df.empty:
        st.write(f"No top athletes data available for {selected_country}.")
    else:
        st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x1, name='Overall Age Distribution', opacity=0.75, histnorm='density'))
    fig.add_trace(go.Histogram(x=x2, name='Gold Medalists', opacity=0.75, histnorm='density'))
    fig.add_trace(go.Histogram(x=x3, name='Silver Medalists', opacity=0.75, histnorm='density'))
    fig.add_trace(go.Histogram(x=x4, name='Bronze Medalists', opacity=0.75, histnorm='density'))

    fig.update_layout(
        title='Age Distribution',
        barmode='overlay',
        xaxis_title='Age',
        yaxis_title='Density'
    )

    st.title("Distribution of Age")
    st.plotly_chart(fig)

    st.title("Height vs Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    if not temp_df.empty:
        fig, ax = plt.subplots()
        sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', data=temp_df, s=60)
        st.pyplot(fig)
    else:
        st.warning(f"No data available for {selected_sport}.")

    st.title("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    if not final.empty:
        fig = px.line(final, x="Year", y=["Male", "Female"], title="Men vs Women Participation Over the Years")
        st.plotly_chart(fig)
    else:
        st.warning("No participation data available.")
