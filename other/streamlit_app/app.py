import streamlit as st
import pandas as pd

# Load the CSV data
@st.cache_data
def load_data():
    df = pd.read_csv('../../data/aluguel.csv')
    return df

# Load the data
df = load_data()

# show a scatterplot of aluguel vs area
st.subheader('Scatter Plot')

# add a slider for aluguel

values = st.slider(
    'Select a range of values for Aluguel',
    df.aluguel.min(), df.aluguel.max(), (0, 2000))


st.scatter_chart(
    df.query(f'aluguel >= {values[0]} and aluguel <= {values[1]}'),
    x='area',
    y='aluguel',
    color='vaga',
    size='quartos',
)

# add a bar chart

st.subheader('Bar Chart')
st.bar_chart(
    df.query(f'aluguel >= {values[0]} and aluguel <= {values[1]}').aluguel,
)


# add a parallel coordinates plot using plotly.express
import plotly.express as px

st.subheader('Parallel Coordinates Plot')
fig = px.parallel_coordinates(
    df.query(f'aluguel >= {values[0]} and aluguel <= {values[1]}'),
    dimensions=['area', 'condominio', 'quartos'],
    color='aluguel',
)
st.plotly_chart(fig)
