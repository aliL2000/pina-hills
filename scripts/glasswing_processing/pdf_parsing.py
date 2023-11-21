from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_path
import glob
import re
import csv
import os
import pandas as pd
import datetime
from db_processing import (
    write_pinahills_produce_inpsection_db,
    write_shipping_db,
    write_pina_hills_supplier_db,
    write_pina_hills_cost_breakdown_db,
    write_channel_island_page_db,
)

size_dictionary = {
    "Crown": {5: "Crown5", 6: "Crown6", 7: "Crown7", 8: "Crown8"},
    "Crownless": {
        5: "Crownless5",
        6: "Crownless6",
        7: "Crownless7",
        8: "Crownless8",
    },
}

channel_islands_dictionary = {
    "USDA": {
        "Restack": "Inspection Restacking",
        "Restrap": "Inspection Restrapping",
        "Reload": "Inpsection Reloading",
        "Inspection": "Inspection",
        "Supplemental": "Supplemental"
    },
    "Transport": {
        "Reload": "Reload",
        "Unload": "Unload"
    },
    "ColdStorage": "Cold Storage",
    "Presold": {
        "Crossdock": "Cross Dock",
        "Yard": "Yard Drayage",
        
    }
}

channel_islands_dictionary_keys = list(channel_islands_dictionary.keys())

def read_pina_hills_supplier_cost_pdfs(path):
    listing = os.listdir(path)
    for fle in listing:
        reader = PdfReader(path + fle)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text()
        # print(raw_text)
        # Code below is used for the first table
        dateindex = raw_text.find("DATE")
        date = raw_text[dateindex + 4 : dateindex + 15].replace(" ", "")
        datetime_string = datetime.datetime.strptime(date, "%d/%m/%Y")
        filtered_text = raw_text[
            raw_text.find("DESCRIPTION CANTIDAD PRECIO MONTO") :
        ].replace("\n", "")
        index = filtered_text.find("CONTAINER")
        container = filtered_text[index + 10 : index + 21]
        index = filtered_text.find("BALANCE DUE USD")
        money = re.sub(r"[^0-9.,]", "", filtered_text[index + 16 : index + 30]).replace(
            ",", ""
        )
        write_pina_hills_supplier_db(datetime_string, container, money)

        # Code below is used for the third table
        price_breakdown_list = list(
            filter(
                None,
                raw_text[raw_text.find("MONTO") + 5 : raw_text.find("GUIA")]
                .replace(",", "")
                .split("\n"),
            )
        )
        for price_string in price_breakdown_list:
            pattern = r"([^\d]+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)"
            match = re.match(pattern, price_string)

            description = match.group(1).strip()
            size = int(match.group(2))
            quantity = int(match.group(3))
            unit_price = float(match.group(4))
            total = float(match.group(5))

            if "corona" in description.lower():
                type = size_dictionary["Crown"][size]
            write_pina_hills_cost_breakdown_db(
                container, type, quantity, unit_price, total
            )


def read_pinahills_produce_inspection_pdfs(path):
    listing = os.listdir(path)
    for fle in listing:
        reader = PdfReader(path + fle)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text()
        print(raw_text)
        filtered_text_list = re.split(
            "[.]\d{2}",
            raw_text[
                raw_text.find("Thank you for your business!") : raw_text.find(
                    "Semana/Week:"
                )
            ].replace("\n", ""),
        )
        total = float(filtered_text_list[0][len(filtered_text_list[0]) - 3 :])
        filtered_text_list.pop()
        row_dataframes = []
        for i in range(1, len(filtered_text_list)):
            container = filtered_text_list[i][:13].replace("-", "")
            price = float(filtered_text_list[i][len(filtered_text_list[i]) - 3 :])
            row_values = [container, price]
            row_df = pd.DataFrame(
                [row_values], columns=["Container Number", "QAInspection"]
            )
            row_dataframes.append(row_df)
        df = pd.concat(row_dataframes, ignore_index=True)
        if df["QAInspection"].sum() != total:
            print(
                f"WARNING, processing file: {fle}, ran into a summation issue, double check"
            )
        else:
            write_pinahills_produce_inpsection_db(df)


def read_shipping_pdfs(path):
    listing = os.listdir(path)

    for fle in listing:
        reader = PdfReader(path + fle)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text()
        filtered_text = raw_text[
            raw_text.find("Service Contract No.") : raw_text.find(
                "Tax Specification Invoice Currency(USD)"
            )
        ].replace("\n", "")
        row_dataframes = []
        container = filtered_text[21:32]
        price = float(
            filtered_text[filtered_text.find("Payable Amount USD") + 19 :].replace(
                ",", ""
            )
        )
        row_values = [container, price]
        row_df = pd.DataFrame(
            [row_values], columns=["Container Number", "SealandFreight"]
        )
        row_dataframes.append(row_df)
        df = pd.concat(row_dataframes, ignore_index=True)
        write_shipping_db(df)


