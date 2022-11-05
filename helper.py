# import numpy as np
#
# def medal_tally(data):
#     medals = data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'])
#     medals = medals.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(ascending=False, by='Gold')
#     medals['Total'] = medals['Gold'] + medals['Silver'] + medals['Bronze']
#     medals['Gold'] = medals['Gold'].astype(int)
#     medals['Silver'] = medals['Silver'].astype(int)
#     medals['Bronze'] = medals['Bronze'].astype(int)
#     medals['Total'] = medals['Total'].astype(int)
#
#     return medals
#
#
# def country_year_list(df):
#     # print(df[df['region']])
#     years = df['Year'].unique().tolist()
#     years.sort()
#     years.insert(0, 'Overall')
#     country = np.unique(df['region'].dropna().values).tolist()
#     # country = df['region'].dropna().unique().tolist()
#     country.sort()
#     country.insert(0, 'Overall')
#     return years, country
#
#
# def fetch_medal_tally(data, year, country):
#     medals = data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'])
#     flag = 0
#     if year == 'Overall' and country == 'Overall':
#         temp_df = medals
#     if year == 'Overall' and country != 'Overall':
#         temp_df = medals[medals['region'] == country]
#         flag = 1
#     if year != 'Overall' and country == 'Overall':
#         temp_df = medals[medals['Year'] == int(year)]
#     if year != 'Overall' and country != 'Overall':
#         temp_df = medals[(medals['Year'] == int(year)) & (medals['region'] == country)]
#
#     if flag == 1:
#         temp_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
#     else:
#         temp_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
#
#
#     temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
#     temp_df['Gold'] = temp_df['Gold'].astype(int)
#     temp_df['Silver'] = temp_df['Silver'].astype(int)
#     temp_df['Bronze'] = temp_df['Bronze'].astype(int)
#     temp_df['Total'] = temp_df['Total'].astype(int)
#     return temp_df



import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def data_time(df, column):

    if column=='region':
        nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('index')
        nations_over_time.rename(columns={'index': 'Year', 'Year': 'Nations'}, inplace=True)
        return nations_over_time

    if column=='Event':
        events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('index')
        events_over_time.rename(columns={'index': 'Year', 'Year': 'No. of Events'}, inplace=True)
        return events_over_time

    if column=='athelets':
        athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('index')
        athletes_over_time.rename(columns={'index': 'Year', 'Year': 'No. of Athelets'}, inplace=True)
        return athletes_over_time


def most_successful(df, sport):
    df1 = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        df1 = df1[df1['Sport']==sport]
    x = df1['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates(['index'])
    x.rename(columns={'index':'Name', 'Name_x':'Medals', 'region':'Country'}, inplace=True)
    return x


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    return new_df


def most_successful_atheletes(df, country):
    df1 = df.dropna(subset=['Medal'])
    df1 = df1[df1['region']==country]
    x = df1['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates(['index'])
    x.rename(columns={'index':'Name', 'Name_x':'Medals', 'region':'Country'}, inplace=True)
    return x


def wvh_distribution(df, sport):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    athelete_df['Medal'].fillna('No Medal', inplace=True)
    temp_df = athelete_df[athelete_df['Sport'] == sport]
    return temp_df


def men_women(df):
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    athelete_df['Medal'].fillna('No Medal', inplace=True)
    men = athelete_df[athelete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athelete_df[athelete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final_df = men.merge(women, on='Year', how='left')
    final_df.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final_df.fillna(0, inplace=True)
    return final_df