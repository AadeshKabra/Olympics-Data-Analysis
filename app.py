import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
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


if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title("Statistics")

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

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header("Events")
        st.title(events)
    with col5:
        st.header("Athletes")
        st.title(athletes)
    with col6:
        st.header("Nations")
        st.title(nations)

    st.title("Participating Nations over Time")
    nations_over_time = helper.data_time(df, 'region')
    fig = px.line(nations_over_time, x='Year', y='Nations')
    st.plotly_chart(fig)

    st.title("No. of Events over Time")
    events_over_time = helper.data_time(df, 'Event')
    fig = px.line(events_over_time, x='Year', y='No. of Events')
    st.plotly_chart(fig)

    st.title("No. of Athelets over Time")
    events_over_time = helper.data_time(df, 'athelets')
    fig = px.line(events_over_time, x='Year', y='No. of Athelets')
    st.plotly_chart(fig)


    st.title("Events Heatmap")
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    fig, pt = plt.subplots(figsize=(20, 18))
    pt = sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype('int'), annot=True)
    # plt.figure(figsize=(20, 15))

    st.pyplot(fig)

    st.title("Most Successful Athelets")
    sports = df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sports)
    succ = helper.most_successful(df, selected_sport)
    st.table(succ)


if user_menu == "Country-wise Analysis":
    st.sidebar.title("Country wise Analysis")
    countries = df['region'].unique().tolist()
    selected_country = st.sidebar.selectbox("Select Country", countries)
    st.title("Medal Tally over years - " + selected_country)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.plotly_chart(fig)


    st.title("Event analysis over the years - " + selected_country)
    data2 = helper.country_event_heatmap(df, selected_country)
    fig, pt = plt.subplots(figsize=(20, 18))
    pt = sns.heatmap(data2.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.title("Most successful Atheletes of " + selected_country)
    st.table(helper.most_successful_atheletes(df, selected_country))


if user_menu=="Athlete wise Analysis":
    st.title("Athlete Age Analysis")
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Age Distribution', 'Gold', 'Silver', 'Bronze'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=850, height=500)
    st.plotly_chart(fig)


    st.title("Age-Distribution for various sports (Gold)")
    x1 = ['Gold', 'Silver', 'Bronze']
    selected_medal = st.selectbox("Select Medal", x1)
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving',                           'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis',                            'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens',                                'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athelete_df[athelete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']==selected_medal]['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=500)
    st.plotly_chart(fig)

    st.title('Height Vs Weight Distribution for sports')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    # sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.wvh_distribution(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)


    st.title("Men vs Women Participation")
    final_df = helper.men_women(df)
    fig = px.line(final_df, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=800, height=500)
    st.plotly_chart(fig)