# Setup your Python Environment

1. Install Pycharm (Community), or Visual Studio Code, or whatever code editor you like to use.
https://www.jetbrains.com/fr-fr/pycharm/download/#section=mac

2. Install Python 3 : 
https://www.python.org/downloads/

3. In the folder installed, run the command "Install Certificates.command"

4. Download the package from Github (via the "Code" green button > Download Zip) 
https://github.com/antoine-sch/sm-dl

5. Unzip it and store it in a convenient location (Like a "Python Scripts" folder in your Projects folder)

6. Open Pycharm. On the welcome screen, click Open, and select the folder. 

7. When Creating Virtual Environment prompted, select Python 3. Install the thing if it asks for it.

8. Pycharm should prompt you on top to install requirements. Do it.


# Setup your Google Sheet

1. Check that your Google Sheet isn't at XLSX format. (If so, there is a green "XLSX" icon next to the title. Then you should go to File > Save as Google Sheet, and work with the new file.)

2. Share the document with this address, and give Editing rights : sm-dl-875@sm-dl-333110.iam.gserviceaccount.com

3. Make sure your sheet has columns labelled that way: ID, LINK and STATUS 

4. Copy the ID of the document from the URL

# Setup the script

1. Back to Pycharm, look to the top left "Project" panel, and double-click on "sm-dl_V1.py"

2. On top of this document, there are the variables you need to edit:
- fill "SPREADSHEET_ID" with the id of the Google Sheet document, collected from the url
- fill "TAB" with the label of tab of the Google Sheet (bottom left)
- fill "START_ROW" with the starting row number (the sheet number, not the number specified in the ID column)
- fill "END_ROW" with the ending row number.

3. Run the script by going to the the "Project" panel, then right-clicking on "sm-dl_V1.py" > "Run sm-dl_V1"  

