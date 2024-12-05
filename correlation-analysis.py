import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Processed Dataset
@st.cache_data
def load_movies_data():
    return pd.read_csv('IMDb Top 250 Movies (Director & Actors).csv')

movies_df = load_movies_data()

# Page Title
st.subheader('Correlation Analysis')

# Sidebar Checkboxes of User Input for Pairs of Numerical Variables to Plot
st.sidebar.subheader('Select Correlations to Display')
checkboxes = {
    'IMDb Rating vs. Box Office': st.sidebar.checkbox('IMDb Rating vs. Box Office', value=True),
    'IMDb Rating vs. Total Wins': st.sidebar.checkbox('IMDb Rating vs. Total Wins', value=False),
    'IMDb Rating vs. Total Nominations': st.sidebar.checkbox('IMDb Rating vs. Total Nomanations', value=False),
    'Box Office vs. Total Wins': st.sidebar.checkbox('Box Office vs. Total Wins', value=False),
    'Rotten Tomatoes Tomatometer vs. Metacritic Metascore': st.sidebar.checkbox('Rotten Tomatoes Tomatometer vs. Metacritic Metascore', value=False),
}

# Map Checkbox Options to Corresponding Columns
plot_mapping = {
    'IMDb Rating vs. Box Office': ('IMDb Rating', 'Box Office'),
    'IMDb Rating vs. Total Wins': ('IMDb Rating', 'Total Wins'),
    'IMDb Rating vs. Total Nominations': ('IMDb Rating', 'Total Nominations'),
    'Box Office vs. Total Wins': ('Box Office', 'Total Wins'),
    'Rotten Tomatoes Tomatometer vs. Metacritic Metascore': ('Rotten Tomato Tomatometer', 'Metacritic Metascore'),
}

# Display Scatterplots Based on the Selected Checkboxes
for key, checked in checkboxes.items():
    if checked:
        # Extract the x and y variables for the scatterplot
        x_var, y_var = plot_mapping[key]

        # Generate the scatterplot for the selected pairs of numerical variables
        fig = px.scatter(
            movies_df,
            x=x_var,
            y=y_var,
            labels={x_var: x_var, y_var: y_var},
            opacity=0.7,
            trendline='ols'
        )

        # Add titles
        fig.update_layout(
            title=f'{x_var} vs. {y_var}',
            xaxis_title=x_var,
            yaxis_title=y_var
        )

        # Display the scatterplots
        st.plotly_chart(fig, use_container_width=True)
