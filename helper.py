import pandas as pd

# Returns list of years and countries with 'Overall' added for dropdowns
def country_year_list(df):
    years = df['Year'].dropna().unique().tolist()
    years = sorted(list(map(int, years)))
    years.insert(0, 'Overall')

    countries = df['region'].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries

# Fetches medal tally filtered by year and/or country
def fetch_medal_tally(df, year, country):
    temp_df = df.copy()

    if year != 'Overall':
        temp_df = temp_df[temp_df['Year'] == int(year)]
    if country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    if country == 'Overall':
        medal_tally = (
            temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .sort_values('Gold', ascending=False)
            .reset_index()
        )
    else:
        medal_tally = (
            temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .sort_values('Year')
            .reset_index()
        )

    medal_tally['Total'] = (
        medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    )

    return medal_tally

# Generic function to calculate value counts of a column over years
def data_over_time(df, col):
    temp_df = df.drop_duplicates(subset=['Year', col])
    data = temp_df['Year'].value_counts().reset_index()
    data.columns = ['Edition', col]
    data = data.sort_values('Edition')
    return data

# Specifically for plotting participation over time
def participating_nations_over_time(df, col):
    temp_df = df.drop_duplicates(subset=['Year', col])
    data = temp_df['Year'].value_counts().reset_index()
    data.columns = ['Edition', col]
    data = data.sort_values('Edition')
    return data

# Top 15 most successful athletes (overall or for a specific sport)
def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport.lower() != 'overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15)
    x.columns = ['Name', 'Medals']

    x = (
        x.merge(df[['Name', 'Sport', 'region']], on='Name', how='left')
        .drop_duplicates('Name')
    )

    return x[['Name', 'Medals', 'Sport', 'region']]

# Year-wise medal tally for a given country
def year_wise_medal_tally(df, country):
    mp_df = df.dropna(subset=['Medal'])
    mp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
        inplace=True
    )

    new_df = mp_df[mp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

# Returns heatmap-style pivot table: Sports vs Year (medal counts)
def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
        inplace=True
    )

    new_df = temp_df[temp_df['region'] == country]

    pt = (
        new_df.pivot_table(
            index='Sport',
            columns='Year',
            values='Medal',
            aggfunc='count'
        )
        .fillna(0)
    )

    return pt

# Top 10 athletes of a country by medals won
def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10)
    x.columns = ['Name', 'Medals']

    x = x.merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']]
    return x.drop_duplicates('Name')

# Returns filtered athlete dataframe for height-vs-weight plot
def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

# Returns yearly count of male and female athletes
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final
