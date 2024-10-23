# CHIMERA Application
CHIMERA is an application used to create concept sets at scale, map source codes to standard codes and integrate the end-to-end curation of concept sets in one application. The user uploads a lists of codes as input file (XLSX, XLS, CSV, XLSM), the application processes it to create and save concept sets in ATLAS. 

It uses WebAPI to generate multiple concepts sets in ATLAS with appropriate naming conventions. It effectively manages the inclusion and exclusion of codes and their descendants.

NOTE: Vocabulary search is not enabled in CHIMERA, for that we refer the users to ATLAS or ATHENA (https://athena.ohdsi.org/). 

# Prerequisites

### 1. **Python Programming Language**
Python is required to run various scripts in CHIMERA. Ensure that Python 3.9.7 is installed.

- Download Python from the official website: [Python.org](https://www.python.org/downloads/release/python-397/)
- During installation, check the box for **Add Python to PATH**
- Verify Python installation by running the following command in the command prompt:

    ```bash
    python --version
    ```
    
- If Python is installed and successfully added to your system's user environment variables, running the above command will display the Python version (i.e., 3.9.7) in the command prompt.

### 2. **R Programming Language**
CHIMERA requires R for access the ATLAS WebAPIs. Ensure that R 4.4.1 is installed.

- Download R from the official website: [R for Windows](https://cran.r-project.org/bin/windows/base/)
- Follow the installation instructions
- After installation, make sure to add R to your system's user environment variables, so it can be accessed from the command prompt

   To add R to the environment variable on Windows:
   - Type **Edit the system environment variables** in your system's search bar and click **Open**. A dialog box called **Environment Variables** appears.
   - Click on **Path** variable under User variables section and click **Edit**.
   - Add the directory path where R is installed (e.g., `C:\Program Files\R\R-4.4.1\bin`)
   - Click **OK** to save and close

- Open a new command prompt and verify the R installation by running the following command:

    ```bash
    R --version
    ```
    
- If R is installed and successfully added to your system's user environment variables, running the above command will display the R version (i.e., 4.4.1) in the command prompt.

### 3. **Java - JDK**
Java JDK is required to one of the R ATLAS WebAPI, where it requires rJava. Ensure that java 23.0.1 is installed.

- Download Java from the official website: [Java for Windows](https://www.oracle.com/java/technologies/downloads/?er=221886#jdk23-windows)
- Follow the installation instructions
- After installation, make sure to add Java to your system's user environment variables, so it can be accessed from the command prompt

   To add Java to the environment variable on Windows:
   - Type **Edit the system environment variables** in your system's search bar and click **Open**. A dialog box called **Environment Variables** appears.
   - Click on **Path** variable under User variables section and click **Edit**.
   - Add the directory path where Java is installed (e.g., `C:\Program Files\Java\jdk-23\bin`)
   - Click **OK** to save and close

- Open a new command prompt and verify the R installation by running the following command:

    ```bash
    java --version
    ```
    
- If Java is installed and successfully added to your system's user environment variables, running the above command will display the Java version (i.e., 23.0.1) in the command prompt.


**NOTE:** After modifying the environment variables, always open a new command prompt. If you have administrator privileges, it's recommended to run the command prompt as an administrator for better results.

### 4. **Prepare the required files into your local environment**

- Download all the scripts available in the repository and place them alltogether into a folder.
  
- Create a new folder inside the created folder called "Vocabulary_Tables". The folder in your local environment should have the following files:

  ![image](https://github.com/user-attachments/assets/291a6a04-2c0f-4422-a576-2b6280d24c10)

- Download vocabularies from [ATHENA](https://athena.ohdsi.org/search-terms/terms/255891) and include the tables "CONCPETS.csv" and "CONCEPT_RELATIONSHIP.csv" into the "Vocabulary_Tables" folder.

### 5. **Running the Application**

- Open a new command prompt.
  
-  Change the current directory to the path where all the CHIMERA code scripts and vocabularies are located (eg. cd C:\Users\Downloads\CHIMERA_Code_Scripts_folder).

     ```bash
    cd path
    ```
- Then run the prerequisite files in Python and R.
  
     ```bash
    python CHIMERA_Prerequisities.py
    Rscript CHIMERA_Prerequisities.R
    ```
- Launch the application
  
     ```bash
    streamlit run CHIMERA_Main_Script.py
    ```
## Home

In the home page, there are two menus at the top:
1. **Home** – where users will create concept sets.
2. **Delete Concept Sets** – where users can delete already created concept sets.

## Creating a Concept Set

1. The application will default to the home menu upon startup. If it does not, click on the "Home" menu.
2. In this section, you will find an option to upload a file.
3. Users can upload files in XLSX, XLS, CSV, and XLSM formats. We provide an example of the input file CHIMERA_Input_Template.xlsx, but the format is flexible so users can slightly deviate from this template.
4. Please take care when uploading:
   - The Excel file may contain one or multiple sheets. Maintain a consistent data structure across multiple sheets.
   - The Concept ID and Vocabulary columns are required, while I/E and Descendants are optional.  
5. By default, CHIMERA will create a concept set for all sheets. If you want to create it for specific sheets, check the appropriate boxes to select them.
6. A table will then appear, displaying the selected sheet codes.
7. Next, enter your ATLAS credentials and press Enter.
   - The ATLAS username will be included in the naming convention for the Concept Set, formatted as follows: `CHI_first2charactersOfATLASUserName_last2charactersOfATLASUserName_sheetname_keyword`.
   - Ensure that the sheet name is unique to avoid conflicts when saving the concept set in ATLAS.
8. After your credentials are validated, select the type of concept set. You can choose one or more options.
9. Check the Concept Set Name, and CHIMERA will indicate whether the name is acceptable.
10. Next, select the required fields: **Select Concept Code** and **Select Vocabulary ID** columns. These two columns are mandatory.
11. CHIMERA will display a data table after the cleaning process, along with the total number of concept codes per sheet.
12. You will also see the Standard Code Mapping table and the total number of concept codes per sheet.
13. If you want to create separate concept sets based on domain, check the corresponding box. Otherwise, CHIMERA will create a single concept set that includes all domains.
14. There will be a section for missing codes. If CHIMERA cannot find certain codes, it will list them in a table under the Missing Codes section.
15. Finally, if everything meets your requirements, click the button labeled **Press to Proceed Generating Concept Set in ATLAS**.
16. At the end, there is an option to provide user feedback for the CHIMERA application.

## Deleting Concept Sets

1. Click on the "Delete Concept Set" menu located at the top of the application.
2. Enter your credentials and press Enter.
3. Once your credentials are validated, a table displaying all available concept sets in ATLAS will appear.
4. Below the table, enter the concept set ID that you wish to delete. You can also delete multiple concept sets by entering a list of comma separated concept ids.

**NOTE:** Users can only delete concept sets if they possess both read and write access. Please check the `hasWriteAccess` and `hasReadAccess` columns in the table above.


# CHIMERA Project team:
Marcela Rivera, Shahithya Lalitha Prabakaran, Satyajit Pande, Anna Ostropolets, Luisa Martinez

# CHIMERA Software Development Lead: 
Shahithya Lalitha Prabakaran

# Acknowledgements: 
Alan Andryc, Chris Knoll
