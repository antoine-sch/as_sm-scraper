from __future__ import unicode_literals
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import datetime
from telethon.sync import TelegramClient
from instaloader import Instaloader, Post
import youtube_dl
import requests
import shutil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.

currentdatetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


# SM-SCRAPER v1.3
# Social Media scraper

#Needs 'ID', 'LINK' and 'SAVED' COLUMN



# INFO TO EDIT
SPREADSHEET_ID = '10-lpH5ismBgfvcfIlW69-yxLHXG9HCTXdx278m6lKBc'
TAB = "Leicester"
START_ROW = 2
END_ROW = 24
#! these should be the sheet line numbers, not ids
# INFO TO EDIT (END)






# INIT
print("Init")

# Google
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys-joneslola794.json'
RANGES = TAB+"!A1:R"+str(END_ROW+1)
ROWNUM_ID = None
LINK_ID = None
SAVED_ID = None
# Telegram (Telethon)
api_id = 16749610
api_hash = '3242d0947b67a3cd7935d2b52b1d6ead'
telethon_api_name = 'anilsharma299'



# VERIFICATIONS
if START_ROW == 1:
    print(">> ERROR! The START_ROW parameter can not be set at '1', as it's the labels row.")
    exit()


# INIT GOOGLE SHEETS API
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=RANGES).execute()
values = result.get('values', [])


# INIT INSTALOADER
instaloaderFlag = False
try:
    L = Instaloader()
    L.login('antoineschirer', 'ayk!VBU8yhj.ubh*ucy')  # (login))
    L.download_geotags = False
    L.download_pictures = False
    L.post_metadata_txt_pattern = ''
    L.download_video_thumbnails = False
    L.save_metadata = False
    L.save_metadata_json = False
    instaloaderFlag = True
    print("> INSTALOADER PLUGGED")
except:
    print('! ERROR LOGIN INSTALOADER')

def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

colnum_string(28)

# SEARCH IN GOOGLE SHEET FOR 'ID', 'LINK' and 'SAVED' COLUMN
for y in range(0, len(values[0])):
    if "ID" == values[0][y]:
        #print("> ID COLUMN FOUND")
        ROWNUM_ID = y

    if "LINK" == values[0][y]:
        #print("> LINK COLUMN FOUND")
        LINK_ID = y

    if "SAVED" == values[0][y]:
        #print("> SAVED COLUMN FOUND")
        SAVED_ID = y

# IF ANY OF THE COLUMN MISSES, RETURN ERROR - IF NOT CONTINUE
if ROWNUM_ID == None or LINK_ID == None or SAVED_ID == None:
    print("ERROR: your sheet misses one of these columns: ID, LINK and SAVED.")
