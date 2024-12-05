import streamlit as st

# App Title
st.title('IMDb Top 250 Movies: Insights and Interactivity')

# App Pages
pages = {
    'Navigation': [
        st.Page('overview.py', title='Overview'),
        st.Page('over-the-decades.py', title='Over the Decades'),
        st.Page('genre-analysis.py', title='Genre Analysis'),
        st.Page('correlation-analysis.py', title='Correlation Analysis')
    ],
}

# Initialize and Run App Pages in the Navigation Sidebar
pg = st.navigation(pages)
pg.run()