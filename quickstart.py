from __future__ import print_function
import pickle
import os.path
import io
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.

class GoogleProvider():

    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/documents']

    def get_credentials(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds



def main():

    googleProvider = GoogleProvider()
    credentials = googleProvider.get_credentials()

    docs_service = DocsService(credentials)
    drive_service = DriveService(credentials)

    drive_service.list_files()

    #Lista de archivos
    #list_files(service = auth.drive_service)

    #Descargar un archivo
    #download_file(service = drive_service, file_id= '1XP9pfqmewIsIANMJJNMBkXnWG5HYJs_3')
    
    #Obtener el contenido en json de documento google
    #get_document(docs_service)



class DocsService():
    def __init__(self,credentials):
        self.service = build('docs', 'v1', credentials=credentials)
    
    def get_document(self):
        # Retrieve the documents contents from the Docs service.
        document = self.service.documents().get(documentId='1Cc-y40_VYprQWIWVpOfXVVK5gYsPVn8cD6mDaEbibIg').execute()
        print('The title of the document is: {}'.format(document.get('title')))
        parsed = document.get('body')
        print(json.dumps(parsed, indent=4, sort_keys=True))

    def create_document():
        title = 'New document'
        body = {
            'title': title
        }
        doc = self.service.documents() \
            .create(body=body).execute()
        print('Created document with title: {0}'.format(
            doc.get('title')))

class DriveService():
    def __init__(self,credentials):
        self.service = build('drive', 'v3', credentials=credentials)

    def download(self,file_id):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

    def list_files(self):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()