else:
    print("> GOOGLE SHEET PLUGGED")
    # START LOOP
    status_to_update = "x"
    for x in range(START_ROW-1, END_ROW):

        status_to_update = ""
        # Test if the line is filled
        try:
            if len(values[x]) < LINK_ID: # If link field isn't filled, don't run the engine
                status_to_update = "-"
            else:
                #First, look if it hasn't been saved already:
                if len(values[x]) > SAVED_ID and values[x][SAVED_ID] == "Green":

                        if "tiktok.com" in values[x][LINK_ID]: # LOOP FOR TIKTOK
                            #tiktok_scraper.
                            print(" …Tiktok…")
                            driver = webdriver.Chrome('chromedriver 4', chrome_options=options)
                            driver.get(values[x][LINK_ID])
                            res = driver.page_source
                            driver.quit()
                            soup = BeautifulSoup(res, 'lxml')
                            vidlink = soup.find('video')['src']
                            local_filename = f'{os.getcwd()}/TikTok_Test{values[x][ROWNUM_ID]}_{TAB}'
                            with requests.get(vidlink, stream=True) as r:
                                with open(local_filename, 'wb') as f:
                                    try:
                                        shutil.copyfileobj(r.raw, f)
                                    except:
                                        print('oh no')
                            status_to_update = "Green"
                        else:
                            print("     #" + values[x][ROWNUM_ID] + " > Already saved.")
                            status_to_update = "Green"
                else:
                    print("     #" + values[x][ROWNUM_ID])
                    try:
                        if "tiktok.com" in values[x][LINK_ID]: # LOOP FOR TIKTOK
                            #tiktok_scraper.
                            print("     …Tiktok…")
                            driver = webdriver.Chrome('chromedriver 4', chrome_options=options)
                            driver.get(values[x][LINK_ID])
                            res = driver.page_source
                            driver.quit()
                            soup = BeautifulSoup(res, 'lxml')
                            vidlink = soup.find('video')['src']
                            local_filename = f'{os.getcwd()}/TikTok_Test{values[x][ROWNUM_ID]}_{TAB}'
                            with requests.get(vidlink, stream=True) as r:
                                with open(local_filename, 'wb') as f:
                                    try:
                                        shutil.copyfileobj(r.raw, f)
                                    except:
                                        print('oh no')
                            status_to_update = "Green"
                        elif instaloaderFlag == True and "instagram.com/p/" in values[x][LINK_ID]: # LOOP FOR INSTAGRAM
                                print("     > Instaloader…")
                                trimmedInstaUrl = (values[x][LINK_ID].split("https://www.instagram.com/p/", 1)[1])
                                trimmedInstaUrl = trimmedInstaUrl.replace('/', '')
                                post = Post.from_shortcode(L.context,trimmedInstaUrl)
                                dateInsta = str(post.date_local)[0:10]
                                dateInsta = dateInsta.replace('-', '')
                                L.filename_pattern = values[x][ROWNUM_ID]+ ' ' + dateInsta
                                resulInsta = L.download_post(post, target= currentdatetime + " > " + TAB)
                                if resulInsta == True:
                                    status_to_update = "Green"
                                else:
                                    status_to_update = "Red 2"
                        elif "https://t.me/" in values[x][LINK_ID]: # LOOP FOR TELEGRAM
                            print("     …Telegram…")
                            with TelegramClient(telethon_api_name, api_id, api_hash) as client:
                                trimmedTelegramUrl = (values[x][LINK_ID].split("https://t.me/", 1)[1]) # return what's after the begining of the url
                                infoFromTelegramUrl = trimmedTelegramUrl.split("/") # return a array with user ID and message ID
                                msg = client.get_messages(infoFromTelegramUrl[0], ids=int(infoFromTelegramUrl[1]))
                                msg_date = str(msg.date)[0:10] #get the first 10 char from the date,
                                msg_date = msg_date.replace('-','')
                                if msg != None:
                                    rqst = msg.download_media(file=os.path.join(currentdatetime + " > " + TAB, values[x][ROWNUM_ID]+ ' ' + msg_date))
                                    if rqst == None:
                                        status_to_update = "Red 3"
                                    else:
                                        status_to_update = "Green"
                                else:
                                    mess_return = "Wrong link"
                        elif "http" in values[x][LINK_ID]:
                            print("     …YoutubeDL")
                            ydl_opts = {
                                'outtmpl': currentdatetime + " > " + TAB  + "/" + values[x][ROWNUM_ID] + ' %(upload_date)s' + '.%(ext)s'}
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                theresult = ydl.download([values[x][LINK_ID]])
                            status_to_update = "Green"
                    except:
                            if values[x][LINK_ID] == "":
                                print("[ERROR] No url here: " + values[x][ROWNUM_ID])
                                status_to_update = "! NO URL "
                            else:
                                print("[ERROR] Problem: " + values[x][ROWNUM_ID])
                                status_to_update = "Red 5"
                    print("     > " + status_to_update)
        except:
            status_to_update = "Red ?"
            print("[ERROR] In the row: " + values[x][ROWNUM_ID])
        request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                                range=TAB + "!" + colnum_string(SAVED_ID + 1) + str(x + 1),
                                                valueInputOption="USER_ENTERED",
                                                body={"values": [[status_to_update]]}).execute()
