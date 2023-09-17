
import openpyxl
import csv
import pandas as pd
import sqlite3
from pathlib import Path
from shutil import copyfile
import sys
 
def convert_from_excel_to_csv(input_file: str, output_dir: str):
	read_file = openpyxl.load_workbook(input_file)
	sheet = read_file.active
	file_name = Path(input_file).stem
	output_path = Path(output_dir) / (file_name + ".csv")
	col = csv.writer(open(output_path,'w',newline=''))
	for r in sheet.rows:
		col.writerow([cell.value for cell in r])

def convert_from_db_to_csv(input_file: str, output_dir: str):
	file_name = Path(input_file).stem
	output_path = Path(output_dir) / (file_name + ".csv")
	con = sqlite3.connect(input_file)
	cur = con.cursor()
	table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
	if len(table_list) == 2:
		table_name = table_list[0]
		for row in cur.execute("SELECT * FROM " + list(table_name)[0]):
			with open(output_path, 'a') as f:
				writer = csv.writer(f, delimiter=';', lineterminator='\n')
				writer.writerow(row)
	if len(table_list) > 2:
		for i in range(len(table_list)):
			#output_path = Path(output_dir) / (file_name) / (list(table_list[i])[0] + ".csv")
			table_name = table_list[i]
			for row in cur.execute("SELECT * FROM " + list(table_name)[0]):
				with open(output_path, 'a') as f:
					writer = csv.writer(f, delimiter=';', lineterminator='\n')
					writer.writerow(row)

def convert_other_to_csv(input_file: str, output_dir: str):
    file_name = Path(input_file).stem
    output_path = Path(output_dir) / (file_name + ".csv")
    copyfile(input_file, output_path)

