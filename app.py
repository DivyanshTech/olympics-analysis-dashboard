import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

# Load datasets
df = pd.read_csv('assets/athlete_events.csv')
region_df = pd.read_csv('assets/noc_regions.csv')

# Preprocess the dataset using the custom preprocessor module
df = preprocessor.preprocess(df, region_df)

# Sidebar UI
st.sidebar.title("Olympics Analysis")
st.sidebar.image(r"D:\ML project\Olympic data analysis\ASSETS\Screenshot 2025-07-25 171239.png")

# Sidebar menu
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

# ----------------------- Medal Tally ----------------------- #
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Dynamic title based on user selection
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} overall performance")
    else:
        st.title(f"{selected_country} performance in {selected_year} Olympics")

    st.dataframe(medal_tally)

# ----------------------- Overall Analysis ----------------------- #
elif user_menu == 'Overall Analysis':
    st.title("Top Statistics")

    # Key stats
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    # Display in columns
    c1, c2, c3 = st.columns(3)
    with c1:
        st.header("Editions")
        st.title(editions)
    with c2:
        st.header("Hosts")
        st.title(cities)
    with c3:
        st.header("Sports")
        st.title(sports)

    c4, c5, c6 = st.columns(3)
    with c4:
        st.header("Events")
        st.title(events)
    with c5:
        st.header("Nations")
        st.title(nations)
    with c6:
        st.header("Athletes")
        st.title(athletes)

    # Time series visualizations
    nations_over_time = helper.data_over_time(df, 'region')
    fig1 = px.line(nations_over_time, x="Edition", y="region", title="Number of Participating Countries Over Time", labels={"region": "No. of Countries"})
    st.plotly_chart(fig1)

    events_over_time = helper.participating_nations_over_time(df, 'Event')
    fig2 = px.line(events_over_time, x="Edition", y="Event", title="Events Over Time")
    st.plotly_chart(fig2)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    # Heatmap of number of events per sport over the years
    st.title("No. of Events over the time (Event Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    sns.heatmap(pivot, annot=True, cmap="Greens", ax=ax)
    ax.set_title("Number of Events per Sport over the Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sport")
    plt.tight_layout()
    st.pyplot(fig)

    # Most successful athletes by sport
    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

# ----------------------- Country-wise Analysis ----------------------- #
elif user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    # Line chart of medal tally over years
    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    # Heatmap of best sports
    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    # Top 10 athletes from the country
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# ----------------------- Athlete-wise Analysis ----------------------- #
elif user_menu == 'Athlete wise Analysis':
    st.title("Distribution of Age")

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    # Age distribution plot
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    # Age distribution across sports (gold medalists)
    st.title("Distribution of Age wrt Sports (Gold Medalists)")
    x, name = [], []
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
        'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
        'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
        'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig2 = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig2.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig2)

    # Scatter plot for height vs weight
    st.title("Height vs Weight of Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()
    sns.scatterplot(
        x=temp_df['Weight'],
        y=temp_df['Height'],
        hue=temp_df['Medal'],
        style=temp_df['Sex'],
        s=60,
        ax=ax
    )
    st.pyplot(fig)

    # Male vs Female participation over the years
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        title="Male vs Female Athletes Over the Years",
        xaxis_title="Year",
        yaxis_title="Number of Participants"
    )
    st.plotly_chart(fig)
