# CHIMERA Setup Guide for Windows Users

## CHIMERA Application
CHIMERA is an application used to create concept sets at scale, map source codes to standard codes and integrate the end-to-end curation of concept sets in one application. The user uploads a lists of codes as input file (XLSX, XLS, CSV, XLSM), the application processes it to create and save concept sets in ATLAS. 

It uses WebAPI to generate multiple concepts sets in ATLAS with appropriate naming conventions. It effectively manages the inclusion and exclusion of codes and their descendants.

NOTE: Vocabulary search is not enabled in CHIMERA, for that we refer the users to ATLAS or ATHENA (https://athena.ohdsi.org/). 

## Prerequisites

### 1. **Download "CHIMERA for Windows" folder**
If you are a Windows user, all you need is this "CHIMERA for WINDOWS" folder to launch the application. 

- **NOTE:** When downloading the zip file from GitHub, additional scripts and files will be included along with the "CHIMERA for Windows" folder. After extracting the zip file, you can delete everything except the "CHIMERA for Windows" folder.

### 2. **Run CHIMERA_Installation.exe**
Run the executable file, CHIMERA_Installation.exe, with administrator privileges.

- Right-click the executable file and select "Run with Elevated Privileges". This will open a terminal / Command Prompt with administrator privileges.

  <img src="https://github.com/user-attachments/assets/47fbd0d9-b016-4771-bd2c-87c4656a66a0" alt="Run with Elevated Privileges" width="200" height="400">

#### 2.1. Install Python
After a few seconds, the executable file will check for the availability of Python version 3.9.7 in your system. If it’s not available, it will download and begin the installation.
   
 - The installation process requires user interaction, and a pop-up dialog box for Python installation will appear
   
 - **Ensure to select the checkbox "Add Python 3.9 to PATH" and then click "Install Now". This step is essential, as it adds Python to your system's PATH variable, which is required to run the CHIMERA application**
      
 - Follow the instructions in the dialog box; there’s no need to customize any settings. Click **Close** once the installation is completed.

   <img src="https://github.com/user-attachments/assets/a471b087-6f5c-4f59-92a4-c009263424a8" alt="Python Installation" width="600" height="400">

   <img src="https://github.com/user-attachments/assets/fca9dec0-f3a0-405e-855c-ff5e520ff55c" alt="Python Installation" width="600" height="400">
   

 - If Python 3.9.7 is already installed on your system and its path is added to your system’s PATH variable, the terminal will display the following message:

    <img src="https://github.com/user-attachments/assets/912db110-596a-490b-a470-4f1216ff82a8" alt="Terminal" width="800" height="100">
    

#### 2.2 Install R
Once the Python software installation is completed, the executable file will check for the availability of R version 4.4.1 in your system. If it’s not available, it will download and begin the installation.

- The installation process requires user interaction, and a pop-up dialog box for R installation will appear

  <img src="https://github.com/user-attachments/assets/35224472-2842-408c-bc2b-d3c5d363c1f0" alt="R Installation" width="300" height="150">

- Follow the instructions in the dialog box; there’s no need to customize any settings. Just click **Next** to proceed through the installation steps

- The R installation wizard will prompt you to select a folder path for installing R, and it will display a default path. You can either leave the default path as is or choose a different path of your preference. **Make sure to note down the chosen path, as you will need to provide the R bin folder path in the terminal after the installation is complete**

  <img src="https://github.com/user-attachments/assets/fc603e81-cbd5-4723-9a11-9d1faf7f4025" alt="R Installation" width="500" height="400">

- Click **Next** to proceed further. Post few clicks the installation starts.
  
- Click **Finish** once the installation is completed

  <img src="https://github.com/user-attachments/assets/1f16399e-6673-43c6-a9ae-0d6c7d968432" alt="R Installation" width="500" height="400">

- Now, in the terminal / Command Prompt that the executable file opened, it will prompt you for the R bin folder path
  - You should have noted down the path where R was installed, as per the above instruction
  - Navigate to that path, where you will find a folder named **R**
  - Naviagte to **R > R-4.4.1 > bin**
  - Copy this path (e.g., C:\Program Files\R\R-4.4.1\bin) and paste it into the terminal, then press **Enter**
  - Once the path is successfully added to your system's PATH variable, you will see the following message in the terminal
 
    <img src="https://github.com/user-attachments/assets/09384836-900c-40ea-bdc1-b95badc1e89c" width="800" height="400"> 

- If R 4.4.1 is already installed on your system and its path is added to your system’s PATH variable, the terminal will display the following message:

  <img src="https://github.com/user-attachments/assets/5921f318-e580-4121-95c3-9327dbb3b872" alt="Terminal" width="500" height="200">


#### 2.3 Install Java
Once the R software installation is completed, the executable file will check for the availability of Java version 23.0.1 in your system. If it’s not available, it will download and begin the installation.

- The installation process requires user interaction, and a pop-up dialog box for R installation will appear

- Follow the instructions in the dialog box; there’s no need to customize any settings. Just click **Next** to proceed through the installation steps

- The Java installation wizard will prompt you to select a folder path for installing java, and it will display a default path. You can either leave the default path as is or choose a different path of your preference. **Make sure to note down the chosen path, as you will need to provide the java bin folder path in the terminal after the installation is complete** 

- Click **Close** once the installation is completed

- Now, in the terminal / Command Prompt that the executable file opened, it will prompt you for the Java bin folder path
  - You should have noted down the path where Java was installed, as per the above instruction
  - Navigate to that path, where you will find a folder named **Java**
  - Naviagte to **Java > jdk-23 > bin**
  - Copy this path (e.g., C:\Program Files\Java\jdk-23\bin) and paste it into the terminal, then press **Enter**
  - Once the path is successfully added to your system's PATH variable, you will see the following message in the terminal

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

### 4. **Prepare the required files in your local environment**

- Download all the scripts available in the repository and place them together in a folder.
  
- Create a new folder inside the created folder called "Vocabulary_Tables". The folder in your local environment should contain the following files:

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
