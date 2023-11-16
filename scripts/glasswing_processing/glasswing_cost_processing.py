from email_attachment import download_attachments
from pdf_parsing import read_produce_inspection_pdfs

PATH_TO_EML = 'data/email/'
PATH_TO_PRODUCE_INSPECTION_INVOICE = 'data/email_attachment/produce_inspection/'
PATH_TO_SHIPPING_INVOICE = 'data/email_attachment/shipping/'
PATH_TO_CHANNEL_ISLAND = 'data/email_attachment/channel_island/'


if __name__ == "__main__":
    #First, we download the PDF's from the given attachments and print out a count of what happened
    
    #download_attachments(PATH_TO_EML)

    #MANUAL: Move the PDF's to the correct directory (THIS CAN BE AUTOMATED,NEEDS TO BE DONE)

    #Then, once we have the PDF's downloaded, we need to get the data from each different type of PDF, and shove it into an MSACCESS DB
    read_produce_inspection_pdfs(PATH_TO_PRODUCE_INSPECTION_INVOICE)
    
    
