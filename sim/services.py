import os
import gspread
from typing import List
from django.conf import settings

def initialize_gspread() -> gspread.client.Client:
  """
  Initialize a gspread client with the given credentials.
  """
  return gspread.service_account_from_dict(get_credentials())  # Note: we could move this to settings to do this once.
  # gspread.service_account(filename='credentials.json')

def get_credentials() -> dict:
  """
  Return gspread credentials.
  """
  return {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
  }

def get_all_rows(doc_name: str, sheet_name: str = None) -> List[dict]:
  """
  Fetches all rows from a given Google Sheet worksheet.
  """
  sh = settings.GSPREAD_CLIENT.open(doc_name)
  worksheet = sh.worksheet[sheet_name] if sheet_name else sh.get_worksheet(0)
  return worksheet.get_all_records() # Returns a list of dictionaries

def insert_row(doc_name, name, descr, url):
  sh = settings.GSPREAD_CLIENT.open(doc_name)
  # get current max row
  worksheet1 = sh.get_worksheet(1)
  counter_str = worksheet1.acell('A1').value
  counter = int(counter_str)
  # insert value
  worksheet = sh.get_worksheet(0)
  worksheet.update(f'A{counter+1}', name)
  worksheet.update(f'B{counter+1}', descr)
  worksheet.update(f'C{counter+1}', url)
  worksheet.update(f'D{counter+1}', f'{counter+1}') # id
  # update max row
  worksheet1.update('A1', f'{counter+1}')