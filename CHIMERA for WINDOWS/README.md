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
 
    <img src="https://github.com/user-attachments/assets/09384836-900c-40ea-bdc1-b95badc1e89c" width="900" height="250"> 

- If R 4.4.1 is already installed on your system and its path is added to your system’s PATH variable, the terminal will display the following message:

  <img src="https://github.com/user-attachments/assets/5921f318-e580-4121-95c3-9327dbb3b872" alt="Terminal" width="500" height="150">


#### 2.3 Install Java
Once the R software installation is completed, the executable file will check for the availability of Java version 23.0.1 in your system. If it’s not available, it will download and begin the installation.

- The installation process requires user interaction, and a pop-up dialog box for Java installation will appear

- Follow the instructions in the dialog box; there’s no need to customize any settings. Just click **Next** to proceed through the installation steps

- The Java installation wizard will prompt you to select a folder path for installing java, and it will display a default path. You can either leave the default path as is or choose a different path of your preference. **Make sure to note down the chosen path, as you will need to provide the java bin folder path in the terminal after the installation is complete** 

- Click **Close** once the installation is completed

- Now, in the terminal / Command Prompt that the executable file opened, it will prompt you for the Java bin folder path
  - You should have noted down the path where Java was installed, as per the above instruction
  - Navigate to that path, where you will find a folder named **Java**
  - Naviagte to **Java > jdk-23 > bin**
  - Copy this path (e.g., C:\Program Files\Java\jdk-23\bin) and paste it into the terminal, then press **Enter**
  - Once the path is successfully added to your system's PATH variable, you will see the following message in the terminal
 
- If Java version 23.0.1 is already installed on your system and its path is added to your system’s PATH variable, the terminal will display the following message:

  <img src="https://github.com/user-attachments/assets/3b226f6e-d369-4e98-a156-d7358ca5a450" alt="Terminal" width="750" height="200">


## CHIMERA Project team:
Marcela Rivera, Shahithya Lalitha Prabakaran, Satyajit Pande, Anna Ostropolets, Luisa Martinez

## CHIMERA Software Development Lead: 
Shahithya Lalitha Prabakaran

## Acknowledgements: 
Alan Andryc, Chris Knoll
