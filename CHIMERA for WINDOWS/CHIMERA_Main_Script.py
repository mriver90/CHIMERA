####################
# Dashboard Packages
####################
import streamlit as st 
from PIL import Image 
import pandas as pd 
import numpy as np 
from sqlalchemy import create_engine 
import time
import re
import subprocess
import textwrap
from io import StringIO 
import os
import random

try:
    import CHIMERA_User_Defined_Functions as ws
except ImportError as e:
    print(f"Error importing CHIMERA_User_Defined_Functions: {e}. Ensure the module is available and properly configured.")

g_error = "" # Global error needed for exception block from Rscript

#############
# UI Elements
#############
st.session_state['init_load'] = 0
try: 
    jnj_logo = Image.open('dummy.jpg') # Ensure that the image is in the same directory as the script
except Exception as e:
    jnj_logo = None

# Set up the page to occupy entire screen
st.set_page_config(page_title="CHIMERA",
                   layout='wide', initial_sidebar_state='collapsed')

# Remove menu lines
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Logo and Title setup
col1, col2 = st.columns([4, 50])
col1.image(jnj_logo, width=50)
col2.markdown("<h3 style='text-align: center; color: #003479;'>CHIMERA: Automatic Concept-set Creation</h3>",
              unsafe_allow_html=True)

# Function to load CSS file to this UI
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
if st.session_state['init_load'] == 0:
    local_css("style.css")
    st.session_state['init_load'] += 1

try:
    import hydralit_components as hc
    # Hydralit Components is imported successfully, use the hc.nav_bar method
    menu_data = [
        {'id': 'Home', 'label': 'Home'},
        {'id': 'Delete Concept-Sets', 'label': 'Delete Concept-Sets'}
    ]
    over_theme = {'txc_inactive': '#FFFFFF', 'menu_background': '#003479'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        hide_streamlit_markers=False,
        sticky_nav=True,
        sticky_mode='pinned',
    )
except ImportError as e:
    print(f"Hydralit Components not available: {e}. Falling back to an alternative approach.")

    # Alternative: Streamlit's standard selectbox or radio buttons for navigation
    import streamlit as st
    menu_id = st.selectbox(
        "Choose a menu option:",
        ['Home', 'Delete Concept-Sets']
    )

