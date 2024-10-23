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

### 2. **Java - JDK**
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

# CHIMERA Project team:
Marcela Rivera, Shahithya Lalitha Prabakaran, Satyajit Pande, Anna Ostropolets, Luisa Martinez

# CHIMERA Software Development Lead: 
Shahithya Lalitha Prabakaran

# Acknowledgements: 
Alan Andryc, Chris Knoll
