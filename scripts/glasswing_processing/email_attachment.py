import email
import os

def download_attachments(path):
    listing = os.listdir(path)
    print(listing)
    countSuccess = 0
    countFail = 0
    for fle in listing:
        if str.lower(fle[-3:])=="eml":
            msg = email.message_from_file(open("data/email/"+fle))
            attachments=msg.get_payload()
            
            for attachment in attachments:
                try:
                    fnam=attachment.get_filename()
                    fnam = fnam.replace("\n","")
                    f=open("data/emailattachment/"+fnam, 'wb').write(attachment.get_payload(decode=True,))
                    countSuccess+=1
                except Exception as detail:
                    countFail+=1
                    pass
    print(f"Downloaded {countSuccess} PDFs")