###########
# Home Menu
###########
if menu_id == 'Home':
    #############
    # Upload File
    #############
    selected_data = pd.DataFrame()
    
    uploaded_file = st.file_uploader("Upload excel/csv file:",type=["xlsx", "xls", "csv", "xlsm"] )
    st.markdown("<span style='font-size: smaller; color: #0F68B2;'><strong>NOTE:</strong> Ensure that each sheet has an appropriate name, as concept sets will be generated per sheet and saved in ATLAS using the sheet name of the input file</span>", unsafe_allow_html=True)
    st.text("")
    st.text("")
    
    if uploaded_file is not None:
    
        # Ensuring the data type is string for all the column values in input file
        file_extension = uploaded_file.name.split('.')[-1]
        file_name = '.'.join(uploaded_file.name.split('.')[:-1])
        if file_extension in ['xlsx', 'xls', 'xlsm']:
            try:
                excel_data = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl', dtype=str)
                for sheet_name, df in excel_data.items():
                    df['sheet_name'] = sheet_name 
                    selected_data = pd.concat([selected_data, df], ignore_index=False)
            except Exception as e:
                st.error(f"Error reading Excel file: {e}")
        elif file_extension == 'csv':
            try:
                selected_data = pd.read_csv(uploaded_file, encoding='utf-8', dtype=str)
                selected_data['sheet_name'] = file_name
            except UnicodeDecodeError:
                selected_data = pd.read_csv(uploaded_file, encoding='latin1', dtype=str)
                selected_data['sheet_name'] = file_name
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")
        
        # Choose specific sheet(s)
        filtered_data_flag = 0
        list_sheet_name = selected_data['sheet_name'].unique().tolist()
        st.text("")
        specific_sheet = st.checkbox("Would you like to choose specific sheet(s) from the excel file?")
        if specific_sheet and 'sheet_name' in selected_data.columns:
            try:
                selected_sheets = st.multiselect("Select sheet(s):", list_sheet_name)
                if selected_sheets:
                    filtered_data_flag = 1
                    filtered_data = selected_data[selected_data['sheet_name'].isin(selected_sheets)]
                    columns_order = ['sheet_name'] + [col for col in filtered_data.columns if col != 'sheet_name'] # Reorder columns
                    filtered_data = filtered_data[columns_order]
                    st.dataframe(filtered_data)
            except Exception as e:
                st.error(f"Error reading Excel file: {e}")
    
        # All Sheets
        else:
            st.text("")
            st.text("")
            st.markdown("<strong> View Data:</strong>", unsafe_allow_html=True)
            selected_sheet = st.selectbox("Select a sheet", list_sheet_name)
            if selected_sheet:
                filtered_data = selected_data[selected_data['sheet_name'] == selected_sheet]
                columns_order = ['sheet_name'] + [col for col in filtered_data.columns if col != 'sheet_name']
                filtered_data = filtered_data[columns_order]
                st.dataframe(filtered_data)
                st.markdown("<span style='font-size: smaller; color: #0F68B2;'>NOTE: Since no specific sheets are selected, all sheets in the provided input file will be used to create concept sets (one concept set per sheet).</span>", unsafe_allow_html=True)
    
        ############################
        # Check for Concept Set Name
        ############################

        ### Concept Set Name List
        if filtered_data_flag == 1:
            concept_set_name_list = selected_sheets
            selected_data = filtered_data
        else:
            concept_set_name_list = list_sheet_name

        ### ATLAS Login Credentials
        st.text("")
        st.text("")
        st.text("")
        st.markdown("<strong> ATLAS Login Credentials:</strong>", unsafe_allow_html=True)
        col_11, col_22, col_33 = st.columns(3)
        with col_11:
            base_url = st.text_input('Enter the URL of your ATLAS instance:', None)
        with col_22:
            atlas_user_name = st.text_input('Enter ATLAS User Name:', None)
        with col_33:
            atlas_password = st.text_input('Enter ATLAS Password:', type="password")
        
        # Check ATLAS connectivity
        flag_atlas_login = 0
        if base_url and atlas_user_name and atlas_password:
            r_script_path = "CHIMERA_R_User_Defined_Function.R" # Assuming the current directory is set to the location of this file
            try:
                command = ["Rscript", r_script_path, "authorize_web_api", base_url, atlas_user_name, atlas_password]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, g_error = process.communicate()
                output_decoded = output.decode("utf-8")
                if output_decoded: 
                    st.error(output_decoded)
                    flag_atlas_login = 1
                else:
                    st.success("Successfully connected to ATLAS")
            except Exception as e:
                st.write(f"Failed to check the ATLAS connectivity: {e}")

        st.markdown("<span style='font-size: smaller; color: #0F68B2;'><strong>NOTE:</strong> <br>1. The ATLAS username will be incorporated into the Concept Set naming convention along with the keyword CHI as follows: `CHI_first2charactersOfATLASUserName_last2charactersOfATLASUserName_sheetname_keyword` <br>2. Ensure that the sheet name is unique to avoid conflicts when saving the concept set in ATLAS", unsafe_allow_html=True)
        

        if flag_atlas_login == 0:
            ### Check boxes
            st.text("")
            st.text("")
            st.text("")
            st.markdown("<strong> Type of Concept-Set:</strong>", unsafe_allow_html=True)
            st.markdown("<span style='font-size: smaller; color: #0F68B2;'>Please select one or more of the options below. Based on your selection, the number of concept sets and the type of codes to be included in those concept sets will be determined. <br> <strong>NOTE:</strong> Each sheet in your input file is treated individually. Therefore, if multiple sheets are selected, the options below will be applied separately to each sheet.</span>", unsafe_allow_html=True)
            st.text("")
            
            flag_checkbox = 0
            flag_enable_domain = 0
            selected_options = []
            keywords = []
            if st.checkbox('Standard Codes only'):
                selected_options.append('Standard Codes only')
                keywords.append('OnlyStandards')
                flag_checkbox = 1
                flag_enable_domain = 1

            if st.checkbox('Standard and Non-Standard Codes (All in one)'):
                selected_options.append('Standard and Non-Standard Codes (All in one)')
                keywords.append('All')
                flag_checkbox = 1

            if st.checkbox(
                'Codes from your input file only. Here, Inclusion/Exclusion and Descendants features are considered but mapped standard codes are NOT. Example use-case: Your input file already has a list of standard codes, and you only want those codes without adding any extra codes to your concept set.'
            ):
                selected_options.append('Codes from your input file only')
                keywords.append('OnlyInputFileCodes')
                flag_checkbox = 1
                flag_enable_domain = 1

            ### Checking for the names in ATLAS
            flag_existing_concept_set_name = 0
            flag_indicators = 0
            if atlas_user_name and atlas_password and flag_checkbox == 1:
                st.text("")
                st.text("")
                st.text("")
                st.markdown("<strong> Check Concept-Set Name:</strong>", unsafe_allow_html=True)
                st.markdown("<span style='font-size: smaller; color: #0F68B2;'><strong>NOTE:</strong> When multiple sheets are selected, some might have acceptable concept-set names while others do not. In such cases, you can deselect the sheets with unaccepted concept-set names and proceed with the accepted ones.</span>", unsafe_allow_html=True)
                flag_indicators = 1
                flag_existing_concept_set_name = ws.check_concept_set_names(concept_set_name_list, r_script_path, atlas_user_name, atlas_password, keywords, flag_indicators, flag_enable_domain, base_url)

            ################
            # Select columns
            ################
            if (flag_existing_concept_set_name == 0 | (flag_existing_concept_set_name == 1 and flag_enable_domain == 1)) and atlas_user_name and atlas_password and flag_checkbox == 1:
                st.text("")
                st.text("")
                st.text("")
                st.markdown("<strong> Select the required fields:</strong>", unsafe_allow_html=True)
                try:
                    column_names = selected_data.columns 
                    col_111, col_222, col_333, col_444 = st.columns(4)
                    with col_111:
                        col_concept_code = st.selectbox("Select Concept_Code column:", column_names)
                    with col_222:
                        col_vocabulary_id = st.selectbox("Select Vocabulary_ID column:", column_names)
                    with col_333:
                        col_ie_criteria_options = ["None"] + list(selected_data.columns)
                        col_ie_criteria = st.selectbox("Select I/E_Criteria column:", col_ie_criteria_options)
                    with col_444:
                        col_descendants_options = ["None"] + list(selected_data.columns)
                        col_descendants = st.selectbox("Select Descendants column:", col_descendants_options)
                    st.markdown(
                        """
                        <span style='font-size: smaller; color: #0F68B2;'>
                            <strong>NOTE:</strong>
                            <br>1. Ensure that the column names are consistent across all sheets in case of multiple sheets.
                            <br>2. If the Excel file does not contain a specific column indicating whether a concept code should be included or excluded, the program will default to considering it as an inclusion. The Inclusion/Exclusion criteria column in the input file can contain either text (e.g., 'Inclusion', 'Exclusion', 'I', 'E', etc.) or binary values. The application can convert it into a binary field where 'Inclusion' = 1 and 'Exclusion' = 0.
                            <br>3. To include descendants for a specific concept code, make sure there's a separate column in your input file for this purpose. If the Excel file does not contain a specific column indicating whether descendants should be included for a concept, the program will default to not including descendants. The descendants column in the input file can contain either text (e.g., 'Yes', 'No', 'Y', 'N', etc.) or binary values. The application can convert it into a binary field where 'Yes' = 1 and 'No' = 0.
                        """,
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.text("")
                
            #################################
            # Data Cleaning and Preprocessing
            #################################
            st.text("")
            st.text("")
            st.text("")
            st.markdown("<strong> Data Cleaning and Preprocessing </strong>", unsafe_allow_html=True)
            clean_data = selected_data.copy()
            flag_cleaned_data = 0
            # Rename Concept_Code and Vocabulary column
            try: 
                if col_concept_code in clean_data.columns:
                    clean_data.rename(columns={col_concept_code: 'concept_code'}, inplace=True)
                if col_vocabulary_id in clean_data.columns:
                    clean_data.rename(columns={col_vocabulary_id: 'vocabulary_id'}, inplace=True)
                if col_ie_criteria != "None" and col_ie_criteria in clean_data.columns:
                    clean_data.rename(columns={col_ie_criteria: 'IE_Info'}, inplace=True)
                if col_ie_criteria == "None":
                    clean_data['IE_Info'] = 1
                if col_descendants != "None" and col_descendants in clean_data.columns:
                    clean_data.rename(columns={col_descendants: 'Descendants'}, inplace=True)
                if col_descendants == "None":
                    clean_data['Descendants'] = 0
                # Select required columns
                selected_columns = ['sheet_name', 'concept_code', 'vocabulary_id', 'IE_Info', 'Descendants']
                clean_data = clean_data[selected_columns]
                # Remove the rows that has empty value in Concept_Code column
                clean_data = clean_data[clean_data['concept_code'].notna() & (clean_data['concept_code'] != '')]
                clean_data = clean_data.groupby('sheet_name').apply(lambda x: x.reset_index(drop=True))
                # Handle empty values in vocabulary_id, IE_Info and Descendants column
                clean_data['vocabulary_id'] = clean_data['vocabulary_id'].fillna("")
                clean_data['IE_Info'] = clean_data['IE_Info'].fillna(1)
                clean_data.loc[clean_data['IE_Info'] == '', 'IE_Info'] = 1
                clean_data['Descendants'] = clean_data['Descendants'].fillna(0)
                clean_data.loc[clean_data['Descendants'] == '', 'Descendants'] = 0
                # Create Flag for Wildcards
                conditions = [
                    clean_data['concept_code'].str.contains('[*%]'),
                    clean_data['concept_code'].str.contains('x')
                ]
                flag_values = [1, 2]
                clean_data['Wildcard_Flag'] = np.select(conditions, flag_values, default=0)
                try:
                  cleaned_data = clean_data.groupby(clean_data['sheet_name']).apply(ws.process_data)
                  num_levels = cleaned_data.index.nlevels
                  if isinstance(cleaned_data.index, pd.MultiIndex) and num_levels > 1:
                     cleaned_data = cleaned_data.droplevel(list(range(num_levels - 1)))
                     cleaned_data = cleaned_data.groupby('sheet_name').apply(lambda x: x.reset_index(drop=True))
                  else:
                     cleaned_data = cleaned_data.groupby('sheet_name').apply(lambda x: x.reset_index(drop=True))
                  # Display cleaned data
                  required_columns = ['sheet_name', 'concept_code', 'vocabulary_id', 'IE_Info', 'IE_Info_Flag', 'Descendants', 'Descendants_Flag', 'Wildcard_Flag']
                  cleaned_data = cleaned_data[required_columns]
                  num_levels = cleaned_data.index.nlevels
                  cleaned_data = cleaned_data.droplevel(list(range(num_levels - 1)))
                  st.dataframe(cleaned_data)
                  # Flag
                  flag_cleaned_data = 1
                except Exception as e:
                     st.write(f"An error occurred while processing the data: {e}")

                # Summary
                row_counts = cleaned_data.groupby('sheet_name').size().rename('N_concept_code')
                st.markdown("<span style='font-size: smaller; color: #0F68B2;'>Total number of concept codes per sheet:", unsafe_allow_html=True)    
                st.write(row_counts)
            except Exception as e:
                st.text("")

            #######################
            # Standard Code Mapping
            #######################
            st.text("")
            st.text("")
            st.text("")
            st.markdown("<strong> Standard Code Mapping:</strong>", unsafe_allow_html=True)
            
            connection_successful = 0
            if flag_cleaned_data == 1:
                try:
                   connection_string = 'sqlite:///chimera.db'
                   engine = create_engine(connection_string)

                   with engine.connect() as connection:
                        result = pd.read_sql("SELECT * FROM concept", con=connection)
                        if not result.empty:
                           st.write(f"Concept Table (Rows, Columns): {result.shape}") 
                           st.success("Successfully connected to the CHIMERA database")
                           connection_successful = 1
                except Exception as e:
                    st.error(f"Could not load the vocabularies. Error: {e}")
            else:
                st.text("")

            if connection_successful == 1:
                base_table_df = ws.conceptid_for_input(cleaned_data, engine)
                mapped_table_df = ws.standard_code_mapping(base_table_df, engine)
                mapped_table_df['IE_Info_Flag_mapped'] = mapped_table_df['IE_Info_Flag']
                column_order = ['sheet_name', 'concept_id', 'IE_Info_Flag', 'concept_code', 'concept_name', 'vocabulary_id', 'domain', 'Wildcard_Flag', 'flag_standard_concept_input', 'standard_code', 'IE_Info_Flag_mapped', 'standard_concept_name', 'vocabulary', 'standard_domain', 'Descendants_Flag', 'flag_standard_concept', 'relationship_id']
                mapped_table_df = mapped_table_df[column_order]
                mapped_table_df = mapped_table_df.sort_values(by=['sheet_name', 'concept_code']).groupby('sheet_name').apply(lambda x: x.reset_index(drop=True))
                st.dataframe(mapped_table_df)                               
                
                #####################
                # Final list of codes
                #####################
                st.text("")
                st.text("")
                st.text("")
                st.markdown("<strong> Final list of concept IDs:</strong>", unsafe_allow_html=True)
 
                base_table_unique = base_table_df.rename(columns={'group_identifier': 'sheet_name'})[['sheet_name', 'concept_id', 'IE_Info_Flag', 'Descendants_Flag', 'flag_standard_concept', 'domain_id']].drop_duplicates()
                mapped_table_unique_1 = (
                    mapped_table_df[['sheet_name', 'concept_id', 'IE_Info_Flag', 'Descendants_Flag', 'flag_standard_concept_input', 'domain']]
                    .drop_duplicates()
                    .rename(columns={'flag_standard_concept_input': 'flag_standard_concept' ,'domain': 'domain_id'})
                )
                mapped_table_unique_2 = (
                    mapped_table_df[['sheet_name', 'standard_code', 'IE_Info_Flag_mapped', 'Descendants_Flag', 'flag_standard_concept', 'standard_domain']]
                    .drop_duplicates()
                    .rename(columns={'standard_code': 'concept_id', 'IE_Info_Flag_mapped': 'IE_Info_Flag', 'standard_domain': 'domain_id'})
                )
                mapped_table_unique = pd.concat([mapped_table_unique_1, mapped_table_unique_2], ignore_index=True).drop_duplicates()
 
                appended_df = pd.merge(base_table_unique, 
                        mapped_table_unique, 
                        on='concept_id', 
                        how='outer', 
                        suffixes=('_base', '_mapped'))
                appended_df['sheet_name'] = appended_df['sheet_name_mapped'].combine_first(appended_df['sheet_name_base'])
                appended_df['IE_Info_Flag'] = appended_df['IE_Info_Flag_mapped'].combine_first(appended_df['IE_Info_Flag_base'])
                appended_df['Descendants_Flag'] = appended_df['Descendants_Flag_mapped'].combine_first(appended_df['Descendants_Flag_base'])
                appended_df['flag_standard_concept'] = appended_df['flag_standard_concept_mapped'].combine_first(appended_df['flag_standard_concept_base'])
                appended_df['domain_id'] = appended_df['domain_id_mapped'].combine_first(appended_df['domain_id_base'])
                appended_df = appended_df[['concept_id', 'sheet_name', 'IE_Info_Flag', 'Descendants_Flag', 'flag_standard_concept', 'domain_id']]
                appended_df = appended_df.reset_index(drop=True)
                st.dataframe(appended_df)
 
                row_n = appended_df.groupby('sheet_name').size().rename('N_concept_id')
                st.markdown("<span style='font-size: smaller; color: #0F68B2;'>Total number of concept ids per sheet (non-standard and their mapped standard codes):", unsafe_allow_html=True)
                st.write(row_n)
 
                ###############################
                # Check box: Domain-wise option
                ###############################
                flag_domainwise = 0
                flag_indicator = 0
                if flag_enable_domain == 1:
                    st.text("")
                    st.text("")
                    st.text("")
                    domain_wise = st.checkbox("Would you like to create individual concept-sets for each domain as well? NOTE: This includes Standard Codes only")           
                    keywords = []
                    if domain_wise:
                        unique_keywords_df = appended_df.groupby(['sheet_name', 'domain_id']).size().reset_index()[['sheet_name', 'domain_id']]
                        unique_keywords_df['keywords'] = unique_keywords_df['sheet_name'] + '_' + unique_keywords_df['domain_id']
                        keywords = unique_keywords_df['keywords'].tolist()
                        flag_indicator = 2
                        flag_domainwise = ws.check_concept_set_names(concept_set_name_list, r_script_path, atlas_user_name, atlas_password, keywords, flag_indicator, flag_enable_domain)
                else:
                    domain_wise = None
 
                ###############
                # Missing Codes
                ###############
                st.text("")
                st.text("")
                st.text("")
                st.markdown("<strong> Missing Codes:</strong>", unsafe_allow_html=True)
 
                not_found_rows = []
                def missing_codes(group, base_df):
                    for value in group['concept_code']:
                        cleaned_value = re.sub(r'[^a-zA-Z0-9._-]', '', str(value))  
                        pattern = cleaned_value.replace('_', '.')  
                        regex = re.compile(f'^{pattern}$')  
                        if not any(regex.match(base_code) for base_code in base_df['concept_code'].values):
                            not_found_rows.append(group[group['concept_code'] == value])
 
                cleaned_data.groupby('sheet_name').apply(missing_codes, base_table_df)
 
                if not not_found_rows:
                    st.write("There are no missing codes")
                else:
                    not_found_df = pd.concat(not_found_rows)
                    not_found_df = not_found_df.drop_duplicates()
                    not_found_df = not_found_df.astype(str)
                    st.markdown("<span style='font-size: smaller; color: #0F68B2;'>Below is the list of source concept codes for which a corresponding concept ID or standard mapping is not found in the CDM vocabulary. Please verify the accuracy of these codes in your input file.</span>", unsafe_allow_html=True)
                    st.write(not_found_df)

                ################################################
                # Options for Concept Set Creation (Check Boxes)
                ################################################        
                # Initialize empty DataFrames to store results
                df_standard_codes = pd.DataFrame()
                df_standard_non_standard = pd.DataFrame()
                df_input_file_codes = pd.DataFrame()
                df_standard_domain_wise = pd.DataFrame()

                # Process selections and store results in separate DataFrames
                if 'Standard Codes only' in selected_options:
                    df_standard_codes = appended_df[appended_df['flag_standard_concept'] == 'S']
                    df_standard_codes['sheet_name'] = df_standard_codes['sheet_name'].astype(str) + '_OnlyStandards'

                if 'Standard and Non-Standard Codes (All in one)' in selected_options:
                    df_standard_non_standard = appended_df.copy()
                    df_standard_non_standard['sheet_name'] = df_standard_non_standard['sheet_name'].astype(str) + '_All'
                    
                if 'Codes from your input file only' in selected_options:
                    df_input_file_codes = base_table_unique.drop_duplicates()
                    df_input_file_codes['sheet_name'] = df_input_file_codes['sheet_name'].astype(str) + '_OnlyInputFileCodes'

                if domain_wise:
                    df_standard_domain_wise = appended_df[appended_df['flag_standard_concept'] == 'S']
                    df_standard_domain_wise['sheet_name'] = df_standard_domain_wise['sheet_name'].astype(str) + '_OnlyStandards_' + df_standard_domain_wise['domain_id'].astype(str)

                # List of DataFrames and their corresponding actions
                dataframes_and_actions = [
                    (df_standard_codes, "Standard Codes only"),
                    (df_standard_non_standard, "Standard and Non-Standard Codes (All in one)"),
                    (df_input_file_codes, "Codes from your input file only"),
                    (df_standard_domain_wise, "Standard Codes only: Stratified by Domain")
                ]

                ########################################
                # Call R script that creates Concept Set
                ########################################
                if all(df.empty for df, _ in dataframes_and_actions):
                    st.text("")
                    st.text("")
                    st.text("")
                    st.write("No valid concept sets to create.")
                else:
                    st.text("")
                    st.text("")
                    st.text("")
                    if st.button("Press to proceed generating concept set in ATLAS"):
                        # Iterate through the DataFrames and perform actions if they are not empty
                        for df, action_name in dataframes_and_actions:
                            if not df.empty:
                                st.markdown(f"<p style='color:black; font-weight:bold;'>Processing `{action_name}` for the selected sheet(s)...</p>", unsafe_allow_html=True)
                                df['IE_Info_Flag'] = df['IE_Info_Flag'].astype(int)
                                df['Descendants_Flag'] = df['Descendants_Flag'].astype(int)
                                conditions = [
                                    (df['IE_Info_Flag'] == 1) & (df['Descendants_Flag'] == 0),
                                    (df['IE_Info_Flag'] == 1) & (df['Descendants_Flag'] == 1),
                                    (df['IE_Info_Flag'] == 0) & (df['Descendants_Flag'] == 0),  
                                    (df['IE_Info_Flag'] == 0) & (df['Descendants_Flag'] == 1),  
                                ]
                                values = [1, 2, 3, 4]
                                df['Final_Flag'] = np.select(conditions, values, default=-1)
                                df_leveling = df.groupby(['sheet_name', 'concept_id'])
                                idx = df_leveling['Final_Flag'].idxmax()
                                df = df.loc[idx]

                                # Create a temporary directory
                                output_directory = "/tmp"
                                if not os.path.exists(output_directory):
                                    os.makedirs(output_directory)
                                
                                for group_name, group_df in df.groupby(['sheet_name']):
                                    group_df = group_df.drop_duplicates()
                                    try:
                                        st.markdown(f"**_For `{group_name}`:_**")
                                        random_integer = random.randint(1, 1000)
                                        dataframe_csv_file = os.path.join(output_directory, f"conceptidlist_{random_integer}.csv")
                                        
                                        if not os.access(output_directory, os.W_OK):
                                            st.write("Error: Cannot write to the specified directory")
                                        else:
                                            group_df.to_csv(dataframe_csv_file, index=False)
                                            command = ["Rscript", r_script_path, 'postConceptSet', dataframe_csv_file, atlas_user_name, atlas_password, output_directory, base_url]
                                            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                            output, g_error = process.communicate()
                                            output_decoded = output.decode("utf-8")
                                            output_lines = output_decoded.split("\n")
                                            status_message = output_lines[0]
                                            csv_data = "\n".join(output_lines[1:])

                                            try:
                                                result_df = pd.read_csv(StringIO(csv_data))
                                                st.write(status_message)
                                                st.dataframe(result_df)
                                                st.text("")
                                            except pd.errors.ParserError as e:
                                                st.write(f"Failed to parse CSV output: {e}")
                                    
                                    except Exception as e:
                                        st.error(f"Error processing group {group_name}: {e}")
                                        st.text("")

                                st.text("")
                                st.text("")

##########################
# Delete Concept-Sets Menu
##########################
if menu_id == 'Delete Concept-Sets':

    ### ATLAS Login Credentials
    st.text("")
    st.markdown("<strong> ATLAS Login Credentials:</strong>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        base_url_delete = st.text_input('Enter the URL of your ATLAS instance:', None)
    with col_b:
        atlas_user_name_delete = st.text_input('Enter ATLAS User Name:', None)
    with col_c:
        atlas_password_delete = st.text_input('Enter ATLAS Password:', type="password")

    st.text("")
    st.text("")
    st.markdown("<strong> Concept-Sets available in ATLAS:</strong>", unsafe_allow_html=True)
    r_script_path = "CHIMERA_R_User_Defined_Function.R"
    flag_metadata = "metadata"
    if atlas_user_name_delete and atlas_password_delete:
        try:
            # Construct and run the R script command
            command = ["Rscript", r_script_path, "conceptSetMetadata", flag_metadata, atlas_user_name_delete, atlas_password_delete, base_url_delete]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, g_error = process.communicate()
            output_decoded = output.decode("utf-8")
            output_lines = output_decoded.split("\n")
            csv_data = "\n".join(output_lines)
        
            # Parse CSV output
            try:
                result_df = pd.read_csv(StringIO(csv_data))
                result_df['modifiedDate'] = pd.to_datetime(result_df['modifiedDate'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
                result_df = result_df.sort_values(by=['createdDate', 'modifiedDate'], ascending=[False, False])
                result_df['id'] = result_df['id'].astype(str)
                st.dataframe(result_df)
                st.text("")
                flag_metadata = "done"
            except pd.errors.ParserError as e:
                st.write(f"Failed to parse CSV output: {e}")

        except Exception as e:
            st.error(f"Error processing metadata extraction for concept-sets: {e}")
    
    if flag_metadata == "done":
        st.text("")
        st.text("")
        st.markdown("<strong> Delete Concept-Sets using Concept-Set Ids:</strong>", unsafe_allow_html=True)
        concept_set_id_list = st.text_input('Enter concept-set id(s) [use comma as delimiter]:', None)
        st.markdown("<span style='font-size: smaller; color: #0F68B2;'><strong>NOTE:</strong> Users can delete concept sets only if they have both read and write access. Please verify `hasWriteAccess` and `hasReadAccess` columns in the above table./span>", unsafe_allow_html=True)
        if concept_set_id_list:
            concept_set_id_list = [id.strip() for id in concept_set_id_list.split(',')]
            for concept_id in concept_set_id_list:
                try:
                    command = ["Rscript", r_script_path, 'deleteConceptSet', concept_id, atlas_user_name_delete, atlas_password_delete, base_url_delete]
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output, g_error = process.communicate()
                    output_decoded = output.decode("utf-8")
                    output_lines = output_decoded.split("\n")
                    status_message = output_lines[0]
                    csv_data = "\n".join(output_lines[1:])

                    try:
                        st.text("")
                        st.write(status_message)
                    except pd.errors.ParserError as e:
                        st.write(f"Failed to parse CSV output: {e}")
            
                except Exception as e:
                    st.text("")
                    st.error(f"Error processing concept-set id '{concept_id}': {e}")
   
###############
# Feedback Form
###############
st.text("")
st.text("")
st.text("")
st.write("Link to Feedback form: [https://forms.office.com/Pages/ResponsePage.aspx?id=M0vJOjWRIUiVAur9plkqNcstdl0WE7pJpJiTVbZFO-lUMlo0SDBZUDhVMEZFMFhOMEY2RjdGRE1FNi4u](https://forms.office.com/Pages/ResponsePage.aspx?id=M0vJOjWRIUiVAur9plkqNcstdl0WE7pJpJiTVbZFO-lUMlo0SDBZUDhVMEZFMFhOMEY2RjdGRE1FNi4u)")