import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Processed Dataset
@st.cache_data
def load_movies_data():
    return pd.read_csv('IMDb Top 250 Movies (Director & Actors).csv')

movies_df = load_movies_data()

# Page Title
st.subheader('Genre Analysis')

# Sidebar Checkboxes of User Input for Metrics
st.sidebar.subheader('Genre Analysis Options')
st.sidebar.write('Select Metrics to Display the Top Genres by:')
show_average_box_office = st.sidebar.checkbox('Average Box Office', value=True) # Default checked
show_average_imdb_rating = st.sidebar.checkbox('Average IMDB Rating', value=False)
show_average_tomatometer = st.sidebar.checkbox('Average Rotten Tomatoes Tomatometer', value=False)
show_average_metascore = st.sidebar.checkbox('Average Metacritic Metascore', value=False)

# Sidebar Radio Buttons of User Input for the Number of Top Genres
top_n_genres = st.sidebar.radio(
    'Select the Number of Top Genres to Display:',
    options=[5, 10, 20],
    index=1 # Default to 10
)

# Explode Genres to Make Each Genre A Separate Row
movies_df['Genre List'] = movies_df['Genre'].str.split(', ')
exploded_genres = movies_df.explode('Genre List')

# Function to Generate Bar Chart for Top Genres by Metric
def generate_genres_by_metric_bar_chart(df, metric, metric_label, top_n):
    avg_metric_by_genre = df.groupby('Genre List')[metric].mean().sort_values(ascending=False).head(top_n)

    fig = px.bar(
        avg_metric_by_genre,
        x=avg_metric_by_genre.index,
        y=avg_metric_by_genre.values,
        labels={'x': 'Genre', 'y': metric_label},
        color_discrete_sequence=['#636EFA']
    )

    fig.update_layout(
        title=f'Top {top_n} Genres by {metric_label}',
        xaxis_title='Genre',
        yaxis_title=metric_label
    )
    return fig

# Display Bar Charts Based on the Selected Checkboxes
if any([show_average_box_office, show_average_imdb_rating, show_average_tomatometer, show_average_metascore]):
    if show_average_box_office:
        st.plotly_chart(generate_genres_by_metric_bar_chart(exploded_genres, 'Box Office', 'Average Box Office', top_n_genres), use_container_width=True)
    if show_average_imdb_rating:
        st.plotly_chart(generate_genres_by_metric_bar_chart(exploded_genres, 'IMDb Rating', 'Average IMDb Rating', top_n_genres), use_containter_width=True)
    if show_average_tomatometer:
        st.plotly_chart(generate_genres_by_metric_bar_chart(exploded_genres, 'Rotten Tomatoes Tomatometer', 'Average Rotten Tomates Tomatometer', top_n_genres), use_container_width=True)
    if show_average_metascore:
        st.plotly_chart(generate_genres_by_metric_bar_chart(exploded_genres, 'Metacritic Metascore', 'Average Metacritic Metascore', top_n_genres), use_container_width=True)
else:
    st.write('Please select at least one metric to display.')