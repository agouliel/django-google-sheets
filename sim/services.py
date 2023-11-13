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
  worksheet = sh.worksheet(sheet_name) if sheet_name else sh.get_worksheet(0)
  return worksheet.get_all_records() # Returns a list of dictionaries

def insert_row(doc_name, sheet, data):
  sh = settings.GSPREAD_CLIENT.open(doc_name)
  # get current max row
  # we could use append_row instead
  worksheet1 = sh.worksheet(sheet+'_max')
  counter_str = worksheet1.acell('A1').value
  counter = int(counter_str)
  # insert value
  worksheet = sh.worksheet(sheet)
  worksheet.add_rows(1)
  worksheet.update(range_name=f'A{counter+1}', values=[[data['your_name']]])
  worksheet.update(range_name=f'B{counter+1}', values=[[data['descr']]])
  worksheet.update(range_name=f'C{counter+1}', values=[[data['pic_url']]])
  worksheet.update(range_name=f'D{counter+1}', values=[[counter+1]]) # id
  # update max row
  worksheet1.update(range_name='A1', values=[[counter+1]])

def create_worksheets(doc_name, user_name):
  sh = settings.GSPREAD_CLIENT.open(doc_name)
  try:
    worksheet = sh.worksheet(user_name)
  except: # worksheets don't exist
    worksheet = sh.add_worksheet(title=user_name, rows=2, cols=4)
    worksheet.update(range_name='A1', values=[['title']])
    worksheet.update(range_name='B1', values=[['description']])
    worksheet.update(range_name='C1', values=[['url']])
    worksheet.update(range_name='D1', values=[['id']])
    worksheet.update(range_name='A2', values=[['Welcome']])
    worksheet.update(range_name='B2', values=[['Welcome']])
    worksheet.update(range_name='C2', values=[['https://static.vecteezy.com/system/resources/thumbnails/011/976/274/small/stick-figures-welcome-free-vector.jpg']])
    worksheet.update(range_name='D2', values=[[2]])
    worksheet = sh.add_worksheet(title=user_name+'_max', rows=1, cols=1)
    worksheet.update(range_name='A1', values=[[2]])

def get_one_row(doc_name, user_name, photo_id):
  sh = settings.GSPREAD_CLIENT.open(doc_name)
  worksheet = sh.worksheet(user_name)
  return worksheet.row_values(int(photo_id)) # Returns a list

def delete_row(doc_name, user_name, photo_id):
  sh = settings.GSPREAD_CLIENT.open(doc_name)
  # get current max row
  worksheet1 = sh.worksheet(user_name+'_max')
  counter_str = worksheet1.acell('A1').value
  max_id = int(counter_str)

  worksheet = sh.worksheet(user_name)

  # update all next rows first
  for i in range(photo_id+1, max_id+1):
    worksheet.update(range_name=f'D{i}', values=[[i-1]])
  
  # delete row
  worksheet.delete_rows(photo_id)
  
  # update max row
  worksheet1.update(range_name='A1', values=[[max_id-1]])
