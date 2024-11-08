########################
# Check Concept Set Name
########################
def check_concept_set_names(concept_set_name_list, r_script_path, atlas_user_name, atlas_password, keywords, flag_indicator, flag_enable_domain, base_url):
    import subprocess
    import pandas as pd
    from io import StringIO
    import streamlit as st
    
    flag_existing_concept_set_name = 0
    first_two = atlas_user_name[:2]
    last_two = atlas_user_name[-2:]
    keywords_list = keywords

    for name in concept_set_name_list:

        if flag_indicator == 2:
            keywords = []
            keywords = [item.split('_')[-1] for item in keywords_list if item.rsplit('_', 1)[0] == name]
 
        for keyword in keywords:
            if flag_indicator == 2:
                cs_name = "CHI" + "_" + first_two + "_" + last_two + "_" + name + "_OnlyStandards_" + keyword 
            else:
                cs_name = "CHI" + "_" + first_two + "_" + last_two + "_" + name + "_" + keyword

            try:
                # Construct and run the R script command
                command = ["Rscript", r_script_path, "checkConceptSet", cs_name, atlas_user_name, atlas_password, base_url]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, g_error = process.communicate()
                output_decoded = output.decode("utf-8")
                output_lines = output_decoded.split("\n")
                status_message = output_lines[0]
                csv_data = "\n".join(output_lines[1:])

                # Parse CSV output
                try:
                    result_df = pd.read_csv(StringIO(csv_data))
                    if result_df.empty and 'FALSE' in result_df.columns:
                        st.write(f"Concept Set name: `{cs_name}` is accepted")
                    else:
                        st.write(status_message)
                        st.dataframe(result_df)
                except pd.errors.ParserError as e:
                    st.write(f"Failed to parse CSV output: {e}")

            except Exception as e:
                if flag_indicator == 1 and flag_enable_domain == 1:
                    st.write(f"Concept Set name: `{cs_name}` already exists. Modify the sheet name and feed the input file again (or) proceed further to create concept sets categorized by domain.")
                if (flag_indicator == 2) or (flag_indicator == 1 and flag_enable_domain == 0):
                    st.write(f"Concept Set name: `{cs_name}` already exists. Modify the sheet name and feed the input file again.")
                flag_existing_concept_set_name = 1

    return flag_existing_concept_set_name

##############################
# Data Cleaning: Nearest Match
##############################
def replace_with_closest_match(input_string, predefined_strings):
    from difflib import get_close_matches
    closest_match = get_close_matches(input_string, predefined_strings, n=1)
    if closest_match:
        return closest_match[0]
    else:
        return input_string

###############
# Data Cleaning
###############
def process_data(temp):

    import re
    import numpy as np
    import pandas as pd

    temp.sort_values(by='vocabulary_id', inplace=True)

    # Clean and preprocess concept_code column
    temp['concept_code'] = temp['concept_code'].astype(str).str.strip()
    temp = temp[(temp['concept_code'] != 'undefined')]
    temp.drop_duplicates(inplace=True)
    temp['concept_code'] = temp['concept_code'].apply(lambda x: str(x).replace('*', '%').replace('x', '_'))
    temp['concept_code'] = temp['concept_code'].apply(lambda x: re.sub(r'[^a-zA-Z0-9.\-_ %]', '', str(x)))

    # Clean and preprocess Vocabulary ID column
    temp['vocabulary_id'] = temp['vocabulary_id'].astype(str).str.strip().str.upper()
    temp['vocabulary_id'] = temp['vocabulary_id'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x)))
    pattern1 = '.*ICD.*10.*CM.*'
    temp['vocabulary_id'] = np.where(temp['vocabulary_id'].str.contains(pattern1, case=False, regex=True), 'ICD10CM', temp['vocabulary_id'])
    pattern2 = '.*ICD.*9.*CM.*'
    temp['vocabulary_id'] = np.where(temp['vocabulary_id'].str.contains(pattern2, case=False, regex=True), 'ICD9CM', temp['vocabulary_id'])
    predefined_strings = ["ICD10", "ICD10CM", "ICD9", "ICD9CM", "LOINC", "ATC", "RXNORM", "RXNORMEXTENSION", "CPT4", "ICD10PROC", "ICD9PROC", "SNOMED", "NDC", "READCODE", "OMOP EXTENSION"]
    temp['vocabulary_id'] = temp['vocabulary_id'].apply(lambda x: replace_with_closest_match(x, predefined_strings))
    temp['vocabulary_id'] = temp['vocabulary_id'].fillna('')
    temp['vocabulary_id'] = temp['vocabulary_id'].replace('ICD10PROC', 'ICD10PCS', regex=True)
    temp['vocabulary_id'] = temp['vocabulary_id'].replace('READCODE', 'READ', regex=True)
    temp['vocabulary_id'] = np.where(temp['vocabulary_id'].str.contains('NDC', regex=True), 'NDC', temp['vocabulary_id'])

    # Clean and preprocess IE_Info column
    temp['IE_Info'] = temp['IE_Info'].astype(str).str.strip().str.upper()
    ie_categories = ["INCLUSION", "INC", "I", "EXCLUSION", "EXC", "E", "NONE", "X"]
    temp['IE_Info'] = temp['IE_Info'].apply(lambda x: replace_with_closest_match(x, ie_categories))
    mapping = {'INCLUSION': 1, 'INC': 1, "I": 1, 'NONE': 1, "1.0": 1, "1":1, 'EXCLUSION': 0, 'EXC': 0, 'E': 0,  "0.0": 0, "0":0}
    temp['IE_Info_Flag'] = temp['IE_Info'].map(mapping).astype("Int64")

    # Clean Descendants column
    temp['Descendants'] = temp['Descendants'].astype(str).str.strip().str.upper()
    desc_categories = ["Y", "YES", "N", "NO", "NONE"]
    temp['Descendants'] = temp['Descendants'].apply(lambda x: replace_with_closest_match(x, desc_categories))
    desc_mapping = {'Y': 1, 'YES': 1, '1': 1, '1.0': 1, "N": 0, 'NO': 0, 'NONE': 0, '0': 0, '0.0': 0}
    temp['Descendants_Flag'] = temp['Descendants'].map(desc_mapping).astype("Int64")

    return temp

