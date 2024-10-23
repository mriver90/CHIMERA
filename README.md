# CHIMERA Application
CHIMERA is an application used to create concept sets at scale, map source codes to standard codes and integrate the end-to-end curation of concept sets in one application. The user uploads a lists of codes as input file (XLSX, XLS, CSV, XLSM), the application processes it to create and save concept sets in ATLAS. 

It uses WebAPI to generate multiple concepts sets in ATLAS with appropriate naming conventions. It effectively manages the inclusion and exclusion of codes and their descendants.

NOTE: Vocabulary search is not enabled in CHIMERA, for that we refer the users to ATLAS or ATHENA (https://athena.ohdsi.org/). 

# Prerequisites

### 1. **Python Programming Language**
Python is required to run various scripts in CHIMERA. Ensure that Python 3.9.7 is installed.

- Download Python from the official website: [Python.org](https://www.python.org/downloads/release/python-397/)
- During installation, check the box for "Add Python to PATH".
- Verify Python installation by running the following command in the command prompt:

    ```bash
    python --version
    ```
- If Python is installed and successfully added to the system path, running the above command will display the Python version (i.e., 3.9.7) in the command prompt.


# CHIMERA Project team:
Marcela Rivera, Shahithya Lalitha Prabakaran, Satyajit Pande, Anna Ostropolets, Luisa Martinez

# CHIMERA Software Development Lead: 
Shahithya Lalitha Prabakaran

# Acknowledgements: 
Alan Andryc, Chris Knoll
