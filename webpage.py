import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
# st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
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


    nations_over_time=helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x="Year", y="NO. Of Countires")
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    nations_over_time=helper.events_conducting_each_year(df)
    fig1 = px.line(nations_over_time, x="Year", y="Events Conducted", title="Number of Events Held Over Time")


    st.title("Evnets Held each Olympic Edition")
    st.plotly_chart(fig1)


    nations_over_time = helper.Athletes_participating_each_year(df)

    fig2 = px.line(nations_over_time, x="Year", y="count", title="Number of Athletes Participating Each Year")


    st.title("Athletes Participating Each Year")
    st.plotly_chart(fig2)

    

    st.title("Number of Events over Time")

    fig4, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Edition', 'Sport', 'Event'])  # Adjust column names here
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Edition', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)  # Adjust column names here
    st.pyplot(fig4)


    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')



    # st.title("Most successful Athletes")
    # sport_list = df['Sport'].unique().tolist()
    # sport_list.sort()
    # sport_list.insert(0,'Overall')

    # selected_sport = st.selectbox('Select a Sport',sport_list)
    # x = helper.most_successful(df,selected_sport)
    # st.table(x)