##############################################################################################
# Identify the concept ids for a given code and also its respective standard code's concept id
##############################################################################################
def conceptid_for_input(data, engine, concept, db_type):
    import pandas as pd
    from fuzzywuzzy import process
    import re

    result_dataframes = []
    for group_name, group_data in data.groupby('sheet_name'):
        group_result_dataframes = []
        for index, row in group_data.iterrows():
            concept_code = row['concept_code']
            vocabulary_id = row['vocabulary_id']

            if db_type == "RedShift": 
                query = f"""SELECT DISTINCT CONCEPT_CODE, CONCEPT_ID, VOCABULARY_ID, DOMAIN_ID, STANDARD_CONCEPT AS FLAG_STANDARD_CONCEPT
                            FROM {concept}
                            WHERE UPPER(CONCEPT_CODE) LIKE UPPER(%s)
                            AND UPPER(VOCABULARY_ID) LIKE UPPER(%s)
                            AND UPPER(VOCABULARY_ID) NOT LIKE 'READ'

                            UNION

                            SELECT DISTINCT CONCEPT_CODE, CONCEPT_ID, VOCABULARY_ID, DOMAIN_ID, STANDARD_CONCEPT AS FLAG_STANDARD_CONCEPT
                            FROM {concept}
                            WHERE CONCEPT_CODE LIKE %s
                            AND UPPER(VOCABULARY_ID) LIKE UPPER(%s)
                            AND UPPER(VOCABULARY_ID) LIKE 'READ'
                            """
            else:
                query = f"""SELECT DISTINCT CONCEPT_CODE, CONCEPT_ID, VOCABULARY_ID, DOMAIN_ID, STANDARD_CONCEPT AS FLAG_STANDARD_CONCEPT
                            FROM {concept}
                            WHERE UPPER(CONCEPT_CODE) LIKE UPPER(?)
                            AND UPPER(VOCABULARY_ID) LIKE UPPER(?)
                            AND UPPER(VOCABULARY_ID) NOT LIKE 'READ'

                            UNION

                            SELECT DISTINCT CONCEPT_CODE, CONCEPT_ID, VOCABULARY_ID, DOMAIN_ID, STANDARD_CONCEPT AS FLAG_STANDARD_CONCEPT
                            FROM {concept}
                            WHERE CONCEPT_CODE LIKE ?
                            AND UPPER(VOCABULARY_ID) LIKE UPPER(?)
                            AND UPPER(VOCABULARY_ID) LIKE 'READ'
                            """

            # Execute the query with parameterized values
            result = pd.read_sql_query(query, engine, params=[(f"{concept_code}", f'%{vocabulary_id}%', f"{concept_code}", f'%{vocabulary_id}%')])
            group_result_dataframes.append(result)
        
        if group_result_dataframes:
            group_final = pd.concat(group_result_dataframes, ignore_index=True).drop_duplicates().sort_values(by='concept_code')
            group_final['group_identifier'] = group_name
            result_dataframes.append(group_final) 
    
    final = pd.concat(result_dataframes, ignore_index=False)
    final['concept_id'] = final['concept_id'].astype(str)
    final = final.sort_values(by=['group_identifier', 'concept_code'])
    
    column_names = ['group_identifier', 'concept_id', 'concept_code', 'vocabulary_id', 'domain_id', 'flag_standard_concept']
    final = final.reindex(columns=column_names)

    # Join IE_Info, Descendants and Wildcards column
    df1 = final
    df2 = data
    
    def get_nearest_match(concept_code, df2, column_name):
        df2['primary_concept_code'] = df2['concept_code'].str.replace('%', '').str.replace('*', '').str.replace('_', '.')
        # Exact match
        exact_match = df2[df2['primary_concept_code'].str.match(f'^{concept_code}$')]
        if not exact_match.empty:
            return exact_match.iloc[0][column_name]
        # Partial match
        regex_pattern = re.compile(f'^{concept_code}$')
        partial_match = df2[df2['primary_concept_code'].apply(lambda pattern: bool(re.search(pattern, concept_code)))]
        if not partial_match.empty:
            return partial_match.iloc[0][column_name]
        # Fuzzy match
        matches = process.extractOne(concept_code, df2['concept_code'])
        if matches[1] > 80:  # Adjust the threshold as needed
            nearest_match = df2[df2['concept_code'] == matches[0]]
            return nearest_match.iloc[0][column_name]
        else:
            return None  
    
    df1['IE_Info_Flag'] = df1['concept_code'].apply(lambda x: get_nearest_match(x, df2, 'IE_Info_Flag'))
    df1['Descendants_Flag'] = df1['concept_code'].apply(lambda x: get_nearest_match(x, df2, 'Descendants_Flag'))
    df1['Wildcard_Flag'] = df1['concept_code'].apply(lambda x: get_nearest_match(x, df2, 'Wildcard_Flag'))
    
    return df1


