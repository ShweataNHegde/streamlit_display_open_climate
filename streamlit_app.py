import streamlit as st
import pandas as pd

#streamlit variables
PAGE_TITLE = "Semantic IPCC"
#other variables
CSV_FILE_COUNTRY = 'countries.csv'
CSV_FILE_TERMS = 'terms.csv'
SEPARATOR = ';'

def get_data(csv_file):
    return pd.read_csv(csv_file)

def merge_df_for_cooccurence(df1, df2):
    merged_df = pd.merge(df1, df2)
    return merged_df

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
    st.set_page_config(page_title=PAGE_TITLE, page_icon='💻', layout="centered", initial_sidebar_state="auto", menu_items=None)
    st.title(PAGE_TITLE)
    col1, col2 = st.columns(2)
    df_countries = get_data(CSV_FILE_COUNTRY)
    df_terms = get_data(CSV_FILE_TERMS)
    merged_df = merge_df_for_cooccurence(df_countries, df_terms)
    df_with_id = get_report_details(merged_df, 'para_id')
    all_countries_unique = get_filter_list(df_with_id, 'countries', SEPARATOR)
    all_terms_unique = get_filter_list(df_with_id, 'terms', SEPARATOR)
    col1.write('### By country')
    all_countries_unique.sort()
    all_terms_unique.sort()
    select_country = col1.multiselect("Select Countries:", all_countries_unique)
    all_options_country = col1.checkbox("Select all countries")
    if all_options_country:
        select_country = all_countries_unique
    col1.write('### By Terms')
    select_terms = col1.multiselect('Select Climate Terms:', all_terms_unique)
    all_options_terms = col1.checkbox("Select all terms")
    if all_options_terms:
        select_terms = all_terms_unique
    col2.write('### By IPCC Report')
    all_reports = get_filter_list(df_with_id, 'id', SEPARATOR)
    all_reports.sort()
    select_report = col2.multiselect("Select Reports:", all_reports)
    '## Filtered List of Paragraphs'
    filtered_df = df_with_id[df_with_id['countries'].str.contains('|'.join(select_country)) & df_with_id['id'].str.contains('|'.join(select_report)) & df_with_id['terms'].str.contains('|'.join(select_terms))]
    st.metric(label="No. of paragraphs", value = len(filtered_df.index))
    st.write(filtered_df)
# https://stackoverflow.com/questions/11350770/filter-pandas-dataframe-by-substring-criteria



if __name__ == "__main__":
    main()