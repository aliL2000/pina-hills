from PyPDF2 import PdfReader 
import pytesseract
from pdf2image import convert_from_path
import glob
import re
import csv
  
print("test")
path = "data/document.pdf"


#reader = PdfReader(path) 
  
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
print(text)


csv_filename = "data.csv"







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
        
        


print("completed")
