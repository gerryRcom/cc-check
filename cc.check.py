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
SAMPLE_SPREADSHEET_ID = sys.argv[1]
SAMPLE_RANGE_NAME = 'cc!A1:B100'

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

  # 
  def queryip(ipinput):
    ipresult = subprocess.getoutput('nslookup '+ ipinput)
    return ipresult


  # Call the Sheets API
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range=SAMPLE_RANGE_NAME).execute()
  values = result.get('values', [])

  if not values:
    print('No data found.')
  else:      
    for row in values:
      output = queryip(row[0])
      print (output)

if __name__ == '__main__':
    main()