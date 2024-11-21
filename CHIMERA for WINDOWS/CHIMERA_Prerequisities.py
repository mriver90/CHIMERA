import subprocess
import re
import os
import urllib.request
import ctypes
import sys

# Add environment path
def add_path_variable_persistently(new_path):
    try:
        result = subprocess.run(
            ["powershell", "-Command", "[System.Environment]::GetEnvironmentVariable('PATH', 'User')"],
            capture_output=True, text=True, check=True
        )
        current_persistent_path = result.stdout.strip()
        updated_path = f"{new_path};{current_persistent_path}"
        subprocess.run(["setx", "PATH", updated_path], check=True)
        print(f"Persistently added {new_path} to the beginning of the user PATH variable.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update PATH variable: {e}")

# Python Prerequisites
def install_python_prerequisites():
    """Run the CHIMERA_Prerequisities.py script from the current directory."""
    try:
        print("Running Python prerequisites for CHIMERA...")
        
        import importlib
        import subprocess
        import sys

        # Dictionary to store package names and their required versions
        required_packages = {
            'sqlalchemy': '2.0.36',
            'pandas': '2.2.3',
            'numpy': '2.0.2',
            'streamlit': '1.12.0',
            'PIL': '11.0.0',  # Commented out as Pillow is mapped below
            'altair': '4.2.0',
            'hydralit_components': '1.0.10',
            'openpyxl': '3.1.5',
            'fuzzywuzzy': '0.18.0',
            'python-Levenshtein': '0.26.0',
            'pymysql': '1.1.1',
            'cx_Oracle': '8.3.0',
            'pyodbc': '5.2.0'

        }

        # Dictionary to map alternative package names (e.g., PIL -> Pillow)
        package_mapping = {
            'PIL': 'Pillow'  # 'PIL' maps to 'Pillow'
        }

        # Function to install packages with their version
        def install_packages(package, version):
            try:
                # Try to import the package
                importlib.import_module(package)
                print(f"Package '{package}' is already installed.")
            except ImportError:
                # Install the package with the specified version if not found
                package_to_install = f"{package_mapping.get(package, package)}=={version}"
                print(f"Package '{package}' not found. Installing version {version}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_to_install, "--user"])
                print(f"Package '{package}' version {version} has been installed successfully.")

        # Loop through the required packages and install them with their versions
        for package, version in required_packages.items():
            package_to_install = package_mapping.get(package, package)
            install_packages(package_to_install, version)

        # ATHENA VOCABULARIES
        import pandas as pd
        from sqlalchemy import create_engine

        print("")
        print("1. IMPORTANT: Ensure that the CONCEPT and CONCEPT_RELATIONSHIP CSV files are located inside the 'Vocabulary_Tables' folder, which should be within the CHIMERA Code Scripts folder that you downloaded from GitHub. Refer Readme file for more information.")
        print("2. IMPORTANT: The 'chimera.db' database is essential for performing standard code mapping operations. If this database file already exists in the folder containing the CHIMERA code scripts, you can skip the next step of loading the CONCEPT and CONCEPT_RELATIONSHIP CSV files into 'chimera.db'.")
        print("3. If you wish to use a specific or updated version of the ATHENA vocabularies, please ensure you have the relevant CSV files in the 'Vocabulary_Tables' folder, delete the old 'chimera.db' file and proceed with loading the data to refresh the 'chimera.db' file.")
        print("")

        def get_user_approval():
            response = input("Do you want to proceed with loading the CONCEPT and CONCEPT_RELATIONSHIP csv files into the database 'chimera.db'? (y/n): ").strip().lower()
            return response == 'y'

        # Create a SQLAlchemy engine for a persistent SQLite database
        engine = create_engine('sqlite:///chimera.db')  # Store the database in a file named chimera.db

        if get_user_approval():
            chunk_size = 200000  # Adjust this based on system memory

            # Define data types for CONCEPT.csv
            dtype_dict_concept = {
                'concept_id': 'Int64',  
                'concept_name': 'string',  
                'domain_id': 'string',
                'vocabulary_id': 'string',
                'concept_class_id': 'string',
                'standard_concept': 'string',
                'concept_code': 'string', 
                'invalid_reason': 'string',
            }

            # Read CONCEPT.csv in chunks and write each chunk directly to SQLite
            concept_file = r"Vocabulary_Tables/CONCEPT.csv"
            for chunk in pd.read_csv(
                concept_file, 
                sep='\t', 
                header=0, 
                on_bad_lines='skip', 
                low_memory=False, 
                dtype=dtype_dict_concept,  
                parse_dates=['valid_start_date', 'valid_end_date'], 
                chunksize=chunk_size
            ):
                print(f"Processing concept chunk with {chunk.shape[0]} rows...")
                chunk.to_sql('concept', con=engine, index=False, if_exists='append')  # Append each chunk

            # Define data types for CONCEPT_RELATIONSHIP.csv
            dtype_dict_concept_relationship = {
                'concept_id_1': 'Int64',  
                'concept_id_2': 'Int64',  
                'relationship_id': 'string',  
                'invalid_reason': 'string',  
            }

            # Read CONCEPT_RELATIONSHIP.csv in chunks and write each chunk directly to SQLite
            concept_relationship_file = r"Vocabulary_Tables/CONCEPT_RELATIONSHIP.csv"
            for chunk in pd.read_csv(
                concept_relationship_file, 
                sep='\t', 
                header=0, 
                on_bad_lines='skip', 
                low_memory=False, 
                dtype=dtype_dict_concept_relationship,  
                parse_dates=['valid_start_date', 'valid_end_date'], 
                chunksize=chunk_size
            ):
                print(f"Processing concept_relationship chunk with {chunk.shape[0]} rows...")
                chunk.to_sql('concept_relationship', con=engine, index=False, if_exists='append')  # Append each chunk

            # Optional: Querying SQLite for validation
            query_concept = pd.read_sql('SELECT * FROM concept WHERE vocabulary_id = "SNOMED"', con=engine)
            print(query_concept.head())  

            query_concept_relationship = pd.read_sql('SELECT DISTINCT relationship_id FROM concept_relationship', con=engine)
            print(query_concept_relationship.head())
        else:
            print("User chose not to proceed with loading the data.")

        print("")
        print("Python prerequisite operations completed successfully.")
        print("")
        
        print(r"Python packages: A user installation always places packages in the Roaming directory (e.g., C:\Users\YourUserName\AppData\Roaming\Python\Python39\Scripts).")
        add_path_of_additional_packages = input("Would you like to add the Roaming path to your system environment? "
                                                "If this path is already included, you may skip this step. "
                                                "Type 'y' to proceed or 'n' to skip: ").strip().lower()

        if add_path_of_additional_packages == 'y':
            roaming_path = input("Please provide the roaming path to add it to the system environment: ").strip()
            add_path_variable_persistently(roaming_path)
            print("")
            print(f"IMPORTANT: Environment variable for Python user-installed packages is updated. You may need to open a new terminal / Command Prompt for changes to take effect.")
            print("NOTE:  you open a new terminal or Command Prompt, rerun the 'CHIMERA_Prerequisites.py' script.")
            print("")
            proceed_1 = input("Type 'y' to continue or 'n' to exit: ").strip().lower()
            if proceed_1 != 'y':
                print("Exiting the script...")
                sys.exit()
        else:
            print("User chose not to add the Roaming path to system's envrionment variable.")

    except (ImportError, subprocess.CalledProcessError) as e:
        print(f"An error occurred during package installation: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"No data found in the file: {e}")
    except pd.errors.ParserError as e:
        print(f"Error parsing the data file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def install_r_prerequisites():
    """Run the CHIMERA_Prerequisities.r script from the current directory."""
    try:
        print("Running R prerequisites for CHIMERA...")
        print("")
        subprocess.run(["Rscript", "CHIMERA_Prerequisities.r"], check=True)
        print("")
        print("R prerequisite operations completed successfully.")
    except FileNotFoundError:
        print("CHIMERA_Prerequisities.r not found in the current directory. Skipping R prerequisite operations.")
    except subprocess.CalledProcessError as e:
        print(f"Error performing R prerequisite operations: {e}")

try:
    install_python_prerequisites()
    print("")
    install_r_prerequisites()
    print("")
    proceed_2 = input("Type 'y' to proceed launching the application: ").strip().lower()
    if proceed_2 == 'y':
        print("Attempting to launch CHIMERA...")
        try:
            result = subprocess.run(["streamlit", "run", "CHIMERA_Main_Script.py"], check=True)
            print("Streamlit app is running successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the Streamlit app: {e}")
    else:
        print("Exiting...")

except FileNotFoundError:
    print(f"The directory {chimera_directory} does not exist. Please check the path and try again.")
except Exception as e:
    print(f"An error occurred while changing the directory: {e}")
