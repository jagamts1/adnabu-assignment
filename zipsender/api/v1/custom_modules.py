from django.conf import settings

import requests
import tempfile
import shutil
import os
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition)


class DataProcess:

    def __init__(self, email, urls):
        self.email = email
        self.urls = urls
        self.dirpath = tempfile.mkdtemp()
        self.send_file_path = None

    def save_file(self, data, domain):
        """
            To create temporary file and save data 
        """
        with open(os.path.join(self.dirpath, domain + ".html"), 'w') as temp_file:
            temp_file.write(data.text)

    def download_html(self):
        """
            download data from url
        """
        with requests.Session() as Session:
            for url in self.urls:
                data = Session.get(url)
                domain = url.split('//')[-1].split('/')[0].split('.')[1]
                self.save_file(data, domain)
        return self

    def make_zip(self):
        """
            from folder make zip file
        """
        tempfolder = os.path.normpath(self.dirpath + os.sep + os.pardir)
        file_name = "download_html_file"
        self.send_file_path = shutil.make_archive(os.path.join(
            tempfolder, file_name), "zip", self.dirpath)
        shutil.rmtree(self.dirpath)
        return self

    def message_format(self):
        message = Mail(
            from_email=settings.SENDER_EMAIL,
            to_emails=self.email,
            subject='Send Downloaded html file as zip',
            html_content='<strong>I have attached zip file with this mail. Kindly check it.</strong>')
        return message

    def encode_data(self):
        """
            encode data to base64 format
        """
        with open(self.send_file_path, 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        return encoded

    def create_attachment(self):
        """
            create attachment to zip file
        """
        encoded = self.encode_data()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('application/zip')
        attachment.file_name = FileName('website.zip')
        attachment.disposition = Disposition('attachment')
        return attachment

    def send_zip(self):
        """
            send zip file to given mail
        """
        message = self.message_format()        
        message.attachment = self.create_attachment()
        try:
            sg = SendGridAPIClient(
                settings.SEND_GRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(e.message)
