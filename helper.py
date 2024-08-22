import numpy as np
import pandas as pd

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    else:
        return pd.DataFrame()  # Return empty DataFrame if no condition matches

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

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

    return years, country


def participating_nations_over_time(df):
    df_no_duplicates = df.drop_duplicates(['Year', 'region'])
    nations_over_time = df_no_duplicates.groupby('Year').count()['region'].reset_index()
    nations_over_time.rename(columns={'region': 'NO. Of Countries'}, inplace=True)
    return nations_over_time


def events_conducting_each_year(df):
    df_no_duplicates = df.drop_duplicates(['Year', 'Event'])
    events_over_time = df_no_duplicates.groupby('Year').count()['Event'].reset_index()
    events_over_time.rename(columns={'Event': 'Events Conducted'}, inplace=True)
    return events_over_time


def athletes_participating_each_year(df):
    df_no_duplicates = df.drop_duplicates(['Year', 'Name'])
    athletes_over_time = df_no_duplicates.groupby('Year').count()['Name'].reset_index()
    athletes_over_time.rename(columns={'Name': 'Participants'}, inplace=True)
    return athletes_over_time


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    if temp_df.empty:
        return pd.DataFrame(columns=['Year', 'Medal'])  # Return empty DataFrame with expected columns
    final_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    if temp_df.empty:
        return pd.DataFrame()  # Return empty DataFrame
    pt = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    
    # Count the number of medals won by each athlete
    medal_count = temp_df['Name'].value_counts().reset_index().head(10)
    
    if medal_count.empty:
        return pd.DataFrame(columns=['Name', 'Medals'])  # Return empty DataFrame with expected columns
    
    # Rename columns to avoid 'index' key error
    medal_count.columns = ['Name', 'Medals']
    
    # Merge with the original DataFrame to get the sport
    merged_df = medal_count.merge(temp_df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
    
    return merged_df


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