def read_formatted_channel_island_pdfs(path):
    listing = os.listdir(path)
    for fle in listing:
        reader = PdfReader(path + fle)
        for page in reader.pages:
            row_dataframes = []
            page_text = page.extract_text()
            date = page_text[page_text.find("Date") + 6 : page_text.find("Date") + 16]
            datetime_string = datetime.datetime.strptime(date, "%m/%d/%Y") 
            charges = page_text[
                page_text.find("Equipment Qty Rate Amount")
                + 25 : page_text.find("TOTAL BY COMMODITY")
            ].split("\n")
            charges[:] = [x for x in charges if x]
            print(len(charges))
            for charge in charges:
                match = re.search(r"\b[A-Z]{4}\d{7}\b", charge)

                match_index = match.start()
                test = charge[: match_index + 12].rstrip()

                # Use re.match to apply the pattern to the input string
                match = re.match(
                    r"^([^0-9]+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\w+(?:\s+\w+)*)$",
                    test,
                )

                if match:
                    description = match.group(1).strip().lower()
                    amount = float(match.group(2))
                    qty = float(match.group(3))
                    rate = float(match.group(4))
                    container_number = match.group(5)

                    category = ""
                    subcategory = ""
                    if "inspection" in description:
                        if "restack" in description:
                            category = channel_islands_dictionary_keys[0]
                            subcategory = channel_islands_dictionary["USDA"]["Restack"]
                        elif "restrap" in description:
                            category = channel_islands_dictionary_keys[0]
                            subcategory = channel_islands_dictionary["USDA"]["Restrap"]
                        elif "reload" in description:
                            category = channel_islands_dictionary_keys[0]
                            subcategory = channel_islands_dictionary["USDA"]["Reload"]
                        elif "supplemental" in description:
                            category = channel_islands_dictionary_keys[0]
                            subcategory = channel_islands_dictionary["USDA"]["Supplemental"]
                        else:
                            category = channel_islands_dictionary_keys[0]
                            subcategory = channel_islands_dictionary["USDA"]["Inspection"]
                    elif "unload" in description:
                        category = channel_islands_dictionary_keys[1]
                        subcategory = channel_islands_dictionary["Transport"]["Unload"]
                    elif "reload" in description:
                        category = channel_islands_dictionary_keys[1]
                        subcategory = channel_islands_dictionary["Transport"]["Reload"]
                    elif "cold storage" in description:
                        category = channel_islands_dictionary_keys[2]
                        subcategory = channel_islands_dictionary["ColdStorage"]
                    elif "cross dock" in description:
                        category = channel_islands_dictionary_keys[3]
                        subcategory = channel_islands_dictionary["Presold"]["Crossdock"]
                    elif "yard drayage" in description:
                        category = channel_islands_dictionary_keys[3]
                        subcategory = channel_islands_dictionary["Presold"]["Yard"]
                    
                    row_values = [container_number, category, subcategory,rate,qty,amount]
                    row_df = pd.DataFrame(
                        [row_values], columns=["ContainerNumber", "Category","SubCategory","UnitPrice","Quantity","Total"]
                    )
                    row_dataframes.append(row_df)


            print(f"Will write {len(row_dataframes)} rows to the DB")
            df = pd.concat(row_dataframes, ignore_index=True)
            write_channel_island_page_db(datetime_string,df)
        print("------------")


def read_nonformatted_channel_island_pdfs(path):
    listing = os.listdir(path)

    for fle in listing:
        pages = convert_from_path(path + fle)
        text = ""
        for pageNum, imgBlob in enumerate(pages):
            text += pytesseract.image_to_string(imgBlob, lang="eng")
        print(text.replace("\n", ""))
        matches = re.findall(r"([A-Z]{4}\d{7}(?!\d))", text.replace("\n", ""))
        for match in matches:
            index = text.find(match)
            sub_match = text[index : index + 45].replace("\n", "")
            container = sub_match[:11]
            left_over = sub_match[11:]
            filtered_string = re.sub(r"[^0-9.,]", "", left_over)
            filtered_string.replace(",", ".")
            numberlist = []
            current_number = ""
            for i in range(len(filtered_string)):
                if filtered_string[i] == ".":
                    current_number += filtered_string[i]
                    current_number += filtered_string[i + 1]
                    current_number += filtered_string[i + 2]
                    numberlist.append(float(current_number))
                    current_number = ""
                    i += 2
                else:
                    current_number += filtered_string[i]
            print(container, numberlist)
            text = text[index:]
            numberlist = []
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


# Reading from images

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
