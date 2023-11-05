from PyPDF2 import PdfReader 
import pytesseract
from pdf2image import convert_from_path
import glob
import re
import csv
  
print("test")
path = "data/AUTORIZACION_2023_PINA_HILLS.pdf"
path2 = "data/AUTORIZACION_2023_PINA_HILLS test.pdf"
reader = PdfReader(path2) 
  
# # printing number of pages in pdf file 
# print(len(reader.pages)) 
# text = ""
# for page in reader.pages:
#     text+=page.extract_text()

# print(text) 
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

pages = convert_from_path(path)
text = ""
print(len(pages))
for pageNum,imgBlob in enumerate(pages):
    text += pytesseract.image_to_string(imgBlob,lang='eng')
#print(text)
sublist = text.split("Descripcién Ampliada")


csv_filename = "data.csv"

# Open the CSV file for writing
with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(['Tax Code', 'Description'])

    # Write the data in a for loop
    for item in sublist:

        item = item.replace("\n", "")
        if item.find("www.hacienda.go.cr")!=-1:
            item = item[:item.find("www.hacienda.go.cr")]+item[item.find("BIENES Y SERVICIOS")+18:]
    
        pattern = r'\d{13,}'
        match = re.search(pattern, item)

        if match:
            start_index = match.start()
    
        tax_codes = item[start_index:]
        numbers = tax_codes[:14]
        characters = tax_codes[14:].replace("|","")
        csv_writer.writerow([numbers, characters])


print("completed")
