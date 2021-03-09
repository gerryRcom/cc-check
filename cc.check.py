#!/bin/python3
# need to run below installs to get the Google Sheets interaction working
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# Google sheets code from https://developers.google.com/sheets/api/quickstart/python
#
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# import subprocess to allow running of shell commands
import subprocess
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID (pass as 1st argument) and range of a sample spreadsheet.
CC_SPREADSHEET_ID = sys.argv[1]
CC_RANGE_NAME = 'cc!A1:B100'

def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)

  service = build('sheets', 'v4', credentials=creds)

  # query type a (replace with cnc)
  def queryip(ipinput):
    ipresult = subprocess.run(['nslookup', ipinput], capture_output=True, text=True)
    if (ipresult.stderr != ""):
      return ipresult.stderr
    else:
      return ipresult.stdout

  # query type b (replace with rig)

  # query type c (replace with net)

  # Call the Sheets API
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=CC_SPREADSHEET_ID,
                              range=CC_RANGE_NAME).execute()
  values = result.get('values', [])

  # keep track of row number for reporting
  rowNum=1

  if not values:
    print('No data found in sheet (check cc tab).')
  else:      
    for row in values:
      # check for missing entries
      if (row[0] == "" or row[1] == ""):
        print("Missing data on row: " + str(rowNum))
        rowNum+=1
      # run a naming check on the entries
      elif (row[0][-4:] != ".com" or row[1][-4:] != ".com"):
        print("Invalid data on row: " + str(rowNum))
        rowNum+=1
      else:
        output = queryip(row[0])
        for line in output.splitlines():
          if ('Server' in line):
            print(line)
          elif ('Address' in line):
            print(line.split()[-1])    
        rowNum+=1

if __name__ == '__main__':
    main()