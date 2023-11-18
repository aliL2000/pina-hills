from email_attachment import download_attachments
from pdf_parsing import (
    read_pinahills_produce_inspection_pdfs,
    read_shipping_pdfs,
    read_nonformatted_channel_island_pdfs,
    read_pina_hills_supplier_cost_pdfs,
    read_formatted_channel_island_pdfs,
)
from db_processing import set_customs_for_container_purchase

PATH_TO_EML = "data/email/"
PATH_TO_PINAHILLS_SUPPLIER_COST = "data/email_attachment/pinahills_supplier_cost/"
PATH_TO_PINAHILLS_PRODUCE_INSPECTION_INVOICE = "data/email_attachment/pinahills_produce_inspection/"
PATH_TO_SHIPPING_INVOICE = "data/email_attachment/shipping/"
PATH_TO_IMPROPER_CHANNEL_ISLAND = "data/email_attachment/picture_pdf_channel_island/"
PATH_TO_PROPER_CHANNEL_ISLAND = "data/email_attachment/proper_pdf_channel_island/"


if __name__ == "__main__":
    # First, we download the PDF's from the given attachments and print out a count of what happened

    # download_attachments(PATH_TO_EML)

    # MANUAL: Move the PDF's to the correct directory (THIS CAN BE AUTOMATED,NEEDS TO BE DONE)

    # Then, once we have the PDF's downloaded, we need to get the data from each different type of PDF, and shove it into an MSACCESS DB

    #read_pina_hills_supplier_cost_pdfs(PATH_TO_PINAHILLS_SUPPLIER_COST)
    #read_pinahills_produce_inspection_pdfs(PATH_TO_PINAHILLS_PRODUCE_INSPECTION_INVOICE)
    #read_shipping_pdfs(PATH_TO_SHIPPING_INVOICE)
    
    #read_formatted_channel_island_pdfs(PATH_TO_PROPER_CHANNEL_ISLAND)
    #read_nonformatted_channel_island_pdfs(PATH_TO_IMPROPER_CHANNEL_ISLAND)

    ###DB DIRECT CHANGES###

    ## --------------------------- ##

    set_customs_for_container_purchase(125)
