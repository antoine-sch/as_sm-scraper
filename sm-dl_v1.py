# SM-DL v1.0
# Social Media downloader

# INFO TO EDIT
SPREADSHEET_ID = 'XXXX'
TAB = "XXXX"
START_ROW = 2
END_ROW = 20
# INFO TO EDIT (END)

from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import datetime

# INIT
currentdatetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");
os.system('ls')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys-joneslola794.json'
RANGES = TAB+"!A1:R"+str(END_ROW+1)
ROWNUM_ID = None
LINK_ID = None
STATUS_ID = None

# INIT GOOGLE SHEETS API
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=RANGES).execute()
values = result.get('values', [])


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

colnum_string(28)

# SEARCH IN GOOGLE SHEET FOR 'ID', 'LINK' and 'STATUS' COLUMN
for y in range(0, len(values[0])):
    if "ID" == values[0][y]:
        #print("> ID COLUMN FOUND")
        ROWNUM_ID = y

    if "LINK" == values[0][y]:
        #print("> LINK COLUMN FOUND")
        LINK_ID = y

    if "STATUS" == values[0][y]:
        #print("> STATUS COLUMN FOUND")
        STATUS_ID = y

# IF ANY OF THE COLUMN MISSES, RETURN ERROR - IF NOT CONTINUE
if ROWNUM_ID == None or LINK_ID == None or STATUS_ID == None:
    print("ERROR: your sheet misses one of these columns: ID, LINK and STATUS.")
else:
    print("> GOOGLE SHEET PLUGGED")
    # START LOOP
    status_to_update = "x"
    for x in range(START_ROW-1, END_ROW):

        status_to_update = "x"
        try:
            len(values[x][LINK_ID])
            if "http" in values[x][LINK_ID]:
                command = 'youtube-dl -o\"' + TAB + " - " + currentdatetime + "/" + values[x][ROWNUM_ID] + ' %(upload_date)s.E' + str(x) + '.%(ext)s\"' + ' ' + values[x][LINK_ID]
                resultRequest = os.system(command)
                if resultRequest == 0:
                    status_to_update = "SAVED"
                else:
                    status_to_update = "!! ERROR !!"
        except:
                print("[ERROR] No url here: " + values[x][ROWNUM_ID])
                status_to_update = "!! NO URL !!"
            # UPDATE STATUS
        request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                            range=TAB + "!" + colnum_string(STATUS_ID + 1) + str(x + 1),
                                            valueInputOption="USER_ENTERED",
                                            body={"values": [[status_to_update]]}).execute()
