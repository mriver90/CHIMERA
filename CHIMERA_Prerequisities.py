###################################
# INSTALL REQUIRED PACKAGES: Python
###################################
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
    'python-Levenshtein': '0.26.0'
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

#####################
# ATHENA VOCABULARIES
#####################
import pandas as pd
from sqlalchemy import create_engine

# Create a SQLAlchemy engine for a persistent SQLite database
engine = create_engine('sqlite:///chimera.db')  # Store the database in a file named chimera.db

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





