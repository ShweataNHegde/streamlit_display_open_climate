import streamlit as st
import pandas as pd

CSV_FILE = 'country_ami.csv'
SEPARATOR = ';'

def get_data(csv_file):
    return pd.read_csv(csv_file)

def get_report_details(df, column_name):
    df['id'] = df[column_name].str.split("/").str.get(-2)
    return df

def get_filter_list(df, column_name, separator):
    entities_list = df[column_name].unique()
    # https://stackoverflow.com/questions/50755500/generate-a-list-from-another-list-with-comma-separated-values
    all_entitites = [single_entity for country_list in entities_list for single_entity in country_list.split(separator)]
    unique_entities = list(set(all_entitites))
    return unique_entities


df = get_data(CSV_FILE)
df_with_id = get_report_details(df, 'para_id')
all_countries_unique = get_filter_list(df_with_id, 'countries', SEPARATOR)
'## By country'
select_country = st.multiselect("Select Countries:", all_countries_unique)
all_options_country = st.checkbox("Select all options")
if all_options_country:
    select_country = all_countries_unique
'## By IPCC Report'
all_reports = get_filter_list(df_with_id, 'id', SEPARATOR)
select_report = st.multiselect("Select Reports:", all_reports)

#all_climate_terms = get_filter_list(df,'1')
#country = st.selectbox('Country', selected_options)
#climate_terms = st.selectbox('Climate Terms', all_climate_terms)

# https://stackoverflow.com/questions/11350770/filter-pandas-dataframe-by-substring-criteria
'## Filtered List of Sentences'
df_with_id[df_with_id['countries'].str.contains('|'.join(select_country)) & df_with_id['id'].str.contains('|'.join(select_report))]
#df[df['countries'].str.contains(country) & df['1'].str.contains(climate_terms)]
