import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the Processed Dataset
@st.cache_data
def load_movies_data():
    return pd.read_csv('IMDb Top 250 Movies (Director & Actors).csv')

movies_df = load_movies_data()

# Calculate the Decade for Each Movie
movies_df['Decade'] = (movies_df['Release Year'] // 10) * 10

# Extract Unique Decades for the Slider
decade_options = sorted(movies_df['Decade'].dropna().unique())

# User Input for Decade Range
st.sidebar.subheader('Filter by Decade (Distribution of Top 250 IMDb Movies)')
decade_range = st.sidebar.select_slider(
    'Select the Decade Range:',
    options=decade_options,
    value=(min(decade_options), max(decade_options)),  # Default to full range
)

# Filter the Dataset Based on the Selected Decade Range
filtered_df = movies_df[(movies_df['Decade'] >= decade_range[0]) & (movies_df['Decade'] <= decade_range[1])]

# Function to Create Bar Chart for Distribution of Movies by Decade
def create_movies_distribution_bar_chart(data, start_decade, end_decade):
    movie_counts = data['Decade'].value_counts().sort_index()

    fig = px.bar(
        x=movie_counts.index.astype(str),
        y=movie_counts.values,
        labels={'x': 'Decade', 'y': 'Number of Movies'},
    )

    fig.update_traces(marker_color='skyblue')
    fig.update_layout(
        title=f'Distribution of IMDb Top 250 Movies Between the "{start_decade}s" and "{end_decade}s"',
        xaxis_title='Decade',
        yaxis_title='Number of Movies',
        template='plotly_white'
    )
    return fig

# Function to Create Line Graph for Average Ratings by Decade
def create_average_ratings_line_graph(data, title):
    data['Rotten Tomatoes Tomatometer (Standardized)'] = data['Rotten Tomatoes Tomatometer'] / 10
    data['Metacritic Metascore (Standardized)'] = data['Metacritic Metascore'] / 10

    avg_imdb_ratings_by_decade = data.groupby('Decade')['IMDb Rating'].mean()
    avg_tomatometers_by_decade = data.groupby('Decade')['Rotten Tomatoes Tomatometer (Standardized)'].mean()
    avg_metascore_by_decade = data.groupby('Decade')['Metacritic Metascore (Standardized)'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=avg_imdb_ratings_by_decade.index, y=avg_imdb_ratings_by_decade,
                             mode='lines+markers', name='IMDb Rating', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=avg_tomatometers_by_decade.index, y=avg_tomatometers_by_decade,
                             mode='lines+markers', name='Rotten Tomates Tomatometer', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=avg_metascore_by_decade.index, y=avg_metascore_by_decade,
                             mode='lines+markers', name='Metacritic Metascore', line=dict(color='green')))
    
    fig.update_layout(
        title=title,
        xaxis_title='Decade',
        yaxis_title='Average Ratings',
        template='plotly_white',
        legend_title_text='Ratings'
    )
    return fig

# Create Tabs in the Over the Decades Section
tab1, tab2 = st.tabs(['Distribution of IMDb Top 250 Movies by Decade', 'Average Ratings by Decade'])

# Tab 1: Bar Chart for Distribution of Movies by Decade
with tab1:
    fig = create_movies_distribution_bar_chart(filtered_df, decade_range[0], decade_range[1])
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Line Graph of Average Ratings by Decade
with tab2:
    fig = create_average_ratings_line_graph(movies_df, 'Average Ratings by Decade')
    st.plotly_chart(fig, use_container_width=True)