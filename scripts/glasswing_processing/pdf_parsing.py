from PyPDF2 import PdfReader 
import pytesseract
from pdf2image import convert_from_path
import glob
import re
import csv
import os
import pandas as pd
from db_processing import write_produce_inpsection_db, write_shipping_db


def read_produce_inspection_pdfs(path):
    listing = os.listdir(path)
    for fle in listing:
        reader = PdfReader(path+fle)
        raw_text = ""
        for page in reader.pages:
            raw_text+=page.extract_text()

        filtered_text_list = re.split("[.]\d{2}", raw_text[raw_text.find('Thank you for your business!'):raw_text.find('Semana/Week:')].replace("\n",""))
        total = float(filtered_text_list[0][len(filtered_text_list[0])-3:])
        filtered_text_list.pop()
        row_dataframes = []
        for i in range(1,len(filtered_text_list)):
            container = filtered_text_list[i][:13].replace("-","")
            price = float(filtered_text_list[i][len(filtered_text_list[i])-3:])
            row_values = [container, price]
            row_df = pd.DataFrame([row_values], columns=["Container Number", "QA Inspection Price"])
            row_dataframes.append(row_df)
        df = pd.concat(row_dataframes, ignore_index=True)
        if df["QA Inspection Price"].sum() != total:
            print(f"WARNING, processing file: {fle}, ran into a summation issue, double check")
        else:
            print(len(df))
            write_produce_inpsection_db(df)

def read_shipping_pdfs(path):
    listing = os.listdir(path)
    
    for fle in listing:
        reader = PdfReader(path+fle)
        raw_text = ""
        for page in reader.pages:
            raw_text+=page.extract_text()
        filtered_text = raw_text[raw_text.find('Service Contract No.'):raw_text.find('Tax Specification Invoice Currency(USD)')].replace("\n","")
        row_dataframes = []
        container = filtered_text[21:32]
        price = float(filtered_text[filtered_text.find("Payable Amount USD")+19:].replace(",",""))
        row_values = [container, price]
        row_df = pd.DataFrame([row_values], columns=["Container Number", "Shipping Price"])
        row_dataframes.append(row_df)
        df = pd.concat(row_dataframes, ignore_index=True)
        write_shipping_db(df)

def read_channel_island_pdfs(path):
    listing = os.listdir(path)
    
    for fle in listing:
        pages = convert_from_path(path+fle)
        text = ""
        for pageNum,imgBlob in enumerate(pages):
            text += pytesseract.image_to_string(imgBlob,lang='eng')
        
        
        text_list = text.replace("\n","").split("Description")
        text_list.pop(0)
        for text_section in text_list:
            print(text_section)
            inner_list = re.split('CROSS DOCK|YARD DRYAGE', text_section)
            print(inner_list)
            print("-----")

        print("__________________________")
        

#
  
# # printing number of pages in pdf file 
# 

#  
# find = text.split("\n")
# regex_pattern = r'\d{13,}'
# print(find)
# sublist = [s for s in find if re.search(regex_pattern, s)]
# print(sublist)
# # count = 1
# # for tax_line in sublist:
# #     parts = tax_line.split(' ', 1)
# #     code = parts[0]
# #     description = parts[1]
# #     print(count,code,description)
# #     print("--")
# #     count+=1




#Reading from images

# pages = convert_from_path(path)
# text = ""
# print(len(pages))
# for pageNum,imgBlob in enumerate(pages):
#     text += pytesseract.image_to_string(imgBlob,lang='eng')
# #print(text)
# print(text)


# csv_filename = "data.csv"







# Open the CSV file for writing
# with open(csv_filename, mode='w', newline='') as csv_file:
#     csv_writer = csv.writer(csv_file)

#     # Write the header row
#     csv_writer.writerow(['Number','Tax Code', 'Description'])

#     # Write the data in a for loop
#     for item in sublist:

#         item = item.replace("\n", "")
#         if item.find("www.hacienda.go.cr")!=-1:
#             item = item[:item.find("www.hacienda.go.cr")]+item[item.find("BIENES Y SERVICIOS")+18:]
    
#         two_digit_pattern = r'\d{2} \| \d{13}'
#         one_digit_pattern = r'\d{1} \| \d{13}'
#         three_digit_pattern = r'\d{3} \| \d{13}'
#         one_match = re.search(one_digit_pattern, item)
#         two_match = re.search(two_digit_pattern, item)
#         three_match = re.search(three_digit_pattern,item)

#         if three_match:
#             start_index = three_match.start()
#             tax_codes = item[start_index:]
#             number = tax_codes[:3]
#             code = tax_codes[6:19]
#             characters = tax_codes[19:].replace("|","")
#             csv_writer.writerow([number,code,characters])
            
#         elif two_match:
#             start_index = two_match.start()
#             tax_codes = item[start_index:]
#             number = tax_codes[:2]
#             code = tax_codes[5:18]
#             characters = tax_codes[18:].replace("|","")
#             csv_writer.writerow([number,code,characters])
            
#         elif one_match:
#             start_index = one_match.start()
#             tax_codes = item[start_index:]
#             number = tax_codes[:1]
#             code = tax_codes[4:17]
#             characters = tax_codes[17:].replace("|","")
#             csv_writer.writerow([number,code,characters])
