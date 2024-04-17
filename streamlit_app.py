import streamlit as st
import pandas as pd

def get_data():
    return pd.read_csv('country_climate.csv')

def get_filter_list(df, column_name):
    countries = df[column_name].unique()
    # https://stackoverflow.com/questions/50755500/generate-a-list-from-another-list-with-comma-separated-values
    all_countries = [single_country for country_list in countries for single_country in country_list.split(", ")]
    all_countries_unique = list(set(all_countries))
    return all_countries_unique

'## By country'
df = get_data()
all_countries_unique = get_filter_list(df, '0')
all_climate_terms = get_filter_list(df,'1')
country = st.selectbox('Country', all_countries_unique)
climate_terms = st.selectbox('Climate Terms', all_climate_terms)
df
#df[df['0'].str.contains(country) & df['1'].str.contains(climate_terms)]

#year = st.slider('Year', min_year, max_year)
#df[df['Year'] == year]
