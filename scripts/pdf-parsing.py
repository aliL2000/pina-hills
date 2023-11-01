# from PyPDF2 import PdfReader 
  
# # creating a pdf reader object
# # 
# path = "data/document (2).pdf" 
# reader = PdfReader(path) 
  
# # printing number of pages in pdf file 
# print(len(reader.pages)) 
  
# # getting a specific page from the pdf file 
# page = reader.pages[0] 
  
# # extracting text from page 
# text = page.extract_text() 
# print(text) 
import pytesseract
from pdf2image import convert_from_path
import glob

# pdfs = glob.glob()


pages = convert_from_path("data/document.pdf", 500)

for pageNum,imgBlob in enumerate(pages):
    text = pytesseract.image_to_string(imgBlob,lang='eng')
    print(text)
    print(f"-------{pageNum+1}-------")