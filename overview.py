import streamlit as st
import pandas as pd

# Load the Processed Dataset
@st.cache_data
def load_movies_data():
    return pd.read_csv('IMDb Top 250 Movies (Director & Actors).csv')

movies_df = load_movies_data()

# Create Tabs in the Overview Section
tab1, tab2 = st.tabs(['IMDb Top 250 Movies Dataset', 'Numerical Variables Summary Statistics'])

# Tab 1: Display the Dataset
with tab1:
    st.subheader('IMDb Top 250 Movies Dataset')
    st.dataframe(movies_df)
    st.write('Dataset Shape:', movies_df.shape)
    st.write('Data Type:', movies_df.dtypes)

# Tab 2: Display Summary Statistics for Selected Numerical Variables
with tab2:
    st.subheader("Numerical Variables Summary Statistics")

    # User selection of numerical variables
    numerical_variables = ['IMDb Rating', 'Rotten Tomatoes Tomatometer', 'Metacritic Metascore', 'Box Office', 'Total Wins', 'Total Nominations']
    selected_variables = st.multiselect('Select numerical variables to view summary statistics:', 
                                        options=numerical_variables, 
                                        default=numerical_variables) # Default shows all

    # Display the selected summary statistics
    if selected_variables:
        for selected_variable in selected_variables:
            st.write(f'Summary Statistics for "{selected_variable}":')
            st.dataframe(movies_df[selected_variable].describe())
    else:
        st.write('No variables selected. Please choose at least one variable to display statistics.')