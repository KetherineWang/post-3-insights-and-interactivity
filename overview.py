import streamlit as st
import pandas as pd

# Load the Processed Dataset
@st.cache_data
def load_movies_data():
    return pd.read_csv('IMDb Top 250 Movies (Director & Actors).csv')

movies_df = load_movies_data()

# Page Title
st.subheader('Overview')

# Specify the File Path of the Existing CSV Dataset
file_path = 'IMDb Top 250 Movies (Director & Actors).csv'

# Open the CSV File and Read Its Content
with open(file_path, 'r') as file:
    csv_content = file.read()

# Sidebar Download Button to Download the Dataset as CSV
st.sidebar.download_button(
    label='Download the "IMDb Top 250 Movies" Dataset as CSV',
    data=csv_content,
    file_name='IMDb Top 250 Movies',
    mime='text/csv'
)

# Create Tabs in the Overview Section
tab1, tab2, tab3 = st.tabs(['IMDb Top 250 Movies Dataset', 'Numerical Variables Summary Statistics', 'Search IMDb Top 250 Movies by Movie Name'])

# Tab 1: IMDb Top 250 Movies Dataset
with tab1:
    st.subheader('IMDb Top 250 Movies Dataset')
    st.dataframe(movies_df)
    st.write('Dataset Shape:', movies_df.shape)
    st.write('Data Type:', movies_df.dtypes)

# Tab 2: Numerical Variables Summary Statistics
with tab2:
    st.subheader("Numerical Variables Summary Statistics")

    # User selection of numerical variables
    numerical_variables = ['IMDb Rating', 'Rotten Tomatoes Tomatometer', 'Metacritic Metascore', 'Box Office', 'Total Wins', 'Total Nominations']
    selected_variables = st.multiselect('Select numerical variables to view summary statistics:', 
                                        options=numerical_variables, 
                                        default=numerical_variables) # Default shows all

    # Display the corresponding summary statistics
    if selected_variables:
        for selected_variable in selected_variables:
            st.write(f'Summary Statistics for "{selected_variable}":')
            st.dataframe(movies_df[selected_variable].describe())
    else:
        st.write('No variables selected. Please choose at least one variable to display statistics.')

# Tab 3: Search IMDb Top 250 Movies by Movie Name
with tab3:
    st.subheader('Search for An IMDb Top 250 Movie')

    # User input for the movie name
    movie_name = st.text_input('Enter A Movie Name (Case-Insensitive):', "Inception")

    if movie_name:
        # Filter the dataset for the given movie name
        search_results = movies_df[movies_df['Movie Title'].str.contains(movie_name, case=False, na=False)]

        if not search_results.empty:
            st.write(f'Results for "{movie_name}":')
            st.dataframe(search_results)
        else:
            st.write(f'No results found for "{movie_name}". It might not be a movie in the IMDb Top 250 Movies list. Please try another movie name.')
    else:
        st.write('Enter a movie name to search.')