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



# All FUntion of overall analysis start are below


def participating_nations_over_time(df):
    # Drop duplicates based on 'Year' and 'region'
    df_no_duplicates = df.drop_duplicates(['Year','region'])
    
    # Count occurrences of each unique 'Year' and sort by 'Year' including NaNs
    nations_over_time = df_no_duplicates['Year'].value_counts().reset_index().sort_values(by='Year', na_position='first')
    
    # Rename the 'Year' column to 'Edition'
    df.rename(columns={'Year':'Edition'}, inplace=True)
    
    # Count occurrences of each unique 'Edition' and sort by 'Edition' including NaNs
    nations_over_time = df.drop_duplicates(['Edition','region'])['Edition'].value_counts().reset_index().sort_values(by='Edition', na_position='first')
    
    # Rename columns
    nations_over_time.rename(columns={'Edition': 'Year', 'count': 'NO. Of Countires'}, inplace=True)

    return nations_over_time



def events_conducting_each_year(df):
    # Drop duplicates based on 'Edition' and 'Event'
    df_no_duplicates = df.drop_duplicates(['Edition', 'Event'])

    # Count occurrences of each unique 'Edition' and sort by 'Edition' including NaNs
    nations_over_time = df_no_duplicates['Edition'].value_counts().reset_index().sort_values(by='Edition', na_position='first')

    # Create nations_over_time DataFrame with counts of events held per edition
    nations_over_time = df.drop_duplicates(['Edition', 'Event'])['Edition'].value_counts().reset_index().sort_values(by='Edition', na_position='first')
    nations_over_time.rename(columns={'Edition': 'Year', 'count': 'Events Conducted'}, inplace=True)

    return nations_over_time


def Athletes_participating_each_year(df):
    # Drop duplicates based on 'Edition' and 'Name'
    df_no_duplicates = df.drop_duplicates(['Edition', 'Name'])

    # Count occurrences of each unique 'Edition' and sort by 'Edition'
    nations_over_time = df_no_duplicates['Edition'].value_counts().reset_index().sort_values(by='Edition', na_position='first')

    # Create nations_over_time DataFrame with counts of athletes per edition
    nations_over_time = df.drop_duplicates(['Edition', 'Name'])['Edition'].value_counts().reset_index().sort_values(by='Edition', na_position='first')
    nations_over_time.rename(columns={'Edition': 'Year', 'Name': 'Participants'}, inplace=True)

    return nations_over_time


# def most_successful_countrywise(df, country):
#     temp_df = df.dropna(subset=['Medal'])

#     temp_df = temp_df[temp_df['region'] == country]

#     x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[
#         ['index', 'Name_x', 'Sport']].drop_duplicates('index')
#     x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
#     return x





