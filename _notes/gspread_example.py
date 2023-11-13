import gspread

gc = gspread.service_account(filename='_notes/genuine-haiku-403407-71cf52b79e57.json')
sh = gc.open('db')
worksheet = sh.get_worksheet(0)
worksheet.update('A11', 'Bingo!')

worksheet = sh.add_worksheet(title="Number of rows", rows=1, cols=1)

worksheet1 = sh.get_worksheet(1)
worksheet1.update('A1', '11')

ws1_list = worksheet1.get_all_records()
for key in ws1_list[0]:
  counter = ws1_list[0][key]

counter = worksheet1.acell('A1').value

worksheet.update(f'A{counter+1}', 'Alex')
