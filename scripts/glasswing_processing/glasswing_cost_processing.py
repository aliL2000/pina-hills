from email_attachment import download_attachments

PATH_TO_EML = 'data/email/'


if __name__ == "__main__":
    #First, we download the PDF's from the given attachments and print out a count of what happened
    download_attachments(PATH_TO_EML)
     
