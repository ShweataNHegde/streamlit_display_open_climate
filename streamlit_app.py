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

def main():
    st.set_page_config(page_title='Semantic IPCC', page_icon='💻', layout="centered", initial_sidebar_state="auto", menu_items=None)
    st.title('Semantic IPCC')
    col1, col2 = st.columns(2)
    df = get_data(CSV_FILE)
    df_with_id = get_report_details(df, 'para_id')
    all_countries_unique = get_filter_list(df_with_id, 'countries', SEPARATOR)
    col1.write('### By country')
    all_countries_unique.sort()
    select_country = col1.multiselect("Select Countries:", all_countries_unique)
    all_options_country = col1.checkbox("Select all options")
    if all_options_country:
        select_country = all_countries_unique
    col2.write('### By IPCC Report')
    all_reports = get_filter_list(df_with_id, 'id', SEPARATOR)
    all_reports.sort()
    select_report = col2.multiselect("Select Reports:", all_reports)
    '## Filtered List of Paragraphs'
    filtered_df = df_with_id[df_with_id['countries'].str.contains('|'.join(select_country)) & df_with_id['id'].str.contains('|'.join(select_report))]
    st.metric(label="No. of paragraphs", value = len(filtered_df.index))
    st.write(filtered_df)

# https://stackoverflow.com/questions/11350770/filter-pandas-dataframe-by-substring-criteria



if __name__ == "__main__":
    main()