def standard_code_mapping(df1, engine, concept, concept_relationship, db_type):
    import streamlit as st
    import pandas as pd
    from sqlalchemy.exc import SQLAlchemyError

    group_result_dataframes = []
    for group_identifier, group_data in df1.groupby('group_identifier'):
        concept_id_list = group_data['concept_id'].tolist()
        
        try:
            if db_type == "RedShift":
                concept_id_list = [int(id) for id in concept_id_list if id is not None]
                placeholders = ', '.join(['%s'] * len(concept_id_list))
            else:
                placeholders = ', '.join(['?'] * len(concept_id_list))
            
            sql_base_table = f"""
                SELECT DISTINCT 
                    C.CONCEPT_ID AS concept_id,
                    C.CONCEPT_CODE AS concept_code,
                    C.CONCEPT_NAME AS concept_name,
                    C.VOCABULARY_ID AS vocabulary_id,
                    C.DOMAIN_ID AS domain,
                    C.STANDARD_CONCEPT AS flag_standard_concept_input,
                    CR.CONCEPT_ID_2 AS standard_code,
                    C2.VOCABULARY_ID AS vocabulary,
                    C2.CONCEPT_NAME AS standard_concept_name,
                    C2.STANDARD_CONCEPT AS flag_standard_concept,
                    C2.DOMAIN_ID AS standard_domain,
                    CR.RELATIONSHIP_ID AS relationship_id
                FROM (
                        SELECT CONCEPT_ID, CONCEPT_CODE, CONCEPT_NAME, VOCABULARY_ID, DOMAIN_ID, STANDARD_CONCEPT
                        FROM {concept}
                        WHERE CONCEPT_ID IN ({placeholders}) ) C
                JOIN {concept_relationship} CR ON C.CONCEPT_ID = CR.CONCEPT_ID_1
                JOIN {concept} C2 ON C2.CONCEPT_ID = CR.CONCEPT_ID_2
                WHERE UPPER(RELATIONSHIP_ID) IN ('MAPS TO', 'MAPS TO VALUE')
                AND CR.INVALID_REASON IS NULL
                ORDER BY C.CONCEPT_ID;"""
            st.write(sql_base_table)
            
            result_sql_base_table = pd.read_sql(sql_base_table, engine, params=(concept_id_list,))
            # result_sql_base_table = pd.read_sql(sql_base_table, engine, params=tuple(concept_id_list))        
            result_sql_base_table['group_identifier'] = group_identifier
            result_sql_base_table['concept_id'] = result_sql_base_table['concept_id'].astype(str)
            result_sql_base_table = result_sql_base_table.merge(
                group_data[['concept_id', 'IE_Info_Flag', 'Descendants_Flag', 'Wildcard_Flag']],
                on='concept_id', how='left'
            )
            group_result_dataframes.append(result_sql_base_table)

        except SQLAlchemyError as e:
            st.error(f"Error processing group {group_identifier}: {str(e)}")

    result_df = pd.concat(group_result_dataframes, ignore_index=True)
    result_df['concept_id'] = result_df['concept_id'].astype(str)
    result_df['standard_code'] = result_df['standard_code'].astype(str)
    result_df = result_df.rename(columns={'group_identifier': 'sheet_name'})
    column_names = ['sheet_name', 'concept_id', 'concept_code', 'concept_name', 'vocabulary_id', 'domain', 
                    'Wildcard_Flag', 'flag_standard_concept_input', 'standard_code', 'standard_concept_name', 
                    'vocabulary', 'standard_domain', 'IE_Info_Flag', 'Descendants_Flag', 'flag_standard_concept', 
                    'relationship_id']
    result_df = result_df.reindex(columns=column_names)
    result_df = result_df.sort_values(by=['sheet_name', 'concept_code']).reset_index(drop=True)

    return result_df
